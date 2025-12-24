import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Activity, Brain, Pill, Stethoscope, Heart } from 'lucide-react';

const Sidebar = () => {
    const location = useLocation();

    const menuItems = [
        { path: '/', icon: Activity, label: 'Dashboard', color: 'from-blue-500 to-blue-600' },
        { path: '/diagnostics', icon: Stethoscope, label: 'AI Diagnostics', color: 'from-purple-500 to-purple-600' },
        { path: '/treatment', icon: Pill, label: 'Treatment & Safety', color: 'from-green-500 to-green-600' },
        { path: '/mental-health', icon: Brain, label: 'Mental Health', color: 'from-pink-500 to-pink-600' },
    ];

    return (
        <div className="fixed left-0 top-0 h-screen w-64 bg-gradient-to-b from-indigo-900 via-indigo-800 to-indigo-900 text-white shadow-2xl z-50 animate-slideInLeft">
            {/* Header with breathing animation */}
            <div className="p-6 border-b border-indigo-700/50 backdrop-blur-sm">
                <div className="flex items-center gap-3 mb-2">
                    <div className="relative">
                        <Heart className="w-8 h-8 text-red-400 animate-heartbeat" fill="currentColor" />
                        <div className="absolute inset-0 animate-gentle-pulse opacity-50">
                            <Heart className="w-8 h-8 text-red-300" fill="currentColor" />
                        </div>
                    </div>
                    <div>
                        <h1 className="text-2xl font-bold bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">
                            Aarogya AI
                        </h1>
                    </div>
                </div>
                <p className="text-indigo-300 text-sm ml-11 animate-fadeIn delay-200">Hospital Intelligence</p>
            </div>

            {/* Navigation with staggered animations */}
            <nav className="mt-8 px-4 space-y-2">
                {menuItems.map((item, index) => {
                    const Icon = item.icon;
                    const isActive = location.pathname === item.path;

                    return (
                        <Link
                            key={item.path}
                            to={item.path}
                            className={`group flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 animate-fadeInScale ${
                                isActive
                                    ? 'bg-white text-indigo-900 shadow-soft-lg scale-105'
                                    : 'text-indigo-100 hover:bg-indigo-700/50 hover:text-white hover:scale-105 hover:shadow-soft'
                            }`}
                            style={{ animationDelay: `${index * 0.1}s` }}
                        >
                            <div className={`relative ${isActive ? 'animate-gentle-pulse' : 'group-hover:animate-float'}`}>
                                <Icon size={20} className={isActive ? 'text-indigo-600' : ''} />
                                {isActive && (
                                    <div className="absolute inset-0 bg-gradient-to-r opacity-20 rounded-full blur-sm animate-glow" 
                                         style={{ background: `linear-gradient(135deg, ${item.color})` }}>
                                    </div>
                                )}
                            </div>
                            <span className="font-medium">{item.label}</span>
                            
                            {/* Active indicator */}
                            {isActive && (
                                <div className="ml-auto w-2 h-2 rounded-full bg-gradient-to-r from-blue-400 to-purple-400 animate-gentle-pulse"></div>
                            )}
                        </Link>
                    );
                })}
            </nav>

            {/* Health Status Indicator */}
            <div className="absolute bottom-20 left-0 right-0 px-6">
                <div className="bg-indigo-800/50 backdrop-blur-sm rounded-xl p-4 border border-indigo-600/30 animate-fadeInScale delay-500">
                    <div className="flex items-center gap-3 mb-2">
                        <div className="relative">
                            <div className="w-3 h-3 bg-green-400 rounded-full animate-gentle-pulse"></div>
                            <div className="absolute inset-0 w-3 h-3 bg-green-400 rounded-full animate-ping opacity-75"></div>
                        </div>
                        <span className="text-xs font-semibold text-green-300">System Online</span>
                    </div>
                    <p className="text-xs text-indigo-300">All agents operational</p>
                </div>
            </div>

            {/* Footer with gentle animation */}
            <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-indigo-700/50 backdrop-blur-sm">
                <div className="flex items-center justify-center gap-2 text-xs text-indigo-300 animate-breathe">
                    <span className="inline-block animate-rotate-gentle">✨</span>
                    <p>Powered by Google Gemini AI</p>
                </div>
            </div>
        </div>
    );
};

export default Sidebar;
