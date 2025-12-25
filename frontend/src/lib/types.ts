export interface Lead {
  id: string;
  email: string;
  first_name?: string;
  last_name?: string;
  company?: string;
  job_title?: string;
  phone?: string;
  website?: string;
  linkedin_url?: string;
  source: string;
  status: string;
  score: number;
  score_breakdown: {
    firmographic?: number;
    behavioral?: number;
    engagement?: number;
    fit?: number;
    reasoning?: string;
    recommendations?: string[];
  };
  score_tier?: string;
  enrichment_data: any;
  intent_signals: any[];
  intent_score: number;
  tags: string[];
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface DashboardStats {
  total_leads: number;
  hot_leads: number;
  warm_leads: number;
  cold_leads: number;
  average_score: number;
  enriched_leads: number;
  enrichment_rate: number;
}
