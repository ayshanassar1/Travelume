import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Send, Paperclip, Smile, MoreVertical, ChevronDown, User, Loader2, Bot, Mic, Play, Pause, Square, Volume2 } from 'lucide-react';
import { useSelector } from 'react-redux';
import { RootState } from '../../../store';
import apiClient from '../../../api/client';

interface ChatBotWindowProps {
    isOpen: boolean;
    onClose: () => void;
}

const ChatBotWindow: React.FC<ChatBotWindowProps> = ({ isOpen, onClose }) => {
    const { user } = useSelector((state: RootState) => state.auth);
    const [messages, setMessages] = useState<any[]>([]);
    const [inputText, setInputText] = useState('');
    const [sessionId, setSessionId] = useState<string | null>(null);
    const [isTyping, setIsTyping] = useState(false);
    const [isRecording, setIsRecording] = useState(false);
    const [currentPlayingId, setCurrentPlayingId] = useState<number | null>(null);
    const [isPaused, setIsPaused] = useState(false);
    const [showEmojiPicker, setShowEmojiPicker] = useState(false);
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const audioRef = useRef<HTMLAudioElement>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);
    const recognitionRef = useRef<any>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    const handleAudio = (msgId: number, audioUrl: string) => {
        if (!audioRef.current) return;

        if (currentPlayingId === msgId) {
            if (isPaused) {
                audioRef.current.play();
                setIsPaused(false);
            } else {
                audioRef.current.pause();
                setIsPaused(true);
            }
        } else {
            // New audio
            const fullUrl = `${apiClient.defaults.baseURL}${audioUrl}`;
            audioRef.current.src = fullUrl;
            audioRef.current.play();
            setCurrentPlayingId(msgId);
            setIsPaused(false);
        }
    };

    // Listen for audio end
    useEffect(() => {
        const audio = audioRef.current;
        if (!audio) return;

        const handleEnded = () => {
            setCurrentPlayingId(null);
            setIsPaused(false);
        };

        audio.addEventListener('ended', handleEnded);
        return () => audio.removeEventListener('ended', handleEnded);
    }, []);

    const toggleListening = () => {
        if (isRecording && recognitionRef.current) {
            recognitionRef.current.stop();
            return;
        }

        const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
        if (!SpeechRecognition) {
            alert("Speech recognition is not supported in this browser. Please try Chrome or Edge.");
            return;
        }

        const recognition = new SpeechRecognition();
        recognitionRef.current = recognition;
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = () => setIsRecording(true);
        recognition.onend = () => {
            setIsRecording(false);
            recognitionRef.current = null;
        };
        recognition.onerror = (event: any) => {
            console.error('Speech recognition error:', event.error);
            setIsRecording(false);
            recognitionRef.current = null;
            if (event.error === 'not-allowed') {
                alert("Microphone access was denied. Please check your browser permissions.");
            }
        };

        recognition.onresult = (event: any) => {
            const transcript = event.results[0][0].transcript;
            setInputText(transcript);
            // Optionally auto-send transcribed text
            // sendMessage(transcript);
        };

        recognition.start();
    };

    const playAudio = (relativeUrl: string | null) => {
        if (!relativeUrl || !audioRef.current) return;
        const fullUrl = `${apiClient.defaults.baseURL}${relativeUrl}`;
        audioRef.current.src = fullUrl;
        audioRef.current.play().catch(err => console.error('Audio playback failed:', err));
    };

    // Reset session state when chat is closed so a fresh session starts on next open
    useEffect(() => {
        if (!isOpen) {
            setSessionId(null);
            setMessages([]);
            setInputText('');
            setSelectedFile(null);
            setShowEmojiPicker(false);
        }
    }, [isOpen]);

    useEffect(() => {
        if (isOpen) {
            scrollToBottom();
        }
    }, [messages, isTyping, isOpen]);

    useEffect(() => {
        const startChat = async () => {
            if (!isOpen || sessionId) return;

            try {
                setIsTyping(true);
                const response = await apiClient.post('/chat/start', {
                    user_email: user?.email || 'guest@travelume.ai'
                });

                setSessionId(response.data.session_id);
                setMessages([{
                    id: Date.now(),
                    type: 'bot',
                    text: response.data.text || "Hi, I’m your AI Travel Partner\nWelcome! I can help you plan trips, find flights & hotels, and build itineraries just for you ✈️🌍\nHow would you like to start?\n\nButtons / Quick replies:",
                    showQuickReplies: true,
                    audio_url: response.data.audio_url
                }]);

                // Auto-play greeting disabled per user request
                /*
                if (response.data.audio_url) {
                    playAudio(response.data.audio_url);
                }
                */

            } catch (err) {
                console.error('Failed to start chat:', err);
                // Fallback message if API fails
                setMessages([{
                    id: Date.now(),
                    type: 'bot',
                    text: "Hi, I’m your AI Travel Partner\nWelcome! I can help you plan trips, find flights & hotels, and build itineraries just for you ✈️🌍\nHow would you like to start?\n\nButtons / Quick replies:",
                    showQuickReplies: true
                }]);
            } finally {
                setIsTyping(false);
            }
        };

        startChat();
    }, [isOpen, sessionId, user?.email]);

    const quickReplies = [
        { label: 'plan a trip' },
        { label: 'best time to visit' }
    ];

    const appendEmoji = (emoji: string) => {
        setInputText(prev => prev + emoji);
        setShowEmojiPicker(false);
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            setSelectedFile(file);
        }
    };

    const sendMessage = async (text: string) => {
        if (!text.trim() || !sessionId || isTyping) return;

        const lowercaseText = text.toLowerCase().trim();

        // Add user message
        const userMsg = {
            id: Date.now(),
            type: 'user',
            text: text,
            showQuickReplies: false
        };

        // Remove quick replies from last bot message
        setMessages(prev => [...prev.map(m => ({ ...m, showQuickReplies: false })), userMsg]);
        setInputText('');

        // Combined regular AI response (handles buttons too now)
        setIsTyping(true);
        try {
            const formData = new FormData();
            formData.append('session_id', sessionId);
            formData.append('text', text);
            if (selectedFile) {
                formData.append('file', selectedFile);
            }

            const response = await apiClient.post('/chat/message', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            if (selectedFile) {
                setSelectedFile(null); // Clear file after sending
            }

            const botMsg = {
                id: Date.now() + 1,
                type: 'bot',
                text: response.data.text,
                showQuickReplies: false, // Don't show quick replies after regular AI answers
                audio_url: response.data.audio_url
            };
            setMessages(prev => [...prev, botMsg]);

            // Auto-play AI response disabled per user request
            /*
            if (response.data.audio_url) {
                playAudio(response.data.audio_url);
            }
            */
        } catch (err) {
            console.error('Failed to send message:', err);
            const errorMsg = {
                id: Date.now() + 1,
                type: 'bot',
                text: "I'm sorry, I'm having trouble connecting to my travel brain. Please try again in a moment.",
                showQuickReplies: false
            };
            setMessages(prev => [...prev, errorMsg]);
        } finally {
            setIsTyping(false);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey && !isTyping) {
            e.preventDefault();
            sendMessage(inputText);
        }
    };

    return (
        <AnimatePresence>
            {isOpen && (
                <motion.div
                    initial={{ opacity: 0, y: 20, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, y: 20, scale: 0.95 }}
                    className="fixed bottom-28 right-8 w-[400px] h-[600px] bg-white rounded-[2rem] shadow-[0_20px_50px_rgba(0,0,0,0.15)] overflow-hidden z-[9999] flex flex-col border border-gray-100"
                >
                    {/* Header */}
                    <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-6 text-white shrink-0">
                        <div className="flex items-center justify-between mb-4">
                            <div className="flex items-center gap-4">
                                <div className="relative">
                                    <div className="w-12 h-12 rounded-full border-2 border-white/20 overflow-hidden bg-white/10 flex items-center justify-center">
                                        <User className="text-white w-6 h-6" />
                                    </div>
                                    <div className="absolute bottom-0 right-0 w-3.5 h-3.5 bg-green-400 border-2 border-blue-600 rounded-full" />
                                </div>
                                <div className="flex flex-col">
                                    <span className="text-blue-100 text-sm font-medium">Chat with</span>
                                    <h3 className="font-bold text-lg leading-tight">AI travel assistant</h3>
                                </div>
                            </div>
                            <div className="flex items-center gap-2 opacity-80">
                                <MoreVertical size={20} className="cursor-pointer hover:opacity-100" />
                                <ChevronDown size={24} className="cursor-pointer hover:opacity-100" onClick={onClose} />
                            </div>
                        </div>
                        <p className="text-blue-100/90 text-[13px] font-medium flex items-center gap-2">
                            We are online!
                        </p>
                    </div>

                    {/* Chat Area */}
                    <div className="flex-grow overflow-y-auto p-4 space-y-4 bg-gray-50/30">
                        {messages.map((msg) => (
                            <div key={msg.id} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <motion.div
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    className={`relative p-4 rounded-2xl shadow-sm max-w-[85%] leading-relaxed whitespace-pre-line text-sm ${msg.type === 'bot'
                                        ? 'bg-white border border-gray-100 text-gray-800 rounded-tl-none'
                                        : 'bg-primary-600 text-white rounded-tr-none'
                                        }`}
                                >
                                    {msg.text}

                                    {msg.type === 'bot' && msg.audio_url && (
                                        <div className={`mt-3 pt-3 border-t flex items-center gap-3 ${msg.type === 'bot' ? 'border-gray-50' : 'border-white/10'}`}>
                                            <button
                                                onClick={() => handleAudio(msg.id, msg.audio_url)}
                                                className={`w-8 h-8 rounded-full flex items-center justify-center transition-colors ${msg.type === 'bot' ? 'bg-blue-50 text-blue-600 hover:bg-blue-100' : 'bg-white/10 text-white hover:bg-white/20'
                                                    }`}
                                            >
                                                {currentPlayingId === msg.id && !isPaused ? (
                                                    <Pause size={14} fill="currentColor" />
                                                ) : (
                                                    <Play size={14} fill="currentColor" className="ml-0.5" />
                                                )}
                                            </button>
                                            <span className={`text-[10px] font-bold uppercase tracking-tight ${msg.type === 'bot' ? 'text-gray-400' : 'text-white/60'}`}>
                                                {currentPlayingId === msg.id ? (isPaused ? 'Paused' : 'Playing...') : 'Listen'}
                                            </span>
                                        </div>
                                    )}
                                </motion.div>

                                {msg.showQuickReplies && (
                                    <div className="flex flex-wrap gap-2">
                                        {quickReplies.map((reply, i) => (
                                            <motion.button
                                                key={i}
                                                whileHover={{ scale: 1.05 }}
                                                whileTap={{ scale: 0.95 }}
                                                onClick={() => sendMessage(reply.label)}
                                                className="px-4 py-2 bg-white border-2 border-primary-500/30 text-primary-600 rounded-full text-sm font-bold hover:border-primary-600 hover:bg-primary-50 transition-all shadow-sm"
                                            >
                                                {reply.label}
                                            </motion.button>
                                        ))}
                                    </div>
                                )}
                            </div>
                        ))}

                        {isTyping && (
                            <motion.div
                                initial={{ opacity: 0, x: -10 }}
                                animate={{ opacity: 1, x: 0 }}
                                className="bg-white p-4 rounded-2xl rounded-tl-none shadow-sm border border-gray-100 w-20 flex items-center justify-center gap-1"
                            >
                                <motion.div animate={{ opacity: [0.3, 1, 0.3] }} transition={{ repeat: Infinity, duration: 1 }} className="w-1.5 h-1.5 bg-gray-400 rounded-full" />
                                <motion.div animate={{ opacity: [0.3, 1, 0.3] }} transition={{ repeat: Infinity, duration: 1, delay: 0.2 }} className="w-1.5 h-1.5 bg-gray-400 rounded-full" />
                                <motion.div animate={{ opacity: [0.3, 1, 0.3] }} transition={{ repeat: Infinity, duration: 1, delay: 0.4 }} className="w-1.5 h-1.5 bg-gray-400 rounded-full" />
                            </motion.div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    {/* Input Area */}
                    <div className="p-4 bg-white border-t border-gray-100 shrink-0 relative">
                        {/* Emoji Picker */}
                        {showEmojiPicker && (
                            <div className="absolute bottom-full left-4 mb-2 p-2 bg-white border border-gray-100 shadow-xl rounded-2xl grid grid-cols-6 gap-2 z-[10000]">
                                {['✈️', '🌍', '🏨', '🏖️', '⛰️', '📸', '🗺️', '🎫', '🎒', '🚕', '🍣', '🍹'].map(emoji => (
                                    <button
                                        key={emoji}
                                        onClick={() => appendEmoji(emoji)}
                                        className="text-xl hover:bg-gray-50 p-1 rounded transition-colors"
                                    >
                                        {emoji}
                                    </button>
                                ))}
                            </div>
                        )}

                        {/* File Preview */}
                        {selectedFile && (
                            <div className="mb-3 px-2 flex items-center justify-between bg-blue-50/50 p-2 rounded-xl border border-blue-100">
                                <div className="flex items-center gap-2 overflow-hidden">
                                    <Paperclip size={14} className="text-blue-500 shrink-0" />
                                    <span className="text-xs text-blue-700 font-medium truncate">{selectedFile.name}</span>
                                </div>
                                <button
                                    onClick={() => setSelectedFile(null)}
                                    className="p-1 hover:bg-blue-100 rounded-full text-blue-500"
                                >
                                    <X size={14} />
                                </button>
                            </div>
                        )}

                        <div className="relative flex items-center gap-3">
                            <input
                                type="text"
                                value={inputText}
                                onChange={(e) => setInputText(e.target.value)}
                                onKeyDown={handleKeyPress}
                                placeholder={isRecording ? "Listening..." : "Enter your message..."}
                                className={`w-full py-4 pl-4 pr-24 bg-gray-50 border-none rounded-xl text-gray-600 placeholder:text-gray-400 focus:ring-2 focus:ring-primary-500/20 outline-none transition-all ${isRecording ? 'animate-pulse bg-red-50' : ''}`}
                            />
                            <div className="flex items-center gap-3 absolute right-4">
                                <Mic
                                    size={20}
                                    className={`cursor-pointer transition-all duration-300 ${isRecording ? 'text-red-500 scale-125' : 'text-gray-400 hover:text-gray-600'}`}
                                    onClick={toggleListening}
                                />
                                <Smile
                                    size={20}
                                    className={`cursor-pointer transition-colors ${showEmojiPicker ? 'text-primary-600' : 'text-gray-400 hover:text-gray-600'}`}
                                    onClick={() => setShowEmojiPicker(!showEmojiPicker)}
                                />
                                <Paperclip
                                    size={20}
                                    className={`cursor-pointer transition-colors ${selectedFile ? 'text-primary-600' : 'text-gray-400 hover:text-gray-600'}`}
                                    onClick={() => fileInputRef.current?.click()}
                                />
                                <input
                                    type="file"
                                    ref={fileInputRef}
                                    className="hidden"
                                    onChange={handleFileChange}
                                />
                            </div>
                        </div>
                        <div className="mt-4 flex items-center justify-between px-2">
                            <div className="flex items-center gap-4">
                                <div className="w-8 h-8 rounded-lg bg-gray-100 flex items-center justify-center">
                                    <Bot size={16} className="text-gray-400" />
                                </div>
                            </div>
                            <div className="flex items-center gap-2 text-[10px] text-gray-400 font-medium uppercase tracking-wider">
                                Powered by <span className="text-primary-600 font-bold">Travelume AI</span>
                            </div>
                            <motion.button
                                whileHover={{ scale: 1.1 }}
                                whileTap={{ scale: 0.9 }}
                                onClick={() => sendMessage(inputText)}
                                disabled={!inputText.trim() || !sessionId || isTyping}
                                className={`w-12 h-12 bg-primary-600 text-white rounded-full flex items-center justify-center shadow-lg shadow-primary-500/30 transition-all ${(!inputText.trim() || isTyping) ? 'opacity-50 cursor-not-allowed' : 'hover:bg-primary-700'}`}
                            >
                                {isTyping ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send size={20} />}
                            </motion.button>
                        </div>
                    </div>
                    <audio ref={audioRef} className="hidden" />
                </motion.div>
            )}
        </AnimatePresence>
    );
};

export default ChatBotWindow;
