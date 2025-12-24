import React from 'react';

const TypingIndicator = () => {
    return (
        <div className="flex justify-start mb-4">
            <div className="flex items-start gap-2.5">
                {/* AI Avatar */}
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-indigo-600 flex items-center justify-center text-sm">
                    🤖
                </div>

                {/* Typing Animation */}
                <div className="bg-gray-100 border border-gray-200 rounded-2xl rounded-tl-none px-4 py-3 shadow-sm">
                    <div className="flex items-center gap-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default TypingIndicator;
