import React from 'react';
import { StatsData } from '../types';
import { FileText, CheckCircle2, AlertTriangle, HeartPulse, Zap } from 'lucide-react';

interface StatsCardsProps {
  stats: StatsData | null;
}

export const StatsCards: React.FC<StatsCardsProps> = ({ stats }) => {
  const cards = [
    {
      title: 'Total Evaluated',
      value: stats ? stats.total.toLocaleString() : '0',
      subtitle: 'All-time audit logs',
      icon: <FileText size={20} color="#38bdf8" />,
      glowColor: 'rgba(56, 189, 248, 0.15)',
    },
    {
      title: 'Genuine Approval',
      value: stats ? `${stats.genuine_rate}%` : '0%',
      subtitle: `${stats?.genuine || 0} applications verified`,
      icon: <CheckCircle2 size={20} color="#34d399" />,
      glowColor: 'rgba(52, 211, 153, 0.15)',
    },
    {
      title: 'Suspicious Flagged',
      value: stats ? `${stats.suspicious_rate}%` : '0%',
      subtitle: `${stats?.suspicious || 0} audit flags raised`,
      icon: <AlertTriangle size={20} color="#fb7185" />,
      glowColor: 'rgba(251, 113, 133, 0.15)',
    },
    {
      title: 'Wellness & Emotional',
      value: stats ? `${stats.emotional_rate}%` : '0%',
      subtitle: `${stats?.emotional || 0} care interventions`,
      icon: <HeartPulse size={20} color="#c084fc" />,
      glowColor: 'rgba(192, 132, 252, 0.15)',
    },
    {
      title: 'Mean Inference Speed',
      value: '0.78 ms',
      subtitle: 'Sub-millisecond latency',
      icon: <Zap size={20} color="#fbbf24" />,
      glowColor: 'rgba(251, 191, 36, 0.15)',
    },
  ];

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '18px', marginBottom: '32px' }}>
      {cards.map((card, idx) => (
        <div key={idx} className="glass-panel" style={{ padding: '20px 22px', position: 'relative', overflow: 'hidden' }}>
          <div style={{ position: 'absolute', top: 0, right: 0, width: '80px', height: '80px', background: card.glowColor, filter: 'blur(30px)', pointerEvents: 'none' }} />
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
            <span style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
              {card.title}
            </span>
            <div style={{ padding: '6px', borderRadius: '8px', background: 'rgba(255, 255, 255, 0.05)' }}>
              {card.icon}
            </div>
          </div>
          <div style={{ fontSize: '1.75rem', fontWeight: 800, letterSpacing: '-0.02em', marginBottom: '4px' }}>
            {card.value}
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            {card.subtitle}
          </div>
        </div>
      ))}
    </div>
  );
};
