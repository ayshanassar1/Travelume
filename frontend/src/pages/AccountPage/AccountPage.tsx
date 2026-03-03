import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { User, Map, Book, Settings, Trash2, ExternalLink, Loader2, Plus, MapPin } from 'lucide-react';
import { useSelector } from 'react-redux';
import { RootState } from '../../store';
import { NavLink } from 'react-router-dom';
import apiClient, { getStaticUrl } from '../../api/client';

const AccountPage: React.FC = () => {
    const { user } = useSelector((state: RootState) => state.auth);
    const [trips, setTrips] = useState<any[]>([]);
    const [journals, setJournals] = useState<any[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [activeTab, setActiveTab] = useState<'trips' | 'journals'>('trips');

    useEffect(() => {
        const fetchData = async () => {
            if (!user?.email) return;
            try {
                const [tripsRes, journalsRes] = await Promise.all([
                    apiClient.get('/trips/'),
                    apiClient.get('/journals/')
                ]);

                setTrips(tripsRes.data || []);
                setJournals(journalsRes.data || []);
            } catch (err) {
                console.error('Failed to fetch account data:', err);
            } finally {
                setIsLoading(false);
            }
        };

        fetchData();
    }, [user?.email]);

    const handleDeleteTrip = async (tripId: string) => {
        if (!user?.email) return;
        if (!window.confirm('Are you sure you want to delete this journey?')) return;

        try {
            await apiClient.delete(`/trips/${tripId}`);

            setTrips(prev => prev.filter(t => t.id !== tripId));
        } catch (err) {
            alert('Failed to delete trip.');
        }
    };

    const handleDeleteJournal = async (journalId: string) => {
        if (!user?.email) return;
        if (!window.confirm('Are you sure you want to delete this journal?')) return;

        try {
            await apiClient.delete(`/journals/${journalId}`);

            setJournals(prev => prev.filter(j => j.id !== journalId));
        } catch (err) {
            alert('Failed to delete journal.');
        }
    };

    const stats = [
        { id: 'trips', label: 'Trips Planned', value: trips.length.toString(), icon: Map, color: 'text-primary-600' },
        { id: 'journals', label: 'Journals Created', value: journals.length.toString(), icon: Book, color: 'text-secondary-500' },
    ];

    return (
        <div className="bg-white">
            <div className="pt-32 pb-20 px-6 max-w-7xl mx-auto">
                <header className="flex flex-col md:flex-row md:items-center justify-between gap-8 mb-16">
                    <div className="flex items-center gap-6">
                        <div className="w-24 h-24 bg-primary-600 rounded-[2rem] flex items-center justify-center text-white text-4xl font-bold shadow-2xl shadow-primary-500/20">
                            {user?.name?.[0] || 'U'}
                        </div>
                        <div>
                            <h1 className="text-4xl font-bold font-heading text-gray-900">{user?.name || 'Travel Enthusiast'}</h1>
                            <p className="text-lg text-gray-500">{user?.email || 'traveler@travelume.ai'}</p>
                        </div>
                    </div>
                    <button className="flex items-center gap-2 px-8 py-3 bg-gray-100 rounded-2xl font-bold hover:bg-gray-200 transition-all text-gray-600">
                        <Settings size={20} /> Edit Profile
                    </button>
                </header>

                {/* Stats Grid */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-20">
                    {stats.map((stat, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: i * 0.1 }}
                            onClick={() => setActiveTab(stat.id as any)}
                            className={`p-10 rounded-[3rem] border flex items-center gap-8 group cursor-pointer transition-all duration-500 ${activeTab === stat.id
                                ? 'bg-white shadow-2xl border-primary-200'
                                : 'bg-gray-50 border-gray-100 hover:bg-white hover:shadow-xl'
                                }`}
                        >
                            <div className={`p-5 bg-white rounded-3xl shadow-sm group-hover:scale-110 transition-transform ${stat.color} ${activeTab === stat.id ? 'ring-2 ring-primary-100' : ''
                                }`}>
                                <stat.icon size={32} />
                            </div>
                            <div>
                                <p className="text-gray-500 font-bold uppercase tracking-wider text-sm">{stat.label}</p>
                                <p className="text-4xl font-black font-heading mt-1">{stat.value}</p>
                            </div>
                        </motion.div>
                    ))}
                </div>

                {activeTab === 'trips' && (
                    <section>
                        <div className="flex items-center justify-between mb-12">
                            <h2 className="text-4xl font-bold font-heading">Your Saved <span className="text-primary-600">Journeys</span></h2>
                            <button className="text-primary-600 font-bold hover:underline">View All</button>
                        </div>

                        {isLoading ? (
                            <div className="flex justify-center py-20">
                                <Loader2 className="animate-spin text-primary-600 w-12 h-12" />
                            </div>
                        ) : trips.length > 0 ? (
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 text-black">
                                {trips.map((trip) => {
                                    const itinData = trip.itinerary_data || trip.itinerary;
                                    const dayCount = itinData?.itinerary?.length || trip.duration_days;
                                    const theme = itinData?.itinerary?.[0]?.theme || trip.travel_theme;
                                    const intro = itinData?.intro;
                                    const totalCost = itinData?.budget_analysis?.total_estimated_cost || (trip.total_budget ? `${trip.total_budget}` : null);
                                    const tripName = itinData?.title || trip.name || `Trip to ${trip.destination}`;
                                    const tripDest = trip.destination || 'Unknown';
                                    const tripDuration = trip.duration || (trip.duration_days ? `${trip.duration_days} Days` : null);

                                    return (
                                        <motion.div
                                            key={trip.id}
                                            whileHover={{ y: -10 }}
                                            className="group bg-white rounded-[3rem] border border-gray-100 shadow-xl shadow-gray-200/50 overflow-hidden cursor-pointer"
                                        >
                                            <div className="h-48 relative overflow-hidden flex flex-col justify-end p-8">
                                                {trip.image_url ? (
                                                    <img src={getStaticUrl(trip.image_url) || ''} className="absolute inset-0 w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" alt={tripDest} />
                                                ) : (
                                                    <div className="absolute inset-0 bg-gradient-to-br from-primary-500 via-primary-600 to-primary-800" />
                                                )}
                                                <div className="absolute inset-0 bg-black/30 group-hover:bg-black/20 transition-colors" />
                                                <h3 className="text-2xl font-bold font-heading text-white relative z-10 drop-shadow-lg text-left">
                                                    {tripName}
                                                </h3>
                                                {theme && (
                                                    <span className="inline-block mt-2 px-3 py-1 bg-white/20 text-white rounded-full text-xs font-bold w-fit relative z-10">
                                                        {theme}
                                                    </span>
                                                )}
                                            </div>
                                            <div className="p-8">
                                                {intro && (
                                                    <p className="text-gray-500 text-sm mb-4 line-clamp-2 leading-relaxed">{intro}</p>
                                                )}
                                                <div className="flex flex-wrap gap-2 mb-6">
                                                    <span className="px-3 py-1 bg-primary-50 text-primary-600 rounded-full text-xs font-bold">
                                                        📍 {tripDest}
                                                    </span>
                                                    <span className="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-xs font-bold">
                                                        🗓 {dayCount ? `${dayCount} Days` : tripDuration || 'N/A'}
                                                    </span>
                                                    {totalCost && (
                                                        <span className="px-3 py-1 bg-green-50 text-green-600 rounded-full text-xs font-bold">
                                                            💰 {totalCost}
                                                        </span>
                                                    )}
                                                </div>
                                                <div className="flex items-center justify-between pt-6 border-t border-gray-50">
                                                    <div className="flex items-center gap-2">
                                                        <button
                                                            onClick={(e) => { e.stopPropagation(); handleDeleteTrip(trip.id); }}
                                                            className="p-3 bg-gray-50 text-gray-400 rounded-xl hover:bg-red-50 hover:text-red-500 transition-colors"
                                                        >
                                                            <Trash2 size={20} />
                                                        </button>
                                                    </div>
                                                    <NavLink
                                                        to={`/account/trip/${trip.id}`}
                                                        className="flex items-center gap-2 font-bold text-primary-600 group-hover:translate-x-1 transition-transform"
                                                    >
                                                        View Full Itinerary <ExternalLink size={18} />
                                                    </NavLink>
                                                </div>
                                            </div>
                                        </motion.div>
                                    );
                                })}
                            </div>
                        ) : (
                            <div className="bg-gray-50 rounded-[4rem] p-20 text-center border-2 border-dashed border-gray-100">
                                <Map className="mx-auto w-16 h-16 text-gray-300 mb-6" />
                                <h3 className="text-2xl font-bold text-gray-900 mb-2">No journeys yet</h3>
                                <p className="text-gray-500 mb-8">Start planning your next adventure with our AI.</p>
                                <NavLink to="/planner" className="inline-flex px-8 py-4 bg-primary-600 text-white font-bold rounded-2xl hover:bg-primary-700 transition-all">
                                    Create New Trip
                                </NavLink>
                            </div>
                        )}
                    </section>
                )}

                {activeTab === 'journals' && (
                    <section>
                        <div className="flex items-center justify-between mb-12">
                            <h2 className="text-4xl font-bold font-heading text-gray-900">Your <span className="text-secondary-600">Travel Journals</span></h2>
                            <NavLink to="/journals" className="text-secondary-600 font-bold hover:underline flex items-center gap-2">
                                <Plus size={18} /> Create New
                            </NavLink>
                        </div>

                        {isLoading ? (
                            <div className="flex justify-center py-20">
                                <Loader2 className="animate-spin text-secondary-500 w-12 h-12" />
                            </div>
                        ) : journals.length > 0 ? (
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                                {journals.map((journal) => (
                                    <motion.div
                                        key={journal.id}
                                        whileHover={{ y: -10 }}
                                        className="group bg-white rounded-[3rem] border border-gray-100 shadow-xl shadow-gray-200/50 overflow-hidden cursor-pointer flex flex-col"
                                        onClick={() => window.location.href = '/journals'}
                                    >
                                        <div className="h-48 bg-gray-100 relative overflow-hidden">
                                            {journal.tripImgs?.[0] ? (
                                                <img src={getStaticUrl(journal.tripImgs[0]) || ''} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" alt={journal.country} />
                                            ) : (
                                                <div className="w-full h-full flex items-center justify-center text-gray-300">
                                                    <Book size={48} />
                                                </div>
                                            )}
                                        </div>
                                        <div className="p-8">
                                            <div className="flex items-center gap-2 text-secondary-500 font-bold text-xs uppercase tracking-widest mb-3">
                                                <MapPin size={14} />
                                                {journal.country || 'Travel Log'}
                                            </div>
                                            <h3 className="text-2xl font-bold font-heading text-gray-900 mb-2 truncate">
                                                {journal.title || (journal.country ? `${journal.country} Trip` : "Untitled Trip")}
                                            </h3>
                                            <p className="text-gray-400 text-sm font-medium line-clamp-2 mb-6">
                                                {journal.travelStory || 'No story captured yet...'}
                                            </p>
                                            <div className="flex items-center justify-between pt-6 border-t border-gray-50 mt-auto">
                                                <div className="flex items-center gap-2">
                                                    <button
                                                        onClick={(e) => { e.stopPropagation(); handleDeleteJournal(journal.id); }}
                                                        className="p-3 bg-gray-50 text-gray-400 rounded-xl hover:bg-red-50 hover:text-red-500 transition-colors"
                                                    >
                                                        <Trash2 size={18} />
                                                    </button>
                                                </div>
                                                <div className="flex items-center gap-2 text-secondary-600 font-bold text-sm">
                                                    View Journal <ExternalLink size={16} />
                                                </div>
                                            </div>
                                        </div>
                                    </motion.div>
                                ))}
                            </div>
                        ) : (
                            <div className="bg-gray-50 rounded-[4rem] p-20 text-center border-2 border-dashed border-gray-100">
                                <Book className="mx-auto w-16 h-16 text-gray-300 mb-6" />
                                <h3 className="text-2xl font-bold text-gray-900 mb-2">No journals yet</h3>
                                <p className="text-gray-500 mb-8">Start documenting your first trip and watch your library grow!</p>
                                <NavLink to="/journals" className="inline-flex px-8 py-4 bg-secondary-500 text-white font-bold rounded-2xl hover:bg-secondary-600 transition-all">
                                    Create First Journal
                                </NavLink>
                            </div>
                        )}
                    </section>
                )}
            </div>
        </div>
    );
};

export default AccountPage;
