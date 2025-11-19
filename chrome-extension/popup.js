// API Configuration
const API_URL = 'http://localhost:8000/api/v1';

// DOM Elements
const statusEl = document.getElementById('status');
const statusText = document.getElementById('status-text');
const errorEl = document.getElementById('error');
const errorText = document.getElementById('error-text');
const extractBtn = document.getElementById('extract-jd');
const autoFillBtn = document.getElementById('auto-fill');
const quickApplyBtn = document.getElementById('quick-apply');
const settingsBtn = document.getElementById('settings');
const resumeName = document.getElementById('resume-name');
const appCount = document.getElementById('app-count');
const atsScore = document.getElementById('ats-score');

// Initialize
async function init() {
  try {
    // Check auth status
    const token = await getAuthToken();
    if (!token) {
      showError('Not logged in. Please log in at jobhack.io');
      statusText.textContent = 'Not authenticated';
      return;
    }

    // Load user data
    await loadUserData(token);
    statusEl.classList.add('active');
    statusText.textContent = 'Ready';
  } catch (error) {
    showError('Error loading data: ' + error.message);
  }
}

async function getAuthToken() {
  const result = await chrome.storage.local.get(['authToken']);
  return result.authToken;
}

async function loadUserData(token) {
  // Get resumes
  const resumesRes = await fetch(`${API_URL}/resumes`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  if (!resumesRes.ok) {
    throw new Error('Failed to load resumes');
  }

  const resumes = await resumesRes.json();

  if (resumes.length > 0) {
    const defaultResume = resumes[0];
    resumeName.textContent = defaultResume.name;
    atsScore.textContent = defaultResume.ats_score.toFixed(0);
    await chrome.storage.local.set({ defaultResume });
  }

  // Get applications count
  const appsRes = await fetch(`${API_URL}/applications`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  if (appsRes.ok) {
    const apps = await appsRes.json();
    appCount.textContent = apps.length;
  }
}

function showError(message) {
  errorText.textContent = message;
  errorEl.style.display = 'block';
  setTimeout(() => {
    errorEl.style.display = 'none';
  }, 5000);
}

// Extract Job Description
extractBtn.addEventListener('click', async () => {
  try {
    statusText.textContent = 'Extracting...';

    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    // Send message to content script
    const response = await chrome.tabs.sendMessage(tab.id, {
      action: 'extractJobInfo'
    });

    if (response.success) {
      // Save to backend
      const token = await getAuthToken();
      const res = await fetch(`${API_URL}/job-descriptions`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          title: response.data.title,
          company: response.data.company,
          url: tab.url,
          text: response.data.description
        })
      });

      if (res.ok) {
        const jd = await res.json();
        await chrome.storage.local.set({ currentJob: jd });
        statusText.textContent = 'Job extracted!';
      } else {
        throw new Error('Failed to save job description');
      }
    } else {
      throw new Error(response.error || 'Failed to extract job info');
    }
  } catch (error) {
    showError(error.message);
    statusText.textContent = 'Error';
  }
});

// Auto-fill form
autoFillBtn.addEventListener('click', async () => {
  try {
    statusText.textContent = 'Auto-filling...';

    const { defaultResume } = await chrome.storage.local.get(['defaultResume']);

    if (!defaultResume) {
      throw new Error('No resume selected');
    }

    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    const response = await chrome.tabs.sendMessage(tab.id, {
      action: 'autoFill',
      data: {
        resume: defaultResume.parsed_data
      }
    });

    if (response.success) {
      statusText.textContent = 'Form filled!';
    } else {
      throw new Error(response.error || 'Failed to auto-fill');
    }
  } catch (error) {
    showError(error.message);
    statusText.textContent = 'Error';
  }
});

// Quick apply
quickApplyBtn.addEventListener('click', async () => {
  try {
    statusText.textContent = 'Applying...';

    // First extract job info
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    const extractRes = await chrome.tabs.sendMessage(tab.id, {
      action: 'extractJobInfo'
    });

    if (!extractRes.success) {
      throw new Error('Failed to extract job info');
    }

    const token = await getAuthToken();
    const { defaultResume } = await chrome.storage.local.get(['defaultResume']);

    if (!defaultResume) {
      throw new Error('No resume selected');
    }

    // Create job description
    const jdRes = await fetch(`${API_URL}/job-descriptions`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        title: extractRes.data.title,
        company: extractRes.data.company,
        url: tab.url,
        text: extractRes.data.description
      })
    });

    if (!jdRes.ok) {
      throw new Error('Failed to save job description');
    }

    const jd = await jdRes.json();

    // Create application
    const appRes = await fetch(`${API_URL}/applications`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        job_description_id: jd.id,
        resume_id: defaultResume.id,
        company: extractRes.data.company,
        position: extractRes.data.title,
        url: tab.url
      })
    });

    if (!appRes.ok) {
      throw new Error('Failed to create application');
    }

    // Auto-fill form
    const fillRes = await chrome.tabs.sendMessage(tab.id, {
      action: 'autoFill',
      data: {
        resume: defaultResume.parsed_data
      }
    });

    if (fillRes.success) {
      statusText.textContent = 'Applied! ✓';
      // Reload app count
      await loadUserData(token);
    } else {
      throw new Error('Failed to auto-fill form');
    }
  } catch (error) {
    showError(error.message);
    statusText.textContent = 'Error';
  }
});

// Settings
settingsBtn.addEventListener('click', () => {
  chrome.tabs.create({ url: 'http://localhost:3000/dashboard/settings' });
});

// Initialize on load
init();
