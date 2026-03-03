import { createBrowserRouter } from 'react-router-dom';
import MainLayout from './components/layout/MainLayout';
import HomePage from './pages/HomePage/HomePage';
import PlannerPage from './pages/PlannerPage/PlannerPage';
import AccountPage from './pages/AccountPage/AccountPage';
import TripDetailPage from './pages/AccountPage/TripDetailPage';
import LoginPage from './pages/AuthPage/LoginPage';
import SignupPage from './pages/AuthPage/SignupPage';
import DestinationsPage from './pages/DestinationsPage/DestinationsPage';
import JournalsPage from './pages/JournalsPage/JournalsPage';
import NotFoundPage from './pages/NotFoundPage';
import ProtectedRoute from './components/ProtectedRoute';

export const router = createBrowserRouter([
    {
        path: '/',
        element: <MainLayout />,
        children: [
            {
                path: '/',
                element: <HomePage />,
            },
            {
                path: '/planner',
                element: <ProtectedRoute><PlannerPage /></ProtectedRoute>,
            },
            {
                path: '/account',
                element: <ProtectedRoute><AccountPage /></ProtectedRoute>,
            },
            {
                path: '/account/trip/:id',
                element: <ProtectedRoute><TripDetailPage /></ProtectedRoute>,
            },
            {
                path: '/destinations',
                element: <DestinationsPage />,
            },
            {
                path: '/journals',
                element: <ProtectedRoute><JournalsPage /></ProtectedRoute>,
            },
        ]
    },
    {
        path: '/login',
        element: <LoginPage />,
    },
    {
        path: '/signup',
        element: <SignupPage />,
    },
    {
        path: '*',
        element: <NotFoundPage />,
    },
]);
