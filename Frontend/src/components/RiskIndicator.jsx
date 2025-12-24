import React from 'react';

const RiskIndicator = ({ level, showLabel = true }) => {
    const configs = {
        LOW: {
            color: 'bg-green-100 text-green-700 border-green-300',
            icon: '🟢',
            label: 'Low Risk',
            pulse: false
        },
        MODERATE: {
            color: 'bg-yellow-100 text-yellow-700 border-yellow-300',
            icon: '🟡',
            label: 'Moderate Risk',
            pulse: false
        },
        HIGH: {
            color: 'bg-orange-100 text-orange-700 border-orange-300',
            icon: '🟠',
            label: 'High Risk',
            pulse: true
        },
        CRITICAL: {
            color: 'bg-red-100 text-red-700 border-red-300',
            icon: '🔴',
            label: 'Critical - Emergency',
            pulse: true
        }
    };

    const config = configs[level] || configs.LOW;

    return (
        <div className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full border ${config.color} ${
            config.pulse ? 'animate-pulse-slow' : ''
        }`}>
            <span className="text-base">{config.icon}</span>
            {showLabel && (
                <span className="text-xs font-semibold uppercase tracking-wide">
                    {config.label}
                </span>
            )}
        </div>
    );
};

export default RiskIndicator;
