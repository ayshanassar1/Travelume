import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Compass, Home, ArrowLeft } from 'lucide-react';
import Navbar from '../components/layout/Navbar/Navbar';

const NotFoundPage: React.FC = () => {
    const navigate = useNavigate();

    return (
        <div className="min-h-screen bg-white selection:bg-primary-100 italic-text">
            <Navbar />

            <main className="pt-32 pb-20 px-6 flex flex-col items-center justify-center min-h-[90vh] text-center max-w-4xl mx-auto">
                {/* Animated 404 Gradient Text */}
                <motion.div
                    initial={{ opacity: 0, scale: 0.5, rotate: -10 }}
                    animate={{ opacity: 1, scale: 1, rotate: 0 }}
                    transition={{ duration: 0.8, type: "spring" }}
                    className="relative mb-8"
                >
                    <h1 className="text-[12rem] md:text-[18rem] font-black leading-none tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-primary-600 to-primary-800 opacity-20 select-none">
                        404
                    </h1>
                    <div className="absolute inset-0 flex items-center justify-center">
                        <motion.div
                            animate={{
                                rotate: [0, 10, -10, 0],
                                scale: [1, 1.1, 1.1, 1]
                            }}
                            transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
                            className="w-24 h-24 md:w-32 md:h-32 bg-primary-600 rounded-[2rem] shadow-2xl shadow-primary-500/40 flex items-center justify-center text-white"
                        >
                            <Compass size={64} />
                        </motion.div>
                    </div>
                </motion.div>

                {/* Content */}
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3, duration: 0.8 }}
                >
                    <h2 className="text-4xl md:text-6xl font-black font-heading text-gray-900 mb-6 tracking-tight">
                        Journey into the Unknown?
                    </h2>
                    <p className="text-xl md:text-2xl text-gray-500 mb-12 max-w-2xl mx-auto leading-relaxed">
                        Even the best explorers get lost sometimes. The page you're searching for seems to have vanished from our maps.
                    </p>

                    <div className="flex flex-col sm:flex-row gap-6 justify-center items-center">
                        <button
                            onClick={() => navigate('/')}
                            className="group relative flex items-center gap-3 bg-gray-900 text-white px-10 py-5 rounded-2xl font-bold text-lg hover:bg-black transition-all shadow-xl shadow-gray-200"
                        >
                            <Home size={22} className="group-hover:scale-110 transition-transform" />
                            Return to Base
                        </button>

                        <button
                            onClick={() => navigate(-1)}
                            className="flex items-center gap-3 text-gray-600 hover:text-primary-600 font-bold text-lg px-8 py-4 transition-all"
                        >
                            <ArrowLeft size={22} />
                            Go Back
                        </button>
                    </div>
                </motion.div>

                {/* Background Decor */}
                <div className="fixed inset-0 pointer-events-none -z-10 overflow-hidden">
                    <div className="absolute top-1/4 -left-20 w-96 h-96 bg-primary-100 rounded-full blur-[120px] opacity-50" />
                    <div className="absolute bottom-1/4 -right-20 w-96 h-96 bg-secondary-100 rounded-full blur-[120px] opacity-50" />
                </div>
            </main>
        </div>
    );
};

export default NotFoundPage;
