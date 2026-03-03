import React from 'react';
import { motion } from 'framer-motion';
import * as LucideIcons from 'lucide-react';
import { generateJournalPDF } from '../../../utils/JournalGenerator';
import { getStaticUrl } from '../../../api/client';

interface JournalData {
    id?: string;
    country: string;
    tripImgs: (string | null)[];
    companions: string;
    startDate: string;
    endDate: string;
    ratings: number;
    bestMemory: string;
    travelStory: string;
    unforgettableMemory: string;
    memoryDate: string;
    bestMemoryImg: string | null;
    dailyImgs: (string | null)[][];
    foodImg: string | null;
    videoUrl: string | null;
    lastFaveImg: string | null;
    tripDays: number;
}

interface JournalPreviewProps {
    data: JournalData;
    onBack: () => void;
    onDelete?: (id: string) => void;
}

const JournalPreview: React.FC<JournalPreviewProps> = ({ data, onBack, onDelete }) => {
    const [isDownloading, setIsDownloading] = React.useState(false);

    const handleDownload = async () => {
        try {
            setIsDownloading(true);
            console.log('Starting high-resolution PDF generation...');
            await generateJournalPDF(data);
        } catch (error) {
            console.error('v4 Extraction failed:', error);
            alert('Journal capture failed. Please ensure all photos are fully loaded and try again. [v4-generator]');
        } finally {
            setIsDownloading(false);
        }
    };

    // Helper for polaroid style
    const Polaroid = ({ src, tilt = 0, className = "" }: { src: string | null, tilt?: number, className?: string }) => (
        <div
            className={`bg-white p-3 pb-10 shadow-xl border border-gray-100 ${className}`}
            style={{ transform: `rotate(${tilt}deg)` }}
        >
            <div className="bg-gray-100 w-full aspect-square overflow-hidden">
                {src ? (
                    <img
                        src={getStaticUrl(src) || ''}
                        className="w-full h-full object-cover"
                        alt="Memory"
                        crossOrigin={src?.startsWith('data:') ? undefined : "anonymous"}
                    />
                ) : (
                    <div className="w-full h-full flex items-center justify-center text-gray-300 text-sm">No Image</div>
                )}
            </div>
        </div>
    );

    // Helper for Tape
    const Tape = ({ tilt = 0, className = "" }: { tilt?: number, className?: string }) => (
        <div
            className={`absolute w-24 h-8 bg-white/40 backdrop-blur-sm border border-white/50 z-20 ${className}`}
            style={{ transform: `rotate(${tilt}deg)`, mixBlendMode: 'overlay' }}
        />
    );

    return (
        <div className="bg-[#f0f2f5] min-h-screen py-10 px-4 print:p-0 print:bg-white overflow-x-hidden">
            <div className="max-w-[1100px] mx-auto print:max-w-none text-left">
                {/* Header Actions */}
                <div className="flex justify-between items-center mb-10 print:hidden px-4 md:px-0">
                    <button
                        onClick={onBack}
                        className="px-6 py-3 bg-white rounded-2xl font-bold shadow-md hover:bg-gray-50 flex items-center gap-2 transition-all active:scale-95 text-gray-600"
                    >
                        <LucideIcons.ArrowLeft size={20} />
                        Back to Edit
                    </button>
                    <div className="flex gap-4">
                        {onDelete && data.id && (
                            <button
                                onClick={() => {
                                    if (window.confirm('Are you sure you want to delete this journal?')) {
                                        onDelete(data.id!);
                                    }
                                }}
                                className="px-6 py-3 bg-red-50 text-red-600 border-2 border-red-100 rounded-2xl font-bold hover:bg-red-100 transition-all flex items-center gap-2"
                            >
                                <LucideIcons.Trash2 size={20} />
                                Delete
                            </button>
                        )}
                        <button
                            onClick={() => {
                                alert('Journal saved to your account!');
                            }}
                            className="px-8 py-3 bg-white border-2 border-secondary-500 text-secondary-600 rounded-2xl font-bold shadow-lg hover:bg-secondary-50 flex items-center gap-2 transition-all active:scale-95"
                        >
                            <LucideIcons.Heart size={20} className="fill-secondary-500" />
                            Save
                        </button>
                        <button
                            onClick={handleDownload}
                            disabled={isDownloading}
                            className={`px-8 py-3 rounded-2xl font-bold shadow-xl flex items-center gap-2 transition-all active:scale-95 ${isDownloading ? 'bg-gray-400 cursor-not-allowed' : 'bg-gray-900 text-white hover:bg-gray-800'
                                }`}
                        >
                            {isDownloading ? (
                                <>
                                    <div className="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                                    Downloading...
                                </>
                            ) : (
                                <>
                                    <LucideIcons.Download size={20} />
                                    Download PDF
                                </>
                            )}
                        </button>
                    </div>
                </div>

                {/* Downloadable Wrapper */}
                <div id="journal-content">
                    {/* PAGE 1: COVER (Landscape 11.69 x 8.27) */}
                    <div className="journal-page relative w-[11.69in] h-[8.27in] bg-[#d7ccc8] mx-auto shadow-2xl overflow-hidden print:shadow-none print:m-0 print:page-break-after-always">
                        {/* Grid Background Corner */}
                        <div className="absolute top-0 left-0 w-80 h-full bg-white border-r border-gray-300 pattern-grid-lg opacity-20" />

                        {/* Main Collage */}
                        <div className="relative z-10 p-16 flex flex-col items-center h-full justify-center">
                            <header className="mb-8 text-center">
                                <h1 className="text-8xl font-marker text-gray-900 tracking-tighter transform -rotate-1">
                                    MY TRAVEL <br />
                                    <span className="text-9xl text-secondary-600">JOURNAL</span>
                                </h1>
                            </header>

                            <div className="relative w-full h-[60%] flex items-center justify-center">
                                {/* Central Image */}
                                <Polaroid
                                    src={data.tripImgs[0]}
                                    className="w-[30%] relative z-10"
                                    tilt={2}
                                />

                                {/* Side Images */}
                                <Polaroid
                                    src={data.tripImgs[1]}
                                    className="w-[20%] absolute left-[15%] top-10 z-0"
                                    tilt={-10}
                                />
                                <Polaroid
                                    src={data.tripImgs[2]}
                                    className="w-[20%] absolute right-[12%] bottom-5 z-5 overflow-visible"
                                    tilt={8}
                                />

                                {/* Washi Tapes */}
                                <Tape className="top-10 left-1/3" tilt={45} />
                                <Tape className="bottom-20 right-1/3" tilt={-30} />
                            </div>

                            {/* Country Name Tag */}
                            <div className="absolute top-12 right-12 bg-[#fffde7] p-8 pr-16 shadow-2xl transform rotate-2 border-b-4 border-r-4 border-gray-200 z-50">
                                <div className="flex flex-col items-start">
                                    <span className="text-xs font-marker text-gray-400 uppercase tracking-[0.3em] mb-1">Destination:</span>
                                    <h2 className="text-6xl font-marker uppercase text-gray-900 tracking-widest">
                                        {data.country || "France"}
                                    </h2>
                                </div>
                                {/* Paper clip or tape effect */}
                                <div className="absolute -top-4 -left-4 w-12 h-12 bg-gray-300/30 rounded-full border-2 border-white/50 backdrop-blur-sm flex items-center justify-center">
                                    <LucideIcons.MapPin size={24} className="text-secondary-500" />
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* PAGE 2: SUMMARY */}
                    <div className="journal-page relative w-[11.69in] h-[8.27in] bg-[#e0e0e0] mx-auto shadow-2xl overflow-hidden mt-12 print:mt-0 print:shadow-none print:m-0 print:page-break-after-always">
                        <div className="p-16 relative h-full flex flex-row items-center gap-16">
                            <div className="flex-1 flex flex-col justify-between h-full">
                                <h2 className="text-7xl font-marker transform -rotate-2 text-gray-900 mb-10">
                                    HEY {data.country || "WORLD"}
                                </h2>

                                <div className="bg-white/90 backdrop-blur-md p-10 rounded-[3rem] shadow-2xl space-y-6 border border-white/50 transform rotate-1">
                                    <p className="text-2xl font-marker flex items-center gap-4">
                                        <LucideIcons.Users className="text-secondary-500" />
                                        <span className="text-3xl ml-2 text-gray-700">{data.companions || "Solo Traveler"}</span>
                                    </p>
                                    <p className="text-2xl font-marker flex items-center gap-4">
                                        <LucideIcons.Calendar className="text-secondary-500" />
                                        <span className="text-3xl ml-2 text-gray-700">{data.startDate} - {data.endDate}</span>
                                    </p>
                                    <div className="flex items-center gap-4">
                                        <LucideIcons.Star className="text-secondary-500" />
                                        <div className="flex gap-2 ml-4">
                                            {[1, 2, 3, 4, 5].map(i => (
                                                <LucideIcons.Star key={i} size={32} className={i <= data.ratings ? "fill-yellow-400 text-yellow-400" : "text-gray-300"} />
                                            ))}
                                        </div>
                                    </div>
                                </div>

                                <div className="mt-10 self-start">
                                    <span className="text-[12rem] font-script text-gray-400/30 leading-none">scrapbook</span>
                                </div>
                            </div>

                            <div className="flex-1 relative flex flex-col gap-10">
                                <Polaroid src={data.dailyImgs[0]?.[0] || null} className="w-[80%] self-center" tilt={-4} />
                                <Polaroid src={data.dailyImgs[0]?.[1] || null} className="w-[80%] self-center" tilt={6} />
                            </div>
                        </div>
                    </div>

                    {/* PAGE 3: THE STORY */}
                    <div className="journal-page relative w-[11.69in] h-[8.27in] bg-[#f5f5f5] mx-auto shadow-2xl overflow-hidden mt-12 print:mt-0 print:shadow-none print:m-0 print:page-break-after-always">
                        <div className="p-16 flex items-center justify-center h-full">
                            <div className="bg-white shadow-2xl p-12 relative transform rotate-1 border-t-[12px] border-secondary-400 w-full h-full flex flex-col">
                                {/* Tape at top */}
                                <Tape className="-top-6 left-1/2 -translate-x-1/2 w-64 h-12" tilt={0} />

                                <header className="mb-6 flex justify-between items-center">
                                    <div className="flex gap-4">
                                        <div className="w-12 h-12 bg-red-100/50 rounded-xl flex items-center justify-center text-xs font-bold text-red-400 border border-red-200">25</div>
                                        <div className="w-12 h-12 bg-blue-100/50 rounded-xl flex items-center justify-center text-xs font-bold text-blue-400 border border-blue-200">29</div>
                                    </div>
                                </header>

                                <div className="flex-1 relative p-12 bg-white pattern-lined text-4xl leading-[1.7] font-handwritten text-blue-900 border-x-2 border-red-200/50 overflow-hidden">
                                    {data.travelStory || "Writing the best moments of my life..."}
                                </div>

                                {/* Air Mail Stamp */}
                                <div className="absolute bottom-10 left-10 w-48 h-24 border-4 border-red-500 rounded-2xl flex items-center justify-center -rotate-12 opacity-80 scale-125">
                                    <span className="text-red-500 font-black text-2xl tracking-[0.2em] uppercase">AIR MAIL</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* NEW PAGE 4: UNFORGETTABLE MEMORY */}
                    <div className="journal-page relative w-[11.69in] h-[8.27in] bg-white mx-auto shadow-2xl overflow-hidden mt-12 print:mt-0 print:shadow-none print:m-0 print:page-break-after-always">
                        {/* Washtape doodles */}
                        <Tape className="-top-4 left-1/4" tilt={15} />
                        <Tape className="bottom-10 right-10" tilt={-20} />

                        <div className="p-16 flex flex-col items-center h-full">
                            <h2 className="text-7xl font-marker text-gray-900 mb-8 uppercase tracking-tighter invisible h-0">
                                YES, IT'S <span className="text-secondary-500">BEAUTIFUL!</span>
                            </h2>

                            <div className="relative w-[70%] aspect-video bg-gray-100 shadow-2xl border-[15px] border-white overflow-hidden group">
                                {data.bestMemoryImg ? (
                                    <img
                                        src={getStaticUrl(data.bestMemoryImg) || ''}
                                        className="w-full h-full object-cover"
                                        alt="Beautiful Moment"
                                        crossOrigin={data.bestMemoryImg?.startsWith('data:') ? undefined : "anonymous"}
                                    />
                                ) : (
                                    <div className="w-full h-full flex items-center justify-center text-gray-300">
                                        <LucideIcons.Image size={64} />
                                    </div>
                                )}
                                {/* Decorative tape */}
                                <div className="absolute top-4 -left-8 w-32 h-10 bg-white/30 backdrop-blur-sm -rotate-45" />
                                <div className="absolute bottom-4 -right-8 w-32 h-10 bg-white/30 backdrop-blur-sm -rotate-45" />
                            </div>

                            <div className="mt-12 text-center space-y-2">
                                <p className="text-4xl font-marker text-gray-800 tracking-widest">
                                    {data.memoryDate || "10.12.2021"} - {data.unforgettableMemory || "29,000 FEET ABOVE SEA LEVEL"}
                                </p>
                                <div className="flex justify-center gap-1">
                                    {[1, 2, 3].map(i => (
                                        <LucideIcons.Star key={i} size={24} className="fill-yellow-400 text-yellow-400" />
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* PAGE 4+: DYNAMIC DAILY PAGES */}
                    {data.dailyImgs.map((dayImgs, index) => (
                        <div key={index} className="journal-page relative w-[11.69in] h-[8.27in] bg-[#d3d3d3] mx-auto shadow-2xl overflow-hidden mt-12 print:mt-0 print:shadow-none print:m-0 print:page-break-after-always">
                            <div className="p-16 relative h-full flex flex-col justify-between">
                                <h2 className="text-6xl font-marker mb-10 tracking-widest text-gray-800">
                                    DAY <span className="text-white bg-gray-800 px-6 py-2 rounded-full transform rotate-12 inline-block ml-4">{index + 1}</span>
                                </h2>

                                <div className="flex flex-1 items-center justify-center gap-12">
                                    <Polaroid src={dayImgs[0]} className="w-[30%]" tilt={-3} />
                                    <Polaroid src={dayImgs[1]} className="w-[30%]" tilt={5} />
                                    <Polaroid src={dayImgs[2]} className="w-[30%]" tilt={-2} />
                                </div>

                                {index === 0 && (
                                    <div className="mt-10 relative self-center w-full max-w-4xl h-32" />
                                )}
                            </div>
                        </div>
                    ))}

                    {/* NEW PAGE: FOOD TIME - Only if image exists */}
                    {data.foodImg && (
                        <div className="journal-page relative w-[11.69in] h-[8.27in] bg-[#fffcf5] mx-auto shadow-2xl overflow-hidden mt-12 print:mt-0 print:shadow-none print:m-0 print:page-break-after-always">
                            <div className="absolute top-10 left-10 text-gray-900">
                                <div className="relative">
                                    <LucideIcons.Send size={64} className="-rotate-12" />
                                </div>
                            </div>

                            <div className="p-20 flex items-center justify-center h-full">
                                <div className="relative w-[60%] aspect-square bg-white shadow-2xl p-4 transform -rotate-1">
                                    <img
                                        src={getStaticUrl(data.foodImg) || ''}
                                        className="w-full h-full object-cover rounded-sm"
                                        alt="Food Memory"
                                        crossOrigin={data.foodImg?.startsWith('data:') ? undefined : "anonymous"}
                                    />
                                    {/* Washi tape effects */}
                                    <div className="absolute -top-6 left-1/2 -translate-x-1/2 w-32 h-10 bg-gray-200/50 border border-white/20 -rotate-2" />
                                </div>
                            </div>

                            {/* Decorative squiggles */}
                            <div className="absolute bottom-20 left-20 w-32 h-32 border-4 border-dashed border-gray-200 rounded-full" />
                            <div className="absolute top-1/2 right-10 w-2 h-40 bg-secondary-200 rounded-full opacity-50" />
                        </div>
                    )}

                    {/* NEW PAGE: VIDEO MEMORY - Only if video exists */}
                    {data.videoUrl && (
                        <div className="journal-page relative w-[11.69in] h-[8.27in] bg-gray-900 mx-auto shadow-2xl overflow-hidden mt-12 print:mt-0 print:shadow-none print:m-0 print:page-break-after-always">
                            <div className="p-16 flex flex-col items-center justify-center h-full">
                                <h2 className="text-5xl font-marker text-white mb-12 flex items-center gap-4">
                                    <LucideIcons.Video size={48} className="text-secondary-400" />
                                    WATCH THE MAGIC
                                </h2>

                                <div className="w-[85%] aspect-video bg-black rounded-[3rem] shadow-[0_0_100px_rgba(255,255,255,0.1)] overflow-hidden border-8 border-gray-800 relative group">
                                    <video src={getStaticUrl(data.videoUrl) || ''} className="w-full h-full object-cover" controls />
                                </div>

                                <p className="mt-12 text-gray-400 font-handwritten text-3xl">
                                    "Motion captures the soul of the journey."
                                </p>
                            </div>
                        </div>
                    )}

                    {/* PAGE 5: FINALE */}
                    <div className="journal-page relative w-[11.69in] h-[8.27in] bg-white mx-auto shadow-2xl overflow-hidden mt-12 print:mt-0 print:shadow-none print:m-0 flex flex-row items-center justify-center p-20 gap-20">
                        <div className="flex-1 flex flex-col justify-center text-center">
                            <h2 className="text-8xl font-marker mb-10 transform -rotate-2 italic text-secondary-600">BEAUTIFUL!</h2>
                            <div className="h-2 w-48 bg-gray-200 mx-auto rounded-full mb-10" />
                            <p className="text-3xl font-marker tracking-[0.3em] text-gray-800">
                                {data.memoryDate || "12.01.2024"}
                            </p>
                            <p className="text-xl font-marker text-gray-400 mt-4 uppercase">
                                LAST STOP: {data.country}
                            </p>
                        </div>

                        <div className="flex-1 relative">
                            <img
                                src={getStaticUrl(data.lastFaveImg || data.bestMemoryImg) || undefined}
                                className="w-full shadow-[0_50px_100px_-20px_rgba(0,0,0,0.3)] border-[20px] border-white transform rotate-2"
                                alt="Finale"
                                crossOrigin={(data.lastFaveImg?.startsWith('data:') || (!data.lastFaveImg && data.bestMemoryImg?.startsWith('data:'))) ? undefined : "anonymous"}
                            />
                            <Tape className="-top-8 -left-16 w-56 h-12" tilt={-30} />
                            <Tape className="-bottom-8 -right-16 w-56 h-12" tilt={15} />
                        </div>
                    </div>
                </div>
            </div>

            {/* Styles */}
            <style dangerouslySetInnerHTML={{
                __html: `
                @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Indie+Flower&family=Shadows+Into+Light&display=swap');
                
                .font-marker { font-family: 'Permanent Marker', cursive; }
                .font-handwritten { font-family: 'Indie Flower', cursive; }
                .font-script { font-family: 'Shadows Into Light', cursive; }

                .pattern-grid-lg {
                    background-image: radial-gradient(#d1d5db 2px, transparent 2px);
                    background-size: 60px 60px;
                }
                .pattern-grid-sm {
                    background-size: 25px 25px;
                    background-image: linear-gradient(to right, #ccc 1px, transparent 1px), linear-gradient(to bottom, #ccc 1px, transparent 1px);
                }
                .pattern-lined {
                    background-image: linear-gradient(#f0f0f0 0px, transparent 0px), linear-gradient(#f1f5f9 2px, transparent 2px);
                    background-size: 100% 4rem;
                }

                #journal-content {
                    background: transparent;
                }

                @media print {
                    @page {
                        size: 11.69in 8.27in;
                        margin: 0;
                    }
                    body {
                        visibility: hidden;
                        -webkit-print-color-adjust: exact !important;
                        print-color-adjust: exact !important;
                    }
                    .journal-page {
                        visibility: visible;
                        position: relative;
                        width: 11.69in;
                        height: 8.27in;
                        margin: 0 !important;
                        box-shadow: none !important;
                        border: none !important;
                        page-break-after: always;
                    }
                    .print\\:hidden { display: none !important; }
                }
            ` }} />
        </div>
    );
};

export default JournalPreview;
