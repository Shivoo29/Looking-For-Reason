import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class APIClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000,
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        // Add auth token if available
        const token = this.getAuthToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Handle unauthorized
          this.handleUnauthorized();
        }
        return Promise.reject(error);
      }
    );
  }

  private getAuthToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('auth_token');
    }
    return null;
  }

  private handleUnauthorized(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token');
      window.location.href = '/sign-in';
    }
  }

  setAuthToken(token: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem('auth_token', token);
    }
  }

  clearAuthToken(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token');
    }
  }

  // Generic request methods
  async get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.get(url, config);
    return response.data;
  }

  async post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.post(url, data, config);
    return response.data;
  }

  async put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.put(url, data, config);
    return response.data;
  }

  async patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.patch(url, data, config);
    return response.data;
  }

  async delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.delete(url, config);
    return response.data;
  }

  // File upload
  async uploadFile<T = any>(url: string, file: File, onProgress?: (progress: number) => void): Promise<T> {
    const formData = new FormData();
    formData.append('file', file);

    const config: AxiosRequestConfig = {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(progress);
        }
      },
    };

    return this.post<T>(url, formData, config);
  }
}

export const apiClient = new APIClient();

// API Endpoints
export const API = {
  // Authentication
  auth: {
    login: (data: { email: string; password: string }) =>
      apiClient.post('/auth/login', data),
    register: (data: { email: string; password: string; name: string }) =>
      apiClient.post('/auth/register', data),
    logout: () =>
      apiClient.post('/auth/logout'),
  },

  // Users
  users: {
    getProfile: () =>
      apiClient.get('/users/me'),
    updateProfile: (data: any) =>
      apiClient.patch('/users/me', data),
  },

  // Resumes
  resumes: {
    list: () =>
      apiClient.get('/resumes'),
    get: (id: string) =>
      apiClient.get(`/resumes/${id}`),
    upload: (file: File, onProgress?: (progress: number) => void) =>
      apiClient.uploadFile('/resumes/upload', file, onProgress),
    delete: (id: string) =>
      apiClient.delete(`/resumes/${id}`),
    analyze: (id: string) =>
      apiClient.post(`/resumes/${id}/analyze`),
    optimize: (id: string, jobDescriptionId: string) =>
      apiClient.post(`/resumes/${id}/optimize`, { job_description_id: jobDescriptionId }),
    downloadLatex: (id: string) =>
      apiClient.get(`/resumes/${id}/latex`, { responseType: 'blob' }),
  },

  // Job Descriptions
  jobDescriptions: {
    list: () =>
      apiClient.get('/job-descriptions'),
    get: (id: string) =>
      apiClient.get(`/job-descriptions/${id}`),
    create: (data: { url?: string; text?: string; title: string; company: string }) =>
      apiClient.post('/job-descriptions', data),
    delete: (id: string) =>
      apiClient.delete(`/job-descriptions/${id}`),
    parse: (id: string) =>
      apiClient.post(`/job-descriptions/${id}/parse`),
    extractKeywords: (id: string) =>
      apiClient.post(`/job-descriptions/${id}/keywords`),
  },

  // Applications
  applications: {
    list: (params?: { status?: string; limit?: number; offset?: number }) =>
      apiClient.get('/applications', { params }),
    get: (id: string) =>
      apiClient.get(`/applications/${id}`),
    create: (data: {
      job_description_id: string;
      resume_id: string;
      company: string;
      position: string;
      url?: string;
    }) =>
      apiClient.post('/applications', data),
    update: (id: string, data: any) =>
      apiClient.patch(`/applications/${id}`, data),
    delete: (id: string) =>
      apiClient.delete(`/applications/${id}`),
    updateStatus: (id: string, status: string) =>
      apiClient.patch(`/applications/${id}/status`, { status }),
    addNote: (id: string, note: string) =>
      apiClient.post(`/applications/${id}/notes`, { note }),
  },

  // Organization Graph
  orgGraph: {
    get: (company: string) =>
      apiClient.get(`/org-graph/${encodeURIComponent(company)}`),
    findDecisionMakers: (company: string, position: string) =>
      apiClient.post(`/org-graph/${encodeURIComponent(company)}/decision-makers`, { position }),
    getProfile: (linkedinUrl: string) =>
      apiClient.post('/org-graph/profile', { linkedin_url: linkedinUrl }),
  },

  // Outreach
  outreach: {
    list: (applicationId: string) =>
      apiClient.get(`/outreach/${applicationId}`),
    generate: (data: {
      application_id: string;
      contact_name: string;
      contact_title: string;
      contact_linkedin?: string;
      message_type: 'email' | 'linkedin';
    }) =>
      apiClient.post('/outreach/generate', data),
    send: (id: string) =>
      apiClient.post(`/outreach/${id}/send`),
    track: (id: string) =>
      apiClient.get(`/outreach/${id}/track`),
  },

  // Analytics
  analytics: {
    getOverview: () =>
      apiClient.get('/analytics/overview'),
    getApplicationStats: (params?: { startDate?: string; endDate?: string }) =>
      apiClient.get('/analytics/applications', { params }),
    getResumePerformance: () =>
      apiClient.get('/analytics/resumes'),
    getOutreachStats: () =>
      apiClient.get('/analytics/outreach'),
  },

  // Subscription
  subscription: {
    getCurrent: () =>
      apiClient.get('/subscription'),
    createCheckout: (priceId: string) =>
      apiClient.post('/subscription/checkout', { price_id: priceId }),
    cancelSubscription: () =>
      apiClient.post('/subscription/cancel'),
    getUsage: () =>
      apiClient.get('/subscription/usage'),
  },
};
