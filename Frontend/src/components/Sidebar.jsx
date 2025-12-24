import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Activity, Brain, Pill, Stethoscope } from 'lucide-react';

const Sidebar = () => {
    const location = useLocation();

    const menuItems = [
        { path: '/', icon: Activity, label: 'Dashboard' },
        { path: '/diagnostics', icon: Stethoscope, label: 'AI Diagnostics' },
        { path: '/treatment', icon: Pill, label: 'Treatment & Safety' },
        { path: '/mental-health', icon: Brain, label: 'Mental Health' },
    ];

    return (
        <div className="fixed left-0 top-0 h-screen w-64 bg-gradient-to-b from-indigo-900 to-indigo-800 text-white shadow-2xl">
            <div className="p-6 border-b border-indigo-700">
                <h1 className="text-2xl font-bold">🏥 Aarogya AI</h1>
                <p className="text-indigo-300 text-sm mt-1">Hospital Intelligence</p>
            </div>

            <nav className="mt-8 px-4 space-y-2">
                {menuItems.map((item) => {
                    const Icon = item.icon;
                    const isActive = location.pathname === item.path;

                    return (
                        <Link
                            key={item.path}
                            to={item.path}
                            className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 ${isActive
                                    ? 'bg-white text-indigo-900 shadow-lg'
                                    : 'text-indigo-100 hover:bg-indigo-700 hover:text-white'
                                }`}
                        >
                            <Icon size={20} />
                            <span className="font-medium">{item.label}</span>
                        </Link>
                    );
                })}
            </nav>

            <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-indigo-700">
                <p className="text-xs text-indigo-300 text-center">
                    Powered by Google Gemini AI
                </p>
            </div>
        </div>
    );
};

export default Sidebar;
