import axios from 'axios';
import { store } from '../store';
import { logout } from '../store/slices/authSlice';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';

const apiClient = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Attach token to every request
apiClient.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Handle expired/invalid tokens globally — auto-logout on 401
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            console.warn('[API] 401 Unauthorized — token expired or invalid. Logging out.');
            store.dispatch(logout());
            // Redirect to login without losing the current page path
            window.location.href = `/login?redirect=${encodeURIComponent(window.location.pathname)}`;
        }
        return Promise.reject(error);
    }
);

export const getStaticUrl = (path: string | null) => {
    if (!path) return null;
    if (path.startsWith('http') || path.startsWith('data:') || path.startsWith('blob:')) return path;

    const base = (import.meta.env.VITE_API_URL || 'http://localhost:8001').replace(/\/$/, '');

    // Ensure path starts with /static/ if it's a relative path from the database
    let cleanPath = path.replace(/\\/g, '/'); // Fix windows paths
    if (!cleanPath.startsWith('/static/') && !cleanPath.startsWith('static/')) {
        cleanPath = `/static/${cleanPath.startsWith('/') ? cleanPath.slice(1) : cleanPath}`;
    } else if (cleanPath.startsWith('static/')) {
        cleanPath = `/${cleanPath}`;
    }

    return `${base}${cleanPath}`;
};

export default apiClient;

