import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { ClerkProvider } from '@clerk/nextjs';

const inter = Inter({ subsets: ["latin"], variable: '--font-sans' });
const jetbrainsMono = JetBrains_Mono({ subsets: ["latin"], variable: '--font-mono' });

export const metadata: Metadata = {
  title: "JobHack - AI-Powered Job Application Automation",
  description: "Brutally effective job applications. No fluff. Just results. Automate your job search with AI-powered resume optimization, ATS scoring, and targeted outreach.",
  keywords: ["job search", "resume optimization", "ATS", "AI", "job application", "automation", "career"],
  authors: [{ name: "JobHack" }],
  openGraph: {
    title: "JobHack - AI-Powered Job Application Automation",
    description: "Land interviews 3x faster with AI-powered job application automation",
    type: "website",
    url: "https://jobhack.io",
  },
  twitter: {
    card: "summary_large_image",
    title: "JobHack - AI-Powered Job Application Automation",
    description: "Land interviews 3x faster with AI-powered job application automation",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClerkProvider>
      <html lang="en" className={`${inter.variable} ${jetbrainsMono.variable}`}>
        <body className="font-sans antialiased">
          {children}
        </body>
      </html>
    </ClerkProvider>
  );
}
