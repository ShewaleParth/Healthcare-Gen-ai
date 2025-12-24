import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts';
import ImpactMetrics from '../components/ImpactMetrics';
import toast, { Toaster } from 'react-hot-toast';

const Dashboard = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await fetch('http://localhost:8000/api/v1/hospital/optimize', {
                method: 'POST',
            });
            if (!response.ok) throw new Error('Failed to fetch data');
            const result = await response.json();
            setData(result);
            toast.success('Hospital data refreshed successfully!', { icon: '✅' });
        } catch (err) {
            console.error(err);
            setError('Failed to load hospital insights.');
            toast.error('Failed to refresh data. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    if (loading) return (
        <div className="flex justify-center items-center h-screen text-xl text-blue-600 font-semibold animate-pulse">
            Loading Hospital AI Insights...
        </div>
    );

    // Data preparation for charts
    const opdChartData = data?.raw_data?.opd_visits || [];
    const surgeryChartData = data?.raw_data?.surgery_schedule?.map(s => ({ name: s.type, value: s.count })) || [];
    const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

    return (
        <div className="p-6 bg-medical-gradient min-h-screen bg-pattern-dots animate-fadeIn">
            <Toaster position="top-right" />
            
            {/* Header with breathing animation */}
            <header className="mb-8 flex justify-between items-center animate-slideInLeft">
                <div className="relative">
                    <h1 className="text-4xl font-extrabold text-gray-800 tracking-tight flex items-center gap-3">
                        <span className="animate-gentle-pulse">🏥</span>
                        <span className="bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                            Aarogya AI Dashboard
                        </span>
                    </h1>
                    <p className="text-gray-500 mt-2 ml-14 animate-fadeIn delay-200">
                        Real-time Hospital Workflow Optimization & Analytics
                    </p>
                    {/* Decorative healing line */}
                    <div className="absolute -bottom-2 left-14 right-0 h-1 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded-full animate-gradient"></div>
                </div>
                <button
                    onClick={fetchData}
                    disabled={loading}
                    className="group bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-700 hover:to-indigo-800 text-white px-6 py-3 rounded-xl font-medium transition-all shadow-soft hover:shadow-soft-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 animate-slideInRight hover:scale-105 transform"
                >
                    <span className={loading ? 'animate-spin' : 'group-hover:animate-rotate-gentle'}>
                        {loading ? '⚙️' : '🔄'}
                    </span>
                    {loading ? 'Refreshing...' : 'Refresh Analysis'}
                </button>
            </header>

            {error && (
                <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded-xl shadow-soft mb-6 animate-bounceIn">
                    <div className="flex items-center gap-2">
                        <span className="text-xl">⚠️</span>
                        {error}
                    </div>
                </div>
            )}

            {/* Impact Metrics Section with breathing effect */}
            {data && (
                <div className="animate-fadeInScale">
                    <ImpactMetrics />
                </div>
            )}

            {data && (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

                    {/* Left Column: Charts & Metrics */}
                    <div className="space-y-8">

                        {/* OPD Chart with gentle animation */}
                        <div className="glass rounded-2xl p-6 shadow-soft-lg border border-white/20 hover:shadow-soft-lg transition-all duration-500 animate-slideInLeft hover:scale-[1.02] transform">
                            <div className="flex items-center gap-2 mb-4">
                                <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center animate-gentle-pulse">
                                    <span className="text-white text-xl">📈</span>
                                </div>
                                <h2 className="text-lg font-bold text-gray-700">OPD Patient Flow (Forecast)</h2>
                            </div>
                            <div className="h-64">
                                <ResponsiveContainer width="100%" height="100%">
                                    <AreaChart data={opdChartData}>
                                        <defs>
                                            <linearGradient id="colorVisitors" x1="0" y1="0" x2="0" y2="1">
                                                <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8} />
                                                <stop offset="95%" stopColor="#8884d8" stopOpacity={0} />
                                            </linearGradient>
                                        </defs>
                                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e0e7ff" />
                                        <XAxis dataKey="hour" fontSize={12} tickLine={false} axisLine={false} stroke="#6b7280" />
                                        <YAxis fontSize={12} tickLine={false} axisLine={false} stroke="#6b7280" />
                                        <Tooltip 
                                            contentStyle={{ 
                                                borderRadius: '12px', 
                                                border: 'none', 
                                                boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
                                                backgroundColor: 'rgba(255, 255, 255, 0.95)',
                                                backdropFilter: 'blur(10px)'
                                            }} 
                                        />
                                        <Area type="monotone" dataKey="visitors" stroke="#8884d8" strokeWidth={2} fillOpacity={1} fill="url(#colorVisitors)" />
                                    </AreaChart>
                                </ResponsiveContainer>
                            </div>
                        </div>

                        {/* Surgery & Inventory Grid with staggered animation */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            {/* Surgery Chart */}
                            <div className="glass rounded-2xl p-6 shadow-soft border border-white/20 hover:shadow-soft-lg transition-all duration-500 animate-slideInLeft delay-200 hover:scale-[1.02] transform">
                                <div className="flex items-center gap-2 mb-4">
                                    <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl flex items-center justify-center animate-gentle-pulse">
                                        <span className="text-white text-xl">🏥</span>
                                    </div>
                                    <h2 className="text-lg font-bold text-gray-700">Surgery Distribution</h2>
                                </div>
                                <div className="h-48">
                                    <ResponsiveContainer width="100%" height="100%">
                                        <PieChart>
                                            <Pie
                                                data={surgeryChartData}
                                                cx="50%"
                                                cy="50%"
                                                innerRadius={40}
                                                outerRadius={60}
                                                fill="#8884d8"
                                                paddingAngle={5}
                                                dataKey="value"
                                            >
                                                {surgeryChartData.map((entry, index) => (
                                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                                ))}
                                            </Pie>
                                            <Tooltip 
                                                contentStyle={{ 
                                                    borderRadius: '12px', 
                                                    border: 'none', 
                                                    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
                                                    backgroundColor: 'rgba(255, 255, 255, 0.95)'
                                                }} 
                                            />
                                            <Legend wrapperStyle={{ fontSize: '12px' }} />
                                        </PieChart>
                                    </ResponsiveContainer>
                                </div>
                            </div>

                            {/* Inventory List with gentle animations */}
                            <div className="glass rounded-2xl p-6 shadow-soft border border-white/20 hover:shadow-soft-lg transition-all duration-500 animate-slideInLeft delay-300 hover:scale-[1.02] transform">
                                <div className="flex items-center gap-2 mb-4">
                                    <div className="w-10 h-10 bg-gradient-to-br from-red-500 to-red-600 rounded-xl flex items-center justify-center animate-gentle-pulse">
                                        <span className="text-white text-xl">💊</span>
                                    </div>
                                    <h2 className="text-lg font-bold text-gray-700">Low Stock Alerts</h2>
                                </div>
                                <div className="space-y-3 max-h-48 overflow-y-auto pr-2 custom-scrollbar">
                                    {data.raw_data?.pharmacy_inventory?.filter(i => i.stock < i.threshold).map((item, i) => (
                                        <div 
                                            key={i} 
                                            className="flex justify-between items-center bg-gradient-to-r from-red-50 to-orange-50 p-3 rounded-xl border border-red-100 group hover:from-red-100 hover:to-orange-100 transition-all duration-300 animate-fadeInScale hover:scale-105 transform shadow-soft"
                                            style={{ animationDelay: `${i * 0.1}s` }}
                                        >
                                            <div className="flex items-center gap-2">
                                                <span className="text-red-600 animate-gentle-pulse">⚠️</span>
                                                <span className="text-sm font-semibold text-red-700">{item.item}</span>
                                            </div>
                                            <span className="text-xs bg-white text-red-600 px-3 py-1 rounded-full font-bold shadow-soft">
                                                {item.stock} left
                                            </span>
                                        </div>
                                    ))}
                                    {data.raw_data?.pharmacy_inventory?.filter(i => i.stock >= i.threshold).length === 0 && (
                                        <div className="text-sm text-gray-400 text-center py-4 animate-breathe">
                                            <span className="text-2xl mb-2 block">✅</span>
                                            All stock levels are healthy.
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Right Column: AI Analysis Report with gentle entrance */}
                    <div className="glass rounded-2xl p-8 shadow-soft-lg border-t-4 border-indigo-600 h-fit animate-slideInRight hover:shadow-soft-lg transition-all duration-500">
                        <div className="flex items-center gap-3 mb-6 pb-4 border-b border-gray-100">
                            <div className="bg-gradient-to-br from-indigo-500 to-purple-600 p-3 rounded-xl text-white text-2xl animate-gentle-pulse shadow-soft">
                                ✨
                            </div>
                            <div>
                                <h2 className="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                                    AI Chief of Staff Report
                                </h2>
                                <p className="text-sm text-gray-500 mt-1">Generated by Gemini 2.0 Flash</p>
                            </div>
                        </div>

                        <div className="prose prose-indigo prose-sm sm:prose-base max-w-none text-gray-600 animate-fadeIn delay-300">
                            <ReactMarkdown>{data.analysis}</ReactMarkdown>
                        </div>
                        
                        {/* Healing indicator */}
                        <div className="mt-6 p-4 bg-gradient-to-r from-blue-50 to-purple-50 border-l-4 border-indigo-500 rounded-xl text-sm animate-fadeInScale delay-500">
                            <div className="flex items-center gap-2 text-indigo-700">
                                <span className="animate-breathe">💡</span>
                                <strong>AI-Powered Insights:</strong>
                            </div>
                            <p className="text-gray-600 mt-1">
                                Recommendations updated in real-time based on current hospital data
                            </p>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Dashboard;
