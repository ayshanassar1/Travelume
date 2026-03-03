import React from 'react';
import Hero from '../../components/home/Hero/Hero';
import DestinationGrid from '../../components/home/PopularDestinations/DestinationGrid';

const HomePage: React.FC = () => {
    return (
        <div className="bg-white">
            <Hero />
            <main className="max-w-7xl mx-auto">
                <section className="px-6 py-32 text-center">
                    <h2 className="text-5xl font-bold font-heading mb-16 text-gray-900 leading-tight">
                        The Future of <span className="text-primary-600">Travel Planning</span>
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
                        <div className="group p-12 bg-gray-50 rounded-[3rem] hover:bg-primary-50 transition-all duration-700 border border-transparent hover:border-primary-100 relative overflow-hidden text-black text-left">
                            <div className="absolute top-0 right-0 w-32 h-32 bg-primary-100/50 rounded-full blur-3xl -mr-16 -mt-16 group-hover:bg-primary-200/50 transition-colors" />
                            <div className="w-20 h-20 bg-white rounded-3xl shadow-md flex items-center justify-center text-4xl mb-10 group-hover:scale-110 group-hover:rotate-6 transition-all duration-500">🤖</div>
                            <h3 className="text-3xl font-bold mb-6 font-heading">Generative AI Planner</h3>
                            <p className="text-gray-600 leading-relaxed text-lg">Experience a travel assistant that understands your soul, not just your destination. Tailored to your pace and style.</p>
                        </div>

                        <div className="group p-12 bg-gray-50 rounded-[3rem] hover:bg-accent-teal/5 transition-all duration-700 border border-transparent hover:border-accent-teal/20 relative overflow-hidden text-black text-left">
                            <div className="absolute top-0 right-0 w-32 h-32 bg-accent-teal/10 rounded-full blur-3xl -mr-16 -mt-16 group-hover:bg-accent-teal/20 transition-colors" />
                            <div className="w-20 h-20 bg-white rounded-3xl shadow-md flex items-center justify-center text-4xl mb-10 group-hover:scale-110 group-hover:-rotate-6 transition-all duration-500">📍</div>
                            <h3 className="text-3xl font-bold mb-6 font-heading">Curated Experiences</h3>
                            <p className="text-gray-600 leading-relaxed text-lg">Handpicked destinations and hidden gems updated in real-time. Forget the tourist traps and find your place.</p>
                        </div>

                        <div className="group p-12 bg-gray-50 rounded-[3rem] hover:bg-secondary-500/5 transition-all duration-700 border border-transparent hover:border-secondary-500/20 relative overflow-hidden text-black text-left">
                            <div className="absolute top-0 right-0 w-32 h-32 bg-secondary-500/10 rounded-full blur-3xl -mr-16 -mt-16 group-hover:bg-secondary-500/20 transition-colors" />
                            <div className="w-20 h-20 bg-white rounded-3xl shadow-md flex items-center justify-center text-4xl mb-10 group-hover:scale-110 group-hover:rotate-12 transition-all duration-500">📔</div>
                            <h3 className="text-3xl font-bold mb-6 font-heading">Digital Journals</h3>
                            <p className="text-gray-600 leading-relaxed text-lg">Turn your journeys into beautiful digital stories. Capture photos, notes, and export professional PDF memoirs.</p>
                        </div>
                    </div>
                </section>

                <DestinationGrid />
            </main>
        </div>
    );
};

export default HomePage;
