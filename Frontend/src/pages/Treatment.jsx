import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import {
    User, Weight, Activity, FileText, Pill, AlertTriangle, CheckCircle,
    Heart, Shield, TrendingUp, Clock, Brain, Loader, ChevronDown, ChevronUp,
    AlertCircle, Info, Download, Share2, Zap
} from 'lucide-react';
import { RadialBarChart, RadialBar, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell } from 'recharts';

const Treatment = () => {
    const [formData, setFormData] = useState({
        age: '',
        weight: '',
        condition: '',
        history: '',
        current_meds: '',
        allergies: ''
    });
    const [recommendation, setRecommendation] = useState('');
    const [loading, setLoading] = useState(false);
    const [expandedSections, setExpandedSections] = useState({
        treatment: true,
        safety: true,
        alternatives: true,
        monitoring: true
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        const payload = {
            ...formData,
            age: parseInt(formData.age),
            weight: parseFloat(formData.weight),
            current_meds: formData.current_meds.split(',').map(s => s.trim()).filter(Boolean),
            allergies: formData.allergies.split(',').map(s => s.trim()).filter(Boolean)
        };

        try {
            const response = await fetch('http://localhost:8000/api/v1/treatment/recommend-treatment', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });
            const data = await response.json();
            setRecommendation(data.recommendation);
        } catch (error) {
            console.error('Error:', error);
            setRecommendation('**Error**: Unable to generate treatment recommendations. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const toggleSection = (section) => {
        setExpandedSections(prev => ({
            ...prev,
            [section]: !prev[section]
        }));
    };

    // Parse recommendation for risk level
    const getRiskLevel = (text) => {
        if (!text) return null;
        if (text.includes('ESCALATE TO DOCTOR') || text.includes('HIGH RISK')) {
            return { level: 'High', color: '#ef4444', bgColor: 'bg-red-50', textColor: 'text-red-700', value: 85 };
        }
        if (text.includes('MEDIUM RISK') || text.includes('moderate')) {
            return { level: 'Medium', color: '#f59e0b', bgColor: 'bg-amber-50', textColor: 'text-amber-700', value: 55 };
        }
        return { level: 'Low', color: '#10b981', bgColor: 'bg-green-50', textColor: 'text-green-700', value: 25 };
    };

    const riskMetrics = getRiskLevel(recommendation);

    // Check if form is complete
    const isFormComplete = formData.age && formData.weight && formData.condition;

    return (
        <div className="min-h-screen bg-gradient-to-br from-emerald-500 via-teal-500 to-cyan-600 p-6">
            {/* Header */}
            <header className="mb-8 animate-fade-in">
                <div className="glass-card p-6 rounded-3xl">
                    <div className="flex items-center gap-4">
                        <div className="bg-gradient-to-br from-emerald-600 to-teal-600 p-4 rounded-2xl shadow-lg">
                            <Pill className="w-8 h-8 text-white" />
                        </div>
                        <div>
                            <h1 className="text-4xl font-extrabold text-gray-800">Personalized Treatment & Safety</h1>
                            <p className="text-sm text-gray-500 mt-1">AI-powered treatment recommendations · Evidence-based medicine</p>
                        </div>
                    </div>
                </div>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Left Panel - Patient Input Form */}
                <div className="space-y-6">
                    <div className="glass-card p-6 rounded-3xl shadow-2xl animate-slide-in-left">
                        <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
                            <User className="w-6 h-6 text-emerald-600" />
                            Patient Information
                        </h2>

                        <form onSubmit={handleSubmit} className="space-y-5">
                            {/* Age & Weight */}
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                                        Age (years)
                                    </label>
                                    <div className="relative">
                                        <User className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
                                        <input
                                            name="age"
                                            type="number"
                                            value={formData.age}
                                            onChange={handleChange}
                                            className="w-full pl-10 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 transition"
                                            placeholder="35"
                                            required
                                        />
                                    </div>
                                </div>
                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                                        Weight (kg)
                                    </label>
                                    <div className="relative">
                                        <Weight className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
                                        <input
                                            name="weight"
                                            type="number"
                                            step="0.1"
                                            value={formData.weight}
                                            onChange={handleChange}
                                            className="w-full pl-10 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 transition"
                                            placeholder="70"
                                            required
                                        />
                                    </div>
                                </div>
                            </div>

                            {/* Medical Condition */}
                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-2">
                                    Primary Medical Condition
                                </label>
                                <div className="relative">
                                    <Activity className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
                                    <input
                                        name="condition"
                                        type="text"
                                        value={formData.condition}
                                        onChange={handleChange}
                                        className="w-full pl-10 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 transition"
                                        placeholder="e.g., Hypertension, Type 2 Diabetes"
                                        required
                                    />
                                </div>
                            </div>

                            {/* Medical History */}
                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-2">
                                    Medical History
                                </label>
                                <div className="relative">
                                    <FileText className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
                                    <textarea
                                        name="history"
                                        value={formData.history}
                                        onChange={handleChange}
                                        className="w-full pl-10 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 transition resize-none"
                                        rows="3"
                                        placeholder="Previous conditions, surgeries, chronic diseases..."
                                    />
                                </div>
                            </div>

                            {/* Current Medications */}
                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-2">
                                    Current Medications
                                </label>
                                <div className="relative">
                                    <Pill className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
                                    <input
                                        name="current_meds"
                                        type="text"
                                        value={formData.current_meds}
                                        onChange={handleChange}
                                        className="w-full pl-10 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 transition"
                                        placeholder="Metformin 500mg, Lisinopril 10mg (comma separated)"
                                    />
                                </div>
                                <p className="text-xs text-gray-500 mt-1 ml-1">Separate multiple medications with commas</p>
                            </div>

                            {/* Allergies */}
                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-2">
                                    Known Allergies
                                </label>
                                <div className="relative">
                                    <AlertTriangle className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
                                    <input
                                        name="allergies"
                                        type="text"
                                        value={formData.allergies}
                                        onChange={handleChange}
                                        className="w-full pl-10 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 transition"
                                        placeholder="Penicillin, Sulfa drugs (comma separated)"
                                    />
                                </div>
                                <p className="text-xs text-gray-500 mt-1 ml-1">Separate multiple allergies with commas</p>
                            </div>

                            {/* Submit Button */}
                            <button
                                type="submit"
                                disabled={loading || !isFormComplete}
                                className={`w-full px-6 py-4 rounded-2xl font-bold text-base transition-all shadow-lg ${
                                    loading || !isFormComplete
                                        ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                                        : 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white hover:from-emerald-700 hover:to-teal-700 hover:shadow-2xl hover:scale-105'
                                }`}
                            >
                                {loading ? (
                                    <span className="flex items-center justify-center gap-3">
                                        <Loader className="w-5 h-5 animate-spin" />
                                        Generating Treatment Plan...
                                    </span>
                                ) : (
                                    <span className="flex items-center justify-center gap-3">
                                        <Brain className="w-5 h-5" />
                                        Get AI Treatment Recommendation
                                    </span>
                                )}
                            </button>
                        </form>

                        {/* Info Cards */}
                        <div className="grid grid-cols-3 gap-3 mt-6">
                            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 p-3 rounded-xl text-center border border-blue-200">
                                <Shield className="w-5 h-5 text-blue-600 mx-auto mb-1" />
                                <p className="text-xs font-semibold text-gray-700">Safety First</p>
                            </div>
                            <div className="bg-gradient-to-br from-purple-50 to-pink-50 p-3 rounded-xl text-center border border-purple-200">
                                <Brain className="w-5 h-5 text-purple-600 mx-auto mb-1" />
                                <p className="text-xs font-semibold text-gray-700">AI Powered</p>
                            </div>
                            <div className="bg-gradient-to-br from-green-50 to-emerald-50 p-3 rounded-xl text-center border border-green-200">
                                <CheckCircle className="w-5 h-5 text-green-600 mx-auto mb-1" />
                                <p className="text-xs font-semibold text-gray-700">Evidence Based</p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Right Panel - AI Recommendations */}
                <div className="space-y-6">
                    {!recommendation && !loading && (
                        <div className="glass-card p-12 rounded-3xl text-center animate-fade-in">
                            <div className="w-24 h-24 bg-gradient-to-br from-gray-200 to-gray-300 rounded-full mx-auto mb-6 flex items-center justify-center">
                                <Pill className="w-12 h-12 text-gray-400" />
                            </div>
                            <h3 className="text-xl font-bold text-gray-700 mb-3">No Treatment Plan Yet</h3>
                            <p className="text-sm text-gray-500">Complete the patient information form and submit to generate personalized treatment recommendations</p>
                        </div>
                    )}

                    {loading && (
                        <div className="glass-card p-12 rounded-3xl text-center animate-pulse-glow">
                            <div className="w-24 h-24 bg-gradient-to-br from-emerald-500 to-teal-500 rounded-full mx-auto mb-6 flex items-center justify-center animate-float">
                                <Brain className="w-12 h-12 text-white animate-pulse" />
                            </div>
                            <h3 className="text-xl font-bold text-gray-800 mb-3">Analyzing Patient Profile...</h3>
                            <p className="text-sm text-gray-600 mb-6">AI is generating personalized treatment recommendations</p>
                            <div className="space-y-3">
                                {['Analyzing patient metrics', 'Checking drug interactions', 'Calculating dosages', 'Generating safety analysis'].map((step, idx) => (
                                    <div key={idx} className="flex items-center gap-3 text-xs text-gray-600 animate-fade-in" style={{ animationDelay: `${idx * 0.3}s` }}>
                                        <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
                                        {step}
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {recommendation && riskMetrics && (
                        <div className="space-y-6 animate-scale-in">
                            {/* Header Card */}
                            <div className="glass-card p-6 rounded-3xl shadow-2xl border-l-4 border-emerald-500">
                                <div className="flex items-center justify-between mb-6">
                                    <div>
                                        <h2 className="text-2xl font-bold text-gray-800">AI Treatment Recommendations</h2>
                                        <p className="text-sm text-gray-500 mt-1">Personalized for {formData.condition}</p>
                                    </div>
                                    <div className="flex gap-2">
                                        <button className="p-2 hover:bg-gray-100 rounded-lg transition">
                                            <Download className="w-5 h-5 text-gray-600" />
                                        </button>
                                        <button className="p-2 hover:bg-gray-100 rounded-lg transition">
                                            <Share2 className="w-5 h-5 text-gray-600" />
                                        </button>
                                    </div>
                                </div>

                                {/* Summary Cards */}
                                <div className="grid grid-cols-3 gap-4 mb-6">
                                    <div className="bg-gradient-to-br from-gray-50 to-slate-50 p-4 rounded-xl border border-gray-200">
                                        <p className="text-xs text-gray-500 mb-1">Patient Age</p>
                                        <p className="text-lg font-bold text-gray-800">{formData.age} years</p>
                                    </div>
                                    <div className="bg-gradient-to-br from-gray-50 to-slate-50 p-4 rounded-xl border border-gray-200">
                                        <p className="text-xs text-gray-500 mb-1">Weight</p>
                                        <p className="text-lg font-bold text-gray-800">{formData.weight} kg</p>
                                    </div>
                                    <div className="bg-gradient-to-br from-gray-50 to-slate-50 p-4 rounded-xl border border-gray-200">
                                        <p className="text-xs text-gray-500 mb-1">AI Model</p>
                                        <p className="text-sm font-bold text-emerald-600">Gemini AI</p>
                                    </div>
                                </div>

                                {/* Risk Level Gauge */}
                                <div className={`${riskMetrics.bgColor} border-2 ${riskMetrics.textColor.replace('text', 'border')} rounded-2xl p-6`}>
                                    <div className="flex items-center justify-between mb-4">
                                        <h3 className="text-sm font-semibold text-gray-700">Safety Risk Assessment</h3>
                                        <span className={`text-sm font-bold ${riskMetrics.textColor}`}>{riskMetrics.level} Risk</span>
                                    </div>
                                    <div className="relative h-32">
                                        <ResponsiveContainer width="100%" height="100%">
                                            <RadialBarChart 
                                                cx="50%" 
                                                cy="100%" 
                                                innerRadius="80%" 
                                                outerRadius="100%" 
                                                data={[{ value: riskMetrics.value, fill: riskMetrics.color }]}
                                                startAngle={180}
                                                endAngle={0}
                                            >
                                                <RadialBar
                                                    background={{ fill: '#e5e7eb' }}
                                                    dataKey="value"
                                                    cornerRadius={10}
                                                />
                                            </RadialBarChart>
                                        </ResponsiveContainer>
                                        <div className="absolute bottom-0 left-0 right-0 flex justify-between text-xs text-gray-500 px-4">
                                            <span>Low</span>
                                            <span>Medium</span>
                                            <span>High</span>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* ESCALATE Warning if High Risk */}
                            {recommendation.includes('ESCALATE TO DOCTOR') && (
                                <div className="glass-card p-6 rounded-2xl border-2 border-red-500 bg-red-50 animate-pulse">
                                    <div className="flex items-start gap-3">
                                        <AlertCircle className="w-8 h-8 text-red-600 flex-shrink-0" />
                                        <div>
                                            <h3 className="text-lg font-bold text-red-800 mb-2">⚠️ ESCALATE TO DOCTOR</h3>
                                            <p className="text-sm text-red-700">
                                                High-risk factors detected. Immediate physician consultation required before any treatment.
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* Full Recommendation */}
                            <div className="glass-card p-6 rounded-2xl shadow-lg">
                                <div className="prose prose-sm max-w-none text-gray-700 leading-relaxed">
                                    <ReactMarkdown
                                        components={{
                                            strong: ({node, ...props}) => <strong className="font-bold text-gray-900" {...props} />,
                                            h2: ({node, ...props}) => <h2 className="text-xl font-bold text-gray-800 mt-6 mb-3 flex items-center gap-2" {...props} />,
                                            h3: ({node, ...props}) => <h3 className="text-lg font-bold text-gray-800 mt-4 mb-2" {...props} />,
                                            ul: ({node, ...props}) => <ul className="space-y-2 my-3" {...props} />,
                                            li: ({node, ...props}) => <li className="ml-4" {...props} />
                                        }}
                                    >
                                        {recommendation}
                                    </ReactMarkdown>
                                </div>
                            </div>

                            {/* Disclaimer */}
                            <div className="glass-card p-5 rounded-2xl border-l-4 border-amber-400 bg-gradient-to-r from-amber-50 to-yellow-50">
                                <div className="flex items-start gap-3">
                                    <AlertTriangle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                                    <div>
                                        <h4 className="text-sm font-semibold text-gray-800 mb-1">Critical Medical Disclaimer</h4>
                                        <p className="text-xs text-gray-600 leading-relaxed">
                                            This AI-generated treatment plan is for informational purposes only. <span className="font-medium text-gray-700">Do not start, stop, or modify any treatment without consulting a licensed physician.</span> Final treatment decisions must be made by qualified healthcare professionals based on complete clinical evaluation.
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Treatment;
