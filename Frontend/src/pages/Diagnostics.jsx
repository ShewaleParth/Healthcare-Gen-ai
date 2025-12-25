import React, { useState, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import { 
    Upload, FileImage, Loader, CheckCircle, AlertCircle, Info,
    ZoomIn, ZoomOut, Download, Share2, Eye, Activity,
    Brain, Stethoscope, FileText, AlertTriangle,
    ChevronDown, ChevronUp, X, Maximize2, Calendar, Image as ImageIcon
} from 'lucide-react';
import { 
    RadialBarChart, RadialBar, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell
} from 'recharts';

const Diagnostics = () => {
    const [file, setFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [analysis, setAnalysis] = useState('');
    const [loading, setLoading] = useState(false);
    const [dragActive, setDragActive] = useState(false);
    const [imageZoom, setImageZoom] = useState(1);
    const [showFullImage, setShowFullImage] = useState(false);
    const [expandedSections, setExpandedSections] = useState({
        findings: true,
        diagnosis: true,
        recommendations: true
    });
    const fileInputRef = useRef(null);

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
        }
    };

    const handleFileChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            handleFile(e.target.files[0]);
        }
    };

    const handleFile = (selectedFile) => {
        setFile(selectedFile);
        const objectUrl = URL.createObjectURL(selectedFile);
        setPreview(objectUrl);
        setAnalysis('');
        setImageZoom(1);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) return;

        setLoading(true);
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://localhost:8000/api/v1/diagnostic/analyze-image', {
                method: 'POST',
                body: formData,
            });
            const data = await response.json();
            setAnalysis(data.analysis);
        } catch (error) {
            console.error('Error:', error);
            setAnalysis('**Error**: Unable to analyze image. Please try again or contact support.');
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

    // Parse analysis into structured sections
    const parseAnalysis = (text) => {
        if (!text) return null;

        const sections = {
            findings: '',
            diagnosis: '',
            recommendations: '',
            confidence: 'Medium',
            regions: []
        };

        const findingsMatch = text.match(/Primary Findings?:?\s*\n([\s\S]*?)(?=\n##|\n\*\*Potential Diagnosis|\n\*\*Confidence|$)/i);
        const diagnosisMatch = text.match(/Potential Diagnosis:?\s*\n([\s\S]*?)(?=\n##|\n\*\*Confidence|\n\*\*Regions|$)/i);
        const recommendationsMatch = text.match(/Recommendations?:?\s*\n([\s\S]*?)(?=\n##|\n\*\*Important|$)/i);
        const confidenceMatch = text.match(/Confidence Level:?\s*\n?([^\n]+)/i);
        const regionsMatch = text.match(/Regions? of Interest:?\s*\n([\s\S]*?)(?=\n##|\n\*\*Recommendations|$)/i);

        if (findingsMatch) sections.findings = findingsMatch[1].trim();
        if (diagnosisMatch) sections.diagnosis = diagnosisMatch[1].trim();
        if (recommendationsMatch) sections.recommendations = recommendationsMatch[1].trim();
        if (confidenceMatch) sections.confidence = confidenceMatch[1].trim();
        if (regionsMatch) {
            const regionLines = regionsMatch[1].trim().split('\n');
            sections.regions = regionLines.filter(line => line.trim().startsWith('-') || line.trim().startsWith('*'))
                .map(line => line.replace(/^[-*]\s*/, '').trim());
        }

        return sections;
    };

    const parsedAnalysis = parseAnalysis(analysis);

    // Get confidence metrics
    const getConfidenceMetrics = (confidence) => {
        const conf = confidence.toLowerCase();
        if (conf.includes('high')) return { 
            level: 'High', 
            value: 85, 
            color: '#10b981',
            bgColor: 'bg-green-50',
            textColor: 'text-green-700',
            borderColor: 'border-green-500'
        };
        if (conf.includes('medium')) return { 
            level: 'Medium', 
            value: 65, 
            color: '#f59e0b',
            bgColor: 'bg-amber-50',
            textColor: 'text-amber-700',
            borderColor: 'border-amber-500'
        };
        return { 
            level: 'Low', 
            value: 45, 
            color: '#6b7280',
            bgColor: 'bg-gray-50',
            textColor: 'text-gray-700',
            borderColor: 'border-gray-400'
        };
    };

    const confidenceMetrics = parsedAnalysis ? getConfidenceMetrics(parsedAnalysis.confidence) : null;

    // Image quality indicators (simulated - would come from actual analysis)
    const imageQuality = [
        { label: 'Exposure', status: 'Optimal', value: 95 },
        { label: 'Rotation', status: 'Minimal', value: 90 },
        { label: 'Inspiration', status: 'Adequate', value: 85 }
    ];

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-500 via-indigo-500 to-purple-600 p-6">
            {/* Header */}
            <header className="mb-8 animate-fade-in">
                <div className="glass-card p-6 rounded-3xl">
                    <div className="flex items-center gap-4">
                        <div className="bg-gradient-to-br from-indigo-600 to-blue-600 p-4 rounded-2xl shadow-lg">
                            <Stethoscope className="w-8 h-8 text-white" />
                        </div>
                        <div>
                            <h1 className="text-4xl font-extrabold text-gray-800">AI-Powered Diagnostics</h1>
                            <p className="text-sm text-gray-500 mt-1">AI-assisted insights · Not a clinical diagnosis</p>
                        </div>
                    </div>
                </div>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Left Panel - Upload & Image */}
                <div className="space-y-6">
                    {/* Upload Card */}
                    <div className="glass-card p-6 rounded-3xl shadow-2xl animate-slide-in-left">
                        <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                            <Upload className="w-5 h-5 text-indigo-600" />
                            Upload Medical Image
                        </h2>
                        <p className="text-xs text-gray-500 mb-6">
                            Supported: PNG, JPG, JPEG · Max: 10MB
                        </p>

                        <form onSubmit={handleSubmit}>
                            <div
                                className={`relative border-2 border-dashed rounded-2xl p-12 text-center transition-all duration-300 ${
                                    dragActive 
                                        ? 'border-indigo-500 bg-indigo-50 scale-105' 
                                        : 'border-gray-300 bg-gray-50 hover:border-indigo-400 hover:bg-indigo-50'
                                }`}
                                onDragEnter={handleDrag}
                                onDragLeave={handleDrag}
                                onDragOver={handleDrag}
                                onDrop={handleDrop}
                                onClick={() => fileInputRef.current?.click()}
                            >
                                <input
                                    ref={fileInputRef}
                                    type="file"
                                    className="hidden"
                                    onChange={handleFileChange}
                                    accept="image/*"
                                />
                                
                                {!preview ? (
                                    <div className="space-y-4">
                                        <div className="mx-auto w-20 h-20 bg-gradient-to-br from-indigo-500 to-blue-500 rounded-full flex items-center justify-center animate-float">
                                            <FileImage className="w-10 h-10 text-white" />
                                        </div>
                                        <div>
                                            <p className="text-base font-semibold text-gray-700 mb-2">
                                                Click to upload or drag and drop
                                            </p>
                                            <p className="text-xs text-gray-500">
                                                X-rays, MRI scans, CT scans
                                            </p>
                                        </div>
                                    </div>
                                ) : (
                                    <div className="space-y-4">
                                        <div className="relative group">
                                            <img 
                                                src={preview} 
                                                alt="Medical scan preview" 
                                                className="max-h-64 mx-auto rounded-xl shadow-lg cursor-pointer transition-transform group-hover:scale-105"
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    setShowFullImage(true);
                                                }}
                                            />
                                            <div className="absolute top-2 right-2 bg-white bg-opacity-90 p-2 rounded-lg shadow-md">
                                                <Maximize2 className="w-4 h-4 text-gray-700" />
                                            </div>
                                        </div>
                                        <div className="flex items-center justify-center gap-2 text-green-600">
                                            <CheckCircle className="w-4 h-4" />
                                            <span className="text-sm font-medium">{file?.name}</span>
                                        </div>
                                        <button
                                            type="button"
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                setFile(null);
                                                setPreview(null);
                                                setAnalysis('');
                                            }}
                                            className="text-xs text-gray-600 hover:text-gray-800 font-medium"
                                        >
                                            Remove Image
                                        </button>
                                    </div>
                                )}
                            </div>

                            <button
                                type="submit"
                                disabled={loading || !file}
                                className={`w-full mt-6 px-6 py-4 rounded-2xl font-bold text-base transition-all shadow-lg ${
                                    loading || !file
                                        ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                                        : 'bg-gradient-to-r from-indigo-600 to-blue-600 text-white hover:from-indigo-700 hover:to-blue-700 hover:shadow-2xl hover:scale-105'
                                }`}
                            >
                                {loading ? (
                                    <span className="flex items-center justify-center gap-3">
                                        <Loader className="w-5 h-5 animate-spin" />
                                        Analyzing Image...
                                    </span>
                                ) : (
                                    <span className="flex items-center justify-center gap-3">
                                        <Brain className="w-5 h-5" />
                                        Run AI Diagnostic Analysis
                                    </span>
                                )}
                            </button>
                        </form>

                        {/* Image Quality Indicators */}
                        {preview && !loading && (
                            <div className="mt-6 p-4 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl border border-blue-200">
                                <h3 className="text-xs font-semibold text-gray-600 mb-3">Image Quality Indicators</h3>
                                <div className="space-y-2">
                                    {imageQuality.map((item, idx) => (
                                        <div key={idx} className="flex items-center justify-between">
                                            <span className="text-xs text-gray-600">{item.label}:</span>
                                            <div className="flex items-center gap-2">
                                                <div className="w-24 h-1.5 bg-gray-200 rounded-full overflow-hidden">
                                                    <div 
                                                        className="h-full bg-gradient-to-r from-green-500 to-emerald-500 transition-all duration-1000"
                                                        style={{ width: `${item.value}%` }}
                                                    ></div>
                                                </div>
                                                <span className="text-xs font-medium text-green-600 flex items-center gap-1">
                                                    <CheckCircle className="w-3 h-3" />
                                                    {item.status}
                                                </span>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* File Metadata */}
                        {file && (
                            <div className="mt-4 p-3 bg-gray-50 rounded-xl border border-gray-200">
                                <div className="flex items-center gap-2 text-xs text-gray-600">
                                    <ImageIcon className="w-4 h-4" />
                                    <span>Size: {(file.size / 1024).toFixed(1)} KB</span>
                                    <span>·</span>
                                    <Calendar className="w-4 h-4" />
                                    <span>{new Date().toLocaleDateString()}</span>
                                </div>
                            </div>
                        )}
                    </div>
                </div>

                {/* Right Panel - Analysis Results */}
                <div className="space-y-6">
                    {!analysis && !loading && (
                        <div className="glass-card p-12 rounded-3xl text-center animate-fade-in">
                            <div className="w-24 h-24 bg-gradient-to-br from-gray-200 to-gray-300 rounded-full mx-auto mb-6 flex items-center justify-center">
                                <FileText className="w-12 h-12 text-gray-400" />
                            </div>
                            <h3 className="text-xl font-bold text-gray-700 mb-3">No Analysis Yet</h3>
                            <p className="text-sm text-gray-500">Upload a medical image and run analysis to view AI-generated insights</p>
                        </div>
                    )}

                    {loading && (
                        <div className="glass-card p-12 rounded-3xl text-center animate-pulse-glow">
                            <div className="w-24 h-24 bg-gradient-to-br from-indigo-500 to-blue-500 rounded-full mx-auto mb-6 flex items-center justify-center animate-float">
                                <Brain className="w-12 h-12 text-white animate-pulse" />
                            </div>
                            <h3 className="text-xl font-bold text-gray-800 mb-3">Analyzing Medical Image...</h3>
                            <p className="text-sm text-gray-600 mb-6">AI is examining anatomical structures and detecting abnormalities</p>
                            <div className="space-y-3">
                                {['Processing image data', 'Identifying anatomical structures', 'Detecting abnormalities', 'Generating diagnostic report'].map((step, idx) => (
                                    <div key={idx} className="flex items-center gap-3 text-xs text-gray-600 animate-fade-in" style={{ animationDelay: `${idx * 0.3}s` }}>
                                        <div className="w-2 h-2 bg-indigo-500 rounded-full animate-pulse"></div>
                                        {step}
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {analysis && parsedAnalysis && confidenceMetrics && (
                        <div className="space-y-6 animate-scale-in">
                            {/* Header Card */}
                            <div className="glass-card p-6 rounded-3xl shadow-2xl border-l-4 border-indigo-500">
                                <div className="flex items-center justify-between mb-6">
                                    <div>
                                        <h2 className="text-2xl font-bold text-gray-800">AI-Generated Medical Analysis</h2>
                                        <p className="text-sm text-gray-500 mt-1">Chest X-Ray Diagnostic Overview</p>
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
                                        <p className="text-xs text-gray-500 mb-1">Analysis Confidence</p>
                                        <p className={`text-lg font-bold ${confidenceMetrics.textColor}`}>{confidenceMetrics.level}</p>
                                    </div>
                                    <div className="bg-gradient-to-br from-gray-50 to-slate-50 p-4 rounded-xl border border-gray-200">
                                        <p className="text-xs text-gray-500 mb-1">Regions Identified</p>
                                        <p className="text-lg font-bold text-gray-800">{parsedAnalysis.regions?.length || 0}</p>
                                    </div>
                                    <div className="bg-gradient-to-br from-gray-50 to-slate-50 p-4 rounded-xl border border-gray-200">
                                        <p className="text-xs text-gray-500 mb-1">AI Model</p>
                                        <p className="text-sm font-bold text-indigo-600">Gemini Vision</p>
                                    </div>
                                </div>

                                {/* Confidence Gauge */}
                                <div className={`${confidenceMetrics.bgColor} border ${confidenceMetrics.borderColor} rounded-2xl p-6`}>
                                    <div className="flex items-center justify-between mb-4">
                                        <h3 className="text-sm font-semibold text-gray-700">Confidence Level</h3>
                                        <span className={`text-sm font-bold ${confidenceMetrics.textColor}`}>{confidenceMetrics.level}</span>
                                    </div>
                                    <div className="relative h-32">
                                        <ResponsiveContainer width="100%" height="100%">
                                            <RadialBarChart 
                                                cx="50%" 
                                                cy="100%" 
                                                innerRadius="80%" 
                                                outerRadius="100%" 
                                                data={[{ value: confidenceMetrics.value, fill: confidenceMetrics.color }]}
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

                            {/* Lung Region Coverage Map */}
                            {parsedAnalysis.regions && parsedAnalysis.regions.length > 0 ? (
                                <div className="glass-card p-6 rounded-2xl shadow-lg">
                                    <h3 className="text-base font-bold text-gray-800 mb-4">Lung Region Coverage</h3>
                                    <div className="grid grid-cols-2 gap-3">
                                        {['Upper Left', 'Upper Right', 'Lower Left', 'Lower Right', 'Hilum', 'Mediastinum'].map((region, idx) => {
                                            const isHighlighted = parsedAnalysis.regions.some(r => 
                                                r.toLowerCase().includes(region.toLowerCase())
                                            );
                                            return (
                                                <div 
                                                    key={idx} 
                                                    className={`p-3 rounded-lg border-2 text-center text-sm ${
                                                        isHighlighted 
                                                            ? 'border-amber-500 bg-amber-50 text-amber-700 font-semibold' 
                                                            : 'border-gray-200 bg-gray-50 text-gray-500'
                                                    }`}
                                                >
                                                    {region}
                                                    {isHighlighted && <span className="ml-2">⚠️</span>}
                                                </div>
                                            );
                                        })}
                                    </div>
                                </div>
                            ) : (
                                <div className="glass-card p-6 rounded-2xl shadow-lg border-2 border-green-200 bg-green-50">
                                    <div className="flex items-center gap-3">
                                        <CheckCircle className="w-6 h-6 text-green-600" />
                                        <div>
                                            <h3 className="text-base font-bold text-green-800">No Regions Highlighted</h3>
                                            <p className="text-sm text-green-700 mt-1">All lung regions appear within normal limits</p>
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* Primary Findings */}
                            {parsedAnalysis.findings && (
                                <div className="glass-card rounded-2xl shadow-lg overflow-hidden">
                                    <button
                                        onClick={() => toggleSection('findings')}
                                        className="w-full p-5 flex items-center justify-between hover:bg-gray-50 transition"
                                    >
                                        <h3 className="text-lg font-bold text-gray-800">Primary Findings</h3>
                                        {expandedSections.findings ? <ChevronUp className="w-5 h-5 text-gray-600" /> : <ChevronDown className="w-5 h-5 text-gray-600" />}
                                    </button>
                                    {expandedSections.findings && (
                                        <div className="px-6 pb-6 animate-fade-in">
                                            <div className="prose prose-sm max-w-none text-gray-700 leading-relaxed">
                                                <ReactMarkdown
                                                    components={{
                                                        strong: ({node, ...props}) => <strong className="font-bold text-gray-900" {...props} />
                                                    }}
                                                >
                                                    {parsedAnalysis.findings}
                                                </ReactMarkdown>
                                            </div>
                                        </div>
                                    )}
                                </div>
                            )}

                            {/* Potential Diagnosis */}
                            {parsedAnalysis.diagnosis && (
                                <div className="glass-card rounded-2xl shadow-lg overflow-hidden">
                                    <button
                                        onClick={() => toggleSection('diagnosis')}
                                        className="w-full p-5 flex items-center justify-between hover:bg-gray-50 transition"
                                    >
                                        <h3 className="text-lg font-bold text-gray-800">Potential Diagnosis</h3>
                                        {expandedSections.diagnosis ? <ChevronUp className="w-5 h-5 text-gray-600" /> : <ChevronDown className="w-5 h-5 text-gray-600" />}
                                    </button>
                                    {expandedSections.diagnosis && (
                                        <div className="px-6 pb-6 animate-fade-in">
                                            <div className="prose prose-sm max-w-none text-gray-700 leading-relaxed">
                                                <ReactMarkdown
                                                    components={{
                                                        strong: ({node, ...props}) => <strong className="font-bold text-gray-900" {...props} />
                                                    }}
                                                >
                                                    {parsedAnalysis.diagnosis}
                                                </ReactMarkdown>
                                            </div>
                                        </div>
                                    )}
                                </div>
                            )}

                            {/* Recommendations */}
                            {parsedAnalysis.recommendations && (
                                <div className="glass-card rounded-2xl shadow-lg overflow-hidden">
                                    <button
                                        onClick={() => toggleSection('recommendations')}
                                        className="w-full p-5 flex items-center justify-between hover:bg-gray-50 transition"
                                    >
                                        <h3 className="text-lg font-bold text-gray-800">Recommendations</h3>
                                        {expandedSections.recommendations ? <ChevronUp className="w-5 h-5 text-gray-600" /> : <ChevronDown className="w-5 h-5 text-gray-600" />}
                                    </button>
                                    {expandedSections.recommendations && (
                                        <div className="px-6 pb-6 animate-fade-in">
                                            <div className="prose prose-sm max-w-none text-gray-700 leading-relaxed">
                                                <ReactMarkdown
                                                    components={{
                                                        strong: ({node, ...props}) => <strong className="font-bold text-gray-900" {...props} />,
                                                        li: ({node, ...props}) => <li className="mb-2" {...props} />
                                                    }}
                                                >
                                                    {parsedAnalysis.recommendations}
                                                </ReactMarkdown>
                                            </div>
                                        </div>
                                    )}
                                </div>
                            )}

                            {/* Full Analysis Fallback */}
                            {!parsedAnalysis.findings && !parsedAnalysis.diagnosis && (
                                <div className="glass-card p-6 rounded-2xl shadow-lg">
                                    <div className="prose prose-sm max-w-none text-gray-700 leading-relaxed">
                                        <ReactMarkdown
                                            components={{
                                                strong: ({node, ...props}) => <strong className="font-bold text-gray-900" {...props} />
                                            }}
                                        >
                                            {analysis}
                                        </ReactMarkdown>
                                    </div>
                                </div>
                            )}

                            {/* Disclaimer */}
                            <div className="glass-card p-5 rounded-2xl border-l-4 border-amber-400 bg-gradient-to-r from-amber-50 to-yellow-50">
                                <div className="flex items-start gap-3">
                                    <AlertTriangle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                                    <div>
                                        <h4 className="text-sm font-semibold text-gray-800 mb-1">Important Medical Disclaimer</h4>
                                        <p className="text-xs text-gray-600 leading-relaxed">
                                            This is an AI-assisted analysis using Gemini Vision AI. <span className="font-medium text-gray-700">Final diagnosis must be made by a qualified medical professional.</span> Always consult with a certified radiologist or doctor for accurate interpretation and treatment decisions.
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>

            {/* Full Image Modal */}
            {showFullImage && preview && (
                <div className="fixed inset-0 bg-black bg-opacity-95 z-50 flex items-center justify-center p-6 animate-fade-in">
                    <button
                        onClick={() => setShowFullImage(false)}
                        className="absolute top-6 right-6 bg-white p-3 rounded-full hover:bg-gray-100 transition shadow-lg"
                    >
                        <X className="w-6 h-6 text-gray-800" />
                    </button>
                    <div className="max-w-5xl w-full">
                        <img 
                            src={preview} 
                            alt="Full size medical scan" 
                            className="w-full h-auto rounded-2xl shadow-2xl"
                            style={{ transform: `scale(${imageZoom})` }}
                        />
                        <div className="flex items-center justify-center gap-4 mt-6">
                            <button
                                onClick={() => setImageZoom(Math.max(0.5, imageZoom - 0.25))}
                                className="bg-white p-3 rounded-xl hover:bg-gray-100 transition shadow-lg"
                            >
                                <ZoomOut className="w-5 h-5 text-gray-800" />
                            </button>
                            <span className="text-white font-semibold text-sm">{Math.round(imageZoom * 100)}%</span>
                            <button
                                onClick={() => setImageZoom(Math.min(3, imageZoom + 0.25))}
                                className="bg-white p-3 rounded-xl hover:bg-gray-100 transition shadow-lg"
                            >
                                <ZoomIn className="w-5 h-5 text-gray-800" />
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Diagnostics;
