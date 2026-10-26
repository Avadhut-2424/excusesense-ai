export interface KeywordAttribution {
  word: string;
  weight: number;
}

export interface AnalyzeResult {
  id: number;
  text: string;
  prediction: 'Genuine' | 'Suspicious' | 'Emotional';
  confidence: number;
  probabilities: {
    Genuine: number;
    Suspicious: number;
    Emotional: number;
  };
  keywords: string[];
  attributions: KeywordAttribution[];
  risk_level: 'low' | 'medium' | 'high';
  recommendation: string;
  created_at: string;
}

export interface HistoryItem {
  id: number;
  text: string;
  prediction: 'Genuine' | 'Suspicious' | 'Emotional';
  confidence: number;
  keywords: string[];
  created_at: string;
}

export interface StatsData {
  total: number;
  genuine: number;
  suspicious: number;
  emotional: number;
  model_accuracy: number;
  suspicious_rate: number;
  genuine_rate: number;
  emotional_rate: number;
}
