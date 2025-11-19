"use client";

import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { TrendingUp, TrendingDown, Briefcase, Clock, CheckCircle2, Mail, Target } from 'lucide-react';
import { API } from '@/lib/api-client';

export default function AnalyticsPage() {
  const [stats, setStats] = useState<any>(null);
  const [appStats, setAppStats] = useState<any[]>([]);
  const [resumePerf, setResumePerf] = useState<any[]>([]);
  const [outreachStats, setOutreachStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    try {
      const [overview, applications, resumes, outreach] = await Promise.all([
        API.analytics.getOverview(),
        API.analytics.getApplicationStats(),
        API.analytics.getResumePerformance(),
        API.analytics.getOutreachStats(),
      ]);

      setStats(overview);
      setAppStats(applications);
      setResumePerf(resumes);
      setOutreachStats(outreach);
    } catch (error) {
      console.error('Failed to load analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-4xl font-brutal">LOADING ANALYTICS...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="brutal-heading text-4xl mb-2">ANALYTICS</h1>
          <p className="brutal-text text-lg text-gray-700">
            Track your job search performance and optimize your strategy
          </p>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          <Card className="bg-blue-100">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between mb-4">
                <Briefcase className="h-10 w-10" />
                <div className="text-4xl font-brutal">{stats?.totalApplications || 0}</div>
              </div>
              <p className="font-bold uppercase">Total Applications</p>
              <p className="font-mono text-sm text-gray-600">All time</p>
            </CardContent>
          </Card>

          <Card className="bg-yellow-100">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between mb-4">
                <Clock className="h-10 w-10" />
                <div className="text-4xl font-brutal">{stats?.activeApplications || 0}</div>
              </div>
              <p className="font-bold uppercase">Active</p>
              <p className="font-mono text-sm text-gray-600">In progress</p>
            </CardContent>
          </Card>

          <Card className="bg-green-100">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between mb-4">
                <CheckCircle2 className="h-10 w-10" />
                <div className="text-4xl font-brutal">{stats?.interviews || 0}</div>
              </div>
              <p className="font-bold uppercase">Interviews</p>
              <p className="font-mono text-sm text-gray-600">Scheduled</p>
            </CardContent>
          </Card>

          <Card className="bg-purple-100">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between mb-4">
                <TrendingUp className="h-10 w-10" />
                <div className="text-4xl font-brutal">{stats?.responseRate || 0}%</div>
              </div>
              <p className="font-bold uppercase">Response Rate</p>
              <p className="font-mono text-sm text-gray-600">
                {stats?.responseRate > 30 ? 'Excellent!' : stats?.responseRate > 15 ? 'Good' : 'Needs work'}
              </p>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-12">
          {/* Application Status Breakdown */}
          <Card>
            <CardHeader>
              <CardTitle>APPLICATION STATUS BREAKDOWN</CardTitle>
            </CardHeader>
            <CardContent>
              {appStats.length === 0 ? (
                <p className="font-mono text-gray-600 text-center py-8">
                  No data yet. Start applying to jobs!
                </p>
              ) : (
                <div className="space-y-4">
                  {appStats.map((stat: any) => (
                    <div key={stat.status}>
                      <div className="flex justify-between mb-2">
                        <span className="font-bold uppercase">{stat.status}</span>
                        <span className="font-mono">{stat.count} ({stat.percentage}%)</span>
                      </div>
                      <Progress value={stat.percentage} />
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Resume Performance */}
          <Card>
            <CardHeader>
              <CardTitle>RESUME PERFORMANCE</CardTitle>
            </CardHeader>
            <CardContent>
              {resumePerf.length === 0 ? (
                <p className="font-mono text-gray-600 text-center py-8">
                  Upload resumes to see performance data
                </p>
              ) : (
                <div className="space-y-4">
                  {resumePerf.map((resume: any) => (
                    <div key={resume.resume_id} className="brutal-border p-4">
                      <div className="flex justify-between items-start mb-2">
                        <div>
                          <p className="font-bold">{resume.resume_name}</p>
                          <p className="font-mono text-sm text-gray-600">
                            {resume.applications_count} applications
                          </p>
                        </div>
                        <div className="text-2xl font-brutal">{Math.round(resume.ats_score)}</div>
                      </div>
                      <Progress value={resume.ats_score} />
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Outreach Stats */}
        <Card className="mb-12">
          <CardHeader>
            <CardTitle>OUTREACH EFFECTIVENESS</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="brutal-border p-6 bg-white">
                <Mail className="h-8 w-8 mb-4" />
                <div className="text-3xl font-brutal mb-2">{outreachStats?.total_outreach || 0}</div>
                <p className="font-bold uppercase text-sm">Total Messages</p>
              </div>

              <div className="brutal-border p-6 bg-white">
                <Target className="h-8 w-8 mb-4" />
                <div className="text-3xl font-brutal mb-2">{outreachStats?.sent || 0}</div>
                <p className="font-bold uppercase text-sm">Sent</p>
              </div>

              <div className="brutal-border p-6 bg-white">
                <CheckCircle2 className="h-8 w-8 mb-4 text-green-600" />
                <div className="text-3xl font-brutal mb-2">{outreachStats?.replied || 0}</div>
                <p className="font-bold uppercase text-sm">Replies</p>
              </div>

              <div className="brutal-border p-6 bg-white">
                <TrendingUp className="h-8 w-8 mb-4 text-blue-600" />
                <div className="text-3xl font-brutal mb-2">{outreachStats?.reply_rate || 0}%</div>
                <p className="font-bold uppercase text-sm">Reply Rate</p>
              </div>
            </div>

            {outreachStats?.reply_rate > 0 && (
              <div className="mt-6 p-4 bg-yellow-100 border-4 border-black">
                <p className="font-bold mb-2">📊 INSIGHTS:</p>
                <p className="font-mono text-sm">
                  {outreachStats.reply_rate > 20
                    ? "🔥 Your outreach is crushing it! Keep it up."
                    : outreachStats.reply_rate > 10
                    ? "✅ Good reply rate. Try personalizing messages more."
                    : "⚠️ Low reply rate. Make messages more specific and personal."}
                </p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Tips */}
        <Card className="bg-green-100">
          <CardHeader>
            <CardTitle>💡 OPTIMIZATION TIPS</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-3 font-mono text-sm">
              <li className="flex items-start gap-2">
                <CheckCircle2 className="h-5 w-5 flex-shrink-0 mt-0.5" />
                <span>
                  <strong>Target 80+ ATS score:</strong> Optimize resumes to score above 80 for best results
                </span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="h-5 w-5 flex-shrink-0 mt-0.5" />
                <span>
                  <strong>Follow up:</strong> Send follow-up messages 3-5 days after applying
                </span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="h-5 w-5 flex-shrink-0 mt-0.5" />
                <span>
                  <strong>Track everything:</strong> Add notes to applications to remember context
                </span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="h-5 w-5 flex-shrink-0 mt-0.5" />
                <span>
                  <strong>Quality over quantity:</strong> 10 targeted applications beat 100 generic ones
                </span>
              </li>
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
