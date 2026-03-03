import React, { useState, useRef, useEffect, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Calendar,
    MapPin,
    Users,
    Star,
    Heart,
    MessageSquare,
    Sparkles,
    Image as ImageIcon,
    Video,
    Plus,
    Upload,
    Play,
    X,
    ChevronDown,
    ChevronUp
} from 'lucide-react';

interface JournalCreatorProps {
    onGenerate: (data: any) => void;
    onDiscard: () => void;
}

const JournalCreator: React.FC<JournalCreatorProps> = ({ onGenerate, onDiscard }) => {
    // Form States
    const [country, setCountry] = useState('');
    const [tripImgs, setTripImgs] = useState<(string | null)[]>([null, null, null]);
    const [companions, setCompanions] = useState('');
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [ratings, setRatings] = useState(0);
    const [bestMemory, setBestMemory] = useState('');
    const [travelStory, setTravelStory] = useState('');
    const [unforgettableMemory, setUnforgettableMemory] = useState('');
    const [memoryDate, setMemoryDate] = useState('');

    // Dynamic Daily Images
    const [dailyImgs, setDailyImgs] = useState<(string | null)[][]>([]);

    // Other Media
    const [bestMemoryImg, setBestMemoryImg] = useState<string | null>(null);
    const [foodImg, setFoodImg] = useState<string | null>(null);
    const [videoUrl, setVideoUrl] = useState<string | null>(null);
    const [lastFaveImg, setLastFaveImg] = useState<string | null>(null);

    // Refs
    const tripRefs = [useRef<HTMLInputElement>(null), useRef<HTMLInputElement>(null), useRef<HTMLInputElement>(null)];
    const bestMemRef = useRef<HTMLInputElement>(null);
    const foodRef = useRef<HTMLInputElement>(null);
    const videoRef = useRef<HTMLInputElement>(null);
    const lastFaveRef = useRef<HTMLInputElement>(null);

    // Calculate Days
    const tripDays = useMemo(() => {
        if (!startDate || !endDate) return 0;
        const start = new Date(startDate);
        const end = new Date(endDate);
        const diffTime = Math.abs(end.getTime() - start.getTime());
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
        return diffDays > 0 ? diffDays : 0;
    }, [startDate, endDate]);

    // Update Daily Images slots when tripDays changes
    useEffect(() => {
        if (tripDays > 0) {
            setDailyImgs(prev => {
                const newDaily = [...prev];
                if (newDaily.length < tripDays) {
                    // Add new days
                    for (let i = newDaily.length; i < tripDays; i++) {
                        newDaily.push([null, null, null]);
                    }
                } else if (newDaily.length > tripDays) {
                    // Truncate days
                    return newDaily.slice(0, tripDays);
                }
                return newDaily;
            });
        }
    }, [tripDays]);

    const fileToBase64 = (file: File): Promise<string> => {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => resolve(reader.result as string);
            reader.onerror = error => reject(error);
        });
    };

    const handleFile = async (e: React.ChangeEvent<HTMLInputElement>, setter: (val: any) => void) => {
        const file = e.target.files?.[0];
        if (file) {
            try {
                const base64 = await fileToBase64(file);
                setter(base64);
            } catch (err) {
                console.error("Error converting file to base64:", err);
            }
        }
    };

    const handleSlotFile = async (e: React.ChangeEvent<HTMLInputElement>, index: number, state: any[], setter: (val: any) => void) => {
        const file = e.target.files?.[0];
        if (file) {
            try {
                const base64 = await fileToBase64(file);
                const newImgs = [...state];
                newImgs[index] = base64;
                setter(newImgs);
            } catch (err) {
                console.error("Error converting file to base64:", err);
            }
        }
    };

    const handleDailySlotFile = async (e: React.ChangeEvent<HTMLInputElement>, dayIdx: number, slotIdx: number) => {
        const file = e.target.files?.[0];
        if (file) {
            try {
                const base64 = await fileToBase64(file);
                setDailyImgs(prev => {
                    const newDaily = [...prev];
                    const newDayImgs = [...newDaily[dayIdx]];
                    newDayImgs[slotIdx] = base64;
                    newDaily[dayIdx] = newDayImgs;
                    return newDaily;
                });
            } catch (err) {
                console.error("Error converting file to base64:", err);
            }
        }
    };

    const removeDailyImg = (dayIdx: number, slotIdx: number) => {
        setDailyImgs(prev => {
            const newDaily = [...prev];
            const newDayImgs = [...newDaily[dayIdx]];
            newDayImgs[slotIdx] = null;
            newDaily[dayIdx] = newDayImgs;
            return newDaily;
        });
    };

    const handleGenerate = () => {
        onGenerate({
            country,
            tripImgs,
            companions,
            startDate,
            endDate,
            ratings,
            bestMemory,
            travelStory,
            unforgettableMemory,
            memoryDate,
            bestMemoryImg,
            dailyImgs,
            foodImg,
            videoUrl,
            lastFaveImg,
            tripDays
        });
    };

    return (
        <div className="max-w-4xl mx-auto bg-white rounded-[3rem] shadow-2xl border border-gray-100 overflow-hidden transform transition-all">
            {/* Scrapbook Header */}
            <header className="bg-gradient-to-r from-secondary-50 to-white p-12 text-left border-b border-dashed border-gray-200">
                <div className="flex items-center gap-4 mb-2">
                    <Sparkles className="text-secondary-400" />
                    <span className="text-secondary-500 font-bold uppercase tracking-widest text-xs">Memories Beta</span>
                </div>
                <h1 className="text-5xl font-black font-heading text-gray-900 tracking-tight">
                    My Travel <span className="text-secondary-600 italic">Log</span>
                </h1>
            </header>

            <div className="p-12 space-y-12 bg-[#fafafa]">
                {/* 1: Country */}
                <div className="space-y-3">
                    <label className="text-sm font-bold text-gray-600 block px-2">1. Name of the country</label>
                    <div className="relative group">
                        <MapPin className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-300 group-focus-within:text-secondary-500 transition-colors" size={20} />
                        <input
                            type="text"
                            placeholder="Where did you go?"
                            value={country}
                            onChange={(e) => setCountry(e.target.value)}
                            className="w-full pl-12 pr-4 py-4 bg-white border border-gray-100 rounded-2xl shadow-sm focus:ring-4 focus:ring-secondary-500/10 focus:border-secondary-500 transition-all outline-none"
                        />
                    </div>
                </div>

                {/* 2: 3 Images of the Trip */}
                <div className="space-y-3">
                    <label className="text-sm font-bold text-gray-600 block px-2">2. 3 images of the trip</label>
                    <div className="grid grid-cols-3 gap-6">
                        {tripImgs.map((img, idx) => (
                            <div key={idx} className="relative aspect-square">
                                <input
                                    type="file"
                                    id={`trip-img-${idx}`}
                                    className="hidden"
                                    accept="image/*"
                                    onChange={(e) => handleSlotFile(e, idx, tripImgs, setTripImgs)}
                                />
                                <div
                                    onClick={() => document.getElementById(`trip-img-${idx}`)?.click()}
                                    className="w-full h-full bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200 flex items-center justify-center cursor-pointer hover:bg-white transition-all group overflow-hidden"
                                >
                                    {img ? (
                                        <img src={img} className="w-full h-full object-cover" alt={`Trip ${idx + 1}`} />
                                    ) : (
                                        <Plus className="text-gray-300 group-hover:text-secondary-500 transition-colors" size={32} />
                                    )}
                                </div>
                                {img && (
                                    <button
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            const newImgs = [...tripImgs];
                                            newImgs[idx] = null;
                                            setTripImgs(newImgs);
                                        }}
                                        className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 shadow-lg hover:bg-red-600 transition-colors"
                                    >
                                        <X size={14} />
                                    </button>
                                )}
                            </div>
                        ))}
                    </div>
                </div>

                {/* 3: Travel companions */}
                <div className="space-y-3">
                    <label className="text-sm font-bold text-gray-600 block px-2">3. Travel companions</label>
                    <div className="relative group">
                        <Users className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-300 group-focus-within:text-secondary-500 transition-colors" size={20} />
                        <input
                            type="text"
                            placeholder="e.g., Sarah, Mike, Solo"
                            value={companions}
                            onChange={(e) => setCompanions(e.target.value)}
                            className="w-full pl-12 pr-4 py-4 bg-white border border-gray-100 rounded-2xl shadow-sm focus:ring-4 focus:ring-secondary-500/10 focus:border-secondary-500 transition-all outline-none"
                        />
                    </div>
                </div>

                {/* 4: Dates */}
                <div className="space-y-3">
                    <label className="text-sm font-bold text-gray-600 block px-2">4. Travelling dates (Determines total pages)</label>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="relative">
                            <Calendar className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
                            <input
                                type="date"
                                value={startDate}
                                onChange={(e) => setStartDate(e.target.value)}
                                className="w-full pl-12 pr-4 py-4 bg-white border border-gray-100 rounded-2xl shadow-sm outline-none"
                            />
                        </div>
                        <div className="relative">
                            <Calendar className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
                            <input
                                type="date"
                                value={endDate}
                                onChange={(e) => setEndDate(e.target.value)}
                                className="w-full pl-12 pr-4 py-4 bg-white border border-gray-100 rounded-2xl shadow-sm outline-none"
                            />
                        </div>
                    </div>
                    {tripDays > 0 && (
                        <div className="px-4 py-2 bg-secondary-50 text-secondary-600 rounded-xl text-sm font-bold inline-block">
                            Trip Duration: {tripDays} {tripDays === 1 ? 'Day' : 'Days'}
                        </div>
                    )}
                </div>

                {/* 5: Ratings */}
                <div className="space-y-3">
                    <label className="text-sm font-bold text-gray-600 block px-2">5. Total ratings</label>
                    <div className="flex gap-2">
                        {[1, 2, 3, 4, 5].map((star) => (
                            <button
                                key={star}
                                onClick={() => setRatings(star)}
                                className="transition-transform active:scale-95"
                            >
                                <Star
                                    size={36}
                                    className={`${star <= ratings ? 'fill-yellow-400 text-yellow-400' : 'text-gray-200'} transition-colors`}
                                />
                            </button>
                        ))}
                    </div>
                </div>

                {/* 6, 7, 8: Memories and Story */}
                <div className="space-y-8">
                    <div className="space-y-3">
                        <label className="text-sm font-bold text-gray-600 block px-2">6. Best memory</label>
                        <input
                            type="text"
                            placeholder="Describe your best memory"
                            value={bestMemory}
                            onChange={(e) => setBestMemory(e.target.value)}
                            className="w-full px-6 py-4 bg-white border border-gray-100 rounded-2xl shadow-sm outline-none focus:border-secondary-500 transition-all"
                        />
                    </div>

                    <div className="space-y-3">
                        <label className="text-sm font-bold text-gray-600 block px-2">7. Travel story</label>
                        <textarea
                            placeholder="Describe your day..."
                            value={travelStory}
                            onChange={(e) => setTravelStory(e.target.value)}
                            className="w-full px-6 py-4 bg-white border border-gray-100 rounded-2xl shadow-sm outline-none focus:border-secondary-500 transition-all h-32"
                        />
                    </div>

                    <div className="space-y-3">
                        <label className="text-sm font-bold text-gray-600 block px-2">8. Unforgettable memory</label>
                        <div className="relative">
                            <Heart className="absolute left-4 top-1/2 -translate-y-1/2 text-red-300" size={18} />
                            <input
                                type="text"
                                placeholder="Something you'll never forget"
                                value={unforgettableMemory}
                                onChange={(e) => setUnforgettableMemory(e.target.value)}
                                className="w-full pl-12 pr-6 py-4 bg-white border border-gray-100 rounded-2xl shadow-sm outline-none focus:border-secondary-500 transition-all"
                            />
                        </div>
                    </div>
                </div>

                {/* 9 & 10: Best Image and Date */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-end">
                    <div className="space-y-3">
                        <label className="text-sm font-bold text-gray-600 block px-2">9. Best memory (image)</label>
                        <div className="flex gap-4 items-center">
                            <input
                                type="file"
                                ref={bestMemRef}
                                className="hidden"
                                accept="image/*"
                                onChange={(e) => handleFile(e, setBestMemoryImg)}
                            />
                            <div
                                onClick={() => bestMemRef.current?.click()}
                                className="w-40 h-40 bg-gray-100 rounded-[2rem] border-2 border-dashed border-gray-200 flex items-center justify-center relative group overflow-hidden cursor-pointer"
                            >
                                {bestMemoryImg ? (
                                    <img src={bestMemoryImg} className="w-full h-full object-cover" alt="Preview" />
                                ) : (
                                    <ImageIcon className="text-gray-300" size={32} />
                                )}
                                <div className="absolute inset-0 bg-secondary-900/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                                    <Upload className="text-white" size={24} />
                                </div>
                            </div>
                            <button
                                onClick={() => bestMemRef.current?.click()}
                                className="px-6 py-3 bg-white border border-gray-100 shadow-sm rounded-xl font-bold text-sm hover:bg-gray-50 transition-all flex items-center gap-2"
                            >
                                <Plus size={16} /> {bestMemoryImg ? 'Change' : 'Upload'}
                            </button>
                        </div>
                    </div>
                    <div className="space-y-3 text-right">
                        <label className="text-sm font-bold text-gray-600 block px-2">10. When did it happen?</label>
                        <input
                            type="date"
                            value={memoryDate}
                            onChange={(e) => setMemoryDate(e.target.value)}
                            className="px-6 py-4 bg-white border border-gray-100 rounded-2xl shadow-sm outline-none"
                        />
                    </div>
                </div>

                {/* DYNAMIC Daily Images */}
                <div className="space-y-8 py-8 border-y border-dashed border-gray-200">
                    <h3 className="text-xl font-black text-gray-900 px-2 flex items-center gap-2">
                        <ImageIcon className="text-secondary-500" />
                        Daily Captures
                    </h3>

                    <AnimatePresence mode="popLayout">
                        {dailyImgs.map((daySlots, dayIdx) => (
                            <motion.div
                                key={`day-${dayIdx}`}
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, scale: 0.95 }}
                                className="space-y-3 p-6 bg-white rounded-3xl border border-gray-100 shadow-sm"
                            >
                                <label className="text-sm font-bold text-gray-600 block">Day {dayIdx + 1} Images</label>
                                <div className="grid grid-cols-3 gap-4">
                                    {daySlots.map((img, slotIdx) => (
                                        <div key={slotIdx} className="relative aspect-square">
                                            <input
                                                type="file"
                                                id={`day-${dayIdx}-slot-${slotIdx}`}
                                                className="hidden"
                                                accept="image/*"
                                                onChange={(e) => handleDailySlotFile(e, dayIdx, slotIdx)}
                                            />
                                            <div
                                                onClick={() => document.getElementById(`day-${dayIdx}-slot-${slotIdx}`)?.click()}
                                                className="w-full h-full bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200 flex items-center justify-center cursor-pointer hover:bg-white transition-all group overflow-hidden"
                                            >
                                                {img ? (
                                                    <img src={img} className="w-full h-full object-cover" alt={`Day ${dayIdx + 1}`} />
                                                ) : (
                                                    <Plus className="text-gray-300 group-hover:text-secondary-500 transition-colors" size={24} />
                                                )}
                                            </div>
                                            {img && (
                                                <button
                                                    onClick={() => removeDailyImg(dayIdx, slotIdx)}
                                                    className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1"
                                                >
                                                    <X size={12} />
                                                </button>
                                            )}
                                        </div>
                                    ))}
                                </div>
                            </motion.div>
                        ))}
                    </AnimatePresence>

                    {tripDays === 0 && (
                        <div className="text-center py-12 border-2 border-dashed border-gray-100 rounded-[2rem] text-gray-400 italic">
                            Select travel dates to start adding daily photos.
                        </div>
                    )}
                </div>

                {/* 13 & 14: Food and Video */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-12 pt-4">
                    <div className="space-y-3">
                        <label className="text-sm font-bold text-gray-600 block px-2 italic">13. Favourite Food (Not Mandatory)</label>
                        <div className="flex items-center gap-6">
                            <input
                                type="file"
                                ref={foodRef}
                                className="hidden"
                                accept="image/*"
                                onChange={(e) => handleFile(e, setFoodImg)}
                            />
                            <div
                                onClick={() => foodRef.current?.click()}
                                className="w-24 h-24 rounded-full border-4 border-white shadow-lg bg-gray-50 flex items-center justify-center overflow-hidden relative group cursor-pointer"
                            >
                                {foodImg ? (
                                    <img src={foodImg} className="w-full h-full object-cover" alt="Food" />
                                ) : (
                                    <ImageIcon className="text-gray-200" size={32} />
                                )}
                                <div className="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-all">
                                    <Plus className="text-white" size={20} />
                                </div>
                            </div>
                            <p className="text-xs text-gray-400">Add a circular shot of that <br />unforgettable meal.</p>
                        </div>
                    </div>

                    <div className="space-y-3">
                        <label className="text-sm font-bold text-gray-600 block px-2 italic">14. Add a Video (Not Mandatory)</label>
                        <input
                            type="file"
                            ref={videoRef}
                            className="hidden"
                            accept="video/*"
                            onChange={(e) => handleFile(e, setVideoUrl)}
                        />
                        <div
                            onClick={() => videoRef.current?.click()}
                            className="aspect-video w-full bg-slate-900 rounded-[2rem] shadow-xl relative group flex items-center justify-center overflow-hidden cursor-pointer"
                        >
                            {videoUrl ? (
                                <video src={videoUrl} className="w-full h-full object-cover" />
                            ) : (
                                <>
                                    <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                                    <div className="relative z-10 w-16 h-16 bg-white/20 backdrop-blur-md rounded-full flex items-center justify-center text-white scale-100 group-hover:scale-110 transition-transform">
                                        <Play fill="white" size={32} className="ml-1" />
                                    </div>
                                </>
                            )}
                            <button className={`absolute bottom-4 right-4 p-2 bg-white/10 text-white rounded-lg backdrop-blur-sm ${videoUrl ? 'opacity-100' : 'opacity-0 group-hover:opacity-100'} transition-opacity`}>
                                <Plus size={16} />
                            </button>
                        </div>
                    </div>
                </div>

                {/* 15: Last Fave Image */}
                <div className="space-y-3 pt-12">
                    <label className="text-sm font-bold text-teal-600 block px-2">15. One Last Fave Image</label>
                    <input
                        type="file"
                        ref={lastFaveRef}
                        className="hidden"
                        accept="image/*"
                        onChange={(e) => handleFile(e, setLastFaveImg)}
                    />
                    <div
                        onClick={() => lastFaveRef.current?.click()}
                        className="w-full aspect-square md:aspect-video bg-gray-50 rounded-[3rem] border-2 border-dashed border-gray-200 flex flex-col items-center justify-center gap-4 group cursor-pointer hover:bg-white transition-all overflow-hidden"
                    >
                        {lastFaveImg ? (
                            <img src={lastFaveImg} className="w-full h-full object-cover" alt="Last Fave" />
                        ) : (
                            <>
                                <div className="p-6 bg-teal-50 rounded-[2rem] text-teal-500 group-hover:scale-110 transition-transform">
                                    <ImageIcon size={48} />
                                </div>
                                <div className="text-center">
                                    <h4 className="text-lg font-bold text-gray-600">The grand finale</h4>
                                    <p className="text-sm text-gray-400">Landscape or souvenir shot</p>
                                </div>
                            </>
                        )}
                    </div>
                </div>

                {/* Action Buttons */}
                <div className="flex gap-4 pt-12">
                    <button
                        onClick={handleGenerate}
                        className="flex-1 py-5 bg-secondary-500 text-white font-black rounded-3xl shadow-xl shadow-secondary-500/30 hover:bg-secondary-600 active:scale-95 transition-all uppercase tracking-widest text-lg"
                    >
                        Save Travel Log
                    </button>
                    <button
                        onClick={onDiscard}
                        className="px-10 py-5 bg-gray-100 text-gray-400 font-bold rounded-3xl hover:bg-gray-200 transition-all"
                    >
                        Discard
                    </button>
                </div>
            </div>

            {/* Scrapbook Footer */}
            <footer className="p-8 bg-gray-50 border-t border-gray-100 text-center">
                <p className="text-xs text-gray-400 font-medium">© 2024 Travelume AI Journals • Captured with ❤️</p>
            </footer>
        </div>
    );
};

export default JournalCreator;
