import React from 'react';
import { motion } from 'framer-motion';
import { MapPin, Clock } from 'lucide-react';

interface DestinationCardProps {
    country: string;
    duration: string;
    image: string;
    onClick: () => void;
}

const DestinationCard: React.FC<DestinationCardProps> = ({ country, duration, image, onClick }) => {
    return (
        <motion.div
            whileHover={{ y: -15, scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={onClick}
            className="relative h-[500px] w-full rounded-[3rem] overflow-hidden cursor-pointer group shadow-2xl shadow-black/20"
        >
            {/* Background Image with Zoom Effect */}
            <motion.div
                initial={{ scale: 1 }}
                whileHover={{ scale: 1.1 }}
                transition={{ duration: 0.8, ease: "easeOut" }}
                className="absolute inset-0 bg-cover bg-center transition-transform"
                style={{ backgroundImage: `url('${image}')` }}
            />

            {/* Cinematic Overlays */}
            <div className="absolute inset-x-0 bottom-0 h-2/3 bg-gradient-to-t from-black/90 via-black/40 to-transparent transition-all duration-500 group-hover:from-black/100" />
            <div className="absolute inset-0 bg-primary-600/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />

            {/* Content */}
            <div className="absolute inset-0 p-10 flex flex-col justify-end">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                    className="flex items-center gap-2 mb-4"
                >
                    <div className="px-4 py-1.5 bg-white/20 backdrop-blur-md rounded-full border border-white/30 text-white text-xs font-black uppercase tracking-widest flex items-center gap-2">
                        <Clock size={14} /> {duration}
                    </div>
                </motion.div>

                <h3 className="text-4xl font-bold text-white font-heading mb-6 group-hover:scale-105 transition-transform origin-left">{country}</h3>

                <div className="flex items-center gap-2 text-primary-400 group-hover:text-white transition-colors">
                    <MapPin size={18} />
                    <span className="text-sm font-bold uppercase tracking-[0.2em]">View Itinerary</span>
                </div>
            </div>
        </motion.div>
    );
};

export default DestinationCard;
