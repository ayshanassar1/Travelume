import { jsPDF } from 'jspdf';
import 'jspdf-autotable';

// Add type declaration for jspdf-autotable to jsPDF
declare module 'jspdf' {
    interface jsPDF {
        autoTable: (options: any) => jsPDF;
    }
}

export const generateItineraryPDF = (data: any, formData: any) => {
    if (!data) return;

    const doc = new jsPDF();
    const pageWidth = doc.internal.pageSize.getWidth();
    const margin = 20;
    let currY = 30;

    // Title
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(22);
    doc.text(data.title || 'Travel Itinerary', pageWidth / 2, currY, { align: 'center' });
    currY += 15;

    // Subtitle
    doc.setFontSize(14);
    doc.setFont('helvetica', 'italic');
    doc.setTextColor(100);
    const subtitle = `${formData.departure_city || 'Trip'} to ${formData.destination || 'Destination'}`;
    doc.text(subtitle, pageWidth / 2, currY, { align: 'center' });
    currY += 10;

    // Meta info
    doc.setFontSize(10);
    doc.setFont('helvetica', 'bold');
    const meta = `${formData.start_date || ''} • ${formData.passengers || '1'} Travelers`;
    doc.text(meta, pageWidth / 2, currY, { align: 'center' });
    currY += 20;

    // Intro
    if (data.intro) {
        doc.setFont('helvetica', 'normal');
        doc.setFontSize(11);
        doc.setTextColor(50);
        const splitIntro = doc.splitTextToSize(data.intro, pageWidth - (margin * 2));
        doc.text(splitIntro, margin, currY);
        currY += splitIntro.length * 6 + 10;
    }

    // Logistics
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(14);
    doc.setTextColor(0);
    doc.text('Essential Logistics', margin, currY);
    currY += 10;

    const logisticsItems = (data.logistics || []).map((item: any) => [
        item.category || 'N/A',
        item.details || 'N/A',
        item.cost || 'N/A'
    ]);

    doc.autoTable({
        startY: currY,
        margin: { left: margin, right: margin },
        head: [['Category', 'Details', 'Cost']],
        body: logisticsItems,
        theme: 'striped',
        headStyles: { fillColor: [17, 24, 39] }, // Dark slate
        styles: { fontSize: 10 }
    });

    currY = (doc as any).lastAutoTable.finalY + 20;

    // Daily Schedule
    if (data.itinerary && data.itinerary.length > 0) {
        doc.setFont('helvetica', 'bold');
        doc.setFontSize(14);
        doc.text('Daily Schedule', margin, currY);
        currY += 10;

        data.itinerary.forEach((day: any, idx: number) => {
            // Check if we need a new page
            if (currY > 230) {
                doc.addPage();
                currY = 20;
            }

            doc.setFontSize(12);
            doc.setFont('helvetica', 'bold');
            doc.setTextColor(17, 24, 39);
            doc.text(`DAY ${day.day || idx + 1}: ${day.theme || ''}`, margin, currY);

            doc.setFontSize(9);
            doc.setFont('helvetica', 'italic');
            doc.setTextColor(150);
            doc.text(day.date || '', pageWidth - margin, currY, { align: 'right' });
            currY += 8;

            doc.setFontSize(10);
            doc.setFont('helvetica', 'normal');
            doc.setTextColor(50);

            (day.activities || []).forEach((act: any) => {
                // Check if we need a new page for activity
                if (currY > 260) {
                    doc.addPage();
                    currY = 20;
                }

                doc.setFont('helvetica', 'bold');
                doc.text(`${act.time}:`, margin + 5, currY);

                const activityText = `${act.description}\nDining: ${act.dining}`;
                const splitText = doc.splitTextToSize(activityText, pageWidth - margin * 2 - 35);

                doc.setFont('helvetica', 'normal');
                doc.text(splitText, margin + 35, currY);
                currY += splitText.length * 5 + 5;
            });

            currY += 5;
        });
    }

    // Budget Analysis
    if (currY > 200) {
        doc.addPage();
        currY = 20;
    }

    doc.setFont('helvetica', 'bold');
    doc.setFontSize(14);
    doc.setTextColor(0);
    doc.text('Budget Analysis', margin, currY);
    currY += 10;

    const budgetItems = (data.budget_analysis?.breakdown || []).map((item: any) => [
        item.category || 'Category',
        item.explanation || '',
        item.cost || ''
    ]);

    doc.autoTable({
        startY: currY,
        margin: { left: margin, right: margin },
        head: [['Category', 'Explanation', 'Cost']],
        body: budgetItems,
        foot: [['TOTAL ESTIMATED', '', data.budget_analysis?.total_estimated_cost || 'TBD']],
        theme: 'grid',
        headStyles: { fillColor: [17, 24, 39] },
        footStyles: { fillColor: [17, 24, 39] },
        styles: { fontSize: 9 }
    });

    currY = (doc as any).lastAutoTable.finalY + 15;

    // Dining Highlights in PDF
    if (data.budget_analysis?.dining_highlights && data.budget_analysis.dining_highlights.length > 0) {
        if (currY > 230) {
            doc.addPage();
            currY = 20;
        }

        doc.setFont('helvetica', 'bold');
        doc.setFontSize(14);
        doc.setTextColor(17, 24, 39);
        doc.text('Iconic Local Dining Highlights', margin, currY);
        currY += 10;

        const diningItems = data.budget_analysis.dining_highlights.map((item: any) => [
            item.place || '',
            item.dish || '',
            item.vibe || ''
        ]);

        doc.autoTable({
            startY: currY,
            margin: { left: margin, right: margin },
            head: [['Restaurant/Spot', 'Signature Dish', 'Why Visit']],
            body: diningItems,
            theme: 'striped',
            headStyles: { fillColor: [249, 115, 22] }, // Orange-500
            styles: { fontSize: 9 }
        });
    }

    // Footer on all pages
    const pageCount = (doc as any).internal.getNumberOfPages();
    for (let i = 1; i <= pageCount; i++) {
        doc.setPage(i);
        doc.setFontSize(8);
        doc.setTextColor(150);
        doc.text('Generated by Travelume AI • Your Cinematic Journey Begins Here', margin, doc.internal.pageSize.getHeight() - 10);
        doc.text(`Page ${i} of ${pageCount}`, pageWidth - margin, doc.internal.pageSize.getHeight() - 10, { align: 'right' });
    }

    doc.save(`Itinerary_${(data.title || 'Trip').replace(/\s+/g, '_')}.pdf`);
};
