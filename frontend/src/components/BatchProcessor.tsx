import React, { useState } from 'react';
import { UploadCloud, CheckCircle2, AlertTriangle, Heart, Layers, Play } from 'lucide-react';
import { AnalyzeResult } from '../types';

interface BatchProcessorProps {
  onBatchCompleted: () => void;
}

export const BatchProcessor: React.FC<BatchProcessorProps> = ({ onBatchCompleted }) => {
  const [bulkText, setBulkText] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<AnalyzeResult[]>([]);
  const [error, setError] = useState<string | null>(null);

  const sampleBatch = [
    "I have a high fever and doctor advised two days of strict bed rest.",
    "My fish ate my car keys so I cannot commute to work.",
    "I am mourning the loss of a close friend and need time to grieve.",
    "I accidentally locked myself inside the bathroom and it will take all day.",
    "I am taking a mental health day to prioritize emotional well-being.",
  ].join('\n');

  const handleProcessBatch = async () => {
    const lines = bulkText
      .split('\n')
      .map((l) => l.trim())
      .filter((l) => l.length > 0);

    if (lines.length === 0) {
      setError('Please provide at least one leave application (one per line).');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const res = await fetch('/api/v1/batch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ applications: lines }),
      });

      if (!res.ok) {
        throw new Error('Batch processing failed on backend.');
      }

      const data = await res.json();
      setResults(data.results || []);
      onBatchCompleted();
    } catch (err: any) {
      setError(err.message || 'Failed to process batch.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-panel" style={{ padding: '28px', marginBottom: '36px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '18px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Layers size={22} color="#06b6d4" />
          <div>
            <h2 style={{ fontSize: '1.15rem', fontWeight: 700 }}>Batch Multi-Application Processor</h2>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              Evaluate up to 100 employee leave applications concurrently in an atomic transaction.
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={() => setBulkText(sampleBatch)}
          className="btn-ghost"
          style={{ fontSize: '0.8rem' }}
        >
          Load 5 Sample Applications
        </button>
      </div>

      <textarea
        value={bulkText}
        onChange={(e) => setBulkText(e.target.value)}
        placeholder="Enter one leave justification per line...&#10;Line 1: High fever and hospital visit...&#10;Line 2: My pet ate my laptop charger...&#10;Line 3: Emotional burnout recovery..."
        rows={6}
        style={{
          width: '100%',
          background: 'rgba(0, 0, 0, 0.25)',
          border: '1px solid var(--border-color)',
          borderRadius: '12px',
          color: 'var(--text-primary)',
          padding: '16px',
          fontSize: '0.9rem',
          fontFamily: 'inherit',
          outline: 'none',
          marginBottom: '16px',
        }}
      />

      {error && (
        <div style={{ padding: '10px 14px', borderRadius: '8px', background: 'rgba(244, 63, 94, 0.15)', border: '1px solid rgba(244, 63, 94, 0.3)', color: '#fb7185', fontSize: '0.85rem', marginBottom: '16px' }}>
          {error}
        </div>
      )}

      <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '24px' }}>
        <button
          type="button"
          onClick={handleProcessBatch}
          disabled={loading || !bulkText.trim()}
          className="btn-primary"
        >
          {loading ? (
            <span>Processing In Batch...</span>
          ) : (
            <>
              <Play size={16} />
              <span>Execute Batch Analysis</span>
            </>
          )}
        </button>
      </div>

      {results.length > 0 && (
        <div>
          <div style={{ fontSize: '0.9rem', fontWeight: 700, marginBottom: '12px', color: 'var(--text-secondary)' }}>
            Batch Results ({results.length} processed)
          </div>
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-color)', textAlign: 'left', color: 'var(--text-muted)' }}>
                  <th style={{ padding: '10px 14px' }}>#</th>
                  <th style={{ padding: '10px 14px' }}>Justification</th>
                  <th style={{ padding: '10px 14px' }}>Verdict</th>
                  <th style={{ padding: '10px 14px' }}>Confidence</th>
                  <th style={{ padding: '10px 14px' }}>Influential Keywords</th>
                </tr>
              </thead>
              <tbody>
                {results.map((r, i) => (
                  <tr key={i} style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.05)' }}>
                    <td style={{ padding: '12px 14px', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                      #{r.id}
                    </td>
                    <td style={{ padding: '12px 14px', maxWidth: '380px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      {r.text}
                    </td>
                    <td style={{ padding: '12px 14px' }}>
                      <span className={r.prediction === 'Genuine' ? 'badge-genuine' : r.prediction === 'Suspicious' ? 'badge-suspicious' : 'badge-emotional'}>
                        {r.prediction}
                      </span>
                    </td>
                    <td style={{ padding: '12px 14px', fontFamily: 'var(--font-mono)', fontWeight: 600 }}>
                      {(r.confidence * 100).toFixed(1)}%
                    </td>
                    <td style={{ padding: '12px 14px' }}>
                      <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                        {r.keywords.map((k, ki) => (
                          <span key={ki} className="keyword-chip" style={{ fontSize: '0.72rem', padding: '2px 6px' }}>
                            {k}
                          </span>
                        ))}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
