"use client";

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useStore } from '@/store/use-store';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import {
  Plus,
  FileText,
  Briefcase,
  TrendingUp,
  Send,
  BarChart3,
  Target,
  Clock,
  CheckCircle2,
  XCircle,
  AlertCircle
} from 'lucide-react';
import { API } from '@/lib/api-client';
import { formatRelativeTime, getScoreColor, getScoreLabel } from '@/lib/utils';

export default function DashboardPage() {
  const { user, applications, resumes, setApplications, setResumes } = useStore();
  const [stats, setStats] = useState({
    totalApplications: 0,
    activeApplications: 0,
    interviews: 0,
    responseRate: 0,
    avgAtsScore: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [appsData, resumesData, analyticsData] = await Promise.all([
        API.applications.list({ limit: 10 }),
        API.resumes.list(),
        API.analytics.getOverview(),
      ]);

      setApplications(appsData);
      setResumes(resumesData);
      setStats(analyticsData);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status: string) => {
    const statusMap: Record<string, { variant: any; label: string }> = {
      pending: { variant: 'default', label: 'PENDING' },
      applied: { variant: 'secondary', label: 'APPLIED' },
      screening: { variant: 'secondary', label: 'SCREENING' },
      interview: { variant: 'success', label: 'INTERVIEW' },
      offer: { variant: 'success', label: 'OFFER' },
      rejected: { variant: 'destructive', label: 'REJECTED' },
      accepted: { variant: 'success', label: 'ACCEPTED' },
    };
    const config = statusMap[status] || statusMap.pending;
    return <Badge variant={config.variant}>{config.label}</Badge>;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-4xl font-brutal">LOADING...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="border-b-4 border-black bg-white sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <Link href="/" className="text-3xl font-brutal">
            JOBHACK
          </Link>
          <nav className="flex items-center gap-4">
            <Link href="/dashboard">
              <Button variant="ghost" size="sm">DASHBOARD</Button>
            </Link>
            <Link href="/dashboard/resumes">
              <Button variant="ghost" size="sm">RESUMES</Button>
            </Link>
            <Link href="/dashboard/applications">
              <Button variant="ghost" size="sm">APPLICATIONS</Button>
            </Link>
            <Link href="/dashboard/analytics">
              <Button variant="ghost" size="sm">ANALYTICS</Button>
            </Link>
            <Link href="/settings">
              <Button variant="outline" size="sm">SETTINGS</Button>
            </Link>
          </nav>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Welcome Section */}
        <div className="mb-12">
          <h1 className="brutal-heading text-4xl md:text-5xl mb-4">
            WELCOME BACK{user?.name ? `, ${user.name.toUpperCase()}` : ''}
          </h1>
          <p className="brutal-text text-lg text-gray-700">
            Here's your job search command center. Time to destroy some applications.
          </p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-12">
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between mb-2">
                <Briefcase className="h-8 w-8" />
                <div className="text-3xl font-brutal">{stats.totalApplications}</div>
              </div>
              <p className="font-mono text-sm font-bold">TOTAL APPLICATIONS</p>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between mb-2">
                <Clock className="h-8 w-8" />
                <div className="text-3xl font-brutal">{stats.activeApplications}</div>
              </div>
              <p className="font-mono text-sm font-bold">ACTIVE</p>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between mb-2">
                <CheckCircle2 className="h-8 w-8 text-green-600" />
                <div className="text-3xl font-brutal">{stats.interviews}</div>
              </div>
              <p className="font-mono text-sm font-bold">INTERVIEWS</p>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between mb-2">
                <TrendingUp className="h-8 w-8 text-blue-600" />
                <div className="text-3xl font-brutal">{stats.responseRate}%</div>
              </div>
              <p className="font-mono text-sm font-bold">RESPONSE RATE</p>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between mb-2">
                <BarChart3 className="h-8 w-8 text-purple-600" />
                <div className={`text-3xl font-brutal ${getScoreColor(stats.avgAtsScore)}`}>
                  {stats.avgAtsScore}
                </div>
              </div>
              <p className="font-mono text-sm font-bold">AVG ATS SCORE</p>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <div className="mb-12">
          <h2 className="font-brutal text-2xl mb-6">QUICK ACTIONS</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <Link href="/dashboard/resumes/upload">
              <Card className="hover:shadow-brutal-lg transition-all cursor-pointer bg-yellow-300">
                <CardContent className="pt-6 text-center">
                  <FileText className="h-12 w-12 mx-auto mb-4" />
                  <h3 className="font-bold text-lg mb-2">UPLOAD RESUME</h3>
                  <p className="font-mono text-sm">Start with your base resume</p>
                </CardContent>
              </Card>
            </Link>

            <Link href="/dashboard/jobs/new">
              <Card className="hover:shadow-brutal-lg transition-all cursor-pointer bg-blue-300">
                <CardContent className="pt-6 text-center">
                  <Plus className="h-12 w-12 mx-auto mb-4" />
                  <h3 className="font-bold text-lg mb-2">NEW APPLICATION</h3>
                  <p className="font-mono text-sm">Apply to a job</p>
                </CardContent>
              </Card>
            </Link>

            <Link href="/dashboard/outreach">
              <Card className="hover:shadow-brutal-lg transition-all cursor-pointer bg-green-300">
                <CardContent className="pt-6 text-center">
                  <Send className="h-12 w-12 mx-auto mb-4" />
                  <h3 className="font-bold text-lg mb-2">SEND OUTREACH</h3>
                  <p className="font-mono text-sm">Contact hiring managers</p>
                </CardContent>
              </Card>
            </Link>

            <Link href="/dashboard/analytics">
              <Card className="hover:shadow-brutal-lg transition-all cursor-pointer bg-pink-300">
                <CardContent className="pt-6 text-center">
                  <Target className="h-12 w-12 mx-auto mb-4" />
                  <h3 className="font-bold text-lg mb-2">VIEW ANALYTICS</h3>
                  <p className="font-mono text-sm">Track your success</p>
                </CardContent>
              </Card>
            </Link>
          </div>
        </div>

        {/* Recent Applications */}
        <div className="mb-12">
          <div className="flex justify-between items-center mb-6">
            <h2 className="font-brutal text-2xl">RECENT APPLICATIONS</h2>
            <Link href="/dashboard/applications">
              <Button variant="outline">VIEW ALL</Button>
            </Link>
          </div>

          {applications.length === 0 ? (
            <Card className="bg-gray-50">
              <CardContent className="py-12 text-center">
                <AlertCircle className="h-16 w-16 mx-auto mb-4 text-gray-400" />
                <h3 className="font-bold text-xl mb-2">NO APPLICATIONS YET</h3>
                <p className="font-mono text-gray-600 mb-6">
                  Ready to start? Upload your resume and apply to your first job.
                </p>
                <Link href="/dashboard/resumes/upload">
                  <Button>UPLOAD RESUME</Button>
                </Link>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-4">
              {applications.slice(0, 5).map((app) => (
                <Card key={app.id} className="hover:shadow-brutal transition-all">
                  <CardContent className="pt-6">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="font-bold text-xl">{app.position}</h3>
                          {getStatusBadge(app.status)}
                        </div>
                        <p className="font-mono text-lg mb-2">{app.company}</p>
                        <p className="font-mono text-sm text-gray-600">
                          Applied {formatRelativeTime(app.createdAt)}
                        </p>
                      </div>
                      <div className="flex flex-col items-end gap-2">
                        <Link href={`/dashboard/applications/${app.id}`}>
                          <Button size="sm">VIEW DETAILS</Button>
                        </Link>
                        {app.url && (
                          <a href={app.url} target="_blank" rel="noopener noreferrer">
                            <Button variant="outline" size="sm">
                              JOB POSTING
                            </Button>
                          </a>
                        )}
                      </div>
                    </div>
                    {app.notes.length > 0 && (
                      <div className="mt-4 pt-4 border-t-2 border-black">
                        <p className="font-mono text-sm">
                          <strong>Latest Note:</strong> {app.notes[app.notes.length - 1]}
                        </p>
                      </div>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>

        {/* Your Resumes */}
        <div className="mb-12">
          <div className="flex justify-between items-center mb-6">
            <h2 className="font-brutal text-2xl">YOUR RESUMES</h2>
            <Link href="/dashboard/resumes">
              <Button variant="outline">MANAGE ALL</Button>
            </Link>
          </div>

          {resumes.length === 0 ? (
            <Card className="bg-gray-50">
              <CardContent className="py-12 text-center">
                <FileText className="h-16 w-16 mx-auto mb-4 text-gray-400" />
                <h3 className="font-bold text-xl mb-2">NO RESUMES UPLOADED</h3>
                <p className="font-mono text-gray-600 mb-6">
                  Upload your resume to get started with AI optimization and ATS scoring.
                </p>
                <Link href="/dashboard/resumes/upload">
                  <Button>UPLOAD RESUME</Button>
                </Link>
              </CardContent>
            </Card>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {resumes.slice(0, 3).map((resume) => (
                <Card key={resume.id}>
                  <CardHeader>
                    <div className="flex justify-between items-start">
                      <CardTitle className="text-lg">{resume.name}</CardTitle>
                      <div className="flex flex-col items-end">
                        <div className={`text-2xl font-brutal ${getScoreColor(resume.atsScore)}`}>
                          {resume.atsScore}
                        </div>
                        <p className="font-mono text-xs">ATS SCORE</p>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <Progress value={resume.atsScore} className="mb-4" />
                    <p className={`font-mono text-sm font-bold mb-4 ${getScoreColor(resume.atsScore)}`}>
                      {getScoreLabel(resume.atsScore)}
                    </p>
                    <p className="font-mono text-xs text-gray-600 mb-4">
                      Updated {formatRelativeTime(resume.updatedAt)}
                    </p>
                    <div className="flex gap-2">
                      <Link href={`/dashboard/resumes/${resume.id}`} className="flex-1">
                        <Button size="sm" className="w-full">VIEW</Button>
                      </Link>
                      <Link href={`/dashboard/resumes/${resume.id}/optimize`} className="flex-1">
                        <Button variant="outline" size="sm" className="w-full">OPTIMIZE</Button>
                      </Link>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>

        {/* Pro Tips */}
        <Card className="bg-yellow-300">
          <CardHeader>
            <CardTitle>💡 PRO TIPS</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-3 font-mono">
              <li className="flex items-start gap-2">
                <CheckCircle2 className="h-5 w-5 flex-shrink-0 mt-0.5" />
                <span><strong>ATS Score 80+:</strong> Aim for at least 80/100 to pass automated filters</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="h-5 w-5 flex-shrink-0 mt-0.5" />
                <span><strong>Personalize Outreach:</strong> Messages with specific details get 5x more responses</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="h-5 w-5 flex-shrink-0 mt-0.5" />
                <span><strong>Follow Up:</strong> Send a follow-up message 3-5 days after applying</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="h-5 w-5 flex-shrink-0 mt-0.5" />
                <span><strong>Track Everything:</strong> Add notes to applications to remember context</span>
              </li>
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
