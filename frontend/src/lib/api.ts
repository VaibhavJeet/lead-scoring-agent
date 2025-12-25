import axios from 'axios';
import type { Lead, DashboardStats } from './types';

const client = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' },
});

export const api = {
  async getStats(): Promise<DashboardStats> {
    const { data } = await client.get('/api/analytics/stats');
    return data;
  },

  async getLeads(params?: { tier?: string; status?: string; minScore?: number }): Promise<Lead[]> {
    const { data } = await client.get('/api/leads', { params });
    return data;
  },

  async getLead(id: string): Promise<Lead> {
    const { data } = await client.get(`/api/leads/${id}`);
    return data;
  },

  async createLead(lead: Partial<Lead>): Promise<Lead> {
    const { data } = await client.post('/api/leads', lead);
    return data;
  },

  async scoreLead(id: string): Promise<Lead> {
    const { data } = await client.post(`/api/leads/${id}/score`);
    return data;
  },

  async enrichLead(id: string): Promise<Lead> {
    const { data } = await client.post(`/api/leads/${id}/enrich`);
    return data;
  },

  async getAnalytics(): Promise<any> {
    const { data } = await client.get('/api/analytics');
    return data;
  },
};
