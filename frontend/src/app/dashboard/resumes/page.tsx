"use client";

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { FileText, Plus, Download, Trash2, Zap, TrendingUp } from 'lucide-react';
import { API } from '@/lib/api-client';
import { useStore } from '@/store/use-store';
import { formatRelativeTime, getScoreColor, getScoreLabel } from '@/lib/utils';

export default function ResumesPage() {
  const { resumes, setResumes } = useStore();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadResumes();
  }, []);

  const loadResumes = async () => {
    try {
      const data = await API.resumes.list();
      setResumes(data);
    } catch (error) {
      console.error('Failed to load resumes:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this resume?')) return;

    try {
      await API.resumes.delete(id);
      setResumes(resumes.filter(r => r.id !== id));
    } catch (error) {
      console.error('Failed to delete resume:', error);
    }
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
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="brutal-heading text-4xl mb-2">YOUR RESUMES</h1>
            <p className="brutal-text text-lg text-gray-700">
              Manage and optimize your resumes for different roles
            </p>
          </div>
          <Link href="/dashboard/resumes/upload">
            <Button size="lg">
              <Plus className="mr-2 h-5 w-5" />
              UPLOAD NEW
            </Button>
          </Link>
        </div>

        {resumes.length === 0 ? (
          <Card className="bg-gray-50">
            <CardContent className="py-16 text-center">
              <FileText className="h-16 w-16 mx-auto mb-4 text-gray-400" />
              <h3 className="font-bold text-2xl mb-2">NO RESUMES YET</h3>
              <p className="font-mono text-gray-600 mb-6">
                Upload your first resume to get started with AI optimization
              </p>
              <Link href="/dashboard/resumes/upload">
                <Button>
                  <Plus className="mr-2 h-5 w-5" />
                  UPLOAD RESUME
                </Button>
              </Link>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {resumes.map((resume) => (
              <Card key={resume.id} className="hover:shadow-brutal-lg transition-all">
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <CardTitle className="text-xl">{resume.name}</CardTitle>
                    <div className="flex flex-col items-end">
                      <div className={`text-3xl font-brutal ${getScoreColor(resume.atsScore)}`}>
                        {Math.round(resume.atsScore)}
                      </div>
                      <p className="font-mono text-xs">ATS SCORE</p>
                    </div>
                  </div>
                </CardHeader>

                <CardContent>
                  <Progress value={resume.atsScore} className="mb-4" />

                  <Badge
                    variant={resume.atsScore >= 80 ? 'success' : resume.atsScore >= 60 ? 'default' : 'destructive'}
                    className="mb-4"
                  >
                    {getScoreLabel(resume.atsScore)}
                  </Badge>

                  <p className="font-mono text-xs text-gray-600 mb-4">
                    Updated {formatRelativeTime(resume.updatedAt || resume.createdAt)}
                  </p>

                  <div className="space-y-2 font-mono text-sm">
                    {resume.atsScore < 80 && (
                      <div className="flex items-start gap-2">
                        <TrendingUp className="h-4 w-4 flex-shrink-0 mt-0.5 text-yellow-600" />
                        <span className="text-xs">
                          Can be improved by {Math.round(80 - resume.atsScore)} points
                        </span>
                      </div>
                    )}
                  </div>
                </CardContent>

                <CardFooter className="flex gap-2">
                  <Link href={`/dashboard/resumes/${resume.id}`} className="flex-1">
                    <Button variant="outline" size="sm" className="w-full">
                      VIEW
                    </Button>
                  </Link>
                  <Link href={`/dashboard/resumes/${resume.id}/optimize`} className="flex-1">
                    <Button size="sm" className="w-full">
                      <Zap className="mr-1 h-4 w-4" />
                      OPTIMIZE
                    </Button>
                  </Link>
                  <Button
                    variant="destructive"
                    size="sm"
                    onClick={() => handleDelete(resume.id)}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </CardFooter>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
