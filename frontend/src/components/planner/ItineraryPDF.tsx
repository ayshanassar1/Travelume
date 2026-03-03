import React from 'react';
import { Page, Text, View, Document, StyleSheet } from '@react-pdf/renderer';

const styles = StyleSheet.create({
    page: {
        padding: 40,
        backgroundColor: '#ffffff',
        fontFamily: 'Helvetica',
    },
    header: {
        marginBottom: 20,
        borderBottomWidth: 2,
        borderBottomColor: '#111827',
        paddingBottom: 20,
        textAlign: 'center',
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        textTransform: 'uppercase',
        marginBottom: 5,
    },
    subtitle: {
        fontSize: 14,
        color: '#4B5563',
        fontStyle: 'italic',
    },
    meta: {
        fontSize: 12,
        marginTop: 5,
        fontWeight: 'bold',
    },
    section: {
        marginBottom: 20,
    },
    sectionTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        borderBottomWidth: 1,
        borderBottomColor: '#D1D5DB',
        paddingBottom: 5,
        marginBottom: 10,
        textTransform: 'uppercase',
    },
    intro: {
        fontSize: 12,
        lineHeight: 1.6,
        marginBottom: 20,
        color: '#374151',
    },
    logisticsGrid: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        marginBottom: 20,
    },
    logisticsItem: {
        width: '50%',
        marginBottom: 10,
    },
    label: {
        fontSize: 10,
        color: '#6B7280',
        fontWeight: 'bold',
        textTransform: 'uppercase',
        marginBottom: 2,
    },
    value: {
        fontSize: 11,
        color: '#111827',
    },
    dayContainer: {
        marginBottom: 15,
        paddingLeft: 10,
        borderLeftWidth: 2,
        borderLeftColor: '#F3F4F6',
    },
    dayHeader: {
        flexDirection: 'row',
        alignItems: 'baseline',
        marginBottom: 5,
    },
    dayLabel: {
        fontSize: 14,
        fontWeight: 'bold',
        color: '#D1D5DB',
        marginRight: 10,
    },
    dayTheme: {
        fontSize: 14,
        fontWeight: 'bold',
    },
    dayDate: {
        fontSize: 10,
        color: '#9CA3AF',
        marginLeft: 'auto',
        fontStyle: 'italic',
    },
    activity: {
        fontSize: 11,
        marginBottom: 3,
    },
    activityBold: {
        fontWeight: 'bold',
        color: '#4B5563',
    },
    dining: {
        fontSize: 10,
        padding: 5,
        marginTop: 5,
        fontStyle: 'italic',
        backgroundColor: '#F9FAFB',
    },
    budgetItem: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        borderBottomWidth: 1,
        borderBottomColor: '#F3F4F6',
        paddingVertical: 5,
    },
    category: {
        fontSize: 11,
        fontWeight: 'bold',
    },
    explanation: {
        fontSize: 9,
        color: '#6B7280',
    },
    cost: {
        fontSize: 12,
        fontWeight: 'bold',
    },
    totalContainer: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginTop: 15,
        paddingTop: 10,
        borderTopWidth: 2,
        borderTopColor: '#111827',
    },
    totalLabel: {
        fontSize: 16,
        fontWeight: 'bold',
        textTransform: 'uppercase',
    },
    totalValue: {
        fontSize: 20,
        fontWeight: 'bold',
    },
    footer: {
        marginTop: 30,
        paddingTop: 10,
        borderTopWidth: 1,
        borderTopColor: '#E5E7EB',
        textAlign: 'center',
        fontSize: 9,
        color: '#9CA3AF',
        fontStyle: 'italic',
    },
    disclaimer: {
        fontSize: 8,
        marginTop: 5,
        opacity: 0.5,
    }
});

interface ItineraryPDFProps {
    data: any;
    formData: any;
}

const ItineraryPDF: React.FC<ItineraryPDFProps> = ({ data, formData }) => {
    // Return early if data is completely missing
    if (!data) {
        return (
            <Document>
                <Page size="LETTER" style={styles.page}>
                    <Text>Itinerary data is not available.</Text>
                </Page>
            </Document>
        );
    }

    // Safely extract nested data
    const itinerary = data.itinerary || [];
    const logistics = data.logistics || {};
    const budgetAnalysis = data.budget_analysis || { breakdown: [] };
    const safeFormData = formData || {};

    return (
        <Document>
            <Page size="LETTER" style={styles.page}>
                <View style={styles.header}>
                    <Text style={styles.title}>{data.title || 'Travel Itinerary'}</Text>
                    <Text style={styles.subtitle}>{safeFormData.departure_city || 'Trip'} to {safeFormData.destination || 'Destination'}</Text>
                    <Text style={styles.meta}>
                        {safeFormData.start_date || ''} • {safeFormData.passengers || '1'} Travelers
                    </Text>
                </View>

                {data.intro && (
                    <View style={styles.section}>
                        <Text style={styles.intro}>{data.intro}</Text>
                    </View>
                )}

                <View style={styles.section}>
                    <Text style={styles.sectionTitle}>Essential Logistics</Text>
                    <View style={styles.logisticsGrid}>
                        <View style={styles.logisticsItem}>
                            <Text style={styles.label}>Departure</Text>
                            <Text style={styles.value}>{logistics.departure_airport || 'N/A'}</Text>
                        </View>
                        <View style={styles.logisticsItem}>
                            <Text style={styles.label}>Flights</Text>
                            <Text style={styles.value}>{logistics.flight_recommendation || 'N/A'}</Text>
                        </View>
                        <View style={{ width: '100%' }}>
                            <Text style={styles.label}>Accommodation</Text>
                            <Text style={styles.value}>{logistics.accommodation_recommendation || 'N/A'}</Text>
                        </View>
                    </View>
                </View>

                {itinerary.length > 0 && (
                    <View style={styles.section}>
                        <Text style={styles.sectionTitle}>Daily Schedule</Text>
                        {itinerary.map((day: any, idx: number) => (
                            <View key={idx} style={styles.dayContainer} wrap={false}>
                                <View style={styles.dayHeader}>
                                    <Text style={styles.dayLabel}>DAY {day.day || idx + 1}</Text>
                                    <Text style={styles.dayTheme}>{day.theme || ''}</Text>
                                    <Text style={styles.dayDate}>{day.date || ''}</Text>
                                </View>
                                {day.schedule && (
                                    <View style={{ marginBottom: 5 }}>
                                        <Text style={styles.activity}><Text style={styles.activityBold}>Morning: </Text>{day.schedule.morning || ''}</Text>
                                        <Text style={styles.activity}><Text style={styles.activityBold}>Afternoon: </Text>{day.schedule.afternoon || ''}</Text>
                                        <Text style={styles.activity}><Text style={styles.activityBold}>Evening: </Text>{day.schedule.evening || ''}</Text>
                                    </View>
                                )}
                                {day.dining_recommendation && (
                                    <View style={styles.dining}>
                                        <Text><Text style={{ fontWeight: 'bold' }}>Dining: </Text>{day.dining_recommendation}</Text>
                                    </View>
                                )}
                            </View>
                        ))}
                    </View>
                )}

                <View style={styles.section} wrap={false}>
                    <Text style={styles.sectionTitle}>Budget Analysis</Text>
                    {(budgetAnalysis.breakdown || []).map((item: any, idx: number) => (
                        <View key={idx} style={styles.budgetItem}>
                            <View style={{ flex: 1 }}>
                                <Text style={styles.category}>{item.category || 'Category'}</Text>
                                <Text style={styles.explanation}>{item.explanation || ''}</Text>
                            </View>
                            <Text style={styles.cost}>{item.cost || ''}</Text>
                        </View>
                    ))}
                    <View style={styles.totalContainer}>
                        <Text style={styles.totalLabel}>Total Estimated Cost</Text>
                        <Text style={styles.totalValue}>{budgetAnalysis.total_estimated_cost || 'TBD'}</Text>
                    </View>
                </View>

                <View style={styles.footer}>
                    <Text>Generated by Travelume AI • Your Cinematic Journey Begins Here</Text>
                    {data.budget_disclaimer && <Text style={styles.disclaimer}>{data.budget_disclaimer}</Text>}
                </View>
            </Page>
        </Document>
    );
};

export default ItineraryPDF;
