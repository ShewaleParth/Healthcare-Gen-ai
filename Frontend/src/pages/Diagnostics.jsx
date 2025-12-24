import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import toast, { Toaster } from 'react-hot-toast';
import sampleCases from '../../../Dataset/sample_cases.json';

const Diagnostics = () => {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [analysis, setAnalysis] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedCase, setSelectedCase] = useState('');
  const [heatmaps, setHeatmaps] = useState([]);
  const [mlUsed, setMlUsed] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      const objectUrl = URL.createObjectURL(selectedFile);
      setPreview(objectUrl);
      setAnalysis('');
      setSelectedCase('');
      setHeatmaps([]);
      setMlUsed(false);
    }
  };

  const loadDemoCase = (caseData) => {
    setSelectedCase(caseData.id);
    setPreview(caseData.image_url);
    setAnalysis('');
    setFile(null);
    setHeatmaps([]);
    setMlUsed(false);
    toast.success(`Loaded demo case: ${caseData.title}`, { icon: '📋' });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file && !preview) return;

    setLoading(true);
    
    try {
      if (selectedCase) {
        const demoCase = sampleCases.diagnostic_cases.find(c => c.id === selectedCase);
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        const simulatedAnalysis = `
## 🔬 Medical Image Analysis

### Case: ${demoCase.title}

**Patient Information:**
${demoCase.description}

### Primary Findings:
${demoCase.expected_findings}

### Confidence Level: ${demoCase.confidence}

### Clinical Recommendations:
- Correlate with clinical symptoms and patient history
- Consider follow-up imaging if symptoms persist
- Recommend consultation with specialist for treatment planning

---
**Analysis Method**: Demo Mode
**Disclaimer**: This is an AI-assisted analysis. Final diagnosis must be made by a qualified medical professional.
        `;
        setAnalysis(simulatedAnalysis);
        setMlUsed(false);
        toast.success('Analysis complete!', { icon: '✅' });
      } else {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('http://localhost:8000/api/v1/diagnostic/analyze-image', {
          method: 'POST',
          body: formData,
        });
        
        if (!response.ok) throw new Error('Analysis failed');
        
        const data = await response.json();
        setAnalysis(data.analysis);
        setMlUsed(data.ml_used || false);
        setHeatmaps(data.heatmaps || []);
        
        if (data.ml_used) {
          toast.success('ML Analysis complete with Grad-CAM!', { icon: '🔬' });
        } else {
          toast.success('Analysis complete!', { icon: '✅' });
        }
      }
    } catch (error) {
      console.error('Error:', error);
      setAnalysis('Error analyzing image. Please try again.');
      toast.error('Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 bg-medical-gradient min-h-screen bg-pattern-dots animate-fadeIn">
      <Toaster position="top-right" />
      
      <div className="mb-8 animate-slideInLeft">
        <h1 className="text-4xl font-bold text-gray-800 flex items-center gap-3">
          <span className="animate-gentle-pulse">🩻</span>
          <span className="bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent">
            AI-Powered Diagnostics
          </span>
        </h1>
        <p className="text-gray-500 mt-2 ml-14 animate-fadeIn delay-200">Upload medical images for instant AI-powered analysis</p>
        <div className="absolute mt-1 ml-14 h-1 w-64 bg-gradient-to-r from-purple-500 via-indigo-500 to-blue-500 rounded-full animate-gradient"></div>
      </div>

      <div className="mb-6 glass p-4 rounded-xl shadow-soft border border-white/20 animate-fadeInScale">
        <h3 className="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
          <span className="animate-breathe">⚡</span>
          Quick Demo Cases
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {sampleCases.diagnostic_cases.map((demoCase, index) => (
            <button
              key={demoCase.id}
              onClick={() => loadDemoCase(demoCase)}
              className={`text-left p-4 rounded-xl border-2 transition-all duration-300 hover:shadow-soft-lg animate-fadeInScale hover:scale-105 transform ${
                selectedCase === demoCase.id
                  ? 'border-purple-500 bg-gradient-to-br from-purple-50 to-indigo-50 shadow-soft-lg'
                  : 'border-gray-200 hover:border-purple-300 bg-white/50'
              }`}
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="flex items-center gap-2 mb-2">
                {selectedCase === demoCase.id && (
                  <span className="text-purple-600 animate-gentle-pulse">✓</span>
                )}
                <div className="font-semibold text-sm text-gray-800">{demoCase.title}</div>
              </div>
              <div className="text-xs text-gray-500">{demoCase.description}</div>
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="glass p-6 rounded-2xl shadow-soft-lg border border-white/20 h-fit animate-slideInLeft hover:shadow-soft-lg transition-all duration-500">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl flex items-center justify-center animate-gentle-pulse">
              <span className="text-white text-xl">📤</span>
            </div>
            <h2 className="text-xl font-semibold text-gray-700">Upload Medical Image</h2>
          </div>
          <form onSubmit={handleSubmit} className="mb-6">
            <div className="mb-6">
              <label className="block text-gray-600 text-sm font-medium mb-2">
                Supported formats: PNG, JPG, JPEG
              </label>
              <div className="flex items-center justify-center w-full">
                <label htmlFor="dropzone-file" className={`group flex flex-col items-center justify-center w-full h-64 border-2 border-dashed rounded-xl cursor-pointer transition-all duration-300 hover:scale-[1.02] transform ${
                  preview ? 'border-purple-400 bg-purple-50/50' : 'border-gray-300 bg-gray-50/50 hover:bg-purple-50/30 hover:border-purple-300'
                }`}>
                  <div className="flex flex-col items-center justify-center pt-5 pb-6">
                    <svg aria-hidden="true" className="w-12 h-12 mb-3 text-gray-400 group-hover:text-purple-500 transition-colors animate-float" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
                    <p className="mb-2 text-sm text-gray-500"><span className="font-semibold">Click to upload</span> or drag and drop</p>
                    <p className="text-xs text-gray-500">Medical images (X-ray, MRI, CT scan, etc.)</p>
                  </div>
                  <input id="dropzone-file" type="file" className="hidden" onChange={handleFileChange} accept="image/*" />
                </label>
              </div>
              {file && <p className="mt-2 text-sm text-green-600 font-medium animate-fadeIn flex items-center gap-2"><span className="animate-gentle-pulse">✓</span> Selected: {file.name}</p>}
              {selectedCase && <p className="mt-2 text-sm text-purple-600 font-medium animate-fadeIn flex items-center gap-2"><span className="animate-gentle-pulse">✓</span> Demo case loaded</p>}
            </div>

            {preview && (
              <div className="mb-6 relative rounded-xl overflow-hidden border-2 border-purple-200 shadow-soft-lg animate-fadeInScale">
                <img src={preview} alt="Preview" className="w-full object-cover max-h-96" />
                <div className="absolute top-2 right-2 bg-white/90 backdrop-blur-sm px-3 py-1 rounded-full text-xs font-semibold text-purple-600 shadow-soft animate-gentle-pulse">
                  Ready for Analysis
                </div>
              </div>
            )}

            <button
              type="submit"
              disabled={loading || (!file && !preview)}
              className="w-full bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white px-4 py-4 rounded-xl font-semibold disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-soft hover:shadow-soft-lg flex items-center justify-center gap-2 group hover:scale-105 transform"
            >
              {loading ? (
                <>
                  <span className="animate-spin text-xl">⚙️</span>
                  <span className="animate-pulse">Analyzing Image...</span>
                </>
              ) : (
                <>
                  <span className="group-hover:animate-gentle-pulse text-xl">🔬</span>
                  Run Diagnostic Analysis
                </>
              )}
            </button>
          </form>
        </div>

        {analysis && (
          <div className="glass p-8 rounded-2xl shadow-soft-lg border-t-4 border-purple-500 h-fit animate-slideInRight hover:shadow-soft-lg transition-all duration-500">
            <div className="flex items-center gap-3 mb-6 pb-4 border-b border-gray-100">
              <div className="bg-gradient-to-br from-purple-500 to-indigo-600 p-3 rounded-xl text-white text-2xl animate-gentle-pulse shadow-soft">
                🩺
              </div>
              <div>
                <h2 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent">
                  Diagnostic Report
                </h2>
                <p className="text-sm text-gray-500 mt-1">
                  {mlUsed ? '🔬 ML-Powered Analysis with Explainability' : '🤖 AI-Powered Medical Image Analysis'}
                </p>
              </div>
            </div>

            {mlUsed && heatmaps.length > 0 && (
              <div className="mb-6 p-4 bg-gradient-to-br from-purple-50 to-indigo-50 rounded-xl border border-purple-200 animate-fadeInScale">
                <h3 className="text-lg font-semibold text-purple-800 mb-3 flex items-center gap-2">
                  <span className="animate-gentle-pulse">🎯</span>
                  Grad-CAM Visual Explainability
                </h3>
                <p className="text-sm text-purple-700 mb-4">
                  The heatmap below shows which regions of the X-ray influenced the AI's decision. 
                  <span className="font-semibold"> Red = High importance, Blue = Low importance</span>
                </p>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {heatmaps.slice(0, 3).map((heatmapPath, index) => {
                    const filename = heatmapPath.split('/').pop() || heatmapPath.split('\\').pop();
                    const label = filename.includes('heatmap') ? 'Heatmap' : 
                                 filename.includes('overlay') ? 'Overlay' : 'Combined';
                    return (
                      <div key={index} className="relative group">
                        <div className="absolute top-2 left-2 bg-white/90 backdrop-blur-sm px-2 py-1 rounded-lg text-xs font-semibold text-purple-600 shadow-soft z-10">
                          {label}
                        </div>
                        <img 
                          src={`http://localhost:8000/api/v1/diagnostic/heatmap/${filename}`}
                          alt={label}
                          className="w-full rounded-lg shadow-soft hover:shadow-soft-lg transition-all duration-300 hover:scale-105 transform cursor-pointer"
                          onClick={() => window.open(`http://localhost:8000/api/v1/diagnostic/heatmap/${filename}`, '_blank')}
                        />
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            <div className="prose prose-purple max-w-none text-gray-700 animate-fadeIn delay-200">
              <ReactMarkdown>{analysis}</ReactMarkdown>
            </div>
            <div className="mt-6 p-4 bg-gradient-to-r from-yellow-50 to-orange-50 border-l-4 border-yellow-400 rounded-xl text-sm animate-fadeInScale delay-300">
              <div className="flex items-center gap-2 text-yellow-800">
                <span className="text-xl animate-breathe">⚠️</span>
                <strong>Medical Disclaimer:</strong>
              </div>
              <p className="text-yellow-700 mt-1">
                This is an AI-assisted analysis for educational purposes. Always verify findings with a certified radiologist or medical professional before making clinical decisions.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Diagnostics;
