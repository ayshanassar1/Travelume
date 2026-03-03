import React, { Component, ErrorInfo, ReactNode } from 'react';
import { motion } from 'framer-motion';
import { AlertCircle, RefreshCcw, Home } from 'lucide-react';

interface Props {
    children?: ReactNode;
}

interface State {
    hasError: boolean;
    error?: Error;
}

class ErrorBoundary extends Component<Props, State> {
    public state: State = {
        hasError: false
    };

    public static getDerivedStateFromError(error: Error): State {
        return { hasError: true, error };
    }

    public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
        console.error('Uncaught error:', error, errorInfo);
    }

    public render() {
        if (this.state.hasError) {
            return (
                <div className="min-h-screen bg-white flex flex-col items-center justify-center p-6 text-center">
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="max-w-2xl"
                    >
                        <div className="w-20 h-20 bg-red-50 text-red-500 rounded-3xl flex items-center justify-center mx-auto mb-8">
                            <AlertCircle size={40} />
                        </div>

                        <h1 className="text-4xl md:text-5xl font-black font-heading text-gray-900 mb-6 tracking-tight">
                            Something went off-route
                        </h1>

                        <p className="text-xl text-gray-500 mb-10 leading-relaxed font-medium">
                            We encountered an unexpected turbulence while loading this part of your journey. Don't worry, your data is safe.
                        </p>

                        <div className="flex flex-col sm:flex-row gap-4 justify-center">
                            <button
                                onClick={() => window.location.reload()}
                                className="flex items-center justify-center gap-3 bg-primary-600 text-white px-8 py-4 rounded-2xl font-bold hover:bg-primary-700 transition-all shadow-xl shadow-primary-500/20"
                            >
                                <RefreshCcw size={20} />
                                Retry Loading
                            </button>
                            <a
                                href="/"
                                className="flex items-center justify-center gap-3 bg-gray-900 text-white px-8 py-4 rounded-2xl font-bold hover:bg-black transition-all shadow-xl"
                            >
                                <Home size={20} />
                                Back to Home
                            </a>
                        </div>

                        {process.env.NODE_ENV === 'development' && (
                            <div className="mt-12 p-6 bg-gray-50 rounded-2xl text-left border border-gray-100 overflow-auto max-h-48">
                                <p className="text-xs font-black text-red-400 uppercase tracking-widest mb-2">Technical Details</p>
                                <code className="text-sm text-gray-600 break-all">
                                    {this.state.error?.toString()}
                                </code>
                            </div>
                        )}
                    </motion.div>
                </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;
