import React, { useState } from 'react';
import { HistoryItem } from '../types';
import { Search, Trash2, Filter, History, RefreshCw } from 'lucide-react';

interface AuditHistoryTableProps {
  history: HistoryItem[];
  onRefresh: () => void;
  onDeleteRecord: (id: number) => void;
  onClearAll: () => void;
}

export const AuditHistoryTable: React.FC<AuditHistoryTableProps> = ({
  history,
  onRefresh,
  onDeleteRecord,
  onClearAll,
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategory, setFilterCategory] = useState<string>('All');

  const filteredHistory = history.filter((item) => {
    const matchesCategory = filterCategory === 'All' || item.prediction === filterCategory;
    const matchesSearch = item.text.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          item.keywords.some(k => k.toLowerCase().includes(searchTerm.toLowerCase()));
    return matchesCategory && matchesSearch;
  });

  return (
    <div className="glass-panel" style={{ padding: '28px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px', flexWrap: 'wrap', gap: '14px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <History size={22} color="#06b6d4" />
          <div>
            <h2 style={{ fontSize: '1.15rem', fontWeight: 700 }}>Compliance Audit Logs & Records</h2>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              Historical leave analysis log stream with verified predictions and model timestamps.
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <button
            type="button"
            onClick={onRefresh}
            className="btn-ghost"
            title="Refresh history"
          >
            <RefreshCw size={15} />
            <span>Refresh</span>
          </button>

          {history.length > 0 && (
            <button
              type="button"
              onClick={onClearAll}
              className="btn-ghost"
              style={{ color: '#fb7185', borderColor: 'rgba(244, 63, 94, 0.3)' }}
            >
              <Trash2 size={15} />
              <span>Clear All</span>
            </button>
          )}
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div style={{ display: 'flex', gap: '14px', marginBottom: '20px', flexWrap: 'wrap' }}>
        <div style={{ flex: 1, minWidth: '240px', position: 'relative' }}>
          <Search size={16} color="var(--text-muted)" style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)' }} />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search within text or keywords..."
            style={{
              width: '100%',
              padding: '10px 14px 10px 38px',
              background: 'rgba(0, 0, 0, 0.25)',
              border: '1px solid var(--border-color)',
              borderRadius: '10px',
              color: 'var(--text-primary)',
              fontSize: '0.85rem',
              outline: 'none',
            }}
          />
        </div>

        <div style={{ display: 'flex', gap: '6px' }}>
          {['All', 'Genuine', 'Emotional', 'Suspicious'].map((cat) => (
            <button
              key={cat}
              type="button"
              onClick={() => setFilterCategory(cat)}
              className="btn-ghost"
              style={{
                fontSize: '0.8rem',
                padding: '6px 14px',
                background: filterCategory === cat ? 'rgba(56, 189, 248, 0.15)' : 'transparent',
                borderColor: filterCategory === cat ? '#38bdf8' : 'var(--border-color)',
                color: filterCategory === cat ? '#38bdf8' : 'var(--text-secondary)',
                fontWeight: filterCategory === cat ? 700 : 500,
              }}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Table */}
      {filteredHistory.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '40px 20px', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
          No audit records found matching the active filter.
        </div>
      ) : (
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-color)', textAlign: 'left', color: 'var(--text-muted)' }}>
                <th style={{ padding: '12px 14px', width: '70px' }}>ID</th>
                <th style={{ padding: '12px 14px' }}>Application Justification</th>
                <th style={{ padding: '12px 14px', width: '130px' }}>Verdict</th>
                <th style={{ padding: '12px 14px', width: '100px' }}>Confidence</th>
                <th style={{ padding: '12px 14px' }}>Extracted Drivers</th>
                <th style={{ padding: '12px 14px', width: '160px' }}>Timestamp</th>
                <th style={{ padding: '12px 14px', width: '60px', textAlign: 'center' }}>Action</th>
              </tr>
            </thead>
            <tbody>
              {filteredHistory.map((item) => (
                <tr key={item.id} style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.05)' }}>
                  <td style={{ padding: '12px 14px', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                    #{item.id}
                  </td>
                  <td style={{ padding: '12px 14px', maxWidth: '340px' }}>
                    <div style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      {item.text}
                    </div>
                  </td>
                  <td style={{ padding: '12px 14px' }}>
                    <span className={item.prediction === 'Genuine' ? 'badge-genuine' : item.prediction === 'Suspicious' ? 'badge-suspicious' : 'badge-emotional'}>
                      {item.prediction}
                    </span>
                  </td>
                  <td style={{ padding: '12px 14px', fontFamily: 'var(--font-mono)', fontWeight: 600 }}>
                    {(item.confidence * 100).toFixed(1)}%
                  </td>
                  <td style={{ padding: '12px 14px' }}>
                    <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                      {item.keywords.map((kw, kwi) => (
                        <span key={kwi} className="keyword-chip" style={{ fontSize: '0.72rem', padding: '2px 6px' }}>
                          {kw}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td style={{ padding: '12px 14px', color: 'var(--text-muted)', fontSize: '0.78rem' }}>
                    {item.created_at}
                  </td>
                  <td style={{ padding: '12px 14px', textAlign: 'center' }}>
                    <button
                      type="button"
                      onClick={() => onDeleteRecord(item.id)}
                      className="btn-ghost"
                      style={{ padding: '4px', borderRadius: '6px', color: 'var(--text-muted)' }}
                      title="Delete record"
                    >
                      <Trash2 size={14} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
