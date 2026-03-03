import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Sparkles, Loader2, ArrowRight } from 'lucide-react';
import { useSelector } from 'react-redux';
import { RootState } from '../../../store';
import { useNavigate, NavLink } from 'react-router-dom';
import apiClient from '../../../api/client';
import ItineraryDisplay from '../../planner/ItineraryDisplay';

interface DestinationModalProps {
    dest: {
        country: string;
        duration: string;
        itinerary: string;
        image: string;
        structuredData?: any;
        formData?: any;
    } | null;
    onClose: () => void;
}

const DestinationModal: React.FC<DestinationModalProps> = ({ dest, onClose }) => {
    const [isSaving, setIsSaving] = useState(false);
    const [saveMessage, setSaveMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);
    const { isAuthenticated, user } = useSelector((state: RootState) => state.auth);
    const navigate = useNavigate();

    if (!dest) return null;

    const handleSaveTrip = async () => {
        if (!isAuthenticated) {
            navigate('/login');
            return;
        }

        setIsSaving(true);
        setSaveMessage(null);
        try {
            await apiClient.post('/trips/', {
                name: dest.structuredData?.title || `Trip to ${dest.country}`,
                destination: dest.country,
                duration: dest.duration,
                budget: dest.formData?.budget || "Flexible",
                itinerary_data: dest.structuredData || { title: dest.country, intro: dest.itinerary, itinerary: [] },
                planner_form: dest.formData || { destination: dest.country },
                user_email: user?.email
            });
            setSaveMessage({
                type: 'success',
                text: 'This legendary journey has been added to your profile!'
            });
        } catch (err: any) {
            setSaveMessage({ type: 'error', text: 'Failed to save trip. Please try again.' });
        } finally {
            setIsSaving(false);
        }
    };

    const handleRegenerate = () => {
        // Redirect to planner with destination pre-filled
        navigate('/planner');
    };

    return (
        <AnimatePresence>
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="fixed inset-0 z-[100] flex items-center justify-center p-4 md:p-10"
            >
                {/* Backdrop */}
                <div
                    className="absolute inset-0 bg-black/90 backdrop-blur-2xl"
                    onClick={onClose}
                />

                {/* Modal Container */}
                <motion.div
                    initial={{ scale: 0.95, y: 40, opacity: 0 }}
                    animate={{ scale: 1, y: 0, opacity: 1 }}
                    exit={{ scale: 0.95, y: 40, opacity: 0 }}
                    transition={{ type: "spring", damping: 25, stiffness: 200 }}
                    className="relative bg-white rounded-[4rem] w-full max-w-7xl h-[90vh] overflow-hidden shadow-2xl flex flex-col border border-white/10"
                >
                    {/* Header */}
                    <div className="absolute top-0 left-0 right-0 p-8 flex justify-between items-center z-50 bg-white/80 backdrop-blur-md border-b border-gray-100">
                        <div className="flex items-center gap-4">
                            <div className="w-12 h-12 bg-primary-50 rounded-2xl flex items-center justify-center text-primary-600">
                                <Sparkles size={24} />
                            </div>
                            <div>
                                <h2 className="text-2xl font-bold font-heading text-gray-900 leading-none mb-1 uppercase tracking-tighter">
                                    {dest.country} <span className="text-primary-600">Premium Itinerary</span>
                                </h2>
                                <p className="text-sm font-bold text-gray-400 uppercase tracking-widest leading-none mt-1">{dest.duration}</p>
                            </div>
                        </div>
                        <button
                            onClick={onClose}
                            className="p-4 bg-gray-50 hover:bg-gray-100 text-gray-900 rounded-2xl transition-all"
                        >
                            <X size={24} />
                        </button>
                    </div>

                    {/* Content Area */}
                    <div className="flex-1 overflow-y-auto pt-32 pb-20 px-4 md:px-12 bg-gray-50/30">
                        {saveMessage && (
                            <motion.div
                                initial={{ opacity: 0, y: -20 }}
                                animate={{ opacity: 1, y: 0 }}
                                className={`mb-10 p-8 rounded-[2.5rem] border-2 shadow-xl flex flex-col md:flex-row items-center justify-between gap-6 max-w-5xl mx-auto ${saveMessage.type === 'success' ? 'bg-green-50 border-green-100 text-green-700' : 'bg-red-50 border-red-100 text-red-700'
                                    }`}
                            >
                                <div className="flex items-center gap-4">
                                    <Sparkles className={saveMessage.type === 'success' ? 'text-green-600' : 'text-red-500'} size={32} />
                                    <span className="text-xl font-bold">{saveMessage.text}</span>
                                </div>
                                {saveMessage.type === 'success' && (
                                    <NavLink
                                        to="/account"
                                        className="px-10 py-4 bg-green-600 text-white rounded-2xl font-bold hover:bg-green-700 transition-all flex items-center gap-2 shadow-lg shadow-green-600/20"
                                    >
                                        Go to My Journeys <ArrowRight size={18} />
                                    </NavLink>
                                )}
                            </motion.div>
                        )}

                        {dest.structuredData ? (
                            <ItineraryDisplay
                                data={dest.structuredData}
                                formData={dest.formData || { destination: dest.country }}
                                onRegenerate={handleRegenerate}
                                onSave={handleSaveTrip}
                                isSaving={isSaving}
                            />
                        ) : (
                            <div className="max-w-4xl mx-auto bg-white p-12 md:p-20 rounded-[4rem] shadow-sm border border-gray-100">
                                <div className="flex items-center gap-6 mb-12">
                                    <div className="p-4 bg-primary-50 text-primary-600 rounded-3xl">
                                        <Sparkles size={32} />
                                    </div>
                                    <h3 className="text-4xl font-bold font-heading text-gray-900 tracking-tight">Curated Adventure</h3>
                                </div>
                                <div className="prose prose-2xl max-w-none text-gray-600 leading-relaxed font-body whitespace-pre-wrap mb-16 italic">
                                    {dest.itinerary}
                                </div>
                                <button
                                    onClick={handleSaveTrip}
                                    disabled={isSaving}
                                    className="w-full py-6 bg-primary-600 text-white text-xl font-bold rounded-3xl shadow-2xl shadow-primary-500/20 hover:scale-[1.02] active:scale-95 transition-all flex items-center justify-center gap-4 disabled:animate-pulse"
                                >
                                    {isSaving ? <><Loader2 className="animate-spin" /> Weaving...</> : <><Sparkles size={24} /> Save to My Profile</>}
                                </button>
                            </div>
                        )}
                    </div>
                </motion.div>
            </motion.div>
        </AnimatePresence>
    );
};

export default DestinationModal;
