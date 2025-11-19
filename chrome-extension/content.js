// Content script for job board scraping and auto-fill

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'extractJobInfo') {
    extractJobInfo(sendResponse);
    return true; // Keep channel open for async response
  }

  if (request.action === 'autoFill') {
    autoFillForm(request.data.resume, sendResponse);
    return true;
  }
});

// Extract job information from page
function extractJobInfo(sendResponse) {
  try {
    const hostname = window.location.hostname;
    let data = {};

    if (hostname.includes('linkedin.com')) {
      data = extractLinkedIn();
    } else if (hostname.includes('indeed.com')) {
      data = extractIndeed();
    } else if (hostname.includes('glassdoor.com')) {
      data = extractGlassdoor();
    } else {
      // Generic extraction
      data = extractGeneric();
    }

    sendResponse({ success: true, data });
  } catch (error) {
    sendResponse({ success: false, error: error.message });
  }
}

// LinkedIn extraction
function extractLinkedIn() {
  const title = document.querySelector('h1.job-title, h1.t-24')?.textContent?.trim() || '';
  const company = document.querySelector('a.job-card-container__company-name, .company-name')?.textContent?.trim() || '';
  const description = document.querySelector('.jobs-description, .description__text')?.textContent?.trim() || '';

  return { title, company, description };
}

// Indeed extraction
function extractIndeed() {
  const title = document.querySelector('h1.jobsearch-JobInfoHeader-title, h2.jobTitle')?.textContent?.trim() || '';
  const company = document.querySelector('[data-company-name="true"], .company')?.textContent?.trim() || '';
  const description = document.querySelector('#jobDescriptionText, .jobsearch-jobDescriptionText')?.textContent?.trim() || '';

  return { title, company, description };
}

// Glassdoor extraction
function extractGlassdoor() {
  const title = document.querySelector('[data-test="job-title"], h1')?.textContent?.trim() || '';
  const company = document.querySelector('[data-test="employer-name"], .employerName')?.textContent?.trim() || '';
  const description = document.querySelector('[data-test="description"], .desc')?.textContent?.trim() || '';

  return { title, company, description };
}

// Generic extraction
function extractGeneric() {
  // Try common patterns
  const title = document.querySelector('h1, .job-title, .position-title')?.textContent?.trim() || '';
  const company = document.querySelector('.company, .company-name, .employer')?.textContent?.trim() || '';

  // Get all text from page as description fallback
  const description = document.body.textContent?.trim().substring(0, 5000) || '';

  return { title, company, description };
}

// Auto-fill application form
function autoFillForm(resumeData, sendResponse) {
  try {
    const contact = resumeData.contact || {};
    const filled = [];

    // Common field patterns
    const fieldMappings = {
      // Name
      name: [
        'input[name*="name"]',
        'input[id*="name"]',
        'input[placeholder*="name"]'
      ],
      firstName: [
        'input[name*="first"]',
        'input[name*="fname"]',
        'input[id*="firstName"]'
      ],
      lastName: [
        'input[name*="last"]',
        'input[name*="lname"]',
        'input[id*="lastName"]'
      ],
      // Email
      email: [
        'input[type="email"]',
        'input[name*="email"]',
        'input[id*="email"]'
      ],
      // Phone
      phone: [
        'input[type="tel"]',
        'input[name*="phone"]',
        'input[id*="phone"]'
      ],
      // LinkedIn
      linkedin: [
        'input[name*="linkedin"]',
        'input[id*="linkedin"]',
        'input[placeholder*="linkedin"]'
      ],
      // Cover Letter / Summary
      coverLetter: [
        'textarea[name*="cover"]',
        'textarea[name*="letter"]',
        'textarea[id*="coverLetter"]'
      ]
    };

    // Fill name fields
    const nameParts = (contact.name || '').split(' ');
    fillField(fieldMappings.firstName, nameParts[0], filled);
    fillField(fieldMappings.lastName, nameParts.slice(1).join(' '), filled);
    fillField(fieldMappings.name, contact.name, filled);

    // Fill contact info
    fillField(fieldMappings.email, contact.email, filled);
    fillField(fieldMappings.phone, contact.phone, filled);
    fillField(fieldMappings.linkedin, contact.linkedin, filled);

    // Fill cover letter with summary
    const summary = resumeData.summary || 'I am excited to apply for this position.';
    fillField(fieldMappings.coverLetter, summary, filled);

    sendResponse({ success: true, filled });
  } catch (error) {
    sendResponse({ success: false, error: error.message });
  }
}

function fillField(selectors, value, filled) {
  if (!value) return;

  for (const selector of selectors) {
    const elements = document.querySelectorAll(selector);
    for (const el of elements) {
      if (el && !el.value) {
        el.value = value;
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
        filled.push(selector);
        return;
      }
    }
  }
}

// Add visual indicator when extension is active
const indicator = document.createElement('div');
indicator.id = 'jobhack-indicator';
indicator.textContent = 'JOBHACK ACTIVE';
indicator.style.cssText = `
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: #FFFF00;
  border: 4px solid black;
  padding: 12px 20px;
  font-weight: bold;
  z-index: 99999;
  box-shadow: 4px 4px 0 black;
  font-family: Arial, sans-serif;
  text-transform: uppercase;
`;
document.body.appendChild(indicator);

// Remove indicator after 3 seconds
setTimeout(() => {
  indicator.style.display = 'none';
}, 3000);
