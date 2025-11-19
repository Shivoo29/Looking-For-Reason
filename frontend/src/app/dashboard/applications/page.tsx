"use client";

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Plus, Calendar, Building2, Briefcase, ExternalLink } from 'lucide-react';
import { API } from '@/lib/api-client';
import { useStore } from '@/store/use-store';
import { formatRelativeTime } from '@/lib/utils';
import type { ApplicationStatus } from '@/store/use-store';

const STATUS_CONFIG: Record<ApplicationStatus, { color: string; label: string }> = {
  pending: { color: 'bg-yellow-300 text-black', label: 'PENDING' },
  applied: { color: 'bg-blue-500 text-white', label: 'APPLIED' },
  screening: { color: 'bg-purple-500 text-white', label: 'SCREENING' },
  interview: { color: 'bg-green-500 text-white', label: 'INTERVIEW' },
  offer: { color: 'bg-green-600 text-white', label: 'OFFER' },
  rejected: { color: 'bg-red-500 text-white', label: 'REJECTED' },
  accepted: { color: 'bg-green-700 text-white', label: 'ACCEPTED' },
};

export default function ApplicationsPage() {
  const { applications, setApplications } = useStore();
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>('all');

  useEffect(() => {
    loadApplications();
  }, []);

  const loadApplications = async () => {
    try {
      const data = await API.applications.list({});
      setApplications(data);
    } catch (error) {
      console.error('Failed to load applications:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredApplications = filter === 'all'
    ? applications
    : applications.filter(app => app.status === filter);

  if (loading) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-4xl font-brutal">LOADING...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white">
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="brutal-heading text-4xl mb-2">APPLICATIONS</h1>
            <p className="brutal-text text-lg text-gray-700">
              Track all your job applications in one place
            </p>
          </div>
          <Link href="/dashboard/jobs/new">
            <Button size="lg">
              <Plus className="mr-2 h-5 w-5" />
              NEW APPLICATION
            </Button>
          </Link>
        </div>

        {/* Filter tabs */}
        <div className="mb-6 flex gap-2 flex-wrap">
          <Button
            variant={filter === 'all' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setFilter('all')}
          >
            ALL ({applications.length})
          </Button>
          {Object.keys(STATUS_CONFIG).map(status => {
            const count = applications.filter(a => a.status === status).length;
            return (
              <Button
                key={status}
                variant={filter === status ? 'default' : 'outline'}
                size="sm"
                onClick={() => setFilter(status)}
              >
                {STATUS_CONFIG[status as ApplicationStatus].label} ({count})
              </Button>
            );
          })}
        </div>

        {filteredApplications.length === 0 ? (
          <Card className="bg-gray-50">
            <CardContent className="py-16 text-center">
              <Briefcase className="h-16 w-16 mx-auto mb-4 text-gray-400" />
              <h3 className="font-bold text-2xl mb-2">
                {filter === 'all' ? 'NO APPLICATIONS YET' : `NO ${STATUS_CONFIG[filter as ApplicationStatus]?.label} APPLICATIONS`}
              </h3>
              <p className="font-mono text-gray-600 mb-6">
                Start applying to jobs to track your progress
              </p>
              <Link href="/dashboard/jobs/new">
                <Button>
                  <Plus className="mr-2 h-5 w-5" />
                  CREATE APPLICATION
                </Button>
              </Link>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-4">
            {filteredApplications.map((app) => (
              <Card key={app.id} className="hover:shadow-brutal transition-all">
                <CardContent className="pt-6">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-3">
                        <h3 className="font-bold text-2xl">{app.position}</h3>
                        <Badge className={STATUS_CONFIG[app.status].color}>
                          {STATUS_CONFIG[app.status].label}
                        </Badge>
                        {app.matchScore > 0 && (
                          <Badge variant="outline">
                            {Math.round(app.matchScore)}% MATCH
                          </Badge>
                        )}
                      </div>

                      <div className="flex items-center gap-6 mb-4 font-mono text-sm">
                        <div className="flex items-center gap-2">
                          <Building2 className="h-4 w-4" />
                          <span>{app.company}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <Calendar className="h-4 w-4" />
                          <span>Applied {formatRelativeTime(app.createdAt)}</span>
                        </div>
                      </div>

                      {app.notes.length > 0 && (
                        <div className="mb-4 p-3 bg-yellow-50 border-2 border-black">
                          <p className="font-mono text-sm font-bold mb-1">LATEST NOTE:</p>
                          <p className="font-mono text-sm">{app.notes[app.notes.length - 1]}</p>
                        </div>
                      )}

                      {app.nextSteps.length > 0 && (
                        <div className="mb-4">
                          <p className="font-mono text-sm font-bold mb-2">NEXT STEPS:</p>
                          <ul className="space-y-1">
                            {app.nextSteps.map((step, idx) => (
                              <li key={idx} className="font-mono text-sm flex items-start gap-2">
                                <span>•</span>
                                <span>{step}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>

                    <div className="flex flex-col gap-2">
                      <Link href={`/dashboard/applications/${app.id}`}>
                        <Button size="sm">VIEW DETAILS</Button>
                      </Link>
                      {app.url && (
                        <a href={app.url} target="_blank" rel="noopener noreferrer">
                          <Button variant="outline" size="sm" className="w-full">
                            <ExternalLink className="mr-1 h-4 w-4" />
                            JOB POST
                          </Button>
                        </a>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
