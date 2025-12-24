import React from 'react';

const ChatBubble = ({ message, isUser, timestamp, riskLevel }) => {
    return (
        <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 animate-fadeIn`}>
            <div className={`flex items-start gap-2.5 max-w-[75%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
                {/* Avatar */}
                <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold ${
                    isUser 
                        ? 'bg-blue-500 text-white' 
                        : 'bg-gradient-to-br from-purple-500 to-indigo-600 text-white'
                }`}>
                    {isUser ? '👤' : '🤖'}
                </div>

                {/* Message Content */}
                <div className={`flex flex-col gap-1 ${isUser ? 'items-end' : 'items-start'}`}>
                    <div className={`rounded-2xl px-4 py-3 shadow-sm ${
                        isUser 
                            ? 'bg-blue-500 text-white rounded-tr-none' 
                            : 'bg-gray-100 text-gray-800 rounded-tl-none border border-gray-200'
                    }`}>
                        <p className="text-sm leading-relaxed whitespace-pre-wrap">{message}</p>
                    </div>

                    {/* Timestamp and Risk Level */}
                    <div className="flex items-center gap-2 px-2">
                        {timestamp && (
                            <span className="text-xs text-gray-400">
                                {new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                            </span>
                        )}
                        {!isUser && riskLevel && riskLevel !== 'LOW' && (
                            <span className={`text-xs px-2 py-0.5 rounded-full font-semibold ${
                                riskLevel === 'CRITICAL' ? 'bg-red-100 text-red-700' :
                                riskLevel === 'HIGH' ? 'bg-orange-100 text-orange-700' :
                                'bg-yellow-100 text-yellow-700'
                            }`}>
                                {riskLevel === 'CRITICAL' ? '🚨 CRITICAL' :
                                 riskLevel === 'HIGH' ? '⚠️ HIGH RISK' :
                                 '⚡ MODERATE'}
                            </span>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ChatBubble;
