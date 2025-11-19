import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

export interface User {
  id: string;
  email: string;
  name: string;
  avatarUrl?: string;
  subscriptionTier: 'free' | 'pro' | 'team' | 'enterprise';
  subscriptionStatus: 'active' | 'canceled' | 'expired';
  createdAt: string;
}

export interface Resume {
  id: string;
  userId: string;
  name: string;
  fileName: string;
  fileUrl: string;
  parsedData: any;
  atsScore: number;
  createdAt: string;
  updatedAt: string;
}

export interface JobDescription {
  id: string;
  userId: string;
  title: string;
  company: string;
  url?: string;
  rawText: string;
  keywords: string[];
  requiredSkills: string[];
  preferredSkills: string[];
  parsedData: any;
  createdAt: string;
}

export interface Application {
  id: string;
  userId: string;
  resumeId: string;
  jobDescriptionId: string;
  company: string;
  position: string;
  url?: string;
  status: 'pending' | 'applied' | 'screening' | 'interview' | 'offer' | 'rejected' | 'accepted';
  appliedAt?: string;
  notes: string[];
  nextSteps: string[];
  createdAt: string;
  updatedAt: string;
}

export interface OutreachMessage {
  id: string;
  applicationId: string;
  contactName: string;
  contactTitle: string;
  contactLinkedin?: string;
  messageType: 'email' | 'linkedin';
  subject?: string;
  body: string;
  status: 'draft' | 'sent' | 'opened' | 'replied';
  sentAt?: string;
  openedAt?: string;
  repliedAt?: string;
  createdAt: string;
}

interface AppState {
  // User
  user: User | null;
  setUser: (user: User | null) => void;

  // Resumes
  resumes: Resume[];
  currentResume: Resume | null;
  setResumes: (resumes: Resume[]) => void;
  setCurrentResume: (resume: Resume | null) => void;
  addResume: (resume: Resume) => void;
  updateResume: (id: string, data: Partial<Resume>) => void;
  deleteResume: (id: string) => void;

  // Job Descriptions
  jobDescriptions: JobDescription[];
  currentJobDescription: JobDescription | null;
  setJobDescriptions: (jds: JobDescription[]) => void;
  setCurrentJobDescription: (jd: JobDescription | null) => void;
  addJobDescription: (jd: JobDescription) => void;
  deleteJobDescription: (id: string) => void;

  // Applications
  applications: Application[];
  setApplications: (apps: Application[]) => void;
  addApplication: (app: Application) => void;
  updateApplication: (id: string, data: Partial<Application>) => void;
  deleteApplication: (id: string) => void;

  // Outreach
  outreachMessages: OutreachMessage[];
  setOutreachMessages: (messages: OutreachMessage[]) => void;
  addOutreachMessage: (message: OutreachMessage) => void;
  updateOutreachMessage: (id: string, data: Partial<OutreachMessage>) => void;

  // UI State
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
  toggleSidebar: () => void;

  // Loading states
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;

  // Reset
  reset: () => void;
}

const initialState = {
  user: null,
  resumes: [],
  currentResume: null,
  jobDescriptions: [],
  currentJobDescription: null,
  applications: [],
  outreachMessages: [],
  sidebarOpen: true,
  isLoading: false,
};

export const useStore = create<AppState>()(
  persist(
    (set) => ({
      ...initialState,

      // User
      setUser: (user) => set({ user }),

      // Resumes
      setResumes: (resumes) => set({ resumes }),
      setCurrentResume: (currentResume) => set({ currentResume }),
      addResume: (resume) =>
        set((state) => ({ resumes: [...state.resumes, resume] })),
      updateResume: (id, data) =>
        set((state) => ({
          resumes: state.resumes.map((r) =>
            r.id === id ? { ...r, ...data } : r
          ),
        })),
      deleteResume: (id) =>
        set((state) => ({
          resumes: state.resumes.filter((r) => r.id !== id),
        })),

      // Job Descriptions
      setJobDescriptions: (jobDescriptions) => set({ jobDescriptions }),
      setCurrentJobDescription: (currentJobDescription) =>
        set({ currentJobDescription }),
      addJobDescription: (jd) =>
        set((state) => ({
          jobDescriptions: [...state.jobDescriptions, jd],
        })),
      deleteJobDescription: (id) =>
        set((state) => ({
          jobDescriptions: state.jobDescriptions.filter((jd) => jd.id !== id),
        })),

      // Applications
      setApplications: (applications) => set({ applications }),
      addApplication: (app) =>
        set((state) => ({ applications: [...state.applications, app] })),
      updateApplication: (id, data) =>
        set((state) => ({
          applications: state.applications.map((a) =>
            a.id === id ? { ...a, ...data } : a
          ),
        })),
      deleteApplication: (id) =>
        set((state) => ({
          applications: state.applications.filter((a) => a.id !== id),
        })),

      // Outreach
      setOutreachMessages: (outreachMessages) => set({ outreachMessages }),
      addOutreachMessage: (message) =>
        set((state) => ({
          outreachMessages: [...state.outreachMessages, message],
        })),
      updateOutreachMessage: (id, data) =>
        set((state) => ({
          outreachMessages: state.outreachMessages.map((m) =>
            m.id === id ? { ...m, ...data } : m
          ),
        })),

      // UI State
      setSidebarOpen: (sidebarOpen) => set({ sidebarOpen }),
      toggleSidebar: () =>
        set((state) => ({ sidebarOpen: !state.sidebarOpen })),

      // Loading
      setIsLoading: (isLoading) => set({ isLoading }),

      // Reset
      reset: () => set(initialState),
    }),
    {
      name: 'jobhack-storage',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        user: state.user,
        sidebarOpen: state.sidebarOpen,
      }),
    }
  )
);
