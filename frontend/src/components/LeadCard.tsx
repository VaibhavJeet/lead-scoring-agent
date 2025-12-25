'use client';

import { User, Building, Mail, Zap, Sparkles, Loader2 } from 'lucide-react';
import { clsx } from 'clsx';
import type { Lead } from '@/lib/types';

interface LeadCardProps {
  lead: Lead;
  onScore: () => void;
  onEnrich: () => void;
  scoring?: boolean;
  enriching?: boolean;
}

export function LeadCard({ lead, onScore, onEnrich, scoring, enriching }: LeadCardProps) {
  const getTierBadge = (tier?: string) => {
    switch (tier) {
      case 'hot': return 'bg-red-100 text-red-700';
      case 'warm': return 'bg-yellow-100 text-yellow-700';
      case 'cold': return 'bg-blue-100 text-blue-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  return (
    <div className="card hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <h3 className="text-lg font-semibold text-gray-900">
              {lead.first_name} {lead.last_name}
            </h3>
            {lead.score_tier && (
              <span className={clsx('badge', getTierBadge(lead.score_tier))}>
                {lead.score_tier}
              </span>
            )}
            {lead.score > 0 && (
              <span className="text-sm font-medium text-gray-500">
                Score: {Math.round(lead.score)}
              </span>
            )}
          </div>

          <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600">
            <span className="flex items-center gap-1">
              <Mail className="w-4 h-4" /> {lead.email}
            </span>
            {lead.company && (
              <span className="flex items-center gap-1">
                <Building className="w-4 h-4" /> {lead.company}
              </span>
            )}
            {lead.job_title && (
              <span className="flex items-center gap-1">
                <User className="w-4 h-4" /> {lead.job_title}
              </span>
            )}
          </div>

          {lead.score_breakdown?.reasoning && (
            <p className="mt-3 text-sm text-gray-500 line-clamp-2">
              {lead.score_breakdown.reasoning}
            </p>
          )}
        </div>

        <div className="flex items-center gap-2 ml-4">
          <button onClick={onScore} disabled={scoring} className="btn btn-primary text-sm">
            {scoring ? <Loader2 className="w-4 h-4 animate-spin" /> : <Zap className="w-4 h-4 mr-1" />}
            Score
          </button>
          <button onClick={onEnrich} disabled={enriching} className="btn btn-secondary text-sm">
            {enriching ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4 mr-1" />}
            Enrich
          </button>
        </div>
      </div>
    </div>
  );
}
