import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Calendar, MapPin, Wallet, Plane,
    Clock, Utensils, Info, CheckCircle2, Save, RefreshCcw,
    ChevronRight, CreditCard, Sparkles, Loader2, Download, User
} from 'lucide-react';
import { generateItineraryPDF } from '../../utils/ItineraryGenerator';

interface ItineraryData {
    title: string;
    intro: string;
    budget_disclaimer?: string;
    logistics: {
        category: string;
        details: string;
        cost: string;
    }[];
    itinerary: {
        day: number;
        date: string;
        theme: string;
        activities: {
            time: string;
            description: string;
            dining: string;
        }[];
    }[];
    budget_analysis: {
        total_estimated_cost: string;
        breakdown: {
            category: string;
            cost: string;
            explanation: string;
        }[];
        saving_tips: string[];
        dining_highlights?: {
            place: string;
            dish: string;
            vibe: string;
        }[];
    };
}

interface Props {
    data: ItineraryData | any;
    formData: any;
    isRaw?: boolean;
    onRegenerate: (refinement?: string) => void;
    onSave: () => void;
    isGenerating?: boolean;
    isSaving?: boolean;
}

const ItineraryDisplay: React.FC<Props> = ({ data, formData, isRaw, onRegenerate, onSave, isGenerating, isSaving }) => {
    const [activeTab, setActiveTab] = useState<'full' | 'daily' | 'save'>('full');
    const [refinementText, setRefinementText] = useState('');
    const [isDownloading, setIsDownloading] = useState(false);

    const handleDownload = async () => {
        try {
            setIsDownloading(true);
            await new Promise(resolve => setTimeout(resolve, 300));
            generateItineraryPDF(data, formData);
        } catch (error) {
            console.error('PDF Generation failed:', error);
            alert('Failed to generate PDF. Please try again.');
        } finally {
            setIsDownloading(false);
        }
    };

    if (isRaw || typeof data === 'string') {
        return (
            <div className="bg-white p-12 rounded-[4rem] shadow-2xl border border-gray-100 whitespace-pre-wrap leading-relaxed text-xl text-gray-700">
                {typeof data === 'string' ? data : JSON.stringify(data, null, 2)}
            </div>
        );
    }

    const totalBudgetRaw = Number(formData.budget) || (Number(formData.budget_per_person) * Number(formData.passengers));
    const budgetPerPerson = formData.budget_per_person || (totalBudgetRaw / Number(formData.passengers));

    return (
        <div className="max-w-7xl mx-auto pb-20 px-4">
            {/* Success Alert */}
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-green-50 border border-green-100 p-6 rounded-2xl flex items-center gap-3 text-green-700 mb-12 shadow-sm"
            >
                <CheckCircle2 size={24} className="text-green-500" />
                <span className="font-bold text-lg">Personalized {data.itinerary?.length || 0}-Day Itinerary Generated!</span>
            </motion.div>

            {/* Summary Header Cards - Reference Image 1 */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-16">
                <div className="flex items-center gap-6 p-4">
                    <div className="w-10 h-10 bg-primary-50 rounded-full flex items-center justify-center text-primary-600 shrink-0">
                        <MapPin size={20} />
                    </div>
                    <div>
                        <p className="text-sm font-bold text-gray-900">From: <span className="font-medium text-gray-600 uppercase">{formData.departure_city}</span></p>
                        <div className="flex items-center gap-2 mt-1">
                            <Plane size={16} className="text-gray-400" />
                            <p className="text-sm font-bold text-gray-900">To: <span className="font-medium text-gray-600 uppercase">{formData.destination}</span></p>
                        </div>
                    </div>
                </div>

                <div className="flex items-center gap-6 p-4">
                    <div className="w-10 h-10 bg-secondary-50 rounded-full flex items-center justify-center text-secondary-600 shrink-0">
                        <Calendar size={20} />
                    </div>
                    <div>
                        <p className="text-sm font-bold text-gray-900">Dates: <span className="font-medium text-gray-600">{formData.start_date} - {formData.end_date}</span></p>
                        <div className="flex items-center gap-2 mt-1">
                            <User size={16} className="text-gray-400" />
                            <p className="text-sm font-bold text-gray-900">Travelers: <span className="font-medium text-gray-600">{formData.passengers}</span></p>
                        </div>
                    </div>
                </div>

                <div className="flex items-center gap-6 p-4">
                    <div className="w-10 h-10 bg-green-50 rounded-full flex items-center justify-center text-green-600 shrink-0">
                        <Wallet size={20} />
                    </div>
                    <div>
                        <p className="text-sm font-bold text-gray-900">Budget per person: <span className="font-medium text-gray-600">{formData.currency} {Number(budgetPerPerson).toLocaleString()}</span></p>
                        <div className="flex items-center gap-2 mt-1">
                            <CreditCard size={16} className="text-gray-400" />
                            <p className="text-sm font-bold text-gray-900">Total budget: <span className="font-medium text-gray-600">{formData.currency} {Number(totalBudgetRaw).toLocaleString()}</span></p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Custom Tabs Navigation */}
            <div className="flex gap-8 mb-16 border-b border-gray-100">
                {(['full', 'daily', 'save'] as const).map((tab) => (
                    <button
                        key={tab}
                        onClick={() => setActiveTab(tab)}
                        className={`pb-4 px-2 font-bold text-sm uppercase tracking-widest transition-all relative flex items-center gap-2 ${activeTab === tab ? 'text-primary-600' : 'text-gray-400 hover:text-gray-600'
                            }`}
                    >
                        {tab === 'full' && <Plane size={18} />}
                        {tab === 'daily' && <Clock size={18} />}
                        {tab === 'save' && <Save size={18} />}
                        {tab === 'full' ? 'Full Itinerary' : tab === 'daily' ? 'Daily Plan' : 'Save Trip'}
                        {activeTab === tab && (
                            <motion.div
                                layoutId="activeTabDisplay"
                                className="absolute bottom-0 left-0 right-0 h-1 bg-primary-600 rounded-full"
                            />
                        )}
                    </button>
                ))}
            </div>

            {/* Content Area */}
            <AnimatePresence mode="wait">
                <motion.div
                    key={activeTab}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    transition={{ duration: 0.3 }}
                >
                    {activeTab === 'full' && (
                        <div className="space-y-16">
                            {/* Intro Section - Reference Image 1 */}
                            <div>
                                <div className="flex items-center gap-4 mb-8">
                                    <Sparkles size={40} className="text-orange-400" />
                                    <h1 className="text-5xl font-bold font-heading text-gray-900 tracking-tight">Your Personalized <span className="capitalize">{formData.destination}</span> Itinerary</h1>
                                </div>

                                <div className="bg-white p-10 rounded-[2.5rem] shadow-sm border border-gray-100">
                                    <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-3">
                                        <span className="text-3xl text-primary-600">✈️</span> {data.title}
                                    </h2>
                                    <p className="text-lg text-gray-600 leading-relaxed mb-10">{data.intro}</p>

                                    {data.budget_disclaimer && (
                                        <div className="mt-12">
                                            <h3 className="text-4xl font-bold text-gray-900 mb-6 flex items-center gap-4 italic font-heading">
                                                <span className="text-5xl text-orange-500 not-italic">⚠️</span> Important Budget Disclaimer & Adjustment
                                            </h3>
                                            <p className="text-xl text-gray-700 leading-relaxed whitespace-pre-line bg-gray-50/50 p-8 rounded-3xl border border-gray-100">{data.budget_disclaimer}</p>
                                        </div>
                                    )}
                                </div>
                            </div>

                            {/* Logistics - Reference Image 2 */}
                            <div>
                                <h2 className="text-4xl font-bold font-heading text-gray-900 mb-10 flex items-center gap-4">
                                    <span className="text-5xl">🏨</span> Accommodation & Transport Logistics
                                </h2>
                                <div className="bg-white rounded-[2.5rem] shadow-sm border border-gray-100 overflow-hidden">
                                    <table className="w-full text-left border-collapse">
                                        <thead>
                                            <tr className="bg-gray-50/50">
                                                <th className="p-8 font-bold text-gray-900 text-lg border-b border-gray-100">Category</th>
                                                <th className="p-8 font-bold text-gray-900 text-lg border-b border-gray-100">Details</th>
                                                <th className="p-8 font-bold text-gray-900 text-lg border-b border-gray-100">Estimated Cost ({formData.passengers} people)</th>
                                            </tr>
                                        </thead>
                                        <tbody className="divide-y divide-gray-100">
                                            {(data.logistics || []).map((item: any, idx: number) => (
                                                <tr key={idx} className="hover:bg-gray-50/30 transition-colors">
                                                    <td className="p-8 font-bold text-gray-900 align-top">{item.category}</td>
                                                    <td className="p-8 text-gray-600 align-top whitespace-pre-line">{item.details}</td>
                                                    <td className="p-8 text-gray-900 font-medium align-top">{item.cost}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>

                            {/* Daily Itinerary - Reference Images 2, 3, 4, 5 */}
                            <div>
                                <h2 className="text-4xl font-bold font-heading text-gray-900 mb-10 flex items-center gap-4">
                                    <span className="text-5xl">📅</span> Day-by-Day Personalized Itinerary
                                </h2>
                                <div className="space-y-16">
                                    {data.itinerary?.map((day: any) => (
                                        <div key={day.day}>
                                            <h3 className="text-3xl font-bold text-gray-900 mb-8 pb-4 border-b-2 border-gray-100">
                                                Day {day.day}: <span className="font-heading">{day.theme}</span> <span className="text-gray-400 font-medium text-2xl ml-2 font-sans">({day.date})</span>
                                            </h3>
                                            <div className="bg-white rounded-[2.5rem] shadow-sm border border-gray-100 overflow-hidden">
                                                <table className="w-full text-left border-collapse">
                                                    <thead>
                                                        <tr className="bg-gray-50/50">
                                                            <th className="p-8 font-bold text-gray-900 border-b border-gray-100 w-1/4">Time</th>
                                                            <th className="p-8 font-bold text-gray-900 border-b border-gray-100 w-1/2">Activity & Sightseeing</th>
                                                            <th className="p-8 font-bold text-gray-900 border-b border-gray-100 w-1/4">Dining Recommendation</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody className="divide-y divide-gray-100">
                                                        {day.activities?.map((act: any, idx: number) => (
                                                            <tr key={idx} className="hover:bg-gray-50/30 transition-colors">
                                                                <td className="p-8 font-bold text-gray-900 align-top">{act.time}</td>
                                                                <td className="p-8 text-gray-600 align-top leading-relaxed">{act.description}</td>
                                                                <td className="p-8 text-gray-900 font-medium align-top italic">{act.dining}</td>
                                                            </tr>
                                                        ))}
                                                    </tbody>
                                                </table>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {/* Iconic Dining Highlights - NEW */}
                            {data.budget_analysis?.dining_highlights && data.budget_analysis.dining_highlights.length > 0 && (
                                <div className="mt-16">
                                    <h2 className="text-4xl font-bold font-heading text-gray-900 mb-10 flex items-center gap-4">
                                        <span className="text-5xl">🍴</span> Iconic Local Dining Highlights
                                    </h2>
                                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                                        {data.budget_analysis.dining_highlights.map((item: any, idx: number) => (
                                            <div key={idx} className="bg-orange-50/50 p-8 rounded-[2.5rem] border border-orange-100 relative overflow-hidden group hover:bg-orange-50 transition-all">
                                                <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                                                    <Utensils size={80} />
                                                </div>
                                                <h4 className="text-xl font-bold text-gray-900 mb-2">{item.place}</h4>
                                                <div className="flex items-center gap-2 mb-4">
                                                    <Sparkles size={16} className="text-orange-500" />
                                                    <span className="text-sm font-black text-orange-600 uppercase tracking-wider">Must Try: {item.dish}</span>
                                                </div>
                                                <p className="text-gray-600 leading-relaxed italic">"{item.vibe}"</p>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* Budget Breakdown - Reference Image 5 */}
                            <div>
                                <h2 className="text-4xl font-bold font-heading text-gray-900 mb-10 flex items-center gap-4">
                                    <span className="text-5xl">💰</span> Detailed Budget Breakdown (For {formData.passengers} people, {data.itinerary?.length || 0} Days)
                                </h2>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                    {data.budget_analysis?.breakdown?.map((item: any, idx: number) => (
                                        <div key={idx} className="bg-white p-10 rounded-[2.5rem] shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                                            <div className="flex justify-between items-start mb-6">
                                                <h4 className="text-xl font-bold text-gray-400 uppercase tracking-widest">{item.category}</h4>
                                                <p className="text-3xl font-black text-primary-600 font-heading">{item.cost}</p>
                                            </div>
                                            <p className="text-gray-600 leading-relaxed text-lg font-medium">{item.explanation}</p>
                                        </div>
                                    ))}
                                </div>

                                {data.budget_analysis?.saving_tips && (
                                    <div className="mt-12 bg-primary-900 p-12 rounded-[3.5rem] text-white">
                                        <div className="flex items-center gap-4 mb-8">
                                            <Sparkles size={32} className="text-primary-300" />
                                            <h3 className="text-3xl font-bold font-heading tracking-tight">Expert Saving Tips</h3>
                                        </div>
                                        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                                            {data.budget_analysis.saving_tips.map((tip: string, idx: number) => (
                                                <div key={idx} className="flex gap-4 items-start bg-white/10 p-6 rounded-2xl border border-white/5">
                                                    <div className="w-8 h-8 rounded-full bg-primary-400/20 flex items-center justify-center shrink-0 mt-1">
                                                        <span className="font-bold text-primary-200">{idx + 1}</span>
                                                    </div>
                                                    <p className="text-lg leading-relaxed text-primary-50">{tip}</p>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>
                    )}

                    {activeTab === 'daily' && (
                        <div className="space-y-12">
                            {data.itinerary?.map((day: any) => (
                                <div key={day.day} className="bg-white p-12 rounded-[3rem] shadow-sm border border-gray-100 relative overflow-hidden">
                                    <div className="absolute top-0 right-0 w-32 h-32 bg-primary-50 blur-[50px] -mr-16 -mt-16 opacity-50" />

                                    <div className="flex flex-col md:flex-row gap-10 relative z-10">
                                        <div className="md:w-1/4">
                                            <div className="sticky top-0">
                                                <div className="w-20 h-20 bg-primary-600 rounded-3xl flex flex-col items-center justify-center text-white shadow-xl shadow-primary-500/30 mb-6">
                                                    <span className="text-xs font-black uppercase tracking-widest opacity-80">Day</span>
                                                    <span className="text-3xl font-black leading-none">{day.day}</span>
                                                </div>
                                                <h3 className="text-2xl font-bold text-gray-900 mb-2 font-heading leading-tight">{day.theme}</h3>
                                                <p className="text-gray-400 font-bold uppercase tracking-widest text-sm">{day.date}</p>
                                            </div>
                                        </div>

                                        <div className="flex-1 space-y-10">
                                            {day.activities?.map((act: any, idx: number) => (
                                                <div key={idx} className="relative pl-10 border-l-2 border-primary-100 last:border-0 pb-2">
                                                    <div className="absolute left-[-9px] top-2 w-4 h-4 bg-primary-600 rounded-full border-4 border-white shadow-sm" />
                                                    <div className="flex items-center gap-3 mb-3 text-primary-600 uppercase tracking-widest font-black text-xs">
                                                        <Clock size={14} />
                                                        {act.time}
                                                    </div>
                                                    <p className="text-xl text-gray-700 font-medium leading-relaxed mb-6 bg-gray-50/50 p-6 rounded-2xl border border-gray-50">
                                                        {act.description}
                                                    </p>
                                                    {act.dining && (
                                                        <div className="flex items-center gap-4 p-5 bg-orange-50/50 rounded-2xl border border-orange-100 text-orange-800">
                                                            <Utensils size={20} className="text-orange-500 shrink-0" />
                                                            <p className="italic font-medium">
                                                                <span className="font-black uppercase text-[10px] tracking-widest mr-2 opacity-60">Dining Suggestion:</span>
                                                                {act.dining}
                                                            </p>
                                                        </div>
                                                    )}
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}

                    {activeTab === 'save' && (
                        <div className="bg-white p-20 rounded-[4rem] text-center shadow-xl border border-gray-50">
                            <div className="w-24 h-24 bg-green-50 text-green-600 rounded-full flex items-center justify-center mx-auto mb-8">
                                <Save size={48} />
                            </div>
                            <h2 className="text-4xl font-bold font-heading mb-4 text-gray-900">Preserve the Adventure</h2>
                            <p className="text-xl text-gray-500 mb-12 max-w-2xl mx-auto font-medium">
                                Save this itinerary to your profile to access it anytime, download as PDF, or share with fellow explorers.
                            </p>

                            <div className="max-w-xl mx-auto mb-10 text-left">
                                <label className="block text-sm font-bold text-gray-400 uppercase tracking-widest mb-3 ml-2">
                                    Adjust / Refine Your Plan
                                </label>
                                <textarea
                                    value={refinementText}
                                    onChange={(e) => setRefinementText(e.target.value)}
                                    placeholder="e.g. Include more local street food gems, or make the schedule more relaxed..."
                                    className="w-full p-8 bg-gray-50 border border-gray-100 rounded-[2.5rem] focus:ring-4 focus:ring-primary-500/10 focus:border-primary-500 outline-none transition-all text-gray-700 resize-none h-40 text-lg font-medium shadow-inner"
                                />
                            </div>

                            <div className="flex flex-col md:flex-row gap-6 justify-center">
                                <button
                                    onClick={onSave}
                                    disabled={isSaving}
                                    className="px-12 py-6 bg-primary-600 text-white font-bold rounded-3xl hover:scale-105 active:scale-95 transition-all shadow-xl shadow-primary-500/20 flex items-center gap-3 disabled:animate-pulse disabled:opacity-70"
                                >
                                    {isSaving ? (
                                        <><Loader2 size={24} className="animate-spin" /> Saving...</>
                                    ) : (
                                        <><Save size={24} /> Save to My Trips</>
                                    )}
                                </button>
                                <button
                                    onClick={handleDownload}
                                    disabled={isDownloading}
                                    className="px-12 py-6 bg-secondary-500 text-white font-bold rounded-3xl hover:scale-105 active:scale-95 transition-all shadow-xl shadow-secondary-500/20 flex items-center gap-3 disabled:opacity-70"
                                >
                                    {isDownloading ? (
                                        <><Loader2 size={24} className="animate-spin" /> Preparing...</>
                                    ) : (
                                        <><Download size={24} /> Download Clean PDF</>
                                    )}
                                </button>
                                <button
                                    onClick={() => onRegenerate(refinementText)}
                                    disabled={isGenerating}
                                    className="px-12 py-6 bg-gray-900 text-white font-bold rounded-3xl hover:scale-105 active:scale-95 transition-all shadow-xl flex items-center gap-3 disabled:animate-pulse disabled:opacity-70"
                                >
                                    {isGenerating ? (
                                        <><RefreshCcw size={24} className="animate-spin" /> Weaving New Magic...</>
                                    ) : (
                                        <><RefreshCcw size={24} /> Regenerate Plan</>
                                    )}
                                </button>
                            </div>
                        </div>
                    )}
                </motion.div>
            </AnimatePresence>
        </div>
    );
};

export default ItineraryDisplay;
