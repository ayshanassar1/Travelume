"""
Manages verified agency database (combination of OSM + manual verification)
"""

import json
import os
from datetime import datetime

class AgencyDatabase:
    def __init__(self):
        self.agencies_file = "data/verified_agencies.json"
        self.reviews_file = "data/agency_reviews.json"
        self.ensure_data_files()
    
    def ensure_data_files(self):
        """Create data files if they don't exist"""
        os.makedirs("data", exist_ok=True)
        
        if not os.path.exists(self.agencies_file):
            with open(self.agencies_file, 'w') as f:
                json.dump({"verified_agencies": {}}, f, indent=2)
        
        if not os.path.exists(self.reviews_file):
            with open(self.reviews_file, 'w') as f:
                json.dump({"reviews": []}, f, indent=2)
    
    def add_verified_agency(self, osm_agency, verified_by, verification_notes=""):
        """
        Mark an OSM agency as verified by admin
        """
        with open(self.agencies_file, 'r') as f:
            data = json.load(f)
        
        agency_id = f"VERIFIED_{osm_agency['id']}"
        
        verified_agency = {
            **osm_agency,
            'verified': True,
            'verified_by': verified_by,
            'verified_on': datetime.now().isoformat(),
            'verification_notes': verification_notes,
            'trust_score': 100,  # Base score for verified agencies
            'status': 'active',
            'our_notes': "",  # Admin can add private notes
            'contact_preferences': {
                'prefers_email': True,
                'prefers_phone': True,
                'prefers_whatsapp': False,
                'response_time': "24-48 hours"
            }
        }
        
        data['verified_agencies'][agency_id] = verified_agency
        
        with open(self.agencies_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return agency_id
    
    def get_verified_agencies(self, destination=None, service_type=None):
        """
        Get verified agencies, optionally filtered
        """
        with open(self.agencies_file, 'r') as f:
            data = json.load(f)
        
        agencies = list(data['verified_agencies'].values())
        
        # Apply filters
        if destination:
            agencies = [a for a in agencies if self._matches_destination(a, destination)]
        
        if service_type:
            agencies = [a for a in agencies if service_type in a.get('services', [])]
        
        return agencies
    
    def _matches_destination(self, agency, destination):
        """Check if agency serves the destination"""
        # Check address fields
        address_fields = ['city', 'country']
        for field in address_fields:
            if destination.lower() in agency.get('address', {}).get(field, '').lower():
                return True
        
        # Check OSM tags for destination mentions
        osm_tags = agency.get('osm_tags', {})
        for tag_value in osm_tags.values():
            if destination.lower() in str(tag_value).lower():
                return True
        
        return False
    
    def add_review(self, agency_id, user_email, rating, comment):
        """Add user review for an agency"""
        with open(self.reviews_file, 'r') as f:
            data = json.load(f)
        
        review = {
            'review_id': f"REV_{int(datetime.now().timestamp())}",
            'agency_id': agency_id,
            'user_email': user_email,
            'rating': rating,
            'comment': comment,
            'date': datetime.now().isoformat(),
            'verified_purchase': False,
            'helpful_count': 0
        }
        
        data['reviews'].append(review)
        
        with open(self.reviews_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return review['review_id']
    
    def get_agency_reviews(self, agency_id):
        """Get all reviews for an agency"""
        with open(self.reviews_file, 'r') as f:
            data = json.load(f)
        
        return [r for r in data['reviews'] if r['agency_id'] == agency_id]