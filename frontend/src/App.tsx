import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { StatsCards } from './components/StatsCards';
import { AnalysisWorkspace } from './components/AnalysisWorkspace';
import { BatchProcessor } from './components/BatchProcessor';
import { AuditHistoryTable } from './components/AuditHistoryTable';
import { StatsData, HistoryItem, AnalyzeResult } from './types';
import { Sparkles, Layers, History, ShieldAlert } from 'lucide-react';

export const App: React.FC = () => {
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');
  const [activeTab, setActiveTab] = useState<'single' | 'batch' | 'history'>('single');
  const [stats, setStats] = useState<StatsData | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  // Sync theme
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  // Fetch stats and history
  const fetchData = async () => {
    try {
      const [statsRes, historyRes] = await Promise.all([
        fetch('/api/v1/stats'),
        fetch('/api/v1/history?limit=50'),
      ]);

      if (statsRes.ok) {
        const statsData = await statsRes.json();
        setStats(statsData);
      }

      if (historyRes.ok) {
        const historyData = await historyRes.json();
        setHistory(historyData);
      }
    } catch (err) {
      console.error('Failed to load initial data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleToggleTheme = () => {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));
  };

  const handleAnalyzeSuccess = (result: AnalyzeResult) => {
    // Refresh stats & history
    fetchData();
  };

  const handleDeleteRecord = async (id: number) => {
    try {
      const res = await fetch(`/api/v1/history/${id}`, { method: 'DELETE' });
      if (res.ok) {
        setHistory((prev) => prev.filter((item) => item.id !== id));
        fetchData();
      }
    } catch (err) {
      console.error('Failed to delete record:', err);
    }
  };

  const handleClearAll = async () => {
    if (!window.confirm('Are you sure you want to clear all compliance audit logs?')) {
      return;
    }
    try {
      const res = await fetch('/api/v1/history', { method: 'DELETE' });
      if (res.ok) {
        setHistory([]);
        fetchData();
      }
    } catch (err) {
      console.error('Failed to clear history:', err);
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Header
        theme={theme}
        onToggleTheme={handleToggleTheme}
        accuracy={stats?.model_accuracy || 1.0}
      />

      <main style={{ maxWidth: '1280px', margin: '0 auto', width: '100%', padding: '0 24px', flex: 1 }}>
        {/* KPI Stats Overview */}
        <StatsCards stats={stats} />

        {/* Tab Navigation */}
        <div style={{ display: 'flex', gap: '8px', marginBottom: '24px', borderBottom: '1px solid var(--border-color)', paddingBottom: '12px' }}>
          <button
            type="button"
            onClick={() => setActiveTab('single')}
            className="btn-ghost"
            style={{
              padding: '10px 18px',
              fontWeight: activeTab === 'single' ? 700 : 500,
              background: activeTab === 'single' ? 'rgba(56, 189, 248, 0.15)' : 'transparent',
              borderColor: activeTab === 'single' ? '#38bdf8' : 'transparent',
              color: activeTab === 'single' ? '#38bdf8' : 'var(--text-secondary)',
              borderRadius: '10px',
            }}
          >
            <Sparkles size={16} />
            <span>Single Application Workspace</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('batch')}
            className="btn-ghost"
            style={{
              padding: '10px 18px',
              fontWeight: activeTab === 'batch' ? 700 : 500,
              background: activeTab === 'batch' ? 'rgba(56, 189, 248, 0.15)' : 'transparent',
              borderColor: activeTab === 'batch' ? '#38bdf8' : 'transparent',
              color: activeTab === 'batch' ? '#38bdf8' : 'var(--text-secondary)',
              borderRadius: '10px',
            }}
          >
            <Layers size={16} />
            <span>Batch Multi-Screening</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('history')}
            className="btn-ghost"
            style={{
              padding: '10px 18px',
              fontWeight: activeTab === 'history' ? 700 : 500,
              background: activeTab === 'history' ? 'rgba(56, 189, 248, 0.15)' : 'transparent',
              borderColor: activeTab === 'history' ? '#38bdf8' : 'transparent',
              color: activeTab === 'history' ? '#38bdf8' : 'var(--text-secondary)',
              borderRadius: '10px',
            }}
          >
            <History size={16} />
            <span>Audit Trail & Records ({history.length})</span>
          </button>
        </div>

        {/* Tab Content */}
        {activeTab === 'single' && (
          <>
            <AnalysisWorkspace onAnalyzeSuccess={handleAnalyzeSuccess} />
            <AuditHistoryTable
              history={history.slice(0, 5)}
              onRefresh={fetchData}
              onDeleteRecord={handleDeleteRecord}
              onClearAll={handleClearAll}
            />
          </>
        )}

        {activeTab === 'batch' && (
          <BatchProcessor onBatchCompleted={fetchData} />
        )}

        {activeTab === 'history' && (
          <AuditHistoryTable
            history={history}
            onRefresh={fetchData}
            onDeleteRecord={handleDeleteRecord}
            onClearAll={handleClearAll}
          />
        )}
      </main>

      {/* Footer */}
      <footer style={{ marginTop: 'auto', borderTop: '1px solid var(--border-color)', padding: '24px', textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.82rem' }}>
        <p>ExcuseSense AI — Autonomous Human Resources Leave Application Intelligence Platform</p>
        <p style={{ marginTop: '4px', opacity: 0.75 }}>
          Built with FastAPI, Scikit-Learn TF-IDF N-Grams, React 18, and Explainable AI Attribution
        </p>
      </footer>
    </div>
  );
};

export default App;
