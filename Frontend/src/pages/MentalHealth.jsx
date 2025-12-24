import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import ChatBubble from '../components/ChatBubble';
import RiskIndicator from '../components/RiskIndicator';
import TypingIndicator from '../components/TypingIndicator';
import toast, { Toaster } from 'react-hot-toast';

const MentalHealth = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [currentRiskLevel, setCurrentRiskLevel] = useState('LOW');
    const [showEmergency, setShowEmergency] = useState(false);
    const messagesEndRef = useRef(null);
    const chatContainerRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, loading]);

    const detectRiskLevel = (message) => {
        const lowerMsg = message.toLowerCase();
        
        // Critical keywords
        const criticalKeywords = ['suicide', 'kill myself', 'end my life', 'want to die', 'better off dead', 'no reason to live'];
        if (criticalKeywords.some(keyword => lowerMsg.includes(keyword))) {
            return 'CRITICAL';
        }

        // High risk keywords
        const highRiskKeywords = ['self-harm', 'cut myself', 'hurt myself', 'hate myself', 'worthless', 'hopeless'];
        if (highRiskKeywords.some(keyword => lowerMsg.includes(keyword))) {
            return 'HIGH';
        }

        // Moderate risk keywords
        const moderateKeywords = ['depressed', 'anxious', 'scared', 'alone', 'empty', 'overwhelmed'];
        const moderateCount = moderateKeywords.filter(keyword => lowerMsg.includes(keyword)).length;
        if (moderateCount >= 2) {
            return 'MODERATE';
        }

        return 'LOW';
    };

    const sendMessage = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMsg = { 
            role: 'user', 
            content: input,
            timestamp: new Date().toISOString()
        };
        
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setLoading(true);

        // Detect risk level from user message
        const riskLevel = detectRiskLevel(input);

        try {
            const response = await fetch('http://localhost:8000/api/v1/mental-health/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: input }),
            });
            
            if (!response.ok) throw new Error('Failed to get response');
            
            const data = await response.json();
            
            // Check if emergency protocol was activated
            const isEmergency = data.response.includes('EMERGENCY PROTOCOL ACTIVATED') || 
                               data.response.includes('🚨');
            
            if (isEmergency) {
                setShowEmergency(true);
                setCurrentRiskLevel('CRITICAL');
                toast.error('Emergency Protocol Activated', {
                    duration: 5000,
                    icon: '🚨',
                });
            } else {
                setCurrentRiskLevel(riskLevel);
                if (riskLevel === 'HIGH') {
                    toast('High risk detected - Professional help recommended', {
                        icon: '⚠️',
                        duration: 4000,
                    });
                }
            }

            const botMsg = { 
                role: 'bot', 
                content: data.response,
                timestamp: new Date().toISOString(),
                riskLevel: isEmergency ? 'CRITICAL' : riskLevel
            };
            
            setMessages(prev => [...prev, botMsg]);
        } catch (error) {
            console.error('Error:', error);
            toast.error('Connection error. Please try again.');
            const errorMsg = {
                role: 'bot',
                content: 'I apologize, but I\'m having trouble connecting right now. If you\'re in crisis, please call 1-800-273-8255 immediately.',
                timestamp: new Date().toISOString(),
                riskLevel: 'HIGH'
            };
            setMessages(prev => [...prev, errorMsg]);
        } finally {
            setLoading(false);
        }
    };

    const loadDemoScenario = (scenario) => {
        if (scenario === 'anxiety') {
            setInput("I've been feeling really anxious about work lately. I can't sleep at night.");
        } else if (scenario === 'crisis') {
            setInput("I don't see the point in going on anymore");
        }
    };

    return (
        <div className="p-6 h-screen flex flex-col bg-gradient-to-br from-purple-50 to-indigo-50">
            <Toaster position="top-right" />
            
            {/* Header */}
            <div className="mb-6">
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-4xl font-extrabold text-gray-800 flex items-center gap-3">
                            <span className="text-4xl">🧠</span>
                            Mental Health Companion
                        </h1>
                        <p className="text-gray-500 mt-1">Safe, confidential, and compassionate support</p>
                    </div>
                    <div className="flex items-center gap-3">
                        <RiskIndicator level={currentRiskLevel} />
                    </div>
                </div>

                {/* Demo Scenarios */}
                <div className="mt-4 flex gap-2">
                    <button
                        onClick={() => loadDemoScenario('anxiety')}
                        className="text-xs bg-blue-100 text-blue-700 px-3 py-1.5 rounded-full hover:bg-blue-200 transition"
                    >
                        📝 Load Anxiety Demo
                    </button>
                    <button
                        onClick={() => loadDemoScenario('crisis')}
                        className="text-xs bg-red-100 text-red-700 px-3 py-1.5 rounded-full hover:bg-red-200 transition"
                    >
                        🚨 Load Crisis Demo
                    </button>
                </div>
            </div>

            {/* Emergency Overlay */}
            {showEmergency && (
                <div className="fixed inset-0 bg-red-600 bg-opacity-95 z-50 flex items-center justify-center p-6 animate-pulse-red">
                    <div className="bg-white rounded-2xl p-8 max-w-2xl shadow-2xl">
                        <div className="text-center">
                            <div className="text-6xl mb-4">🚨</div>
                            <h2 className="text-3xl font-bold text-red-600 mb-4">EMERGENCY PROTOCOL ACTIVATED</h2>
                            <p className="text-lg text-gray-700 mb-6">
                                Your message indicates you may be in crisis. Please get help immediately.
                            </p>
                            
                            <div className="bg-red-50 border-2 border-red-200 rounded-xl p-6 mb-6 text-left">
                                <h3 className="font-bold text-red-800 mb-3 text-xl">📞 Get Help Now:</h3>
                                <ul className="space-y-2 text-gray-800">
                                    <li className="flex items-center gap-2">
                                        <span className="font-semibold">National Suicide Prevention Lifeline:</span>
                                        <span className="text-2xl font-bold text-red-600">1-800-273-8255</span>
                                    </li>
                                    <li className="flex items-center gap-2">
                                        <span className="font-semibold">Crisis Text Line:</span>
                                        <span className="text-xl font-bold text-red-600">Text HOME to 741741</span>
                                    </li>
                                    <li className="flex items-center gap-2">
                                        <span className="font-semibold">Emergency Services:</span>
                                        <span className="text-2xl font-bold text-red-600">911</span>
                                    </li>
                                </ul>
                            </div>

                            <button
                                onClick={() => setShowEmergency(false)}
                                className="bg-gray-800 text-white px-8 py-3 rounded-lg font-semibold hover:bg-gray-700 transition"
                            >
                                I Understand - Close This Alert
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Chat Container */}
            <div className="flex-1 bg-white rounded-2xl shadow-lg flex flex-col overflow-hidden border border-gray-200">
                {/* Chat Messages */}
                <div 
                    ref={chatContainerRef}
                    className="flex-1 overflow-y-auto p-6 space-y-4 custom-scrollbar"
                    style={{ backgroundImage: 'radial-gradient(circle, #f3f4f6 1px, transparent 1px)', backgroundSize: '20px 20px' }}
                >
                    {messages.length === 0 && (
                        <div className="flex flex-col items-center justify-center h-full text-center">
                            <div className="text-6xl mb-4">💬</div>
                            <h3 className="text-xl font-semibold text-gray-700 mb-2">
                                Welcome to Your Safe Space
                            </h3>
                            <p className="text-gray-500 max-w-md">
                                I'm here to listen without judgment. Share what's on your mind, and I'll provide compassionate support using evidence-based techniques.
                            </p>
                            <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4 max-w-md">
                                <p className="text-sm text-blue-800">
                                    <strong>🔒 Confidential & Safe:</strong> This conversation uses AI-powered risk detection to ensure your safety.
                                </p>
                            </div>
                        </div>
                    )}
                    
                    {messages.map((msg, idx) => (
                        <ChatBubble
                            key={idx}
                            message={msg.content}
                            isUser={msg.role === 'user'}
                            timestamp={msg.timestamp}
                            riskLevel={msg.riskLevel}
                        />
                    ))}
                    
                    {loading && <TypingIndicator />}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <div className="p-4 border-t border-gray-200 bg-gray-50">
                    <form onSubmit={sendMessage} className="flex gap-3">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Type your message here..."
                            className="flex-1 border border-gray-300 px-4 py-3 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                            disabled={loading}
                        />
                        <button 
                            type="submit" 
                            disabled={loading || !input.trim()}
                            className="bg-gradient-to-r from-purple-500 to-indigo-600 text-white px-6 py-3 rounded-xl hover:from-purple-600 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed font-semibold shadow-sm transition-all hover:shadow-md flex items-center gap-2"
                        >
                            <span>Send</span>
                            <span>📤</span>
                        </button>
                    </form>
                    <p className="text-xs text-gray-400 mt-2 text-center">
                        AI-powered support with crisis detection • Not a substitute for professional help
                    </p>
                </div>
            </div>
        </div>
    );
};

export default MentalHealth;
