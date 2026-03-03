import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bot, MessageSquare, X } from 'lucide-react';
import ChatBotWindow from './ChatBotWindow';

const ChatbotButton: React.FC = () => {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <>
            <motion.div
                initial={{ scale: 0, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                className="fixed bottom-6 right-6 z-[999]"
            >
                <motion.button
                    animate={{ y: [0, -10, 0] }}
                    transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    className={`relative group flex items-center justify-center w-16 h-16 rounded-full shadow-[0_10px_40px_-10px_rgba(0,102,255,0.5)] cursor-pointer overflow-hidden border-2 border-white/20 transition-colors ${isOpen ? 'bg-gray-900' : 'bg-primary-600'}`}
                    onClick={() => setIsOpen(!isOpen)}
                >
                    <div className="absolute inset-0 bg-gradient-to-tr from-white/20 to-transparent pointer-events-none" />
                    {isOpen ? (
                        <X className="w-8 h-8 text-white relative z-10" />
                    ) : (
                        <Bot className="w-8 h-8 text-white relative z-10" />
                    )}
                    {!isOpen && (
                        <div className="absolute top-3 right-3 w-3 h-3 bg-green-400 rounded-full border-2 border-primary-600 z-20" />
                    )}

                    {/* Tooltip */}
                    <div className="absolute right-20 bg-gray-900 text-white px-4 py-2 rounded-xl text-sm font-bold opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap shadow-xl">
                        {isOpen ? 'Close chat' : 'Chat with us!'}
                        <div className="absolute -right-1 top-1/2 -translate-y-1/2 w-2 h-2 bg-gray-900 rotate-45" />
                    </div>
                </motion.button>
                {!isOpen && (
                    <div className="absolute inset-0 w-16 h-16 bg-primary-500 rounded-full -z-10 animate-ping opacity-20" />
                )}
            </motion.div>

            <ChatBotWindow isOpen={isOpen} onClose={() => setIsOpen(false)} />
        </>
    );
};

export default ChatbotButton;
