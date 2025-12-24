import React, { useState } from 'react';

const MentalHealth = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);

    const sendMessage = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMsg = { role: 'user', content: input };
        setMessages([...messages, userMsg]);
        setInput('');
        setLoading(true);

        try {
            const response = await fetch('http://localhost:8000/api/v1/mental-health/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: input }),
            });
            const data = await response.json();
            const botMsg = { role: 'bot', content: data.response };
            setMessages(prev => [...prev, botMsg]);
        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [...prev, { role: 'bot', content: 'Connection error.' }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-6 h-screen flex flex-col">
            <h1 className="text-3xl font-bold mb-6">Mental Health Companion</h1>
            <div className="flex-1 bg-white rounded-lg shadow-md flex flex-col overflow-hidden">
                <div className="flex-1 overflow-y-auto p-6 space-y-4">
                    {messages.length === 0 && <p className="text-gray-500 text-center">Start a conversation. I am here to listen.</p>}
                    {messages.map((msg, idx) => (
                        <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                            <div className={`max-w-xs md:max-w-md p-3 rounded-lg ${msg.role === 'user' ? 'bg-indigo-600 text-white' : 'bg-gray-100 text-gray-800'}`}>
                                {msg.content}
                            </div>
                        </div>
                    ))}
                    {loading && <div className="text-gray-400 text-sm">typing...</div>}
                </div>
                <div className="p-4 border-t">
                    <form onSubmit={sendMessage} className="flex gap-2">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Type a message..."
                            className="flex-1 border p-2 rounded"
                        />
                        <button type="submit" className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700">Send</button>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default MentalHealth;
