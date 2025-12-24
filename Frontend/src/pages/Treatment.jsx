import React, { useState } from 'react';

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
            setRecommendation('Error getting recommendation.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-6">
            <h1 className="text-3xl font-bold mb-6">Personalized Treatment & Safety</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-white p-6 rounded-lg shadow-md">
                    <h2 className="text-xl font-semibold mb-4">Patient Details</h2>
                    <form onSubmit={handleSubmit}>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="mb-4">
                                <label className="block text-gray-700 text-sm font-bold mb-2">Age</label>
                                <input name="age" type="number" onChange={handleChange} className="border p-2 w-full" required />
                            </div>
                            <div className="mb-4">
                                <label className="block text-gray-700 text-sm font-bold mb-2">Weight (kg)</label>
                                <input name="weight" type="number" onChange={handleChange} className="border p-2 w-full" required />
                            </div>
                        </div>
                        <div className="mb-4">
                            <label className="block text-gray-700 text-sm font-bold mb-2">Medical Condition</label>
                            <input name="condition" type="text" onChange={handleChange} className="border p-2 w-full" required />
                        </div>
                        <div className="mb-4">
                            <label className="block text-gray-700 text-sm font-bold mb-2">Medical History</label>
                            <textarea name="history" onChange={handleChange} className="border p-2 w-full" />
                        </div>
                        <div className="mb-4">
                            <label className="block text-gray-700 text-sm font-bold mb-2">Current Meds (comma sep)</label>
                            <input name="current_meds" type="text" onChange={handleChange} className="border p-2 w-full" />
                        </div>
                        <div className="mb-4">
                            <label className="block text-gray-700 text-sm font-bold mb-2">Allergies (comma sep)</label>
                            <input name="allergies" type="text" onChange={handleChange} className="border p-2 w-full" />
                        </div>
                        <button
                            type="submit"
                            disabled={loading}
                            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 w-full"
                        >
                            {loading ? 'Processing...' : 'Get Recommendation'}
                        </button>
                    </form>
                </div>

                <div className="bg-white p-6 rounded-lg shadow-md">
                    <h2 className="text-xl font-semibold mb-4">AI Recommendation</h2>
                    <div className="prose bg-gray-50 p-4 rounded border border-gray-200 h-full overflow-auto">
                        <pre className="whitespace-pre-wrap font-sans">{recommendation || "Submit patient data to generate treatment plan."}</pre>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Treatment;
