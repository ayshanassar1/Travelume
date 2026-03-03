import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { NavLink, useNavigate } from 'react-router-dom';
import { LogIn, Mail, Lock, ArrowRight, Loader2 } from 'lucide-react';
import { useDispatch } from 'react-redux';
import { setCredentials } from '../../store/slices/authSlice';
import apiClient from '../../api/client';

const LoginPage: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const dispatch = useDispatch();
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setError(null);

        try {
            const response = await apiClient.post('/auth/login', { email, password });
            dispatch(setCredentials({
                user: { name: response.data.name, email: response.data.email },
                token: response.data.token
            }));
            navigate('/');
        } catch (err: any) {
            const errorData = err.response?.data?.detail;
            const message = typeof errorData === 'string' 
                ? errorData 
                : Array.isArray(errorData) 
                    ? errorData[0]?.msg || JSON.stringify(errorData)
                    : errorData?.msg || JSON.stringify(errorData) || 'Something went wrong. Please try again.';
            setError(message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-[#000814] relative overflow-hidden">
            {/* Abstract Background Blur */}
            <div className="absolute top-0 -left-20 w-96 h-96 bg-primary-600/20 blur-[120px] rounded-full" />
            <div className="absolute bottom-0 -right-20 w-96 h-96 bg-secondary-500/10 blur-[120px] rounded-full" />

            <motion.div
                initial={{ opacity: 0, y: 40 }}
                animate={{ opacity: 1, y: 0 }}
                className="max-w-md w-full mx-6 relative z-10"
            >
                <div className="bg-white/10 backdrop-blur-3xl p-12 rounded-[3.5rem] border border-white/10 shadow-2xl">
                    <div className="text-center mb-12">
                        <div className="w-20 h-20 bg-primary-600 rounded-3xl flex items-center justify-center text-white mx-auto mb-6 shadow-xl shadow-primary-500/20">
                            <LogIn size={32} />
                        </div>
                        <h1 className="text-4xl font-bold font-heading text-white">Welcome Back</h1>
                        <p className="text-white/50 mt-3 text-lg">Your cinematic journey continues.</p>
                    </div>

                    {error && (
                        <div className="mb-6 p-4 bg-red-500/20 border border-red-500/50 rounded-2xl text-red-200 text-sm font-medium">
                            {error}
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div className="relative group">
                            <Mail className="absolute left-5 top-1/2 -translate-y-1/2 text-white/30 group-focus-within:text-primary-400 transition-colors" size={20} />
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="Email Address"
                                required
                                className="w-full bg-white/5 border border-white/10 p-5 pl-14 rounded-2xl text-white outline-none focus:border-primary-500/50 focus:bg-white/10 transition-all text-lg"
                            />
                        </div>

                        <div className="relative group">
                            <Lock className="absolute left-5 top-1/2 -translate-y-1/2 text-white/30 group-focus-within:text-primary-400 transition-colors" size={20} />
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="Password"
                                required
                                className="w-full bg-white/5 border border-white/10 p-5 pl-14 rounded-2xl text-white outline-none focus:border-primary-500/50 focus:bg-white/10 transition-all text-lg"
                            />
                        </div>

                        <button
                            type="submit"
                            disabled={isLoading}
                            className="w-full py-5 bg-primary-600 text-white font-bold rounded-2xl flex items-center justify-center gap-3 text-xl hover:bg-primary-500 transition-all shadow-xl shadow-primary-500/20 active:scale-95 group disabled:opacity-70 disabled:animate-pulse"
                        >
                            {isLoading ? (
                                <Loader2 className="animate-spin" size={24} />
                            ) : (
                                <>Sign In <ArrowRight size={22} className="group-hover:translate-x-1 transition-transform" /></>
                            )}
                        </button>
                    </form>

                    <p className="text-center text-white/40 mt-10 text-lg">
                        New to Travelume? <NavLink to="/signup" className="text-primary-400 font-bold hover:underline">Create Account</NavLink>
                    </p>
                </div>
            </motion.div>
        </div>
    );
};

export default LoginPage;
