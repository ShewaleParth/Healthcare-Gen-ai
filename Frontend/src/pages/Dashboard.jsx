import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts';

const Dashboard = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/v1/hospital/optimize', {
                method: 'POST',
            });
            if (!response.ok) throw new Error('Failed to fetch data');
            const result = await response.json();
            setData(result);
        } catch (err) {
            console.error(err);
            setError('Failed to load hospital insights.');
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
        <div className="p-6 bg-gray-50 min-h-screen">
            <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-4xl font-extrabold text-gray-800 tracking-tight">🏥 Aarogya AI Dashboard</h1>
                    <p className="text-gray-500 mt-1">Real-time Hospital Workflow Optimization & Analytics</p>
                </div>
                <button
                    onClick={fetchData}
                    className="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-2 rounded-lg font-medium transition shadow-sm flex items-center gap-2"
                >
                    🔄 Refresh Analysis
                </button>
            </header>

            {error && (
                <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded shadow-sm mb-6">
                    {error}
                </div>
            )}

            {data && (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

                    {/* Left Column: Charts & Metrics */}
                    <div className="space-y-8">

                        {/* OPD Chart */}
                        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
                            <h2 className="text-lg font-bold text-gray-700 mb-4">📈 OPD Patient Flow (Forecast)</h2>
                            <div className="h-64">
                                <ResponsiveContainer width="100%" height="100%">
                                    <AreaChart data={opdChartData}>
                                        <defs>
                                            <linearGradient id="colorVisitors" x1="0" y1="0" x2="0" y2="1">
                                                <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8} />
                                                <stop offset="95%" stopColor="#8884d8" stopOpacity={0} />
                                            </linearGradient>
                                        </defs>
                                        <CartesianGrid strokeDasharray="3 3" vertical={false} />
                                        <XAxis dataKey="hour" fontSize={12} tickLine={false} axisLine={false} />
                                        <YAxis fontSize={12} tickLine={false} axisLine={false} />
                                        <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
                                        <Area type="monotone" dataKey="visitors" stroke="#8884d8" fillOpacity={1} fill="url(#colorVisitors)" />
                                    </AreaChart>
                                </ResponsiveContainer>
                            </div>
                        </div>

                        {/* Surgery & Inventory Grid */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                            {/* Surgery Chart */}
                            <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
                                <h2 className="text-lg font-bold text-gray-700 mb-4">🏥 Surgery Distribution</h2>
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
                                            <Tooltip />
                                            <Legend wrapperStyle={{ fontSize: '12px' }} />
                                        </PieChart>
                                    </ResponsiveContainer>
                                </div>
                            </div>

                            {/* Inventory List */}
                            <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
                                <h2 className="text-lg font-bold text-gray-700 mb-4">💊 Low Stock Alerts</h2>
                                <div className="space-y-3 max-h-48 overflow-y-auto pr-2 custom-scrollbar">
                                    {data.raw_data?.pharmacy_inventory?.filter(i => i.stock < i.threshold).map((item, i) => (
                                        <div key={i} className="flex justify-between items-center bg-red-50 p-2.5 rounded-lg border border-red-100 group hover:bg-red-100 transition">
                                            <span className="text-sm font-semibold text-red-700">{item.item}</span>
                                            <span className="text-xs bg-white text-red-600 px-2 py-1 rounded font-bold shadow-sm">
                                                {item.stock} left
                                            </span>
                                        </div>
                                    ))}
                                    {data.raw_data?.pharmacy_inventory?.filter(i => i.stock >= i.threshold).length === 0 && (
                                        <div className="text-sm text-gray-400 text-center py-4">All stock levels are healthy.</div>
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Right Column: AI Analysis Report */}
                    <div className="bg-white p-8 rounded-2xl shadow-lg border-t-4 border-indigo-600 h-fit">
                        <div className="flex items-center gap-3 mb-6 pb-4 border-b border-gray-100">
                            <div className="bg-indigo-100 p-2.5 rounded-xl text-indigo-600">
                                ✨
                            </div>
                            <h2 className="text-2xl font-bold text-gray-800">AI Chief of Staff Report</h2>
                        </div>

                        <div className="prose prose-indigo prose-sm sm:prose-base max-w-none text-gray-600">
                            <ReactMarkdown>{data.analysis}</ReactMarkdown>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Dashboard;
