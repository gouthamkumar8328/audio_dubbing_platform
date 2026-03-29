// Player component
import React from 'react';

function Player({ outputFile }) {
  return (
    <div className="space-y-4">
      {/* Audio Player */}
      <div className="bg-slate-700/50 border border-slate-600 rounded-lg p-4">
        <p className="text-slate-400 text-sm mb-3">🎵 Dubbed Audio</p>
        <audio
          controls
          className="w-full rounded-lg"
          src={outputFile.downloadUrl}
          style={{
            filter: 'brightness(0.9)',
          }}
        >
          Your browser does not support the audio element.
        </audio>
      </div>

      {/* Download Button */}
      <a
        href={outputFile.downloadUrl}
        download={outputFile.filename}
        className="w-full py-3 px-6 rounded-lg font-semibold text-lg bg-green-600 text-white hover:bg-green-700 active:scale-95 transition-all duration-300 flex items-center justify-center gap-2"
      >
        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd" />
        </svg>
        Download Dubbed Audio
      </a>

      {/* File Info */}
      <div className="text-center text-slate-400 text-sm">
        <p> File: <span className="text-slate-300">{outputFile.filename}</span></p>
      </div>
    </div>
  );
}

export default Player;