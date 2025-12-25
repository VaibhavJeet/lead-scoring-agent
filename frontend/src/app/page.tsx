'use client';

import { useQuery } from '@tanstack/react-query';
import { Users, Flame, ThermometerSun, Snowflake, TrendingUp, ArrowRight } from 'lucide-react';
import Link from 'next/link';
import { api } from '@/lib/api';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';

const COLORS = ['#ef4444', '#f59e0b', '#3b82f6', '#6b7280'];

export default function Dashboard() {
  const { data: stats, isLoading } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: () => api.getStats(),
  });

  const tierData = [
    { name: 'Hot', value: stats?.hot_leads ?? 0, color: '#ef4444' },
    { name: 'Warm', value: stats?.warm_leads ?? 0, color: '#f59e0b' },
    { name: 'Cold', value: stats?.cold_leads ?? 0, color: '#3b82f6' },
  ].filter(d => d.value > 0);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Lead Scoring Dashboard</h1>
        <p className="mt-2 text-gray-600">AI-powered lead qualification and prioritization</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-blue-100 rounded-lg"><Users className="w-6 h-6 text-blue-600" /></div>
            <div>
              <p className="text-sm text-gray-500">Total Leads</p>
              <p className="text-2xl font-bold">{isLoading ? '...' : stats?.total_leads ?? 0}</p>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-red-100 rounded-lg"><Flame className="w-6 h-6 text-red-600" /></div>
            <div>
              <p className="text-sm text-gray-500">Hot Leads</p>
              <p className="text-2xl font-bold">{isLoading ? '...' : stats?.hot_leads ?? 0}</p>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-yellow-100 rounded-lg"><ThermometerSun className="w-6 h-6 text-yellow-600" /></div>
            <div>
              <p className="text-sm text-gray-500">Warm Leads</p>
              <p className="text-2xl font-bold">{isLoading ? '...' : stats?.warm_leads ?? 0}</p>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-green-100 rounded-lg"><TrendingUp className="w-6 h-6 text-green-600" /></div>
            <div>
              <p className="text-sm text-gray-500">Avg Score</p>
              <p className="text-2xl font-bold">{isLoading ? '...' : stats?.average_score ?? 0}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Lead Distribution</h3>
          {tierData.length > 0 ? (
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={tierData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
                    {tierData.map((entry, i) => <Cell key={i} fill={entry.color} />)}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <p className="text-center text-gray-500 py-8">No leads scored yet</p>
          )}
        </div>
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Quick Actions</h3>
          <div className="space-y-3">
            <Link href="/leads" className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100">
              <span className="font-medium">View All Leads</span>
              <ArrowRight className="w-5 h-5 text-gray-400" />
            </Link>
            <Link href="/leads?tier=hot" className="flex items-center justify-between p-4 bg-red-50 rounded-lg hover:bg-red-100">
              <span className="font-medium text-red-700">Hot Leads Ready for Outreach</span>
              <ArrowRight className="w-5 h-5 text-red-400" />
            </Link>
            <Link href="/analytics" className="flex items-center justify-between p-4 bg-blue-50 rounded-lg hover:bg-blue-100">
              <span className="font-medium text-blue-700">View Analytics</span>
              <ArrowRight className="w-5 h-5 text-blue-400" />
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
