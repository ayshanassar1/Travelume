import React from 'react';
import { motion } from 'framer-motion';
import Questionnaire from '../../components/planner/Questionnaire/Questionnaire';

const PlannerPage: React.FC = () => {
    return (
        <div className="bg-white">
            <div className="pt-32 pb-20 px-6">
                <header className="max-w-4xl mx-auto text-center mb-16">
                    <motion.h1
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="text-5xl md:text-7xl font-bold font-heading mb-6 tracking-tight text-gray-900"
                    >
                        Create Your <span className="text-primary-600">Dream Journey</span>
                    </motion.h1>
                    <motion.p
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.2 }}
                        className="text-xl md:text-2xl text-gray-500 max-w-2xl mx-auto font-body"
                    >
                        Answer a few curated questions and let our world-class AI craft an itinerary that resonates with your travel soul.
                    </motion.p>
                </header>

                <div className="max-w-4xl mx-auto">
                    <Questionnaire />
                </div>
            </div>
        </div>
    );
};

export default PlannerPage;
