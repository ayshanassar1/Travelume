import React from 'react';

const Footer: React.FC = () => {
    return (
        <footer className="bg-gray-900 text-white py-20 px-6">
            <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-10">
                <div className="flex items-center gap-3">
                    <div className="w-12 h-12 bg-primary-600 rounded-xl flex items-center justify-center text-white">✈️</div>
                    <span className="text-3xl font-bold font-heading">Travelume</span>
                </div>
                <p className="text-gray-400 text-lg">&copy; 2026 Travelume AI. Crafting extraordinary journeys.</p>
            </div>
        </footer>
    );
};

export default Footer;
