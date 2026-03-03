import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Loader2, AlertCircle, Download } from 'lucide-react';
import ItineraryDisplay from '../../components/planner/ItineraryDisplay';
import apiClient, { getStaticUrl } from '../../api/client';
import { generateItineraryPDF } from '../../utils/ItineraryGenerator';

const TripDetailPage: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const [trip, setTrip] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [isDownloading, setIsDownloading] = useState(false);

    useEffect(() => {
        const fetchTrip = async () => {
            try {
                const response = await apiClient.get(`/trips/${id}`);
                setTrip(response.data);
            } catch (err: any) {
                setError(err.response?.data?.detail || 'Failed to load trip details.');
            } finally {
                setIsLoading(false);
            }
        };

        if (id) fetchTrip();
    }, [id]);

    const handleDownload = async () => {
        if (!trip) return;
        try {
            setIsDownloading(true);
            await new Promise(resolve => setTimeout(resolve, 300));
            generateItineraryPDF(trip.itinerary_data || trip.itinerary, trip.planner_form || {});
        } catch (error) {
            console.error('PDF Generation failed:', error);
            alert('Failed to generate PDF. Please try again.');
        } finally {
            setIsDownloading(false);
        }
    };

    if (isLoading) {
        return (
            <div className="bg-white">
                <div className="flex flex-col items-center justify-center min-h-[70vh]">
                    <Loader2 className="w-12 h-12 text-primary-600 animate-spin mb-4" />
                    <p className="text-xl font-bold text-gray-500">Unveiling your journey...</p>
                </div>
            </div>
        );
    }

    if (error || !trip) {
        return (
            <div className="bg-white">
                <div className="flex flex-col items-center justify-center min-h-[70vh] px-6 text-center">
                    <AlertCircle className="w-16 h-16 text-red-500 mb-6" />
                    <h1 className="text-4xl font-bold font-heading mb-4 text-gray-900">Trip Not Found</h1>
                    <p className="text-xl text-gray-500 mb-10 max-w-md">{error || "The trip you're looking for doesn't exist or you don't have access."}</p>
                    <button
                        onClick={() => navigate('/account')}
                        className="px-8 py-4 bg-gray-900 text-white font-bold rounded-2xl hover:bg-black transition-all"
                    >
                        Back to My Journeys
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="bg-white">
            <div className="pt-32 pb-20 px-6 max-w-7xl mx-auto">
                <motion.button
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    onClick={() => navigate('/account')}
                    className="flex items-center gap-2 text-gray-500 font-bold hover:text-primary-600 transition-colors mb-12 group"
                >
                    <ArrowLeft size={20} className="group-hover:-translate-x-1 transition-transform" /> Back to Profile
                </motion.button>

                <header className="mb-16 flex flex-col md:flex-row justify-between items-start md:items-end gap-8">
                    <div className="flex-1">
                        {trip.image_url && (
                            <motion.div
                                initial={{ opacity: 0, scale: 0.95 }}
                                animate={{ opacity: 1, scale: 1 }}
                                className="w-full h-[400px] rounded-[3rem] overflow-hidden mb-12 shadow-2xl shadow-primary-500/10"
                            >
                                <img src={getStaticUrl(trip.image_url) || ''} className="w-full h-full object-cover" alt={trip.destination} />
                            </motion.div>
                        )}
                        <motion.h1
                            initial={{ opacity: 0, y: 30 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="text-5xl md:text-7xl font-bold font-heading text-gray-900 tracking-tight"
                        >
                            {trip.name}
                        </motion.h1>
                        <div className="flex flex-wrap gap-4 mt-6">
                            <span className="px-5 py-2 bg-primary-50 text-primary-600 rounded-full font-bold text-sm tracking-wide">
                                {trip.destination}
                            </span>
                            <span className="px-5 py-2 bg-gray-100 text-gray-600 rounded-full font-bold text-sm tracking-wide">
                                {trip.duration}
                            </span>
                            <span className="px-5 py-2 bg-green-50 text-green-600 rounded-full font-bold text-sm tracking-wide">
                                {trip.budget}
                            </span>
                        </div>
                    </div>

                    <button
                        onClick={handleDownload}
                        disabled={isDownloading}
                        className="flex items-center gap-3 px-8 py-4 bg-primary-600 text-white font-bold rounded-2xl hover:bg-primary-700 transition-all shadow-xl shadow-primary-500/20 active:scale-95 whitespace-nowrap disabled:opacity-70"
                    >
                        {isDownloading ? (
                            <>
                                <Loader2 size={20} className="animate-spin" /> Preparing...
                            </>
                        ) : (
                            <>
                                <Download size={20} /> Download PDF Itinerary
                            </>
                        )}
                    </button>
                </header>

                <ItineraryDisplay
                    data={trip.itinerary_data || trip.itinerary}
                    formData={trip.planner_form || {
                        departure_city: trip.departure_city || '',
                        destination: trip.destination || '',
                        start_date: trip.start_date || '',
                        passengers: trip.passengers || 1,
                        currency: 'USD',
                        budget_per_person: trip.budget_per_person || 0
                    }}
                    onRegenerate={() => navigate('/planner')}
                    onSave={() => { }} // Already saved
                    isGenerating={false}
                />
            </div>
        </div>
    );
};

export default TripDetailPage;
