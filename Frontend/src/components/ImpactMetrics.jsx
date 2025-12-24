import React, { useState, useEffect } from 'react';

const ImpactMetrics = () => {
    const [animated, setAnimated] = useState(false);

    useEffect(() => {
        // Trigger animation on mount
        setTimeout(() => setAnimated(true), 100);
    }, []);

    const metrics = [
        {
            icon: '🏥',
            title: 'Patients Analyzed',
            value: 1247,
            suffix: '',
            trend: '+12%',
            trendUp: true,
            color: 'from-blue-500 to-blue-600'
        },
        {
            icon: '⚡',
            title: 'Avg Response Time',
            value: 2.3,
            suffix: 's',
            trend: '-25%',
            trendUp: true,
            subtitle: 'vs 2hr specialist wait',
            color: 'from-purple-500 to-purple-600'
        },
        {
            icon: '🚨',
            title: 'Crisis Interventions',
            value: 3,
            suffix: '',
            trend: 'Today',
            trendUp: false,
            subtitle: 'High-risk escalated',
            color: 'from-red-500 to-red-600'
        },
        {
            icon: '🎯',
            title: 'Diagnostic Accuracy',
            value: 94.2,
            suffix: '%',
            trend: '+3%',
            trendUp: true,
            color: 'from-green-500 to-green-600'
        },
        {
            icon: '📈',
            title: 'Efficiency Gain',
            value: 40,
            suffix: '%',
            trend: 'Wait time ↓',
            trendUp: true,
            subtitle: 'Reduced wait times',
            color: 'from-indigo-500 to-indigo-600'
        },
        {
            icon: '💰',
            title: 'Cost Savings',
            value: 2.5,
            suffix: 'L',
            trend: 'This month',
            trendUp: false,
            subtitle: 'Unnecessary tests avoided',
            color: 'from-amber-500 to-amber-600'
        }
    ];

    const AnimatedCounter = ({ end, duration = 2000, suffix = '' }) => {
        const [count, setCount] = useState(0);

        useEffect(() => {
            if (!animated) return;

            let startTime;
            const step = (timestamp) => {
                if (!startTime) startTime = timestamp;
                const progress = Math.min((timestamp - startTime) / duration, 1);
                setCount(progress * end);
                if (progress < 1) {
                    requestAnimationFrame(step);
                }
            };
            requestAnimationFrame(step);
        }, [animated, end, duration]);

        return (
            <span>
                {count.toFixed(suffix === '%' || suffix === 's' ? 1 : 0)}
                {suffix}
            </span>
        );
    };

    return (
        <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
                <div>
                    <h2 className="text-2xl font-bold text-gray-800">System Impact Metrics</h2>
                    <p className="text-sm text-gray-500 mt-1">Real-time performance and effectiveness indicators</p>
                </div>
                <div className="flex items-center gap-2 text-green-600 text-sm font-semibold">
                    <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                    Live Data
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {metrics.map((metric, index) => (
                    <div
                        key={index}
                        className="bg-white rounded-xl p-5 shadow-sm border border-gray-100 hover:shadow-md transition-all duration-300 hover:-translate-y-1"
                        style={{
                            animation: animated ? `slideInUp 0.5s ease-out ${index * 0.1}s both` : 'none'
                        }}
                    >
                        <div className="flex items-start justify-between mb-3">
                            <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${metric.color} flex items-center justify-center text-2xl shadow-sm`}>
                                {metric.icon}
                            </div>
                            {metric.trendUp !== undefined && (
                                <span className={`text-xs font-semibold px-2 py-1 rounded-full ${
                                    metric.trendUp 
                                        ? 'bg-green-100 text-green-700' 
                                        : 'bg-gray-100 text-gray-600'
                                }`}>
                                    {metric.trend}
                                </span>
                            )}
                        </div>

                        <div className="mb-1">
                            <div className="text-3xl font-bold text-gray-800 mb-1">
                                {animated ? (
                                    <AnimatedCounter end={metric.value} suffix={metric.suffix} />
                                ) : (
                                    `${metric.value}${metric.suffix}`
                                )}
                            </div>
                            <div className="text-sm font-medium text-gray-600">{metric.title}</div>
                            {metric.subtitle && (
                                <div className="text-xs text-gray-400 mt-1">{metric.subtitle}</div>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ImpactMetrics;
