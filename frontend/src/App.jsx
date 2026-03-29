import React, { useState, useEffect } from 'react';
import './App.css';
import Upload from './components/Upload';
import Player from './components/Player';
import LanguageSelector from './components/LanguageSelector';
import StatusLogs from './components/StatusLogs';
import PlatformInfo from './components/PlatformInfo';

function App() {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [selectedLanguage, setSelectedLanguage] = useState('hindi');
  const [isProcessing, setIsProcessing] = useState(false);
  const [outputFile, setOutputFile] = useState(null);
  const [statusLogs, setStatusLogs] = useState([]);
  const [error, setError] = useState(null);
  const [showInfo, setShowInfo] = useState(false);

  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => setError(null), 5000);
      return () => clearTimeout(timer);
    }
  }, [error]);

  const handleFileUpload = (file) => {
    setUploadedFile(file);
    setOutputFile(null);
    setStatusLogs([]);
    setError(null);
  };

  const handleProcess = async () => {
    if (!uploadedFile) {
      setError('Please upload a file first');
      return;
    }

    setIsProcessing(true);
    setStatusLogs([]);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', uploadedFile);
      formData.append('target_language', selectedLanguage);

      addLog(' Starting AI Dubbing Pipeline...');
      addLog(`Input: ${uploadedFile.name}`);
      addLog(`Target Language: ${selectedLanguage.toUpperCase()}`);
      
      const steps = [
        '[1/5] Speech Segmentation & Diarization',
        '[2/5] Transcription & Translation (Per Segment)',
        '[3/5] Voice Synthesis & Audio Mixing',
        '[4/5] Timeline Assembly & Alignment',
        '[5/5] Final Verification',
      ];

      for (const step of steps) {
        addLog(step);
        await new Promise((resolve) => setTimeout(resolve, 800));
      }

      const response = await fetch('http://localhost:8000/dub', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Processing failed');
      }

      const data = await response.json();

      setOutputFile({
        filename: data.output_file,
        downloadUrl: `http://localhost:8000${data.download_url}`,
        features: data.features,
      });

      addLog('Dubbing completed successfully!');
      addLog('Features used:');
      Object.entries(data.features).forEach(([key, value]) => {
        addLog(`  ✓ ${key.replace(/_/g, ' ')}: ${value}`);
      });
    } catch (err) {
      setError(err.message || 'An error occurred during processing');
      addLog(`Error: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  const addLog = (message) => {
    setStatusLogs((prev) => [...prev, `${new Date().toLocaleTimeString()} - ${message}`]);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-4">
      <div className="w-full max-w-4xl">
        {/* Header with Info Button */}
        <div className="text-center mb-8 flex items-center justify-between">
          <div className="flex-1">
            <h1 className="text-5xl font-bold text-white mb-2">🎬 AI Audio Dubbing</h1>
            <p className="text-slate-400 text-lg">Professional Multi-Speaker Dubbing Platform v2.0</p>
          </div>
          <button
            onClick={() => setShowInfo(!showInfo)}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-semibold transition"
          >
            ℹ️ Platform Info
          </button>
        </div>

        {/* Platform Info Modal */}
        {showInfo && <PlatformInfo onClose={() => setShowInfo(false)} />}

        {/* Main Card */}
        <div className="bg-slate-800 rounded-2xl shadow-2xl p-8 border border-slate-700">
          {error && (
            <div className="mb-6 p-4 bg-red-500/20 border border-red-500/50 rounded-lg text-red-400 text-sm">
              ⚠️ {error}
            </div>
          )}

          <div className="mb-8">
            <h2 className="text-xl font-semibold text-white mb-4">1. Upload Media</h2>
            <Upload onFileUpload={handleFileUpload} uploadedFile={uploadedFile} />
          </div>

          <div className="mb-8">
            <h2 className="text-xl font-semibold text-white mb-4">2. Select Target Language</h2>
            <LanguageSelector
              selectedLanguage={selectedLanguage}
              onLanguageChange={setSelectedLanguage}
              disabled={isProcessing}
            />
          </div>

          <div className="mb-8">
            <button
              onClick={handleProcess}
              disabled={isProcessing || !uploadedFile}
              className={`w-full py-3 px-6 rounded-lg font-semibold text-lg transition-all duration-300 flex items-center justify-center gap-2 ${
                isProcessing || !uploadedFile
                  ? 'bg-slate-600 text-slate-400 cursor-not-allowed'
                  : 'bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:shadow-lg hover:shadow-blue-500/50 active:scale-95'
              }`}
            >
              {isProcessing ? (
                <>
                  <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" fill="none" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Processing Pipeline...
                </>
              ) : (
                <> Start AI Dubbing</>
              )}
            </button>
          </div>

          {statusLogs.length > 0 && (
            <div className="mb-8">
              <h2 className="text-xl font-semibold text-white mb-4">3. Processing Pipeline Status</h2>
              <StatusLogs logs={statusLogs} />
            </div>
          )}

          {outputFile && (
            <div className="mb-8">
              <h2 className="text-xl font-semibold text-white mb-4">4. Download Dubbed Audio</h2>
              <Player outputFile={outputFile} />
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-slate-500 text-sm">
          <p>Multi-Speaker | Whisper ASR |  Translation |  Voice Synthesis |  Time Alignment</p>
          <p className="mt-2 text-xs">Powered by FastAPI + React | Modular & Scalable Architecture</p>
        </div>
      </div>
    </div>
  );
}

export default App;