import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import toast, { Toaster } from 'react-hot-toast';
import sampleCases from '../../../Dataset/sample_cases.json';

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
    const [selectedCase, setSelectedCase] = useState('');

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const loadDemoPatient = (caseData) => {
        setSelectedCase(caseData.id);
        setFormData({
            age: caseData.patient_data.age.toString(),
            weight: caseData.patient_data.weight.toString(),
            condition: caseData.patient_data.condition,
            history: caseData.patient_data.history,
            current_meds: caseData.patient_data.current_meds.join(', '),
            allergies: caseData.patient_data.allergies.join(', ')
        });
        setRecommendation('');
        toast.success(`Loaded demo patient: ${caseData.title}`, { icon: '👤' });
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
            
            if (!response.ok) throw new Error('Failed to get recommendation');
            
            const data = await response.json();
            setRecommendation(data.recommendation);
            
            // Check for safety warnings
            if (data.recommendation.includes('ESCALATE TO DOCTOR') || 
                data.recommendation.includes('⚠️') ||
                data.recommendation.includes('WARNING')) {
                toast.error('Safety warning detected!', { icon: '⚠️', duration: 5000 });
            } else {
                toast.success('Treatment plan generated!', { icon: '✅' });
            }
        } catch (error) {
            console.error('Error:', error);
            setRecommendation('Error getting recommendation. Please try again.');
            toast.error('Failed to generate recommendation');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-6 bg-medical-gradient min-h-screen bg-pattern-dots animate-fadeIn">
            <Toaster position="top-right" />
            
            {/* Header with breathing animation */}
            <div className="mb-8 animate-slideInLeft">
                <h1 className="text-4xl font-bold text-gray-800 flex items-center gap-3">
                    <span className="animate-gentle-pulse">💊</span>
                    <span className="bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
                        Personalized Treatment & Safety
                    </span>
                </h1>
                <p className="text-gray-500 mt-2 ml-14 animate-fadeIn delay-200">AI-powered treatment recommendations with drug interaction detection</p>
                {/* Decorative healing line */}
                <div className="absolute mt-1 ml-14 h-1 w-64 bg-gradient-to-r from-green-500 via-emerald-500 to-teal-500 rounded-full animate-gradient"></div>
            </div>

            {/* Demo Patients Section with gentle animation */}
            <div className="mb-6 glass p-4 rounded-xl shadow-soft border border-white/20 animate-fadeInScale">
                <h3 className="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
                    <span className="animate-breathe">⚡</span>
                    Quick Demo Patients
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {sampleCases.treatment_cases.map((demoCase, index) => (
                        <button
                            key={demoCase.id}
                            onClick={() => loadDemoPatient(demoCase)}
                            className={`text-left p-4 rounded-xl border-2 transition-all duration-300 hover:shadow-soft-lg animate-fadeInScale hover:scale-105 transform ${
                                selectedCase === demoCase.id
                                    ? 'border-green-500 bg-gradient-to-br from-green-50 to-emerald-50 shadow-soft-lg'
                                    : 'border-gray-200 hover:border-green-300 bg-white/50'
                            }`}
                            style={{ animationDelay: `${index * 0.1}s` }}
                        >
                            <div className="flex items-center gap-2 mb-2">
                                {selectedCase === demoCase.id && (
                                    <span className="text-green-600 animate-gentle-pulse">✓</span>
                                )}
                                <div className="font-semibold text-sm text-gray-800">{demoCase.title}</div>
                            </div>
                            <div className="text-xs text-gray-500">{demoCase.expected_warnings}</div>
                        </button>
                    ))}
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Patient Form with gentle animation */}
                <div className="glass p-6 rounded-2xl shadow-soft-lg border border-white/20 animate-slideInLeft hover:shadow-soft-lg transition-all duration-500">
                    <div className="flex items-center gap-2 mb-6">
                        <div className="w-10 h-10 bg-gradient-to-br from-green-500 to-green-600 rounded-xl flex items-center justify-center animate-gentle-pulse">
                            <span className="text-white text-xl">📋</span>
                        </div>
                        <h2 className="text-xl font-semibold text-gray-700">Patient Details</h2>
                    </div>
                    <form onSubmit={handleSubmit}>
                        <div className="grid grid-cols-2 gap-4 mb-4">
                            <div className="animate-fadeInScale delay-100">
                                <label className="block text-gray-700 text-sm font-semibold mb-2">Age</label>
                                <input 
                                    name="age" 
                                    type="number" 
                                    value={formData.age}
                                    onChange={handleChange} 
                                    className="border border-gray-300 p-3 w-full rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all hover:border-green-300 shadow-soft" 
                                    required 
                                    placeholder="e.g., 45"
                                />
                            </div>
                            <div className="animate-fadeInScale delay-200">
                                <label className="block text-gray-700 text-sm font-semibold mb-2">Weight (kg)</label>
                                <input 
                                    name="weight" 
                                    type="number" 
                                    value={formData.weight}
                                    onChange={handleChange} 
                                    className="border border-gray-300 p-3 w-full rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all hover:border-green-300 shadow-soft" 
                                    required 
                                    placeholder="e.g., 75"
                                />
                            </div>
                        </div>
                        
                        <div className="mb-4 animate-fadeInScale delay-300">
                            <label className="block text-gray-700 text-sm font-semibold mb-2">Medical Condition</label>
                            <input 
                                name="condition" 
                                type="text" 
                                value={formData.condition}
                                onChange={handleChange} 
                                className="border border-gray-300 p-3 w-full rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all hover:border-green-300 shadow-soft" 
                                required 
                                placeholder="e.g., Hypertension Stage 2"
                            />
                        </div>
                        
                        <div className="mb-4 animate-fadeInScale delay-400">
                            <label className="block text-gray-700 text-sm font-semibold mb-2">Medical History</label>
                            <textarea 
                                name="history" 
                                value={formData.history}
                                onChange={handleChange} 
                                className="border border-gray-300 p-3 w-full rounded-xl h-20 focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all hover:border-green-300 shadow-soft" 
                                placeholder="e.g., Type 2 Diabetes, High cholesterol"
                            />
                        </div>
                        
                        <div className="mb-4 animate-fadeInScale delay-500">
                            <label className="block text-gray-700 text-sm font-semibold mb-2">
                                Current Medications
                                <span className="text-xs text-gray-500 ml-2">(comma separated)</span>
                            </label>
                            <input 
                                name="current_meds" 
                                type="text" 
                                value={formData.current_meds}
                                onChange={handleChange} 
                                className="border border-gray-300 p-3 w-full rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all hover:border-green-300 shadow-soft" 
                                placeholder="e.g., Metformin 1000mg, Atorvastatin 20mg"
                            />
                        </div>
                        
                        <div className="mb-6 animate-fadeInScale delay-700">
                            <label className="block text-gray-700 text-sm font-semibold mb-2">
                                Known Allergies
                                <span className="text-xs text-gray-500 ml-2">(comma separated)</span>
                            </label>
                            <input 
                                name="allergies" 
                                type="text" 
                                value={formData.allergies}
                                onChange={handleChange} 
                                className="border border-gray-300 p-3 w-full rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all hover:border-green-300 shadow-soft" 
                                placeholder="e.g., Penicillin, Sulfa drugs"
                            />
                        </div>
                        
                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white px-6 py-4 rounded-xl font-semibold shadow-soft hover:shadow-soft-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 group hover:scale-105 transform animate-fadeInScale delay-1000"
                        >
                            {loading ? (
                                <>
                                    <span className="animate-spin text-xl">⚙️</span>
                                    <span className="animate-pulse">Processing...</span>
                                </>
                            ) : (
                                <>
                                    <span className="group-hover:animate-gentle-pulse text-xl">🔬</span>
                                    Generate Treatment Plan
                                </>
                            )}
                        </button>
                    </form>
                </div>

                {/* Recommendation Display with gentle entrance */}
                <div className="glass p-6 rounded-2xl shadow-soft-lg border border-white/20 animate-slideInRight hover:shadow-soft-lg transition-all duration-500">
                    <div className="flex items-center gap-2 mb-6">
                        <div className="w-10 h-10 bg-gradient-to-br from-green-500 to-green-600 rounded-xl flex items-center justify-center animate-gentle-pulse">
                            <span className="text-white text-xl">🤖</span>
                        </div>
                        <h2 className="text-xl font-semibold text-gray-700">AI Treatment Recommendation</h2>
                    </div>
                    
                    {recommendation ? (
                        <div className="animate-fadeInScale">
                            <div className="prose prose-green max-w-none bg-white/70 backdrop-blur-sm p-6 rounded-xl border border-gray-200 overflow-auto max-h-[600px] custom-scrollbar shadow-soft">
                                <ReactMarkdown>{recommendation}</ReactMarkdown>
                            </div>
                            <div className="mt-4 p-4 bg-gradient-to-r from-yellow-50 to-orange-50 border-l-4 border-yellow-400 rounded-xl text-sm animate-fadeInScale delay-200">
                                <div className="flex items-center gap-2 text-yellow-800">
                                    <span className="animate-breathe">⚠️</span>
                                    <strong>Safety Reminder:</strong>
                                </div>
                                <p className="text-yellow-700 mt-1">
                                    This AI recommendation is for informational purposes only. Always consult a licensed physician before administering any medication.
                                </p>
                            </div>
                        </div>
                    ) : (
                        <div className="flex flex-col items-center justify-center h-64 text-center animate-breathe">
                            <div className="text-6xl mb-4 animate-float">💊</div>
                            <h3 className="text-lg font-semibold text-gray-700 mb-2">
                                No Recommendation Yet
                            </h3>
                            <p className="text-gray-500 max-w-sm">
                                Fill in the patient details and click "Generate Treatment Plan" to receive AI-powered recommendations with safety analysis.
                            </p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Treatment;
