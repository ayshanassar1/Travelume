import { jsPDF } from 'jspdf';
import html2canvas from 'html2canvas';

const imageToBase64 = async (img: HTMLImageElement): Promise<string> => {
    try {
        const canvas = document.createElement('canvas');
        canvas.width = img.naturalWidth;
        canvas.height = img.naturalHeight;
        const ctx = canvas.getContext('2d');
        if (!ctx) return img.src;
        ctx.drawImage(img, 0, 0);
        return canvas.toDataURL('image/jpeg', 0.8);
    } catch (e) {
        console.warn('v4: Failed to inline image, falling back to original source:', e);
        return img.src;
    }
};

export const generateJournalPDF = async (data: any) => {
    const element = document.getElementById('journal-content');
    if (!element) return;

    try {
        console.log('v4: Starting ultra-robust capture sequence...');

        // 1. Pre-process images in the DOM (Inline them as Base64)
        const images = Array.from(element.getElementsByTagName('img'));
        console.log(`v4: Inlining ${images.length} images to bypass CORS/Taint...`);

        for (const img of images) {
            if (img.src.startsWith('data:')) continue; // Already inlined

            // Critical: Ensure crossOrigin is set for the inlining fetch
            img.crossOrigin = "anonymous";

            // Wait for image to load if not already ready
            if (!img.complete || img.naturalHeight === 0) {
                await new Promise((resolve) => {
                    img.onload = resolve;
                    img.onerror = resolve;
                });
            }

            // Convert to base64
            const b64 = await imageToBase64(img);
            img.src = b64;
        }

        // Wait for layout stability after potential src changes
        await new Promise(resolve => setTimeout(resolve, 1000));

        const pages = element.querySelectorAll('.journal-page');
        if (pages.length === 0) throw new Error('No journal pages found to capture.');

        const doc = new jsPDF({
            orientation: 'landscape',
            unit: 'in',
            format: 'a4',
            compress: true
        });

        for (let i = 0; i < pages.length; i++) {
            const page = pages[i] as HTMLElement;
            console.log(`v4: Capturing page ${i + 1} of ${pages.length}...`);

            const canvas = await html2canvas(page, {
                scale: 1.5, // High resolution, safe with inlined images
                useCORS: true,
                allowTaint: false, // Must be false for reliable toDataURL
                backgroundColor: '#ffffff',
                logging: false,
                width: 1122,
                height: 794,
                onclone: (clonedDoc) => {
                    // Hide non-capturable elements like video tags
                    const videos = clonedDoc.querySelectorAll('video');
                    videos.forEach(v => (v as HTMLElement).style.display = 'none');
                }
            });

            const imgData = canvas.toDataURL('image/jpeg', 0.85);

            if (i > 0) doc.addPage();
            doc.addImage(imgData, 'JPEG', 0, 0, 11.69, 8.27, undefined, 'FAST');
        }

        console.log('v4: Finalizing PDF download...');
        doc.save(`${(data.country || 'Travel').replace(/\s+/g, '_')}_Journal.pdf`);
    } catch (error) {
        console.error('Journal PDF Generation v4 failed:', error);
        throw error;
    }
};
