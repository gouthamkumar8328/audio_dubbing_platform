// Upload component
import React, { useRef } from 'react';

function Upload({ onFileUpload, uploadedFile }) {
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      // Validate file type
      const allowedTypes = ['audio/mpeg', 'audio/wav', 'video/mp4', 'video/quicktime'];
      const allowedExtensions = ['.mp3', '.wav', '.mp4', '.mov', '.avi'];
      
      const fileExtension = `.${file.name.split('.').pop().toLowerCase()}`;
      
      if (!allowedTypes.includes(file.type) && !allowedExtensions.includes(fileExtension)) {
        alert('Please upload a valid audio/video file (MP4, WAV, MP3, MOV, AVI)');
        return;
      }

      onFileUpload(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.currentTarget.classList.add('border-blue-500', 'bg-blue-500/10');
  };

  const handleDragLeave = (e) => {
    e.currentTarget.classList.remove('border-blue-500', 'bg-blue-500/10');
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.currentTarget.classList.remove('border-blue-500', 'bg-blue-500/10');
    
    const file = e.dataTransfer.files?.[0];
    if (file) {
      onFileUpload(file);
    }
  };

  return (
    <div>
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className="border-2 border-dashed border-slate-600 rounded-xl p-8 cursor-pointer transition-all duration-300 hover:border-blue-500 hover:bg-blue-500/5 bg-slate-700/50"
      >
        <div className="flex flex-col items-center gap-3">
          <svg className="w-12 h-12 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          <div className="text-center">
            <p className="text-white font-semibold">Drag & drop your file here</p>
            <p className="text-slate-400 text-sm">or click to browse (MP4, WAV, MP3)</p>
          </div>
        </div>

        <input
          ref={fileInputRef}
          type="file"
          onChange={handleFileChange}
          accept=".mp4,.wav,.mp3,.mov,.avi"
          className="hidden"
        />
      </div>

      {/* Uploaded File Display */}
      {uploadedFile && (
        <div className="mt-4 p-4 bg-green-500/20 border border-green-500/50 rounded-lg flex items-center gap-3">
          <svg className="w-5 h-5 text-green-400 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
          </svg>
          <div className="flex-1 min-w-0">
            <p className="text-green-400 font-semibold truncate">{uploadedFile.name}</p>
            <p className="text-green-300/70 text-sm">{(uploadedFile.size / 1024 / 1024).toFixed(2)} MB</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default Upload;