import React from 'react';

function PlatformInfo({ onClose }) {
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div className="bg-slate-800 rounded-2xl p-8 max-w-2xl max-h-96 overflow-y-auto border border-slate-700">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-white">Platform Capabilities</h2>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white text-2xl"
          >
            ✕
          </button>
        </div>

        <div className="space-y-4 text-slate-300">
          <div>
            <h3 className="text-lg font-semibold text-blue-400 mb-2">🎤 Multi-Speaker Support</h3>
            <p className="text-sm">Automatic speaker diarization with segment-level processing for multiple speakers</p>
          </div>

          <div>
            <h3 className="text-lg font-semibold text-blue-400 mb-2">🎙️ Advanced Transcription</h3>
            <p className="text-sm">OpenAI Whisper ASR with speaker-specific segmentation</p>
          </div>

          <div>
            <h3 className="text-lg font-semibold text-blue-400 mb-2">🌐 Accurate Translation</h3>
            <p className="text-sm">Multi-language translation for 6+ languages with context preservation</p>
          </div>

          <div>
            <h3 className="text-lg font-semibold text-blue-400 mb-2">🔊 Natural Voice Synthesis</h3>
            <p className="text-sm">High-quality TTS with speaker-specific voice generation</p>
          </div>

          <div>
            <h3 className="text-lg font-semibold text-blue-400 mb-2">📍 Time Synchronization</h3>
            <p className="text-sm">Segment-level alignment ensuring dubbed audio matches original timing</p>
          </div>

          <div>
            <h3 className="text-lg font-semibold text-blue-400 mb-2">📦 Modular Architecture</h3>
            <p className="text-sm">Scalable, maintainable design with independent processing modules</p>
          </div>
        </div>

        <button
          onClick={onClose}
          className="mt-6 w-full py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold transition"
        >
          Close
        </button>
      </div>
    </div>
  );
}

export default PlatformInfo;