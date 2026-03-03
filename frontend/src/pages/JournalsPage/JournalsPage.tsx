import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Book,
    PenTool,
    Image as ImageIcon,
    Share2,
    ArrowLeft,
    Sparkles,
    Wand2,
    Plus,
    ArrowRight,
    Trash2,
    Eye,
    Loader2,
    Library,
    MapPin
} from 'lucide-react';
import { useSelector } from 'react-redux';
import JournalCreator from '../../components/journal/JournalCreator/JournalCreator';
import JournalPreview from '../../components/journal/JournalPreview/JournalPreview';
import apiClient, { getStaticUrl } from '../../api/client';

const JournalsPage: React.FC = () => {
    const { user } = useSelector((state: any) => state.auth);
    const [showCreator, setShowCreator] = useState(false);
    const [showPreview, setShowPreview] = useState(false);
    const [journalData, setJournalData] = useState<any>(null);
    const [journals, setJournals] = useState<any[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [isSaving, setIsSaving] = useState(false);

    useEffect(() => {
        if (user?.email) {
            fetchJournals();
        }
    }, [user]);

    const fetchJournals = async () => {
        setIsLoading(true);
        try {
            const response = await apiClient.get('/journals');
            setJournals(response.data);

        } catch (error) {
            console.error('Failed to fetch journals:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleGenerate = async (data: any) => {
        setIsSaving(true);
        try {
            const response = await apiClient.post('/journals', data);

            // Set data for preview (use the full processed data from server)

            setJournalData(response.data);
            setShowPreview(true);
            fetchJournals(); // Refresh list
        } catch (error) {
            console.error('Failed to save journal:', error);
            // Still show preview even if save fails
            setJournalData(data);
            setShowPreview(true);
        } finally {
            setIsSaving(false);
        }
    };

    const handleDelete = async (e: React.MouseEvent | null, id: string) => {
        if (e) e.stopPropagation();
        if (!window.confirm('Are you sure you want to delete this journal?')) return;

        try {
            await apiClient.delete(`/journals/${id}`);

            setJournals(prev => prev.filter(j => j.id !== id));
            if (showPreview && journalData?.id === id) {
                setShowPreview(false);
                setJournalData(null);
            }
        } catch (error) {
            console.error('Failed to delete journal:', error);
        }
    };

    const handleViewJournal = (journal: any) => {
        setJournalData(journal);
        setShowPreview(true);
    };

    const handleBack = () => {
        setShowPreview(false);
    };

    if (showPreview) {
        return (
            <div className="min-h-screen bg-[#f0f2f5]">
                <JournalPreview
                    data={journalData}
                    onBack={handleBack}
                    onDelete={(id) => handleDelete(null, id)}
                />
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-[#fafafa]">
            <main className="pt-32 pb-20 px-4 md:px-8">
                <AnimatePresence mode="wait">
                    {!showCreator ? (
                        <motion.div
                            key="landing"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -20 }}
                            className="max-w-6xl mx-auto"
                        >
                            {/* Hero Section */}
                            <div className="text-center mb-20">
                                <div className="relative mb-8 inline-block">
                                    <div className="w-24 h-24 bg-secondary-50 text-secondary-600 rounded-[2.5rem] flex items-center justify-center shadow-2xl shadow-secondary-500/10 relative z-10">
                                        <Book size={48} />
                                    </div>
                                    <div className="absolute -top-2 -right-2 w-8 h-8 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center shadow-sm animate-pulse">
                                        <Sparkles size={16} />
                                    </div>
                                </div>

                                <h1 className="text-5xl md:text-8xl font-black font-heading text-gray-900 mb-6 tracking-tight leading-none">
                                    Your Stories, <br /><span className="text-secondary-600 italic">Beautifully</span> Captured.
                                </h1>
                                <p className="text-xl text-gray-400 mb-12 max-w-2xl leading-relaxed mx-auto font-medium">
                                    Document your adventures with our rich digital scrapbooks.
                                    Add photos, videos, and daily stories to preserve every moment.
                                </p>

                                <button
                                    onClick={() => setShowCreator(true)}
                                    className="group px-10 py-5 bg-secondary-500 text-white rounded-[2rem] font-bold shadow-2xl shadow-secondary-500/30 hover:bg-secondary-600 transition-all flex items-center gap-3 mx-auto active:scale-95"
                                >
                                    <Plus size={24} />
                                    <span>Create New Adventure</span>
                                    <ArrowRight className="group-hover:translate-x-1 transition-transform" size={20} />
                                </button>
                            </div>

                            {/* My Journals Section */}
                            <div className="mt-32">
                                <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-12">
                                    <div className="flex items-center gap-4">
                                        <div className="w-12 h-12 bg-gray-100 rounded-2xl flex items-center justify-center text-gray-600">
                                            <Library size={24} />
                                        </div>
                                        <h2 className="text-3xl font-black text-gray-900 tracking-tight">My Memories</h2>
                                    </div>
                                    <div className="text-sm font-bold text-gray-400 uppercase tracking-widest bg-white px-6 py-2 rounded-full border border-gray-100 self-start md:self-auto">
                                        {journals.length} Saved Logs
                                    </div>
                                </div>

                                {isLoading ? (
                                    <div className="flex flex-col items-center justify-center py-20 bg-white rounded-[3rem] border border-gray-100 shadow-sm">
                                        <Loader2 className="w-12 h-12 text-secondary-500 animate-spin mb-4" />
                                        <p className="font-bold text-gray-400">Loading your memories...</p>
                                    </div>
                                ) : journals.length > 0 ? (
                                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                                        {journals.map((journal) => (
                                            <motion.div
                                                key={journal.id}
                                                initial={{ opacity: 0, scale: 0.9 }}
                                                animate={{ opacity: 1, scale: 1 }}
                                                whileHover={{ y: -5 }}
                                                onClick={() => handleViewJournal(journal)}
                                                className="group bg-white rounded-[3rem] border border-gray-100 shadow-sm hover:shadow-2xl transition-all overflow-hidden relative cursor-pointer"
                                            >
                                                {/* Card Header/Image */}
                                                <div className="aspect-[4/3] bg-gray-50 relative overflow-hidden">
                                                    {journal.tripImgs?.[0] ? (
                                                        <img
                                                            src={getStaticUrl(journal.tripImgs[0]) || ''}
                                                            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                                                            alt={journal.country}
                                                        />
                                                    ) : (
                                                        <div className="w-full h-full flex items-center justify-center text-gray-200">
                                                            <ImageIcon size={48} />
                                                        </div>
                                                    )}
                                                    <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-8">
                                                        <div className="flex gap-2 w-full">
                                                            <div className="flex-1 py-3 bg-white text-gray-900 rounded-xl font-bold flex items-center justify-center gap-2">
                                                                <Eye size={18} /> View Journal
                                                            </div>
                                                            <button
                                                                onClick={(e) => handleDelete(e, journal.id)}
                                                                className="p-3 bg-white/20 backdrop-blur-md text-white rounded-xl hover:bg-red-500 transition-colors"
                                                            >
                                                                <Trash2 size={18} />
                                                            </button>
                                                        </div>
                                                    </div>
                                                </div>

                                                {/* Card Body */}
                                                <div className="p-8">
                                                    <div className="flex items-center gap-2 text-secondary-500 font-bold text-xs uppercase tracking-widest mb-3">
                                                        <MapPin size={14} />
                                                        {journal.country || "Travel Log"}
                                                    </div>
                                                    <h3 className="text-2xl font-black text-gray-900 mb-2 truncate">
                                                        {journal.title || (journal.country ? `${journal.country} Trip` : "Untitled Trip")}
                                                    </h3>
                                                    <p className="text-gray-400 text-sm font-medium line-clamp-2 mb-6">
                                                        {journal.travelStory || 'No story captured yet...'}
                                                    </p>
                                                    <div className="flex items-center justify-between pt-6 border-t border-dashed border-gray-100">
                                                        <span className="text-xs font-bold text-gray-300 uppercase tracking-tighter">
                                                            {journal.created_at ? new Date(journal.created_at).toLocaleDateString() : 'Draft'}
                                                        </span>
                                                        <div className="flex -space-x-2">
                                                            {journal.tripImgs?.slice(0, 3).map((img: string, idx: number) => (
                                                                img && (
                                                                    <div key={idx} className="w-8 h-8 rounded-full border-2 border-white shadow-sm overflow-hidden bg-gray-100">
                                                                        <img src={getStaticUrl(img) || ''} className="w-full h-full object-cover" alt="trip" />
                                                                    </div>
                                                                )
                                                            ))}
                                                        </div>
                                                    </div>
                                                </div>
                                            </motion.div>
                                        ))}
                                    </div>
                                ) : (
                                    <div className="text-center py-20 bg-white rounded-[3rem] border border-gray-100 shadow-sm border-dashed">
                                        <div className="w-20 h-20 bg-gray-50 text-gray-300 rounded-full flex items-center justify-center mx-auto mb-6">
                                            <PenTool size={32} />
                                        </div>
                                        <h3 className="text-xl font-bold text-gray-900 mb-2">No journals yet</h3>
                                        <p className="text-gray-400 max-w-xs mx-auto">Start documenting your first trip and watch your library grow!</p>
                                    </div>
                                )}
                            </div>

                            {/* Features Section */}
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full mt-32">
                                {[
                                    { title: 'Rich Stories', desc: 'Detail every step of your journey.', icon: PenTool, color: 'text-secondary-600', bg: 'bg-secondary-50' },
                                    { title: 'Photo Galleries', desc: 'Upload and organize trip shots.', icon: ImageIcon, color: 'text-primary-600', bg: 'bg-primary-50' },
                                    { title: 'Community Share', desc: 'Inspire others with your logs.', icon: Share2, color: 'text-green-600', bg: 'bg-green-50' }
                                ].map((feature, i) => (
                                    <motion.div
                                        key={i}
                                        initial={{ opacity: 0, y: 20 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: 0.2 * i }}
                                        className="p-10 rounded-[3rem] border border-gray-100 bg-white hover:shadow-2xl transition-all group text-left"
                                    >
                                        <div className={`w-16 h-16 ${feature.bg} ${feature.color} rounded-[1.5rem] flex items-center justify-center mb-6 group-hover:scale-110 transition-transform`}>
                                            <feature.icon size={32} />
                                        </div>
                                        <h3 className="text-2xl font-bold font-heading mb-3">{feature.title}</h3>
                                        <p className="text-gray-500 font-medium leading-relaxed">{feature.desc}</p>
                                    </motion.div>
                                ))}
                            </div>
                        </motion.div>
                    ) : (
                        <motion.div
                            key="creator"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            className="space-y-8"
                        >
                            <div className="max-w-4xl mx-auto flex items-center justify-between px-4 md:px-0">
                                <button
                                    onClick={() => setShowCreator(false)}
                                    className="px-6 py-2 text-gray-400 font-bold hover:text-gray-600 transition-colors flex items-center gap-2 group"
                                >
                                    <ArrowLeft className="group-hover:-translate-x-1 transition-transform" size={18} />
                                    Back to Library
                                </button>
                                <div className="flex items-center gap-2 text-gray-300 font-medium text-sm italic">
                                    {isSaving ? (
                                        <>
                                            <Loader2 size={16} className="animate-spin text-secondary-500" />
                                            <span>Preserving your memories...</span>
                                        </>
                                    ) : (
                                        <span>Drafting your adventure...</span>
                                    )}
                                </div>
                            </div>
                            <JournalCreator
                                onGenerate={handleGenerate}
                                onDiscard={() => setShowCreator(false)}
                            />
                        </motion.div>
                    )}
                </AnimatePresence>
            </main>
        </div>
    );
};

export default JournalsPage;
