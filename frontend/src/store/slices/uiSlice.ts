import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface UIState {
    theme: 'light' | 'dark';
    isSidebarOpen: boolean;
    activeModal: string | null;
}

const initialState: UIState = {
    theme: 'light',
    isSidebarOpen: false,
    activeModal: null,
};

const uiSlice = createSlice({
    name: 'ui',
    initialState,
    reducers: {
        toggleTheme: (state) => {
            state.theme = state.theme === 'light' ? 'dark' : 'light';
        },
        setSidebarOpen: (state, action: PayloadAction<boolean>) => {
            state.isSidebarOpen = action.payload;
        },
        setActiveModal: (state, action: PayloadAction<string | null>) => {
            state.activeModal = action.payload;
        },
    },
});

export const { toggleTheme, setSidebarOpen, setActiveModal } = uiSlice.actions;
export default uiSlice.reducer;
