'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, Search, Zap, Sparkles, Loader2 } from 'lucide-react';
import { api } from '@/lib/api';
import { LeadCard } from '@/components/LeadCard';
import { AddLeadModal } from '@/components/AddLeadModal';
import type { Lead } from '@/lib/types';

export default function LeadsPage() {
  const [showAddModal, setShowAddModal] = useState(false);
  const [search, setSearch] = useState('');
  const [tierFilter, setTierFilter] = useState('');
  const queryClient = useQueryClient();

  const { data: leads, isLoading } = useQuery({
    queryKey: ['leads', { tier: tierFilter }],
    queryFn: () => api.getLeads({ tier: tierFilter || undefined }),
  });

  const scoreMutation = useMutation({
    mutationFn: (leadId: string) => api.scoreLead(leadId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['leads'] }),
  });

  const enrichMutation = useMutation({
    mutationFn: (leadId: string) => api.enrichLead(leadId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['leads'] }),
  });

  const filteredLeads = leads?.filter(lead =>
    !search || lead.email.toLowerCase().includes(search.toLowerCase()) ||
    lead.company?.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Leads</h1>
          <p className="mt-1 text-gray-600">Manage and score your leads</p>
        </div>
        <button onClick={() => setShowAddModal(true)} className="btn btn-primary">
          <Plus className="w-4 h-4 mr-2" /> Add Lead
        </button>
      </div>

      <div className="card">
        <div className="flex flex-wrap gap-4">
          <div className="flex-1 min-w-[200px] relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search leads..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="input pl-10"
            />
          </div>
          <select value={tierFilter} onChange={(e) => setTierFilter(e.target.value)} className="input w-auto">
            <option value="">All Tiers</option>
            <option value="hot">Hot</option>
            <option value="warm">Warm</option>
            <option value="cold">Cold</option>
          </select>
        </div>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-12"><Loader2 className="w-8 h-8 animate-spin text-primary-600" /></div>
      ) : filteredLeads && filteredLeads.length > 0 ? (
        <div className="grid gap-4">
          {filteredLeads.map((lead) => (
            <LeadCard
              key={lead.id}
              lead={lead}
              onScore={() => scoreMutation.mutate(lead.id)}
              onEnrich={() => enrichMutation.mutate(lead.id)}
              scoring={scoreMutation.isPending && scoreMutation.variables === lead.id}
              enriching={enrichMutation.isPending && enrichMutation.variables === lead.id}
            />
          ))}
        </div>
      ) : (
        <div className="card text-center py-12">
          <p className="text-gray-500">No leads found</p>
        </div>
      )}

      {showAddModal && <AddLeadModal onClose={() => setShowAddModal(false)} />}
    </div>
  );
}
