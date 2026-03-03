import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { RootState } from '../store';

interface ProtectedRouteProps {
    children: React.ReactNode;
}

/**
 * Wraps a route and redirects unauthenticated users to /login.
 * Preserves the attempted URL in the `redirect` query param so
 * the login page can send them back after a successful login.
 */
const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
    const { isAuthenticated } = useSelector((state: RootState) => state.auth);
    const location = useLocation();

    if (!isAuthenticated) {
        return (
            <Navigate
                to={`/login?redirect=${encodeURIComponent(location.pathname)}`}
                replace
            />
        );
    }

    return <>{children}</>;
};

export default ProtectedRoute;
