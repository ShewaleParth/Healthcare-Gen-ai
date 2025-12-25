import React, { useState, useEffect } from 'react';
import { Volume2, VolumeX, Pause, Play, Languages, Loader, RefreshCw } from 'lucide-react';

const MultilingualSpeech = ({ text, className = '', onLanguageChange = null }) => {
    const [language, setLanguage] = useState('en'); // Default: English
    const [isSpeaking, setIsSpeaking] = useState(false);
    const [isPaused, setIsPaused] = useState(false);
    const [voices, setVoices] = useState([]);
    const [selectedVoice, setSelectedVoice] = useState(null);

    // Language options
    const languages = [
        { code: 'en', name: 'English', flag: '🇮🇳', label: 'English' },
        { code: 'hi', name: 'Hindi', flag: '🇮🇳', label: 'हिंदी' },
        { code: 'mr', name: 'Marathi', flag: '🇮🇳', label: 'मराठी' }
    ];

    // Load available voices
    useEffect(() => {
        const loadVoices = () => {
            const availableVoices = window.speechSynthesis.getVoices();
            setVoices(availableVoices);
            
            // Try to find a voice for the selected language
            const langVoice = availableVoices.find(voice => 
                voice.lang.startsWith(language)
            );
            setSelectedVoice(langVoice || availableVoices[0]);
        };

        loadVoices();
        window.speechSynthesis.onvoiceschanged = loadVoices;

        return () => {
            window.speechSynthesis.cancel();
        };
    }, [language]);

    const speak = () => {
        if (!text) return;

        // Cancel any ongoing speech
        window.speechSynthesis.cancel();

        // Clean markdown from text
        const cleanText = text
            .replace(/#{1,6}\s/g, '') // Remove markdown headers
            .replace(/\*\*/g, '') // Remove bold
            .replace(/\*/g, '') // Remove italic
            .replace(/\[([^\]]+)\]\([^\)]+\)/g, '$1') // Remove links
            .replace(/`/g, '') // Remove code blocks
            .replace(/---/g, '') // Remove horizontal rules
            .replace(/>/g, '') // Remove blockquotes
            .trim();

        const utterance = new SpeechSynthesisUtterance(cleanText);
        utterance.lang = language === 'en' ? 'en-IN' : language === 'hi' ? 'hi-IN' : 'mr-IN';
        utterance.rate = 0.9; // Slightly slower for clarity
        utterance.pitch = 1.0;
        utterance.volume = 1.0;

        if (selectedVoice) {
            utterance.voice = selectedVoice;
        }

        utterance.onstart = () => {
            setIsSpeaking(true);
            setIsPaused(false);
        };

        utterance.onend = () => {
            setIsSpeaking(false);
            setIsPaused(false);
        };

        utterance.onerror = (event) => {
            console.error('Speech synthesis error:', event);
            setIsSpeaking(false);
            setIsPaused(false);
        };

        window.speechSynthesis.speak(utterance);
    };

    const pause = () => {
        if (window.speechSynthesis.speaking && !window.speechSynthesis.paused) {
            window.speechSynthesis.pause();
            setIsPaused(true);
        }
    };

    const resume = () => {
        if (window.speechSynthesis.paused) {
            window.speechSynthesis.resume();
            setIsPaused(false);
        }
    };

    const stop = () => {
        window.speechSynthesis.cancel();
        setIsSpeaking(false);
        setIsPaused(false);
    };

    const handleLanguageChange = (langCode) => {
        stop(); // Stop current speech when changing language
        setLanguage(langCode);
        
        // Notify parent component to regenerate report in new language
        if (onLanguageChange) {
            onLanguageChange(langCode);
        }
    };

    return (
        <div className={`glass-card p-4 rounded-2xl border border-indigo-200 ${className}`}>
            <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                    <Languages className="w-5 h-5 text-indigo-600" />
                    <h3 className="text-sm font-bold text-gray-800">Listen in Your Language</h3>
                </div>
                {isSpeaking && (
                    <div className="flex items-center gap-2 text-xs text-indigo-600">
                        <div className="w-2 h-2 bg-indigo-600 rounded-full animate-pulse"></div>
                        Speaking...
                    </div>
                )}
            </div>

            {/* Language Selector */}
            <div className="flex gap-2 mb-3">
                {languages.map((lang) => (
                    <button
                        key={lang.code}
                        onClick={() => handleLanguageChange(lang.code)}
                        className={`flex-1 px-3 py-2 rounded-xl text-xs font-semibold transition-all ${
                            language === lang.code
                                ? 'bg-gradient-to-r from-indigo-600 to-blue-600 text-white shadow-lg'
                                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                        }`}
                    >
                        <div className="flex items-center justify-center gap-1">
                            <span>{lang.flag}</span>
                            <span>{lang.label}</span>
                        </div>
                    </button>
                ))}
            </div>

            {onLanguageChange && (
                <p className="text-xs text-amber-600 mb-3 text-center bg-amber-50 p-2 rounded-lg border border-amber-200">
                    <RefreshCw className="w-3 h-3 inline mr-1" />
                    Changing language will regenerate the report
                </p>
            )}

            {/* Audio Controls */}
            <div className="flex gap-2">
                {!isSpeaking ? (
                    <button
                        onClick={speak}
                        disabled={!text}
                        className={`flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl font-semibold text-sm transition-all ${
                            text
                                ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white hover:from-emerald-700 hover:to-teal-700 shadow-lg hover:shadow-xl'
                                : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                        }`}
                    >
                        <Volume2 className="w-4 h-4" />
                        Play Audio
                    </button>
                ) : (
                    <>
                        {isPaused ? (
                            <button
                                onClick={resume}
                                className="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl font-semibold text-sm hover:from-blue-700 hover:to-indigo-700 transition-all shadow-lg"
                            >
                                <Play className="w-4 h-4" />
                                Resume
                            </button>
                        ) : (
                            <button
                                onClick={pause}
                                className="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 bg-gradient-to-r from-amber-600 to-orange-600 text-white rounded-xl font-semibold text-sm hover:from-amber-700 hover:to-orange-700 transition-all shadow-lg"
                            >
                                <Pause className="w-4 h-4" />
                                Pause
                            </button>
                        )}
                        <button
                            onClick={stop}
                            className="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 bg-gradient-to-r from-red-600 to-pink-600 text-white rounded-xl font-semibold text-sm hover:from-red-700 hover:to-pink-700 transition-all shadow-lg"
                        >
                            <VolumeX className="w-4 h-4" />
                            Stop
                        </button>
                    </>
                )}
            </div>

            {/* Info Text */}
            <p className="text-xs text-gray-500 mt-3 text-center">
                {language === 'hi' && 'अपनी भाषा में सुनें'}
                {language === 'mr' && 'तुमच्या भाषेत ऐका'}
                {language === 'en' && 'Listen to the analysis in your preferred language'}
            </p>
        </div>
    );
};

export default MultilingualSpeech;
