import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { NavLink } from 'react-router-dom';
import { User, Menu, X, Compass, Map, Book, LogIn, UserPlus } from 'lucide-react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../../../store';
import { logout } from '../../../store/slices/authSlice';
import { useNavigate } from 'react-router-dom';

const Navbar: React.FC = () => {
    const [isScrolled, setIsScrolled] = useState(false);
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const { isAuthenticated, user } = useSelector((state: RootState) => state.auth);
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const handleLogout = () => {
        dispatch(logout());
        navigate('/login');
    };

    useEffect(() => {
        const handleScroll = () => {
            setIsScrolled(window.scrollY > 20);
        };
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    const navLinks = [
        { name: 'Home', path: '/', icon: Compass },
        { name: 'Planner', path: '/planner', icon: Map },
        { name: 'Destinations', path: '/destinations', icon: Compass },
        { name: 'Journals', path: '/journals', icon: Book },
    ];

    return (
        <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${isScrolled ? 'bg-white/80 backdrop-blur-md shadow-lg py-4' : 'bg-transparent py-6'}`}>
            <div className="max-w-7xl mx-auto px-6 flex items-center justify-between">
                <NavLink to="/" className="flex items-center gap-2 group">
                    <motion.div
                        whileHover={{ rotate: 180 }}
                        className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center text-white"
                    >
                        <Compass size={24} />
                    </motion.div>
                    <span className={`text-2xl font-bold font-heading tracking-tight transition-colors ${isScrolled ? 'text-gray-900 group-hover:text-primary-600' : 'text-white'}`}>Travelume</span>
                </NavLink>

                {/* Desktop Menu */}
                <div className="hidden md:flex items-center gap-8">
                    {navLinks.map((link) => (
                        <NavLink
                            key={link.path}
                            to={link.path}
                            className={({ isActive }) => `flex items-center gap-2 font-medium transition-all hover:text-primary-600 ${isActive ? 'text-primary-600' : (isScrolled ? 'text-gray-600' : 'text-white/90')}`}
                        >
                            <link.icon size={18} />
                            {link.name}
                        </NavLink>
                    ))}
                </div>

                <div className="hidden md:flex items-center gap-4">
                    {isAuthenticated ? (
                        <div className="flex items-center gap-4">
                            <NavLink to="/account" className="flex items-center gap-2 bg-gray-100 px-4 py-2 rounded-full hover:bg-gray-200 transition-all">
                                <User size={18} />
                                <span className="font-medium">{user?.name}</span>
                            </NavLink>
                            <button
                                onClick={handleLogout}
                                className={`${isScrolled ? 'text-gray-500' : 'text-white/70'} hover:text-red-500 transition-colors font-medium px-2`}
                            >
                                Logout
                            </button>
                        </div>
                    ) : (
                        <div className="flex items-center gap-2">
                            <NavLink to="/login" className={`px-5 py-2 font-medium transition-all text-sm ${isScrolled ? 'text-gray-600 hover:text-primary-600' : 'text-white hover:text-primary-200'}`}>
                                Login
                            </NavLink>
                            <NavLink to="/signup" className="flex items-center gap-2 bg-primary-600 text-white px-6 py-2 rounded-full hover:bg-primary-700 transition-all shadow-md hover:shadow-lg text-sm font-bold">
                                <UserPlus size={16} />
                                Sign up
                            </NavLink>
                        </div>
                    )}
                </div>

                {/* Mobile Menu Toggle */}
                <button
                    className={`md:hidden p-2 transition-colors ${isScrolled ? 'text-gray-600 hover:text-primary-600' : 'text-white hover:text-white/80'}`}
                    onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                >
                    {isMobileMenuOpen ? <X size={28} /> : <Menu size={28} />}
                </button>
            </div>

            {/* Mobile Menu Overlay */}
            <AnimatePresence>
                {isMobileMenuOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: -20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        className="absolute top-full left-0 right-0 bg-white shadow-2xl p-6 md:hidden flex flex-col gap-4"
                    >
                        {navLinks.map((link) => (
                            <NavLink
                                key={link.path}
                                to={link.path}
                                onClick={() => setIsMobileMenuOpen(false)}
                                className="flex items-center gap-3 text-lg font-medium p-3 rounded-xl hover:bg-gray-50 text-gray-600"
                            >
                                <link.icon size={20} />
                                {link.name}
                            </NavLink>
                        ))}
                        <hr className="my-2" />
                        {isAuthenticated ? (
                            <div className="flex flex-col gap-2">
                                <NavLink to="/account" onClick={() => setIsMobileMenuOpen(false)} className="flex items-center gap-3 p-3 rounded-xl bg-gray-50 text-gray-700 font-medium font-heading">
                                    <User size={20} />
                                    {user?.name}
                                </NavLink>
                                <button
                                    onClick={() => { handleLogout(); setIsMobileMenuOpen(false); }}
                                    className="flex items-center gap-3 p-3 text-red-500 font-medium"
                                >
                                    Logout
                                </button>
                            </div>
                        ) : (
                            <div className="flex flex-col gap-3">
                                <NavLink to="/signup" onClick={() => setIsMobileMenuOpen(false)} className="flex items-center justify-center gap-2 bg-primary-600 text-white p-4 rounded-xl font-bold">
                                    <UserPlus size={20} />
                                    Sign up for Elite
                                </NavLink>
                                <NavLink to="/login" onClick={() => setIsMobileMenuOpen(false)} className="flex items-center justify-center gap-2 border border-gray-200 text-gray-600 p-4 rounded-xl font-bold">
                                    <LogIn size={20} />
                                    Login
                                </NavLink>
                            </div>
                        )}
                    </motion.div>
                )}
            </AnimatePresence>
        </nav>
    );
};

export default Navbar;
