"""
Fetches real-time travel agency data from OpenStreetMap
"""

import requests
import json
from datetime import datetime
import streamlit as st

class OSMAgencyFetcher:
    def __init__(self):
        self.base_url = "https://overpass-api.de/api/interpreter"
        self.cache = {}  # Simple cache to avoid repeated calls
    
    def calculate_bbox(self, lat, lon, radius_km=10):
        """
        Calculate bounding box from center point and radius
        1 degree ≈ 111 km
        """
        delta = radius_km / 111.0
        return f"{lat - delta},{lon - delta},{lat + delta},{lon + delta}"
    
    def fetch_agencies(self, lat, lon, radius_km=10):
        """
        Fetch travel agencies from OSM within radius
        Returns: List of agency dictionaries
        """
        bbox = self.calculate_bbox(lat, lon, radius_km)
        cache_key = f"{lat}_{lon}_{radius_km}"
        
        # Check cache first
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Query for both tourism=travel_agency and amenity=travel_agent
        query = f"""
        [out:json][timeout:25];
        (
          node[tourism=travel_agency]({bbox});
          node[amenity=travel_agent]({bbox});
          way[tourism=travel_agency]({bbox});
          way[amenity=travel_agent]({bbox});
          relation[tourism=travel_agency]({bbox});
          relation[amenity=travel_agent]({bbox});
        );
        out body;
        >;
        out skel qt;
        """
        
        try:
            response = requests.post(self.base_url, data={"data": query})
            response.raise_for_status()
            data = response.json()
            
            agencies = self._parse_osm_data(data)
            
            # Cache for 1 hour
            self.cache[cache_key] = agencies
            return agencies
            
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching agency data: {str(e)}")
            return []
    
    def _parse_osm_data(self, osm_data):
        """
        Parse OSM JSON response into structured agency data
        """
        agencies = []
        
        for element in osm_data.get('elements', []):
            if 'tags' not in element:
                continue
                
            tags = element['tags']
            
            # Skip if not a travel agency
            if 'tourism' not in tags and 'amenity' not in tags:
                continue
                
            if tags.get('tourism') != 'travel_agency' and tags.get('amenity') != 'travel_agent':
                continue
            
            agency = {
                'id': element.get('id'),
                'type': element.get('type'),
                'name': tags.get('name', 'Unnamed Travel Agency'),
                'lat': element.get('lat'),
                'lon': element.get('lon'),
                'address': {
                    'street': tags.get('addr:street'),
                    'housenumber': tags.get('addr:housenumber'),
                    'city': tags.get('addr:city'),
                    'postcode': tags.get('addr:postcode'),
                    'country': tags.get('addr:country')
                },
                'contact': {
                    'phone': tags.get('phone'),
                    'website': tags.get('website'),
                    'email': tags.get('email')
                },
                'services': self._extract_services(tags),
                'opening_hours': tags.get('opening_hours'),
                'source': 'osm',
                'last_updated': datetime.now().isoformat(),
                'osm_tags': tags  # Keep all original tags
            }
            
            # Calculate full address string
            agency['full_address'] = self._build_address(agency['address'])
            
            agencies.append(agency)
        
        return agencies
    
    def _extract_services(self, tags):
        """Extract services from OSM tags"""
        services = []
        
        # Common service tags in OSM
        service_mapping = {
            'air_tickets': ['air_tickets', 'flight', 'flights'],
            'bus_tickets': ['bus_tickets', 'bus'],
            'train_tickets': ['train_tickets', 'railway', 'train'],
            'visa_service': ['visa_service', 'visa'],
            'package_tours': ['package_tours', 'tour', 'tours'],
            'hotel_reservation': ['hotel_reservation', 'hotel', 'accommodation'],
            'car_rental': ['car_rental', 'car'],
            'currency_exchange': ['currency_exchange', 'exchange']
        }
        
        # Check tourism tag for specific services
        tourism = tags.get('tourism', '')
        if tourism:
            services.append(tourism)
        
        # Check for service tags
        for service_key in tags:
            for service_type, keywords in service_mapping.items():
                for keyword in keywords:
                    if keyword in service_key.lower():
                        if service_type not in services:
                            services.append(service_type)
        
        return list(set(services))  # Remove duplicates
    
    def _build_address(self, address_dict):
        """Build readable address string"""
        parts = []
        
        if address_dict.get('housenumber') and address_dict.get('street'):
            parts.append(f"{address_dict['housenumber']} {address_dict['street']}")
        elif address_dict.get('street'):
            parts.append(address_dict['street'])
        
        if address_dict.get('city'):
            parts.append(address_dict['city'])
        
        if address_dict.get('postcode'):
            parts.append(address_dict['postcode'])
        
        if address_dict.get('country'):
            parts.append(address_dict['country'])
        
        return ', '.join(parts)
    
    def search_by_destination(self, destination_name, country_code=None):
        """
        Search agencies by destination name using Nominatim geocoding
        """
        # First, geocode the destination to get coordinates
        geocode_url = "https://nominatim.openstreetmap.org/search"
        
        params = {
            'q': destination_name,
            'format': 'json',
            'limit': 1
        }
        
        if country_code:
            params['countrycodes'] = country_code
        
        try:
            response = requests.get(geocode_url, params=params)
            response.raise_for_status()
            results = response.json()
            
            if not results:
                return []
            
            # Get coordinates from first result
            lat = float(results[0]['lat'])
            lon = float(results[0]['lon'])
            
            # Now fetch agencies around these coordinates
            return self.fetch_agencies(lat, lon, radius_km=20)
            
        except Exception as e:
            st.error(f"Error searching for {destination_name}: {str(e)}")
            return []