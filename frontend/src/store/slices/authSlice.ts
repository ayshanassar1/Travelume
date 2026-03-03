import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface User {
    name: string;
    email: string;
}

interface AuthState {
    user: User | null;
    token: string | null;
    isAuthenticated: boolean;
}

/**
 * Checks whether a JWT has passed its `exp` claim.
 * Returns true if expired OR if the token is malformed.
 */
function isTokenExpired(token: string): boolean {
    try {
        const payloadBase64 = token.split('.')[1];
        const payload = JSON.parse(atob(payloadBase64));
        // payload.exp is in seconds; Date.now() is in ms
        return Date.now() >= payload.exp * 1000;
    } catch {
        return true; // Treat any malformed token as expired
    }
}

// Validate token on app load — clear stale tokens immediately
const storedToken = localStorage.getItem('token');
const tokenValid = !!storedToken && !isTokenExpired(storedToken);
if (!tokenValid && storedToken) {
    // Token exists but is expired — clean up storage
    localStorage.removeItem('token');
    localStorage.removeItem('user');
}

const initialState: AuthState = {
    user: tokenValid ? JSON.parse(localStorage.getItem('user')!) : null,
    token: tokenValid ? storedToken : null,
    isAuthenticated: tokenValid,
};

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        setCredentials: (state, action: PayloadAction<{ user: User; token: string }>) => {
            state.user = action.payload.user;
            state.token = action.payload.token;
            state.isAuthenticated = true;
            localStorage.setItem('token', action.payload.token);
            localStorage.setItem('user', JSON.stringify(action.payload.user));
        },
        logout: (state) => {
            state.user = null;
            state.token = null;
            state.isAuthenticated = false;
            localStorage.removeItem('token');
            localStorage.removeItem('user');
        },
    },
});

export const { setCredentials, logout } = authSlice.actions;
export default authSlice.reducer;

