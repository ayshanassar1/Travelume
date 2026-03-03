import React from 'react';

interface CleanItineraryProps {
    data: any;
    formData: any;
}

const CleanItinerary: React.FC<CleanItineraryProps> = ({ data, formData }) => {
    if (!data || !data.itinerary) return null;

    return (
        <div id="clean-itinerary-content" className="bg-white p-12 text-black font-serif leading-relaxed max-w-[8.5in] mx-auto">
            {/* Header */}
            <header className="border-b-2 border-gray-900 pb-8 mb-10 text-center">
                <h1 className="text-4xl font-bold uppercase tracking-widest mb-2">{data.title || 'Travel Itinerary'}</h1>
                <p className="text-xl text-gray-600 italic">{formData.departure_city} to {formData.destination}</p>
                <p className="text-lg mt-2 font-semibold">{formData.start_date} • {formData.passengers} Travelers</p>
            </header>

            {/* Intro */}
            <section className="mb-12">
                <p className="text-xl leading-relaxed first-letter:text-5xl first-letter:font-bold first-letter:float-left first-letter:mr-3 first-letter:mt-1">
                    {data.intro}
                </p>
            </section>

            {/* Logistics */}
            <section className="mb-12">
                <h2 className="text-2xl font-bold border-b border-gray-300 pb-2 mb-6 uppercase tracking-wide">Essential Logistics</h2>
                <div className="grid grid-cols-2 gap-8 text-lg">
                    <div>
                        <p className="font-bold text-gray-500 uppercase text-sm mb-1">Departure</p>
                        <p>{data.logistics.departure_airport}</p>
                    </div>
                    <div>
                        <p className="font-bold text-gray-500 uppercase text-sm mb-1">Flights</p>
                        <p>{data.logistics.flight_recommendation}</p>
                    </div>
                    <div className="col-span-2">
                        <p className="font-bold text-gray-500 uppercase text-sm mb-1">Accommodation</p>
                        <p>{data.logistics.accommodation_recommendation}</p>
                    </div>
                </div>
            </section>

            {/* Daily Schedule */}
            <section className="mb-12">
                <h2 className="text-2xl font-bold border-b border-gray-300 pb-2 mb-8 uppercase tracking-wide">Daily Schedule</h2>
                <div className="space-y-10">
                    {data.itinerary.map((day: any) => (
                        <div key={day.day} className="page-break-inside-avoid">
                            <div className="flex items-baseline gap-4 mb-4">
                                <span className="text-3xl font-black text-gray-300">DAY {day.day}</span>
                                <h3 className="text-2xl font-bold">{day.theme}</h3>
                                <span className="text-gray-400 font-medium ml-auto italic">{day.date}</span>
                            </div>
                            <div className="grid grid-cols-1 gap-4 text-lg pl-6 border-l-2 border-gray-100">
                                <p><span className="font-bold text-gray-600">Morning:</span> {day.schedule.morning}</p>
                                <p><span className="font-bold text-gray-600">Afternoon:</span> {day.schedule.afternoon}</p>
                                <p><span className="font-bold text-gray-600">Evening:</span> {day.schedule.evening}</p>
                                <p className="mt-2 p-3 bg-gray-50 rounded italic"><span className="font-bold text-gray-900 not-italic">Dining:</span> {day.dining_recommendation}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </section>

            {/* Budget */}
            <section className="mb-12 page-break-before-always">
                <h2 className="text-2xl font-bold border-b border-gray-300 pb-2 mb-8 uppercase tracking-wide">Budget Analysis</h2>
                <div className="space-y-6">
                    {data.budget_analysis.breakdown.map((item: any, idx: number) => (
                        <div key={idx} className="flex justify-between items-start border-b border-gray-50 pb-4">
                            <div className="max-w-xl">
                                <p className="font-bold text-lg">{item.category}</p>
                                <p className="text-gray-600 text-sm mt-1">{item.explanation}</p>
                            </div>
                            <p className="text-xl font-bold text-gray-900">{item.cost}</p>
                        </div>
                    ))}
                    <div className="flex justify-between items-center pt-6">
                        <p className="text-2xl font-black uppercase tracking-tighter">Total Estimated Cost</p>
                        <p className="text-3xl font-black border-b-4 border-gray-900">{data.budget_analysis.total_estimated_cost}</p>
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="mt-20 pt-8 border-t border-gray-200 text-center text-gray-400 text-sm italic">
                <p>Generated by Travelume AI • Your Cinematic Journey Begins Here</p>
                {data.budget_disclaimer && <p className="mt-4 text-xs opacity-50 px-10">{data.budget_disclaimer}</p>}
            </footer>
        </div>
    );
};

export default CleanItinerary;
