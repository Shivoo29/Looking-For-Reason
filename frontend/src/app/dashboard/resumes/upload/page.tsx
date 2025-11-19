"use client";

import { useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { useDropzone } from 'react-dropzone';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Progress } from '@/components/ui/progress';
import { Upload, FileText, CheckCircle2, XCircle, Loader2 } from 'lucide-react';
import { API } from '@/lib/api-client';
import { useStore } from '@/store/use-store';

export default function ResumeUploadPage() {
  const router = useRouter();
  const { addResume } = useStore();
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState('');
  const [resumeName, setResumeName] = useState('');

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    setUploading(true);
    setUploadStatus('uploading');
    setUploadProgress(0);

    try {
      const resume = await API.resumes.upload(
        file,
        (progress) => setUploadProgress(progress)
      );

      addResume(resume);
      setUploadStatus('success');

      setTimeout(() => {
        router.push('/dashboard/resumes');
      }, 2000);
    } catch (error: any) {
      setUploadStatus('error');
      setErrorMessage(error.message || 'Failed to upload resume');
    } finally {
      setUploading(false);
    }
  }, [addResume, router]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt']
    },
    maxFiles: 1,
    disabled: uploading
  });

  return (
    <div className="min-h-screen bg-white">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="brutal-heading text-4xl mb-4">UPLOAD RESUME</h1>
          <p className="brutal-text text-lg text-gray-700">
            Upload your resume and get instant ATS scoring and optimization suggestions.
          </p>
        </div>

        <div className="max-w-3xl mx-auto">
          <Card className="mb-8">
            <CardHeader>
              <CardTitle>SUPPORTED FORMATS</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-3 gap-4">
                <div className="flex items-center gap-2">
                  <FileText className="h-6 w-6" />
                  <span className="font-bold">PDF</span>
                </div>
                <div className="flex items-center gap-2">
                  <FileText className="h-6 w-6" />
                  <span className="font-bold">DOCX</span>
                </div>
                <div className="flex items-center gap-2">
                  <FileText className="h-6 w-6" />
                  <span className="font-bold">TXT</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className={`mb-8 ${isDragActive ? 'bg-yellow-100' : ''}`}>
            <CardContent className="pt-6">
              <div
                {...getRootProps()}
                className={`brutal-border p-12 text-center cursor-pointer hover:bg-gray-50 transition-colors ${
                  isDragActive ? 'bg-yellow-100' : 'bg-white'
                }`}
              >
                <input {...getInputProps()} />

                {uploadStatus === 'idle' && (
                  <>
                    <Upload className="h-16 w-16 mx-auto mb-4" />
                    <h3 className="font-bold text-xl mb-2">
                      {isDragActive ? 'DROP IT HERE!' : 'DRAG & DROP YOUR RESUME'}
                    </h3>
                    <p className="font-mono text-gray-600">
                      or click to browse files
                    </p>
                  </>
                )}

                {uploadStatus === 'uploading' && (
                  <>
                    <Loader2 className="h-16 w-16 mx-auto mb-4 animate-spin" />
                    <h3 className="font-bold text-xl mb-4">UPLOADING...</h3>
                    <Progress value={uploadProgress} className="max-w-md mx-auto" />
                    <p className="font-mono text-sm mt-2">{uploadProgress}%</p>
                  </>
                )}

                {uploadStatus === 'success' && (
                  <>
                    <CheckCircle2 className="h-16 w-16 mx-auto mb-4 text-green-600" />
                    <h3 className="font-bold text-xl mb-2 text-green-600">
                      SUCCESS!
                    </h3>
                    <p className="font-mono">Redirecting to resumes...</p>
                  </>
                )}

                {uploadStatus === 'error' && (
                  <>
                    <XCircle className="h-16 w-16 mx-auto mb-4 text-red-600" />
                    <h3 className="font-bold text-xl mb-2 text-red-600">
                      UPLOAD FAILED
                    </h3>
                    <p className="font-mono text-red-600">{errorMessage}</p>
                    <Button
                      className="mt-4"
                      onClick={() => setUploadStatus('idle')}
                    >
                      TRY AGAIN
                    </Button>
                  </>
                )}
              </div>
            </CardContent>
          </Card>

          <Card className="bg-blue-100">
            <CardHeader>
              <CardTitle>💡 TIPS FOR BEST RESULTS</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 font-mono text-sm">
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="h-5 w-5 flex-shrink-0 mt-0.5" />
                  <span>Use a clean, ATS-friendly format (no tables or graphics)</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="h-5 w-5 flex-shrink-0 mt-0.5" />
                  <span>Include all relevant skills and experience</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="h-5 w-5 flex-shrink-0 mt-0.5" />
                  <span>Keep file size under 5MB</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="h-5 w-5 flex-shrink-0 mt-0.5" />
                  <span>PDF format recommended for best parsing</span>
                </li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
