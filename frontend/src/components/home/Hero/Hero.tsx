import React from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, Sparkles } from 'lucide-react';
import { NavLink } from 'react-router-dom';

const Hero: React.FC = () => {
    return (
        <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-[#000814]">
            {/* Cinematic Background Gradient */}
            <div className="absolute inset-0 z-0">
                <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-transparent to-black/80 z-10" />
                <div className="absolute inset-0 bg-black/20 z-0" />
                <motion.div
                    animate={{
                        scale: [1, 1.1, 1],
                        opacity: [0.3, 0.5, 0.3]
                    }}
                    transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                    className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?q=80&w=2021&auto=format&fit=crop')] bg-cover bg-center"
                />
            </div>

            <div className="container mx-auto px-6 relative z-10 text-center">
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-white mb-8"
                >
                    <Sparkles size={16} className="text-secondary-500" />
                    <span className="text-sm font-medium tracking-wide uppercase">AI-Powered Travel Intelligence</span>
                </motion.div>

                <motion.h1
                    initial={{ opacity: 0, y: 40 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 1, delay: 0.2 }}
                    className="text-6xl md:text-8xl lg:text-9xl font-bold font-heading text-white leading-[1.1] mb-8"
                >
                    Travel <span className="text-primary-400">Beyond</span> <br />
                    The <span className="handwritten text-secondary-500 text-7xl md:text-9xl">Ordinary</span>
                </motion.h1>

                <motion.p
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 1, delay: 0.4 }}
                    className="text-xl md:text-2xl text-white/70 max-w-2xl mx-auto mb-12 font-body"
                >
                    Transform your travel dreams into detailed, immersive itineraries with the power of world-class AI.
                </motion.p>

                <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.5, delay: 0.6 }}
                    className="flex flex-col md:flex-row items-center justify-center gap-6"
                >
                    <NavLink
                        to="/planner"
                        className="group relative px-10 py-5 bg-primary-600 text-white font-bold rounded-2xl overflow-hidden transition-all hover:scale-105 active:scale-95 shadow-2xl shadow-primary-500/40"
                    >
                        <div className="absolute inset-0 bg-gradient-to-r from-primary-400 to-primary-600 opacity-0 group-hover:opacity-100 transition-opacity" />
                        <span className="relative z-10 flex items-center gap-3 text-lg">
                            Start Planning Now <ArrowRight size={22} className="group-hover:translate-x-1 transition-transform" />
                        </span>
                    </NavLink>

                    <button className="px-10 py-5 bg-white/5 backdrop-blur-xl border border-white/10 text-white font-bold rounded-2xl hover:bg-white/10 transition-all">
                        Explore Destinations
                    </button>
                </motion.div>
            </div>

            {/* Floating Elements for Parallax Effect */}
            <motion.div
                animate={{ y: [0, -20, 0] }}
                transition={{ duration: 4, repeat: Infinity }}
                className="absolute bottom-20 left-20 hidden lg:block"
            >
                <div className="w-24 h-24 rounded-full border border-white/10 flex items-center justify-center backdrop-blur-lg">
                    <span className="text-3xl">✈️</span>
                </div>
            </motion.div>

            <motion.div
                animate={{ y: [0, 20, 0] }}
                transition={{ duration: 5, repeat: Infinity, delay: 0.5 }}
                className="absolute top-20 right-20 hidden xl:block"
            >
                <div className="w-32 h-32 rounded-3xl border border-white/10 flex items-center justify-center backdrop-blur-lg rotate-12">
                    <span className="text-4xl">📸</span>
                </div>
            </motion.div>
        </section>
    );
};

export default Hero;