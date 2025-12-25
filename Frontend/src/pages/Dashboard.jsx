import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { 
    LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
    RadialBarChart, RadialBar, PieChart, Pie, Cell
} from 'recharts';
import { 
    Heart, Activity, Thermometer, Droplet, Scale, TrendingUp, TrendingDown,
    Calendar, Pill, FileText, Brain, AlertCircle, CheckCircle, Clock,
    User, Phone, MapPin, Upload, MessageSquare, Download, Bell, Minus
} from 'lucide-react';

const Dashboard = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [timelineFilter, setTimelineFilter] = useState('all');

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/v1/user/dashboard', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: 'USER001', date_range: '30d' })
            });
            if (!response.ok) throw new Error('Failed to fetch data');
            const result = await response.json();
            setData(result);
            setError(null);
        } catch (err) {
            console.error(err);
            setError('Failed to load your health data.');
        } finally {
            setLoading(false);
        }
    };

    if (loading) return (
        <div className="flex justify-center items-center h-screen bg-gradient-to-br from-cyan-400 via-blue-500 to-purple-600">
            <div className="text-center">
                <div className="animate-pulse-glow bg-white p-10 rounded-3xl shadow-2xl">
                    <Heart className="w-20 h-20 text-red-500 mx-auto mb-4 animate-float" />
                    <p className="text-3xl font-bold text-gray-800">Loading Your Health Profile...</p>
                    <p className="text-gray-500 mt-2">Analyzing your medical data</p>
                </div>
            </div>
        </div>
    );

    if (error) return (
        <div className="flex justify-center items-center h-screen bg-gradient-to-br from-cyan-400 via-blue-500 to-purple-600 p-6">
            <div className="glass-card p-8 rounded-3xl max-w-md">
                <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
                <h2 className="text-2xl font-bold text-gray-800 text-center mb-2">Unable to Load Data</h2>
                <p className="text-gray-600 text-center mb-6">{error}</p>
                <button onClick={fetchData} className="w-full bg-gradient-to-r from-blue-500 to-cyan-500 text-white px-6 py-3 rounded-xl font-semibold hover:shadow-xl transition">
                    Try Again
                </button>
            </div>
        </div>
    );

    const { user_profile, health_score, vitals, diagnostics, treatments, appointments, mental_health, timeline, health_trends, alerts, ai_insights } = data;

    // Get health score color
    const getScoreColor = (score) => {
        if (score >= 80) return 'from-green-500 to-emerald-500';
        if (score >= 60) return 'from-yellow-500 to-orange-500';
        return 'from-red-500 to-pink-500';
    };

    // Get status badge
    const getStatusBadge = (status) => {
        const badges = {
            normal: { color: 'bg-green-100 text-green-700', icon: CheckCircle, text: 'Normal' },
            attention: { color: 'bg-yellow-100 text-yellow-700', icon: AlertCircle, text: 'Attention' },
            critical: { color: 'bg-red-100 text-red-700', icon: AlertCircle, text: 'Critical' }
        };
        return badges[status] || badges.normal;
    };

    // Filter timeline
    const filteredTimeline = timelineFilter === 'all' 
        ? timeline 
        : timeline.filter(item => item.type === timelineFilter);

    // Vital cards configuration
    const vitalCards = [
        {
            title: 'Heart Rate',
            value: vitals.heart_rate.current,
            unit: vitals.heart_rate.unit,
            icon: Heart,
            gradient: 'from-red-500 to-pink-500',
            trend: vitals.heart_rate.trend,
            history: vitals.heart_rate.history
        },
        {
            title: 'Blood Pressure',
            value: `${vitals.blood_pressure.systolic}/${vitals.blood_pressure.diastolic}`,
            unit: vitals.blood_pressure.unit,
            icon: Activity,
            gradient: 'from-purple-500 to-indigo-500',
            trend: vitals.blood_pressure.trend,
            history: vitals.blood_pressure.history
        },
        {
            title: 'Temperature',
            value: vitals.temperature.current,
            unit: vitals.temperature.unit,
            icon: Thermometer,
            gradient: 'from-orange-500 to-red-500',
            trend: 'stable'
        },
        {
            title: 'Oxygen',
            value: vitals.oxygen_saturation.current,
            unit: vitals.oxygen_saturation.unit,
            icon: Droplet,
            gradient: 'from-cyan-500 to-blue-500',
            trend: 'stable'
        },
        {
            title: 'BMI',
            value: vitals.bmi.value,
            unit: vitals.bmi.category,
            icon: Scale,
            gradient: 'from-green-500 to-teal-500',
            trend: 'stable'
        },
        {
            title: 'Blood Glucose',
            value: vitals.blood_glucose.current,
            unit: vitals.blood_glucose.unit,
            icon: Droplet,
            gradient: 'from-amber-500 to-yellow-500',
            trend: 'stable'
        }
    ];

    return (
        <div className="min-h-screen bg-gradient-to-br from-cyan-400 via-blue-500 to-purple-600 p-6">
            {/* Header */}
            <header className="mb-6 animate-fade-in">
                <div className="glass-card p-6 rounded-3xl">
                    <div className="flex justify-between items-center">
                        <div className="flex items-center gap-4">
                            <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white text-2xl font-bold shadow-lg">
                                {user_profile.name.split(' ').map(n => n[0]).join('')}
                            </div>
                            <div>
                                <h1 className="text-3xl font-extrabold text-gray-800">Welcome back, {user_profile.name.split(' ')[0]}!</h1>
                                <p className="text-gray-600 flex items-center gap-2 mt-1">
                                    <span className="status-dot success"></span>
                                    Your Personal Health Dashboard
                                </p>
                            </div>
                        </div>
                        <div className="flex gap-3">
                            <button onClick={fetchData} className="bg-white hover:bg-gray-50 text-gray-700 px-5 py-2.5 rounded-xl font-medium transition shadow-lg hover:shadow-xl flex items-center gap-2">
                                <Calendar className="w-4 h-4" />
                                Refresh
                            </button>
                            <button className="bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white px-5 py-2.5 rounded-xl font-medium transition shadow-lg hover:shadow-xl flex items-center gap-2">
                                <Download className="w-4 h-4" />
                                Export
                            </button>
                        </div>
                    </div>
                </div>
            </header>

            {/* Alerts Banner */}
            {alerts && alerts.length > 0 && (
                <div className="mb-6 space-y-3 animate-slide-in-left">
                    {alerts.map((alert, idx) => (
                        <div key={idx} className={`glass-card p-4 rounded-2xl border-l-4 ${
                            alert.priority === 'high' ? 'border-red-500' : 
                            alert.priority === 'medium' ? 'border-yellow-500' : 'border-blue-500'
                        }`}>
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-3">
                                    <Bell className={`w-5 h-5 ${
                                        alert.priority === 'high' ? 'text-red-500' : 
                                        alert.priority === 'medium' ? 'text-yellow-500' : 'text-blue-500'
                                    }`} />
                                    <div>
                                        <h3 className="font-bold text-gray-800">{alert.title}</h3>
                                        <p className="text-sm text-gray-600">{alert.message}</p>
                                    </div>
                                </div>
                                <button className="text-sm font-semibold text-blue-600 hover:text-blue-700">
                                    {alert.action}
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                {/* Left Column - Health Score & Vitals */}
                <div className="lg:col-span-1 space-y-6">
                    {/* Health Score Card */}
                    <div className="glass-card p-6 rounded-3xl shadow-2xl animate-scale-in hover-lift">
                        <h2 className="text-lg font-bold text-gray-800 mb-4 text-center">Overall Health Score</h2>
                        <div className="relative w-48 h-48 mx-auto mb-4">
                            <ResponsiveContainer width="100%" height="100%">
                                <RadialBarChart 
                                    cx="50%" 
                                    cy="50%" 
                                    innerRadius="70%" 
                                    outerRadius="100%" 
                                    data={[{ name: 'Score', value: health_score.overall, fill: '#3b82f6' }]}
                                    startAngle={180}
                                    endAngle={-180}
                                >
                                    <RadialBar
                                        minAngle={15}
                                        background
                                        clockWise
                                        dataKey="value"
                                        cornerRadius={10}
                                    />
                                </RadialBarChart>
                            </ResponsiveContainer>
                            <div className="absolute inset-0 flex flex-col items-center justify-center">
                                <p className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                                    {health_score.overall}
                                </p>
                                <p className="text-sm text-gray-600 font-medium">out of 100</p>
                            </div>
                        </div>
                        <div className="grid grid-cols-3 gap-2 text-center">
                            <div className="bg-gradient-to-br from-green-50 to-emerald-50 p-3 rounded-xl">
                                <p className="text-xs text-gray-600">Vitals</p>
                                <p className="text-lg font-bold text-green-600">{health_score.vitals}</p>
                            </div>
                            <div className="bg-gradient-to-br from-purple-50 to-indigo-50 p-3 rounded-xl">
                                <p className="text-xs text-gray-600">Mental</p>
                                <p className="text-lg font-bold text-purple-600">{health_score.mental}</p>
                            </div>
                            <div className="bg-gradient-to-br from-blue-50 to-cyan-50 p-3 rounded-xl">
                                <p className="text-xs text-gray-600">Lifestyle</p>
                                <p className="text-lg font-bold text-blue-600">{health_score.lifestyle}</p>
                            </div>
                        </div>
                    </div>

                    {/* Quick Stats */}
                    <div className="glass-card p-6 rounded-2xl shadow-lg">
                        <h3 className="text-sm font-bold text-gray-700 mb-4">Quick Stats</h3>
                        <div className="space-y-3">
                            <div className="flex items-center justify-between">
                                <span className="text-sm text-gray-600">Age</span>
                                <span className="font-bold text-gray-800">{user_profile.age} years</span>
                            </div>
                            <div className="flex items-center justify-between">
                                <span className="text-sm text-gray-600">Blood Group</span>
                                <span className="font-bold text-red-600">{user_profile.blood_group}</span>
                            </div>
                            <div className="flex items-center justify-between">
                                <span className="text-sm text-gray-600">Height</span>
                                <span className="font-bold text-gray-800">{user_profile.height_cm} cm</span>
                            </div>
                            <div className="flex items-center justify-between">
                                <span className="text-sm text-gray-600">Weight</span>
                                <span className="font-bold text-gray-800">{user_profile.weight_kg} kg</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Main Content Area */}
                <div className="lg:col-span-3 space-y-6">
                    {/* Vital Signs Grid */}
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4 animate-fade-in">
                        {vitalCards.map((vital, idx) => {
                            const Icon = vital.icon;
                            const TrendIcon = vital.trend === 'up' ? TrendingUp : vital.trend === 'down' ? TrendingDown : Minus;
                            return (
                                <div key={idx} className="glass-card p-5 rounded-2xl hover-lift cursor-pointer">
                                    <div className="flex items-start justify-between mb-3">
                                        <div className={`p-2.5 rounded-xl bg-gradient-to-br ${vital.gradient} shadow-lg`}>
                                            <Icon className="w-5 h-5 text-white" />
                                        </div>
                                        <TrendIcon className={`w-4 h-4 ${
                                            vital.trend === 'up' ? 'text-red-500' : 
                                            vital.trend === 'down' ? 'text-green-500' : 'text-gray-400'
                                        }`} />
                                    </div>
                                    <h3 className="text-xs text-gray-600 font-medium mb-1">{vital.title}</h3>
                                    <p className="text-2xl font-bold text-gray-800">{vital.value}</p>
                                    <p className="text-xs text-gray-500 mt-1">{vital.unit}</p>
                                    {vital.history && (
                                        <div className="mt-3 h-8">
                                            <ResponsiveContainer width="100%" height="100%">
                                                <AreaChart data={vital.history}>
                                                    <Area type="monotone" dataKey="value" stroke="#3b82f6" fill="#93c5fd" strokeWidth={2} />
                                                </AreaChart>
                                            </ResponsiveContainer>
                                        </div>
                                    )}
                                </div>
                            );
                        })}
                    </div>

                    {/* Active Treatments & Upcoming Appointments */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {/* Active Treatments */}
                        <div className="glass-card p-6 rounded-2xl shadow-lg">
                            <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                                <Pill className="w-5 h-5 text-blue-600" />
                                Active Medications
                            </h2>
                            <div className="space-y-4">
                                {treatments.map((treatment, idx) => (
                                    <div key={idx} className="bg-gradient-to-r from-blue-50 to-cyan-50 p-4 rounded-xl border border-blue-100">
                                        <div className="flex items-start justify-between mb-2">
                                            <div>
                                                <h3 className="font-bold text-gray-800">{treatment.medication}</h3>
                                                <p className="text-sm text-gray-600">{treatment.dosage} • {treatment.frequency}</p>
                                            </div>
                                            <span className="text-xs font-semibold bg-green-100 text-green-700 px-2 py-1 rounded-lg">
                                                {treatment.adherence}%
                                            </span>
                                        </div>
                                        <div className="mt-3">
                                            <div className="flex justify-between text-xs text-gray-600 mb-1">
                                                <span>Progress</span>
                                                <span>{treatment.days_completed}/{treatment.duration_days} days</span>
                                            </div>
                                            <div className="w-full bg-gray-200 rounded-full h-2">
                                                <div 
                                                    className="bg-gradient-to-r from-blue-500 to-cyan-500 h-2 rounded-full transition-all"
                                                    style={{ width: `${(treatment.days_completed / treatment.duration_days) * 100}%` }}
                                                ></div>
                                            </div>
                                        </div>
                                        <p className="text-xs text-gray-500 mt-2 flex items-center gap-1">
                                            <Clock className="w-3 h-3" />
                                            Next dose: {new Date(treatment.next_dose).toLocaleString()}
                                        </p>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Upcoming Appointments */}
                        <div className="glass-card p-6 rounded-2xl shadow-lg">
                            <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                                <Calendar className="w-5 h-5 text-purple-600" />
                                Upcoming Appointments
                            </h2>
                            <div className="space-y-4">
                                {appointments.upcoming.map((apt, idx) => (
                                    <div key={idx} className="bg-gradient-to-r from-purple-50 to-pink-50 p-4 rounded-xl border border-purple-100">
                                        <div className="flex items-start gap-3">
                                            <div className="bg-gradient-to-br from-purple-500 to-pink-500 text-white p-3 rounded-xl text-center min-w-[60px]">
                                                <p className="text-xs font-medium">{new Date(apt.date).toLocaleDateString('en-US', { month: 'short' })}</p>
                                                <p className="text-2xl font-bold">{new Date(apt.date).getDate()}</p>
                                            </div>
                                            <div className="flex-1">
                                                <h3 className="font-bold text-gray-800">{apt.doctor}</h3>
                                                <p className="text-sm text-gray-600">{apt.department} • {apt.type}</p>
                                                <p className="text-xs text-gray-500 mt-1 flex items-center gap-1">
                                                    <Clock className="w-3 h-3" />
                                                    {apt.time}
                                                </p>
                                                <p className="text-xs text-gray-500 flex items-center gap-1 mt-1">
                                                    <MapPin className="w-3 h-3" />
                                                    {apt.location}
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>

                    {/* Diagnostic Results */}
                    <div className="glass-card p-6 rounded-2xl shadow-lg animate-fade-in">
                        <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                            <FileText className="w-5 h-5 text-green-600" />
                            Recent Diagnostic Results
                        </h2>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            {diagnostics.map((diag, idx) => {
                                const badge = getStatusBadge(diag.status);
                                const BadgeIcon = badge.icon;
                                return (
                                    <div key={idx} className="bg-white p-5 rounded-xl border border-gray-200 hover:shadow-lg transition cursor-pointer">
                                        <div className="flex items-start justify-between mb-3">
                                            <div className="bg-gradient-to-br from-green-500 to-emerald-500 p-2 rounded-lg">
                                                <FileText className="w-5 h-5 text-white" />
                                            </div>
                                            <span className={`text-xs font-semibold px-2 py-1 rounded-lg flex items-center gap-1 ${badge.color}`}>
                                                <BadgeIcon className="w-3 h-3" />
                                                {badge.text}
                                            </span>
                                        </div>
                                        <h3 className="font-bold text-gray-800 mb-1">{diag.type}</h3>
                                        <p className="text-xs text-gray-500 mb-2">{diag.date} • {diag.doctor}</p>
                                        <p className="text-sm text-gray-600 line-clamp-2">{diag.ai_summary}</p>
                                        <button className="text-sm font-semibold text-blue-600 hover:text-blue-700 mt-3">
                                            View Full Report →
                                        </button>
                                    </div>
                                );
                            })}
                        </div>
                    </div>

                    {/* Health Timeline */}
                    <div className="glass-card p-6 rounded-2xl shadow-lg">
                        <div className="flex items-center justify-between mb-4">
                            <h2 className="text-xl font-bold text-gray-800 flex items-center gap-2">
                                <Activity className="w-5 h-5 text-indigo-600" />
                                Health Timeline
                            </h2>
                            <div className="flex gap-2">
                                {['all', 'diagnostic', 'treatment', 'appointment', 'mental_health'].map(filter => (
                                    <button
                                        key={filter}
                                        onClick={() => setTimelineFilter(filter)}
                                        className={`text-xs px-3 py-1.5 rounded-lg font-medium transition ${
                                            timelineFilter === filter
                                                ? 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white'
                                                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                                        }`}
                                    >
                                        {filter === 'all' ? 'All' : filter.replace('_', ' ')}
                                    </button>
                                ))}
                            </div>
                        </div>
                        <div className="space-y-4 max-h-96 overflow-y-auto custom-scrollbar">
                            {filteredTimeline.map((event, idx) => (
                                <div key={idx} className="flex gap-4">
                                    <div className="flex flex-col items-center">
                                        <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white text-lg shadow-lg">
                                            {event.icon}
                                        </div>
                                        {idx < filteredTimeline.length - 1 && (
                                            <div className="w-0.5 h-full bg-gradient-to-b from-blue-300 to-purple-300 mt-2"></div>
                                        )}
                                    </div>
                                    <div className="flex-1 pb-6">
                                        <div className="bg-white p-4 rounded-xl border border-gray-200 hover:shadow-md transition">
                                            <div className="flex items-start justify-between mb-2">
                                                <h3 className="font-bold text-gray-800">{event.title}</h3>
                                                <span className="text-xs text-gray-500">{event.date}</span>
                                            </div>
                                            <p className="text-sm text-gray-600">{event.description}</p>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* AI Health Coach Insights */}
                    <div className="glass-card p-8 rounded-3xl shadow-2xl animate-fade-in">
                        <div className="flex items-center gap-3 mb-6 pb-4 border-b border-gray-200">
                            <div className="bg-gradient-to-br from-blue-500 to-purple-500 p-3 rounded-xl text-white shadow-lg">
                                🤖
                            </div>
                            <div>
                                <h2 className="text-2xl font-bold text-gray-800">Your AI Health Coach</h2>
                                <p className="text-sm text-gray-600">Personalized insights powered by Google Gemini AI</p>
                            </div>
                        </div>
                        <div className="prose prose-blue prose-sm sm:prose-base max-w-none text-gray-700">
                            <ReactMarkdown>{ai_insights}</ReactMarkdown>
                        </div>
                    </div>

                    {/* Quick Actions */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <button className="glass-card p-6 rounded-2xl hover-lift text-center group">
                            <Calendar className="w-8 h-8 mx-auto mb-2 text-blue-600 group-hover:scale-110 transition" />
                            <p className="font-semibold text-gray-800">Book Appointment</p>
                        </button>
                        <button className="glass-card p-6 rounded-2xl hover-lift text-center group">
                            <Upload className="w-8 h-8 mx-auto mb-2 text-green-600 group-hover:scale-110 transition" />
                            <p className="font-semibold text-gray-800">Upload Report</p>
                        </button>
                        <button className="glass-card p-6 rounded-2xl hover-lift text-center group">
                            <MessageSquare className="w-8 h-8 mx-auto mb-2 text-purple-600 group-hover:scale-110 transition" />
                            <p className="font-semibold text-gray-800">Chat with AI</p>
                        </button>
                        <button className="glass-card p-6 rounded-2xl hover-lift text-center group">
                            <Brain className="w-8 h-8 mx-auto mb-2 text-pink-600 group-hover:scale-110 transition" />
                            <p className="font-semibold text-gray-800">Mental Health</p>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
