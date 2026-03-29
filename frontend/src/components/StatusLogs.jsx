// Status Logs
import React, { useEffect, useRef } from 'react';

function StatusLogs({ logs }) {
  const logsEndRef = useRef(null);

  // Auto-scroll to bottom
  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  return (
    <div className="bg-slate-700/50 border border-slate-600 rounded-lg p-4 max-h-48 overflow-y-auto">
      <div className="font-mono text-sm space-y-2">
        {logs.map((log, index) => (
          <div key={index} className="text-slate-300">
            <span className="text-slate-500">{log.split(' - ')[0]}</span>
            <span className="text-slate-400"> → </span>
            <span className="text-blue-300">{log.split(' - ')[1]}</span>
          </div>
        ))}
        <div ref={logsEndRef} />
      </div>
    </div>
  );
}

export default StatusLogs;