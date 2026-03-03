import React from 'react';
import { motion } from 'framer-motion';
import { MapPin, Sparkles, Compass } from 'lucide-react';

const DestinationsPage: React.FC = () => {
    return (
        <div className="bg-white">
            <main className="pt-32 pb-20 px-6 max-w-7xl mx-auto text-center">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex flex-col items-center"
                >
                    <div className="w-20 h-20 bg-primary-50 text-primary-600 rounded-3xl flex items-center justify-center mb-8 shadow-xl shadow-primary-500/10">
                        <MapPin size={40} />
                    </div>
                    <h1 className="text-5xl md:text-7xl font-black font-heading text-gray-900 mb-6 tracking-tight">
                        Explore the World
                    </h1>
                    <p className="text-xl text-gray-500 mb-12 max-w-2xl leading-relaxed">
                        We're curating the world's most breathtaking destinations just for you. This section will soon feature immersive guides, local secrets, and AI-powered recommendations.
                    </p>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full mt-12">
                        {[
                            { title: 'Local Secrets', icon: Sparkles, color: 'text-amber-500', bg: 'bg-amber-50' },
                            { title: 'Interactive Maps', icon: MapPin, color: 'text-primary-600', bg: 'bg-primary-50' },
                            { title: 'AI Curated', icon: Compass, color: 'text-secondary-600', bg: 'bg-secondary-50' }
                        ].map((feature, i) => (
                            <motion.div
                                key={i}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.2 * i }}
                                className="p-8 rounded-[2.5rem] border border-gray-100 bg-gray-50/50 hover:bg-white hover:shadow-2xl transition-all group"
                            >
                                <div className={`w-14 h-14 ${feature.bg} ${feature.color} rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform`}>
                                    <feature.icon size={28} />
                                </div>
                                <h3 className="text-xl font-bold font-heading mb-3">{feature.title}</h3>
                                <p className="text-gray-500 font-medium">Coming soon to your Travelume experience.</p>
                            </motion.div>
                        ))}
                    </div>
                </motion.div>
            </main>
        </div>
    );
};

export default DestinationsPage;
