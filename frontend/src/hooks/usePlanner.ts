import { useState } from 'react';
import apiClient from '../api/client';

export interface PlannerFormData {
    departure_city: string;
    destination: string;
    start_date: string;
    end_date: string;
    travel_themes: string[];
    travel_pace: string[]; // Fast, Moderate, etc.
    food_preferences: string[]; // Halal, Veg, etc.
    transit_modes: string[]; // Bus, Car, Flight, etc.
    stay_types: string[]; // Hotel, Resort, Airbnb, etc.
    currency: string;
    budget_per_person: string;
    passengers: string;
    additional_prefs: string;
}

const initialData: PlannerFormData = {
    departure_city: '',
    destination: '',
    start_date: '',
    end_date: '',
    travel_themes: [],
    travel_pace: [],
    food_preferences: [],
    transit_modes: [],
    stay_types: [],
    currency: 'INR',
    budget_per_person: '',
    passengers: '1',
    additional_prefs: '',
};

export const usePlanner = () => {
    const [step, setStep] = useState(1);
    const [formData, setFormData] = useState<PlannerFormData>(initialData);
    const [isGenerating, setIsGenerating] = useState(false);
    const [itinerary, setItinerary] = useState<{ itinerary: any; is_raw: boolean } | null>(null);

    const nextStep = () => setStep((s) => Math.min(s + 1, 3));
    const prevStep = () => setStep((s) => Math.max(s - 1, 1));

    const updateFormData = (data: Partial<PlannerFormData>) => {
        setFormData((prev) => ({ ...prev, ...data }));
    };

    const toggleMultiSelect = (field: keyof PlannerFormData, value: string) => {
        setFormData((prev) => {
            const current = prev[field] as string[];
            if (current.includes(value)) {
                return { ...prev, [field]: current.filter((v) => v !== value) };
            } else {
                return { ...prev, [field]: [...current, value] };
            }
        });
    };

    const generateTrip = async (refinement?: string) => {
        setIsGenerating(true);
        try {
            // Mapping multi-select arrays to strings if backend expects strings
            const payload = {
                departure_city: formData.departure_city,
                destination: formData.destination,
                start_date: formData.start_date,
                end_date: formData.end_date,
                travel_theme: formData.travel_themes.join(', '),
                travel_pace: formData.travel_pace.join(', '),
                food_preferences: formData.food_preferences,
                travel_mode: formData.transit_modes.join(', '),
                accommodation_type: formData.stay_types.join(', '),
                currency: formData.currency,
                budget: Number(formData.budget_per_person) * Number(formData.passengers),
                passengers: Number(formData.passengers),
                additional_prefs: formData.additional_prefs,
                refinement: refinement || null
            };
            const response = await apiClient.post('/planner/generate', payload, {
                timeout: 60000 // 60 second timeout
            });
            setItinerary(response.data);
        } catch (error: any) {
            if (error.code === 'ECONNABORTED') {
                alert('Generation timed out. Please try again — the AI is experiencing high traffic.');
            } else {
                console.error('Generation failed:', error);
                alert('Failed to generate itinerary. Please check your connection and try again.');
            }
        } finally {
            setIsGenerating(false);
        }
    };

    const calculateDays = () => {
        if (!formData.start_date || !formData.end_date) return 0;
        const start = new Date(formData.start_date);
        const end = new Date(formData.end_date);
        const diffTime = Math.abs(end.getTime() - start.getTime());
        return Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1; // Inclusive of both days
    };

    const daysCount = calculateDays();
    const totalBudget = Number(formData.budget_per_person) * Number(formData.passengers);

    return {
        step,
        formData,
        nextStep,
        prevStep,
        updateFormData,
        toggleMultiSelect,
        generateTrip,
        isGenerating,
        itinerary,
        daysCount,
        totalBudget,
    };
};
