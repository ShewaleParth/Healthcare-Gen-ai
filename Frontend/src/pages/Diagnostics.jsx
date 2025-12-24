import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';

const Diagnostics = () => {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [analysis, setAnalysis] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      const objectUrl = URL.createObjectURL(selectedFile);
      setPreview(objectUrl);
      setAnalysis(''); // Clear previous analysis
    }
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
      setAnalysis('Error analyzing image. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold mb-8 text-gray-800">🩻 AI-Powered Diagnostics</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Upload Section */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 h-fit">
          <h2 className="text-xl font-semibold mb-4 text-gray-700">Upload Medical Image</h2>
          <form onSubmit={handleSubmit} className="mb-6">
            <div className="mb-6">
              <label className="block text-gray-600 text-sm font-medium mb-2">
                Supported formats: PNG, JPG, JPEG
              </label>
              <div className="flex items-center justify-center w-full">
                <label htmlFor="dropzone-file" className="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100">
                  <div className="flex flex-col items-center justify-center pt-5 pb-6">
                    <svg aria-hidden="true" className="w-10 h-10 mb-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
                    <p className="mb-2 text-sm text-gray-500"><span className="font-semibold">Click to upload</span> or drag and drop</p>
                    <p className="text-xs text-gray-500">SVG, PNG, JPG or GIF (MAX. 800x400px)</p>
                  </div>
                  <input id="dropzone-file" type="file" className="hidden" onChange={handleFileChange} accept="image/*" />
                </label>
              </div>
              {file && <p className="mt-2 text-sm text-green-600 font-medium">Selected: {file.name}</p>}
            </div>

            {preview && (
              <div className="mb-6 relative rounded-lg overflow-hidden border border-gray-200">
                <img src={preview} alt="Preview" className="w-full object-cover" />
              </div>
            )}

            <button
              type="submit"
              disabled={loading || !file}
              className="w-full bg-blue-600 text-white px-4 py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-300 transition shadow-md"
            >
              {loading ? 'Analyzing Image...' : 'Run Diagnostics Analysis'}
            </button>
          </form>
        </div>

        {/* Analysis Result */}
        {analysis && (
          <div className="bg-white p-8 rounded-2xl shadow-lg border-t-4 border-blue-500 animate-fade-in h-fit">
            <div className="flex items-center gap-3 mb-6">
              <div className="bg-blue-100 p-2 rounded-full text-blue-600">
                🩺
              </div>
              <h2 className="text-2xl font-bold text-gray-800">Diagnostic Report</h2>
            </div>
            <div className="prose prose-blue max-w-none text-gray-700">
              <ReactMarkdown>{analysis}</ReactMarkdown>
            </div>
            <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg text-sm text-yellow-800">
              <strong>Disclaimer:</strong> AI-generated analysis. Always verify with a certified radiologist/doctor.
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Diagnostics;
