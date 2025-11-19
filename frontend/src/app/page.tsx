"use client";

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowRight, Zap, Target, Brain, TrendingUp, CheckCircle, XCircle } from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="border-b-4 border-black bg-white sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <Link href="/" className="text-3xl font-brutal">
            JOBHACK
          </Link>
          <nav className="hidden md:flex items-center gap-6">
            <Link href="#features" className="font-bold hover:underline">
              FEATURES
            </Link>
            <Link href="#pricing" className="font-bold hover:underline">
              PRICING
            </Link>
            <Link href="#how-it-works" className="font-bold hover:underline">
              HOW IT WORKS
            </Link>
          </nav>
          <div className="flex items-center gap-4">
            <Link href="/sign-in">
              <Button variant="ghost" size="sm">
                SIGN IN
              </Button>
            </Link>
            <Link href="/sign-up">
              <Button size="sm">
                START FREE
              </Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 md:py-32">
        <div className="max-w-5xl mx-auto text-center">
          <div className="inline-block mb-6 px-4 py-2 border-4 border-black bg-yellow-300 font-bold uppercase text-sm">
            3X MORE INTERVIEWS. GUARANTEED.
          </div>
          <h1 className="brutal-heading mb-8 text-5xl md:text-7xl lg:text-8xl">
            BRUTALLY EFFECTIVE JOB APPLICATIONS
          </h1>
          <p className="brutal-text text-xl md:text-2xl mb-12 max-w-3xl mx-auto">
            Stop wasting time on generic applications. JobHack uses AI to optimize your resume for every job,
            find hiring managers, and automate outreach. No fluff. Just results.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/sign-up">
              <Button size="lg" className="w-full sm:w-auto">
                START FREE TRIAL
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <Link href="#how-it-works">
              <Button variant="outline" size="lg" className="w-full sm:w-auto">
                SEE HOW IT WORKS
              </Button>
            </Link>
          </div>
          <p className="mt-6 font-mono text-sm text-gray-600">
            No credit card required • 5 free applications • Cancel anytime
          </p>
        </div>
      </section>

      {/* The Problem Section */}
      <section className="bg-red-500 text-white py-20 border-y-4 border-black">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <h2 className="brutal-heading mb-12 text-center text-4xl md:text-6xl">
              THE JOB HUNT IS BROKEN
            </h2>
            <div className="grid md:grid-cols-2 gap-8">
              <div className="flex items-start gap-4">
                <XCircle className="h-8 w-8 flex-shrink-0 mt-1" />
                <div>
                  <h3 className="font-bold text-xl mb-2">75% OF RESUMES GET REJECTED BY ATS</h3>
                  <p className="font-mono">Before a human even sees them. Missing keywords = instant rejection.</p>
                </div>
              </div>
              <div className="flex items-start gap-4">
                <XCircle className="h-8 w-8 flex-shrink-0 mt-1" />
                <div>
                  <h3 className="font-bold text-xl mb-2">11+ HOURS PER WEEK WASTED</h3>
                  <p className="font-mono">Tailoring resumes, filling forms, researching companies. Soul-crushing repetition.</p>
                </div>
              </div>
              <div className="flex items-start gap-4">
                <XCircle className="h-8 w-8 flex-shrink-0 mt-1" />
                <div>
                  <h3 className="font-bold text-xl mb-2">2% RESPONSE RATE ON COLD OUTREACH</h3>
                  <p className="font-mono">Generic messages to strangers. Nobody reads them. Nobody cares.</p>
                </div>
              </div>
              <div className="flex items-start gap-4">
                <XCircle className="h-8 w-8 flex-shrink-0 mt-1" />
                <div>
                  <h3 className="font-bold text-xl mb-2">FINDING DECISION-MAKERS IS IMPOSSIBLE</h3>
                  <p className="font-mono">Who actually makes hiring decisions? Good luck figuring that out.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <h2 className="brutal-heading mb-16 text-center text-4xl md:text-6xl">
            HOW JOBHACK DESTROYS THE COMPETITION
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 max-w-7xl mx-auto">
            <Card>
              <CardHeader>
                <div className="h-16 w-16 bg-yellow-300 border-4 border-black flex items-center justify-center mb-4">
                  <Brain className="h-8 w-8" />
                </div>
                <CardTitle>AI RESUME OPTIMIZATION</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="font-mono text-sm">
                  Upload once. Get ATS-optimized resumes for every job. Real-time scoring. Keyword matching. LaTeX output.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <div className="h-16 w-16 bg-blue-500 border-4 border-black flex items-center justify-center mb-4">
                  <Zap className="h-8 w-8 text-white" />
                </div>
                <CardTitle>ONE-CLICK APPLY</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="font-mono text-sm">
                  Chrome extension auto-fills applications on any job board. Apply to 50+ jobs while you eat lunch.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <div className="h-16 w-16 bg-green-500 border-4 border-black flex items-center justify-center mb-4">
                  <Target className="h-8 w-8 text-white" />
                </div>
                <CardTitle>FIND DECISION-MAKERS</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="font-mono text-sm">
                  AI scrapes LinkedIn and company data to find hiring managers. See org charts. Target the right people.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <div className="h-16 w-16 bg-pink-500 border-4 border-black flex items-center justify-center mb-4">
                  <TrendingUp className="h-8 w-8 text-white" />
                </div>
                <CardTitle>AUTOMATED OUTREACH</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="font-mono text-sm">
                  AI generates personalized emails and LinkedIn DMs. Track opens, clicks, and responses. Actually get replies.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="py-20 bg-yellow-300 border-y-4 border-black">
        <div className="container mx-auto px-4">
          <h2 className="brutal-heading mb-16 text-center text-4xl md:text-6xl">
            4 STEPS TO MORE INTERVIEWS
          </h2>
          <div className="max-w-4xl mx-auto space-y-12">
            <div className="flex gap-6">
              <div className="flex-shrink-0 h-16 w-16 bg-black text-white border-4 border-black flex items-center justify-center font-brutal text-3xl">
                1
              </div>
              <div>
                <h3 className="font-bold text-2xl mb-2">UPLOAD YOUR RESUME</h3>
                <p className="font-mono text-lg">
                  PDF, DOCX, or paste from LinkedIn. We extract your experience, skills, and achievements.
                </p>
              </div>
            </div>

            <div className="flex gap-6">
              <div className="flex-shrink-0 h-16 w-16 bg-black text-white border-4 border-black flex items-center justify-center font-brutal text-3xl">
                2
              </div>
              <div>
                <h3 className="font-bold text-2xl mb-2">PASTE JOB DESCRIPTION</h3>
                <p className="font-mono text-lg">
                  Copy-paste any JD. Our AI extracts required skills, keywords, and what the hiring manager actually wants.
                </p>
              </div>
            </div>

            <div className="flex gap-6">
              <div className="flex-shrink-0 h-16 w-16 bg-black text-white border-4 border-black flex items-center justify-center font-brutal text-3xl">
                3
              </div>
              <div>
                <h3 className="font-bold text-2xl mb-2">GET OPTIMIZED RESUME</h3>
                <p className="font-mono text-lg">
                  AI rewrites your resume to match the JD. ATS score 80+. Keyword density optimized. Download as PDF or LaTeX.
                </p>
              </div>
            </div>

            <div className="flex gap-6">
              <div className="flex-shrink-0 h-16 w-16 bg-black text-white border-4 border-black flex items-center justify-center font-brutal text-3xl">
                4
              </div>
              <div>
                <h3 className="font-bold text-2xl mb-2">APPLY + OUTREACH</h3>
                <p className="font-mono text-lg">
                  One-click apply with Chrome extension. AI finds hiring manager and drafts personalized outreach. Track everything in dashboard.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Social Proof */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <h2 className="brutal-heading mb-16 text-center text-4xl md:text-6xl">
            REAL RESULTS. NO BS.
          </h2>
          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            <Card className="bg-green-100">
              <CardContent className="pt-6">
                <div className="text-6xl font-brutal mb-4">300%</div>
                <p className="font-mono text-lg">
                  Average increase in interview invitations for JobHack users
                </p>
              </CardContent>
            </Card>

            <Card className="bg-blue-100">
              <CardContent className="pt-6">
                <div className="text-6xl font-brutal mb-4">92</div>
                <p className="font-mono text-lg">
                  Average ATS score after optimization (vs 64 before)
                </p>
              </CardContent>
            </Card>

            <Card className="bg-yellow-100">
              <CardContent className="pt-6">
                <div className="text-6xl font-brutal mb-4">18X</div>
                <p className="font-mono text-lg">
                  Faster application process. Apply to 50+ jobs in hours, not weeks.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-20 bg-black text-white">
        <div className="container mx-auto px-4">
          <h2 className="brutal-heading mb-16 text-center text-4xl md:text-6xl">
            SIMPLE PRICING. NO TRICKS.
          </h2>
          <div className="grid md:grid-cols-4 gap-8 max-w-7xl mx-auto">
            {/* Free */}
            <Card className="bg-white text-black">
              <CardHeader>
                <CardTitle>FREE</CardTitle>
                <div className="text-4xl font-brutal mt-4">$0</div>
                <p className="font-mono text-sm">Forever</p>
              </CardHeader>
              <CardContent>
                <ul className="space-y-3 font-mono text-sm">
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-5 w-5 flex-shrink-0 mt-0.5" />
                    <span>5 applications/month</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-5 w-5 flex-shrink-0 mt-0.5" />
                    <span>1 resume upload</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-5 w-5 flex-shrink-0 mt-0.5" />
                    <span>Basic ATS scoring</span>
                  </li>
                </ul>
                <Link href="/sign-up">
                  <Button variant="outline" className="w-full mt-6">
                    GET STARTED
                  </Button>
                </Link>
              </CardContent>
            </Card>

            {/* Pro */}
            <Card className="bg-yellow-300 text-black relative scale-105 shadow-brutal-lg">
              <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-black text-white px-4 py-1 font-bold text-sm border-2 border-black">
                MOST POPULAR
              </div>
              <CardHeader>
                <CardTitle>PRO</CardTitle>
                <div className="text-4xl font-brutal mt-4">$29</div>
                <p className="font-mono text-sm">per month</p>
              </CardHeader>
              <CardContent>
                <ul className="space-y-3 font-mono text-sm">
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-5 w-5 flex-shrink-0 mt-0.5" />
                    <span>Unlimited applications</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-5 w-5 flex-shrink-0 mt-0.5" />
                    <span>AI resume optimization</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-5 w-5 flex-shrink-0 mt-0.5" />
                    <span>Chrome extension</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-5 w-5 flex-shrink-0 mt-0.5" />
                    <span>Outreach automation</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-5 w-5 flex-shrink-0 mt-0.5" />
                    <span>Analytics dashboard</span>
                  </li>
                </ul>
                <Link href="/sign-up?plan=pro">
                  <Button className="w-full mt-6">
                    START 7-DAY TRIAL
                  </Button>
                </Link>
              </CardContent>
            </Card>

            {/* Team */}
            <Card className="bg-white text-black">
              <CardHeader>
                <CardTitle>TEAM</CardTitle>
                <div className="text-4xl font-brutal mt-4">$99</div>
                <p className="font-mono text-sm">per month</p>
              </CardHeader>
              <CardContent>
                <ul className="space-y-3 font-mono text-sm">
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-5 w-5 flex-shrink-0 mt-0.5" />
                    <span>Everything in Pro</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-5 w-5 flex-shrink-0 mt-0.5" />
                    <span>5 team members</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-5 w-5 flex-shrink-0 mt-0.5" />
                    <span>Shared resume library</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-5 w-5 flex-shrink-0 mt-0.5" />
                    <span>Team analytics</span>
                  </li>
                </ul>
                <Link href="/sign-up?plan=team">
                  <Button variant="outline" className="w-full mt-6">
                    GET STARTED
                  </Button>
                </Link>
              </CardContent>
            </Card>

            {/* Enterprise */}
            <Card className="bg-white text-black">
              <CardHeader>
                <CardTitle>ENTERPRISE</CardTitle>
                <div className="text-4xl font-brutal mt-4">$299</div>
                <p className="font-mono text-sm">per month</p>
              </CardHeader>
              <CardContent>
                <ul className="space-y-3 font-mono text-sm">
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-5 w-5 flex-shrink-0 mt-0.5" />
                    <span>Everything in Team</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-5 w-5 flex-shrink-0 mt-0.5" />
                    <span>Unlimited users</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-5 w-5 flex-shrink-0 mt-0.5" />
                    <span>API access</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-5 w-5 flex-shrink-0 mt-0.5" />
                    <span>White-label option</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-5 w-5 flex-shrink-0 mt-0.5" />
                    <span>Priority support</span>
                  </li>
                </ul>
                <Link href="/contact">
                  <Button variant="outline" className="w-full mt-6">
                    CONTACT SALES
                  </Button>
                </Link>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-yellow-300 border-t-4 border-black">
        <div className="container mx-auto px-4 text-center">
          <h2 className="brutal-heading mb-8 text-4xl md:text-6xl">
            STOP WASTING TIME.<br />START GETTING INTERVIEWS.
          </h2>
          <p className="brutal-text text-xl mb-12 max-w-2xl mx-auto">
            Join thousands of job seekers who landed their dream job 3x faster with JobHack.
          </p>
          <Link href="/sign-up">
            <Button size="lg">
              START FREE TRIAL
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </Link>
          <p className="mt-6 font-mono text-sm">
            No credit card required • 7-day free trial • Cancel anytime
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-black text-white py-12 border-t-4 border-black">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <h3 className="font-brutal text-2xl mb-4">JOBHACK</h3>
              <p className="font-mono text-sm text-gray-400">
                Brutally effective job applications. No fluff. Just results.
              </p>
            </div>
            <div>
              <h4 className="font-bold mb-4">PRODUCT</h4>
              <ul className="space-y-2 font-mono text-sm text-gray-400">
                <li><Link href="#features" className="hover:text-white">Features</Link></li>
                <li><Link href="#pricing" className="hover:text-white">Pricing</Link></li>
                <li><Link href="/changelog" className="hover:text-white">Changelog</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold mb-4">COMPANY</h4>
              <ul className="space-y-2 font-mono text-sm text-gray-400">
                <li><Link href="/about" className="hover:text-white">About</Link></li>
                <li><Link href="/blog" className="hover:text-white">Blog</Link></li>
                <li><Link href="/careers" className="hover:text-white">Careers</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold mb-4">LEGAL</h4>
              <ul className="space-y-2 font-mono text-sm text-gray-400">
                <li><Link href="/privacy" className="hover:text-white">Privacy</Link></li>
                <li><Link href="/terms" className="hover:text-white">Terms</Link></li>
                <li><Link href="/contact" className="hover:text-white">Contact</Link></li>
              </ul>
            </div>
          </div>
          <div className="mt-12 pt-8 border-t-2 border-gray-800 text-center font-mono text-sm text-gray-400">
            © 2024 JobHack. Built with rage and caffeine.
          </div>
        </div>
      </footer>
    </div>
  );
}
