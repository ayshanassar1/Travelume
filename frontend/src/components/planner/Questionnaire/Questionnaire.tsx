import React, { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { usePlanner } from '../../../hooks/usePlanner';
import {
    ArrowLeft, ArrowRight, Sparkles, Loader2, MapPin,
    Calendar, Compass, Utensils, Plane, Hotel,
    Coins, Wallet, MessageSquare, Users
} from 'lucide-react';
import { useNavigate, NavLink } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { RootState } from '../../../store';
import apiClient from '../../../api/client';
import ItineraryDisplay from '../ItineraryDisplay';

const MultiSelectGroup: React.FC<{
    label: string;
    options: string[];
    selected: string[];
    onToggle: (val: string) => void;
    icon: React.ReactNode;
}> = ({ label, options, selected, onToggle, icon }) => (
    <div className="mb-10">
        <div className="flex items-center gap-3 mb-4 text-gray-700">
            {icon}
            <h3 className="text-xl font-bold font-heading">{label}</h3>
        </div>
        <div className="flex flex-wrap gap-3">
            {options.map(opt => (
                <button
                    key={opt}
                    onClick={() => onToggle(opt)}
                    className={`px-6 py-3 rounded-2xl border-2 transition-all font-bold text-sm uppercase tracking-wider ${selected.includes(opt)
                        ? 'bg-primary-600 border-primary-600 text-white shadow-lg shadow-primary-500/30 active:scale-95'
                        : 'bg-white border-gray-100 text-gray-400 hover:border-primary-200 hover:text-gray-600 transition-all'
                        }`}
                >
                    {opt}
                </button>
            ))}
        </div>
    </div>
);

const Questionnaire: React.FC = () => {
    const {
        step,
        formData,
        nextStep,
        prevStep,
        updateFormData,
        toggleMultiSelect,
        generateTrip,
        isGenerating,
        itinerary,
        daysCount,
        totalBudget
    } = usePlanner();

    const [isSaving, setIsSaving] = React.useState(false);
    const [saveMessage, setSaveMessage] = React.useState<{ type: 'success' | 'error', text: string } | null>(null);

    const { isAuthenticated, user } = useSelector((state: RootState) => state.auth);
    const navigate = useNavigate();

    const handleSaveTrip = async () => {
        if (!isAuthenticated) {
            navigate('/login');
            return;
        }

        setIsSaving(true);
        setSaveMessage(null);
        try {
            await apiClient.post('/trips/', {
                name: itinerary?.itinerary.title || `Trip to ${formData.destination}`,
                destination: formData.destination,
                duration: `${daysCount} Days`,
                budget: `${formData.currency} ${totalBudget.toLocaleString()}`,
                itinerary_data: itinerary?.itinerary,
                planner_form: formData,
                user_email: user?.email
            });
            setSaveMessage({
                type: 'success',
                text: 'Your journey has been woven and preserved in your profile!'
            });
        } catch (err: any) {
            setSaveMessage({ type: 'error', text: 'Failed to save trip. Please try again.' });
        } finally {
            setIsSaving(false);
        }
    };

    useEffect(() => {
        if (itinerary) {
            setTimeout(() => {
                window.scrollTo({ top: window.innerHeight, behavior: 'smooth' });
            }, 100);
        }
    }, [itinerary]);

    const renderStep = () => {
        switch (step) {
            case 1:
                return (
                    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }} className="space-y-12">
                        <div>
                            <div className="flex items-center gap-4 mb-4 text-primary-600">
                                <MapPin size={24} />
                                <h2 className="text-2xl font-bold font-heading">The Essentials</h2>
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                <div className="space-y-2">
                                    <label className="text-sm font-bold text-gray-400 uppercase tracking-widest pl-2">Starting Point</label>
                                    <input
                                        type="text"
                                        placeholder="e.g. London, UK"
                                        value={formData.departure_city}
                                        onChange={(e) => updateFormData({ departure_city: e.target.value })}
                                        className="w-full p-6 bg-gray-50 border-2 border-transparent focus:border-primary-500 focus:bg-white rounded-3xl outline-none transition-all text-xl"
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label className="text-sm font-bold text-gray-400 uppercase tracking-widest pl-2">Dream Destination</label>
                                    <input
                                        type="text"
                                        placeholder="e.g. Kyoto, Japan"
                                        value={formData.destination}
                                        onChange={(e) => updateFormData({ destination: e.target.value })}
                                        className="w-full p-6 bg-gray-50 border-2 border-transparent focus:border-primary-500 focus:bg-white rounded-3xl outline-none transition-all text-xl"
                                    />
                                </div>
                            </div>
                        </div>

                        <div>
                            <div className="flex items-center justify-between mb-4">
                                <div className="flex items-center gap-4 text-primary-600">
                                    <Calendar size={24} />
                                    <h2 className="text-2xl font-bold font-heading">Travel Dates</h2>
                                </div>
                                <AnimatePresence>
                                    {daysCount > 0 && (
                                        <motion.div
                                            initial={{ opacity: 0, scale: 0.8 }}
                                            animate={{ opacity: 1, scale: 1 }}
                                            exit={{ opacity: 0, scale: 0.8 }}
                                            className="px-4 py-2 bg-primary-50 text-primary-600 rounded-xl border border-primary-100 font-bold flex items-center gap-2"
                                        >
                                            <Sparkles size={16} />
                                            {daysCount} {daysCount === 1 ? 'Day' : 'Days'} Journey
                                        </motion.div>
                                    )}
                                </AnimatePresence>
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                <div className="space-y-2">
                                    <label className="text-sm font-bold text-gray-400 uppercase tracking-widest pl-2">From</label>
                                    <input
                                        type="date"
                                        value={formData.start_date}
                                        onChange={(e) => updateFormData({ start_date: e.target.value })}
                                        className="w-full p-6 bg-gray-50 border-2 border-transparent focus:border-primary-500 focus:bg-white rounded-3xl outline-none transition-all text-xl"
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label className="text-sm font-bold text-gray-400 uppercase tracking-widest pl-2">Until</label>
                                    <input
                                        type="date"
                                        value={formData.end_date}
                                        onChange={(e) => updateFormData({ end_date: e.target.value })}
                                        className="w-full p-6 bg-gray-50 border-2 border-transparent focus:border-primary-500 focus:bg-white rounded-3xl outline-none transition-all text-xl"
                                    />
                                </div>
                            </div>
                        </div>
                    </motion.div>
                );
            case 2:
                return (
                    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}>
                        <MultiSelectGroup
                            label="Travel Pace"
                            icon={<Compass size={24} className="text-primary-600" />}
                            options={['Slow', 'Moderate', 'Fast', 'Intense']}
                            selected={formData.travel_pace}
                            onToggle={(v) => toggleMultiSelect('travel_pace', v)}
                        />
                        <MultiSelectGroup
                            label="Journey Theme"
                            icon={<Sparkles size={24} className="text-primary-600" />}
                            options={['Romantic', 'Adventure', 'Cultural', 'Relaxation', 'Foodie', 'Nature']}
                            selected={formData.travel_themes}
                            onToggle={(v) => toggleMultiSelect('travel_themes', v)}
                        />
                        <MultiSelectGroup
                            label="Cuisine Preferences"
                            icon={<Utensils size={24} className="text-primary-600" />}
                            options={['Halal', 'Veg', 'Non-Veg', 'Seafood', 'Vegan']}
                            selected={formData.food_preferences}
                            onToggle={(v) => toggleMultiSelect('food_preferences', v)}
                        />
                        <MultiSelectGroup
                            label="Preferred Transit"
                            icon={<Plane size={24} className="text-primary-600" />}
                            options={['Bus', 'Car', 'Flight', 'Connection Flight', 'Train']}
                            selected={formData.transit_modes}
                            onToggle={(v) => toggleMultiSelect('transit_modes', v)}
                        />
                        <MultiSelectGroup
                            label="Stay Style"
                            icon={<Hotel size={24} className="text-primary-600" />}
                            options={['Hotel', 'Resort', 'Airbnb', 'Hostel', 'Vila']}
                            selected={formData.stay_types}
                            onToggle={(v) => toggleMultiSelect('stay_types', v)}
                        />
                    </motion.div>
                );
            case 3:
                return (
                    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }} className="space-y-12">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
                            <div className="space-y-4">
                                <div className="flex items-center gap-3 text-primary-600">
                                    <Coins size={24} />
                                    <h3 className="text-xl font-bold font-heading">Currency</h3>
                                </div>
                                <div className="flex gap-3">
                                    {['INR', 'USD', 'EUR', 'GBP'].map(c => (
                                        <button
                                            key={c}
                                            onClick={() => updateFormData({ currency: c })}
                                            className={`px-8 py-4 rounded-2xl border-2 font-bold transition-all ${formData.currency === c
                                                ? 'bg-primary-600 border-primary-600 text-white shadow-lg'
                                                : 'bg-white border-gray-100 text-gray-400 hover:border-primary-200'
                                                }`}
                                        >
                                            {c}
                                        </button>
                                    ))}
                                </div>
                            </div>

                            <div className="space-y-4">
                                <div className="flex items-center gap-3 text-primary-600">
                                    <Users size={24} />
                                    <h3 className="text-xl font-bold font-heading">Number of Travellers</h3>
                                </div>
                                <input
                                    type="number"
                                    min="1"
                                    placeholder="Number of travellers"
                                    value={formData.passengers}
                                    onChange={(e) => updateFormData({ passengers: e.target.value })}
                                    className="w-full p-6 bg-gray-50 border-2 border-transparent focus:border-primary-500 rounded-3xl outline-none text-2xl font-bold tracking-tight"
                                />
                            </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
                            <div className="space-y-4">
                                <div className="flex items-center gap-3 text-primary-600">
                                    <Wallet size={24} />
                                    <h3 className="text-xl font-bold font-heading">Budget Per Person</h3>
                                </div>
                                <input
                                    type="text"
                                    placeholder="e.g. 50000"
                                    value={formData.budget_per_person}
                                    onChange={(e) => updateFormData({ budget_per_person: e.target.value })}
                                    className="w-full p-6 bg-gray-50 border-2 border-transparent focus:border-primary-500 rounded-3xl outline-none text-2xl font-bold tracking-tight"
                                />
                            </div>

                            <div className="space-y-4">
                                <div className="flex items-center gap-3 text-primary-600">
                                    <Sparkles size={24} className="text-secondary-500" />
                                    <h3 className="text-xl font-bold font-heading">Total Planned Budget</h3>
                                </div>
                                <div className="p-6 bg-primary-50 rounded-3xl border-2 border-primary-100 flex items-center justify-center">
                                    <span className="text-3xl font-black text-primary-600 tracking-tighter">
                                        {formData.currency} {totalBudget.toLocaleString()}
                                    </span>
                                </div>
                            </div>
                        </div>

                        <div className="space-y-4">
                            <div className="flex items-center gap-3 text-primary-600">
                                <MessageSquare size={24} />
                                <h3 className="text-xl font-bold font-heading">Additional Preferences</h3>
                            </div>
                            <textarea
                                rows={5}
                                placeholder="Share anything else... Special requirements, dietary restrictions, or specific interests."
                                value={formData.additional_prefs}
                                onChange={(e) => updateFormData({ additional_prefs: e.target.value })}
                                className="w-full p-8 bg-gray-50 border-2 border-transparent focus:border-primary-500 rounded-[2.5rem] outline-none text-lg resize-none"
                            />
                        </div>
                    </motion.div>
                );
            default:
                return null;
        }
    };

    return (
        <div className={`mx-auto transition-all duration-700 ${itinerary ? 'max-w-6xl' : 'max-w-4xl'}`}>
            {/* Cinematic Progress */}
            {!itinerary && (
                <div className="mb-20">
                    <div className="flex justify-between items-end mb-6">
                        <div>
                            <span className="text-xs font-black text-primary-600 uppercase tracking-[0.3em]">Phase {step} of 3</span>
                            <h3 className="text-3xl font-bold font-heading text-gray-900 mt-2">
                                {step === 1 && "The Basics"}
                                {step === 2 && "The Soul of the Trip"}
                                {step === 3 && "Final Details"}
                            </h3>
                        </div>
                        <div className="flex gap-1">
                            {[1, 2, 3].map(s => (
                                <div key={s} className={`w-12 h-1.5 rounded-full transition-all duration-500 ${step >= s ? 'bg-primary-600 shadow-[0_0_15px_rgba(0,102,255,0.5)]' : 'bg-gray-100'}`} />
                            ))}
                        </div>
                    </div>
                </div>
            )}

            <div className="min-h-[600px] p-12 bg-white rounded-[4rem] shadow-2xl border border-gray-100 relative overflow-hidden">
                <div className="absolute top-0 right-0 w-64 h-64 bg-primary-100/20 blur-[100px] -mr-32 -mt-32" />
                <div className="relative z-10">
                    <AnimatePresence mode="wait">
                        {renderStep()}
                    </AnimatePresence>
                </div>
            </div>

            <div className="flex items-center justify-between mt-16 px-4">
                <button
                    onClick={prevStep}
                    disabled={step === 1 || isGenerating}
                    className="flex items-center gap-3 px-10 py-5 text-gray-400 font-bold rounded-2xl hover:bg-gray-50 hover:text-gray-900 transition-all disabled:opacity-0"
                >
                    <ArrowLeft size={24} /> Back
                </button>

                {step === 3 ? (
                    <button
                        onClick={() => generateTrip()}
                        disabled={isGenerating}
                        className="flex items-center gap-4 px-12 py-6 bg-primary-600 text-white text-xl font-bold rounded-[2rem] shadow-2xl shadow-primary-500/40 hover:scale-105 active:scale-95 transition-all disabled:animate-pulse disabled:scale-100"
                    >
                        {isGenerating ? (
                            <>
                                <Loader2 size={24} className="animate-spin" /> Weaving the Universe...
                            </>
                        ) : (
                            <>
                                Ignite My Journey <Sparkles size={24} />
                            </>
                        )}
                    </button>
                ) : (
                    <button
                        onClick={nextStep}
                        className="flex items-center gap-4 px-12 py-6 bg-gray-900 text-white text-xl font-bold rounded-[2rem] shadow-2xl hover:bg-black hover:scale-105 active:scale-95 transition-all"
                    >
                        Advance <ArrowRight size={24} />
                    </button>
                )}
            </div>

            {/* Generated Itinerary Section */}
            <AnimatePresence>
                {itinerary && (
                    <motion.div
                        initial={{ opacity: 0, y: 50 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="mt-20 pt-20 border-t border-gray-100"
                    >
                        {saveMessage && (
                            <div className={`mb-8 p-6 rounded-[2rem] border-2 shadow-xl flex flex-col md:flex-row items-center justify-between gap-6 ${saveMessage.type === 'success' ? 'bg-green-50 border-green-100 text-green-700' : 'bg-red-50 border-red-100 text-red-700'}`}>
                                <div className="flex items-center gap-4">
                                    <Sparkles className={saveMessage.type === 'success' ? 'text-green-600' : 'text-red-500'} size={32} />
                                    <span className="text-xl font-bold">{saveMessage.text}</span>
                                </div>
                                {saveMessage.type === 'success' && (
                                    <NavLink
                                        to="/account"
                                        className="px-8 py-3 bg-green-600 text-white rounded-xl font-bold hover:bg-green-700 transition-all flex items-center gap-2"
                                    >
                                        Go to My Journeys <ArrowRight size={18} />
                                    </NavLink>
                                )}
                            </div>
                        )}
                        <ItineraryDisplay
                            data={itinerary.itinerary}
                            formData={formData}
                            isRaw={itinerary.is_raw}
                            onRegenerate={generateTrip}
                            onSave={handleSaveTrip}
                            isGenerating={isGenerating}
                            isSaving={isSaving}
                        />
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default Questionnaire;
