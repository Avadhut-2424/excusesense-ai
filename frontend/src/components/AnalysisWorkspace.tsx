import React, { useState } from 'react';
import { AnalyzeResult } from '../types';
import { 
  Send, 
  Sparkles, 
  CheckCircle2, 
  AlertTriangle, 
  Heart, 
  ShieldCheck, 
  ArrowRight, 
  Activity,
  Layers,
  HelpCircle
} from 'lucide-react';

interface AnalysisWorkspaceProps {
  onAnalyzeSuccess: (result: AnalyzeResult) => void;
}

const PRESETS = [
  {
    label: 'High Fever & Doctor Bed Rest',
    category: 'Genuine',
    icon: '🏥',
    text: 'I have a high fever and the doctor has advised me to take complete bed rest for two days.',
  },
  {
    label: 'Dog Ate Car Keys & Flight',
    category: 'Suspicious',
    icon: '🐕',
    text: 'My fish ate my car keys so I accidentally boarded a wrong flight and cannot attend work.',
  },
  {
    label: 'Severe Burnout & Mental Fatigue',
    category: 'Emotional',
    icon: '🧘',
    text: 'I am taking a mental health day to prioritize my emotional well-being and recover from severe burnout.',
  },
  {
    label: 'Emergency Dental Surgery',
    category: 'Genuine',
    icon: '🦷',
    text: 'I have an emergency dental surgery scheduled at the clinic this afternoon.',
  },
];

export const AnalysisWorkspace: React.FC<AnalysisWorkspaceProps> = ({ onAnalyzeSuccess }) => {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalyzeResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async (inputText?: string) => {
    const textToSubmit = inputText || text;
    if (!textToSubmit.trim()) {
      setError('Please enter a leave justification to analyze.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const res = await fetch('/api/v1/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: textToSubmit.trim() }),
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({ detail: 'Analysis failed' }));
        throw new Error(errData.detail || 'Analysis request failed');
      }

      const data: AnalyzeResult = await res.json();
      setResult(data);
      onAnalyzeSuccess(data);
    } catch (err: any) {
      setError(err.message || 'An error occurred during classification.');
    } finally {
      setLoading(false);
    }
  };

  const loadPreset = (presetText: string) => {
    setText(presetText);
    handleAnalyze(presetText);
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '28px', marginBottom: '36px' }}>
      {/* Left: Input & Presets */}
      <div className="glass-panel" style={{ padding: '28px', display: 'flex', flexDirection: 'column' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Activity size={20} color="#06b6d4" />
            <h2 style={{ fontSize: '1.1rem', fontWeight: 700 }}>Leave Justification Input</h2>
          </div>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            {text.length} characters
          </span>
        </div>

        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste or write the employee leave justification text here... (e.g. 'I am suffering from severe migraine and visiting the medical clinic for consultation')"
          rows={6}
          style={{
            width: '100%',
            background: 'rgba(0, 0, 0, 0.25)',
            border: '1px solid var(--border-color)',
            borderRadius: '12px',
            color: 'var(--text-primary)',
            padding: '16px',
            fontSize: '0.95rem',
            fontFamily: 'inherit',
            resize: 'vertical',
            outline: 'none',
            marginBottom: '18px',
            transition: 'border-color 0.2s',
          }}
          onFocus={(e) => (e.target.style.borderColor = 'var(--border-focus)')}
          onBlur={(e) => (e.target.style.borderColor = 'var(--border-color)')}
        />

        {error && (
          <div style={{ padding: '10px 14px', borderRadius: '8px', background: 'rgba(244, 63, 94, 0.15)', border: '1px solid rgba(244, 63, 94, 0.3)', color: '#fb7185', fontSize: '0.85rem', marginBottom: '16px' }}>
            {error}
          </div>
        )}

        {/* Quick Presets */}
        <div style={{ marginBottom: '22px' }}>
          <div style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '10px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Quick Canonical Test Presets
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
            {PRESETS.map((p, i) => (
              <button
                key={i}
                type="button"
                onClick={() => loadPreset(p.text)}
                className="btn-ghost"
                style={{ fontSize: '0.8rem', padding: '6px 12px' }}
              >
                <span>{p.icon}</span>
                <span>{p.label}</span>
              </button>
            ))}
          </div>
        </div>

        <div style={{ marginTop: 'auto', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <button
            type="button"
            onClick={() => setText('')}
            className="btn-ghost"
            disabled={!text || loading}
          >
            Clear
          </button>

          <button
            type="button"
            onClick={() => handleAnalyze()}
            disabled={loading || !text.trim()}
            className="btn-primary"
            style={{ minWidth: '160px' }}
          >
            {loading ? (
              <span>Analyzing...</span>
            ) : (
              <>
                <span>Classify Application</span>
                <Send size={16} />
              </>
            )}
          </button>
        </div>
      </div>

      {/* Right: Live Intelligence & Explainability Result */}
      <div className="glass-panel" style={{ padding: '28px', display: 'flex', flexDirection: 'column' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Layers size={20} color="#06b6d4" />
            <h2 style={{ fontSize: '1.1rem', fontWeight: 700 }}>Inference Verdict & Explainability</h2>
          </div>
          {result && (
            <span style={{ fontSize: '0.75rem', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>
              Audit #{result.id}
            </span>
          )}
        </div>

        {!result ? (
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center', color: 'var(--text-muted)', padding: '40px 20px' }}>
            <div style={{ width: '64px', height: '64px', borderRadius: '50%', background: 'rgba(255, 255, 255, 0.03)', border: '1px dashed var(--border-color)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '16px' }}>
              <Sparkles size={28} color="var(--text-secondary)" />
            </div>
            <div style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '6px' }}>
              Awaiting Input Justification
            </div>
            <p style={{ fontSize: '0.85rem', maxWidth: '320px' }}>
              Type an excuse on the left or select a quick canonical test preset to trigger real-time AI classification and feature attribution.
            </p>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', flex: 1 }}>
            {/* Verdict Banner */}
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '16px 20px', borderRadius: '12px', background: result.prediction === 'Genuine' ? 'var(--badge-genuine-bg)' : result.prediction === 'Suspicious' ? 'var(--badge-suspicious-bg)' : 'var(--badge-emotional-bg)', border: `1px solid ${result.prediction === 'Genuine' ? 'var(--badge-genuine-border)' : result.prediction === 'Suspicious' ? 'var(--badge-suspicious-border)' : 'var(--badge-emotional-border)'}` }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                {result.prediction === 'Genuine' && <CheckCircle2 size={28} color="#10b981" />}
                {result.prediction === 'Suspicious' && <AlertTriangle size={28} color="#f43f5e" />}
                {result.prediction === 'Emotional' && <Heart size={28} color="#8b5cf6" />}
                <div>
                  <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.08em', fontWeight: 700, color: 'var(--text-muted)' }}>
                    Predicted Category
                  </div>
                  <div style={{ fontSize: '1.4rem', fontWeight: 800 }}>
                    {result.prediction}
                  </div>
                </div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600 }}>Confidence</div>
                <div style={{ fontSize: '1.4rem', fontWeight: 800, fontFamily: 'var(--font-mono)' }}>
                  {(result.confidence * 100).toFixed(1)}%
                </div>
              </div>
            </div>

            {/* Probability Breakdown Distribution */}
            <div>
              <div style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '10px' }}>
                Class Probability Distribution
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {(['Genuine', 'Emotional', 'Suspicious'] as const).map((cat) => {
                  const prob = result.probabilities[cat] || 0;
                  const pct = (prob * 100).toFixed(1);
                  const color = cat === 'Genuine' ? '#10b981' : cat === 'Emotional' ? '#8b5cf6' : '#f43f5e';
                  return (
                    <div key={cat}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', marginBottom: '4px' }}>
                        <span style={{ fontWeight: 600 }}>{cat}</span>
                        <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>{pct}%</span>
                      </div>
                      <div style={{ width: '100%', height: '8px', borderRadius: '4px', background: 'rgba(255, 255, 255, 0.05)', overflow: 'hidden' }}>
                        <div style={{ width: `${pct}%`, height: '100%', background: color, borderRadius: '4px', transition: 'width 0.4s ease' }} />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Explainable AI (XAI) Feature Attribution Chips */}
            <div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
                  Explainable AI (XAI) Keyword Attribution
                </span>
                <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Influence Weight</span>
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                {result.attributions && result.attributions.length > 0 ? (
                  result.attributions.map((attr, idx) => (
                    <span key={idx} className="keyword-chip">
                      <strong>{attr.word}</strong>
                      <span style={{ opacity: 0.75, fontSize: '0.7rem' }}>+{attr.weight.toFixed(2)}</span>
                    </span>
                  ))
                ) : (
                  <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                    No significant keywords extracted.
                  </span>
                )}
              </div>
            </div>

            {/* HR Compliance Recommendation */}
            <div style={{ marginTop: 'auto', padding: '14px 16px', borderRadius: '10px', background: 'rgba(255, 255, 255, 0.03)', border: '1px solid var(--border-color)', display: 'flex', alignItems: 'center', gap: '12px' }}>
              <ShieldCheck size={20} color="#06b6d4" />
              <div>
                <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                  HR Compliance Directive
                </div>
                <div style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-primary)' }}>
                  {result.recommendation}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
