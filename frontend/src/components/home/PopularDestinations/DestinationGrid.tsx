import React from 'react';
import { motion } from 'framer-motion';
import DestinationCard from './DestinationCard';
import DestinationModal from './DestinationModal';
import { dubaiStructuredData, georgiaStructuredData, switzerlandStructuredData, baliStructuredData, thailandStructuredData, destinationFormData } from '../../../data/predefinedItineraries';

const destinations = [
    {
        country: 'DUBAI',
        duration: '7 DAY PLAN',
        image: 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=2070&auto=format&fit=crop',
        itinerary: `A 7-Day Symphony of Sand, Sky, and Souks. Experience architectural wonders, ancient traditions, and global gastronomy.`,
        structuredData: dubaiStructuredData,
        formData: destinationFormData.DUBAI
    },
    {
        country: 'GEORGIA',
        duration: '6 DAY PLAN',
        image: '/images/destinations/georgia.png',
        itinerary: `A 6-Day Journey Through the Crossroads of Europe and Asia. Explore Tbilisi's charm, the Caucasus Mountains, and the wine region of Kakheti.`,
        structuredData: georgiaStructuredData,
        formData: destinationFormData.GEORGIA
    },
    {
        country: 'SWITZERLAND',
        duration: '7 DAY PLAN',
        image: 'https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?q=80&w=2070&auto=format&fit=crop',
        itinerary: `A 7-Day Alpine Symphony: Mountains, Lakes & Legendary Views. Experience Lucerne, Interlaken, Zermatt, and the 'Top of Europe'.`,
        structuredData: switzerlandStructuredData,
        formData: destinationFormData.SWITZERLAND
    },
    {
        country: 'BALI',
        duration: '8 DAY PLAN',
        image: 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?q=80&w=2076&auto=format&fit=crop',
        itinerary: `An 8-Day Journey Through the Island of Gods. Explore Ubud's rice terraces, Nusa Penida's clifftops, and Seminyak's beach vibes.`,
        structuredData: baliStructuredData,
        formData: destinationFormData.BALI
    },
    {
        country: 'THAILAND',
        duration: '7 DAY PLAN',
        image: '/images/destinations/thailand.png',
        itinerary: `A 7-Day Journey Through the Land of Smiles. Explore Bangkok's energy, Chiang Mai's culture, and Phuket's tropical paradise.`,
        structuredData: thailandStructuredData,
        formData: destinationFormData.THAILAND
    },
    {
        country: 'CHINA',
        duration: '7 DAY PLAN',
        image: '/images/destinations/china.png',
        itinerary: `Day 1: Beijing Forbidden City & Jingshan Park
Day 2: Mutianyu Great Wall Experience
Day 3: Summer Palace & Temple of Heaven
Day 4: High Speed Train to Xi'an & Muslim Quarter
Day 5: Terracotta Warriors & City Wall
Day 6: Fly to Shanghai & The Bund Night View
Day 7: Yu Garden & Shanghai Tower`
    }
];

const DestinationGrid: React.FC = () => {
    const [selectedDest, setSelectedDest] = React.useState<typeof destinations[0] | null>(null);

    return (
        <section className="py-32 px-6">
            <div className="max-w-7xl mx-auto">
                <header className="text-center mb-20">
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        whileInView={{ opacity: 1, scale: 1 }}
                        className="inline-block px-6 py-2 bg-primary-50 text-primary-600 rounded-full text-xs font-black uppercase tracking-[0.3em] mb-6"
                    >
                        Explorer's Choice
                    </motion.div>
                    <h2 className="text-6xl md:text-8xl font-bold font-heading text-gray-900 tracking-tight leading-none mb-8">
                        TOP <span className="text-primary-600">DESTINATIONS</span>
                    </h2>
                    <p className="text-xl md:text-2xl text-gray-400 max-w-2xl mx-auto font-body">
                        Chosen by thousands. Tailored by AI. These curated itineraries are ready for your next adventure.
                    </p>
                </header>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
                    {destinations.map((dest, i) => (
                        <motion.div
                            key={dest.country}
                            initial={{ opacity: 0, y: 30 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            transition={{ delay: i * 0.1, duration: 0.6 }}
                            viewport={{ once: true }}
                        >
                            <DestinationCard
                                {...dest}
                                onClick={() => setSelectedDest(dest)}
                            />
                        </motion.div>
                    ))}
                </div>
            </div>

            <DestinationModal
                dest={selectedDest}
                onClose={() => setSelectedDest(null)}
            />
        </section>
    );
};

export default DestinationGrid;
