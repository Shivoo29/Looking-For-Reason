// Background service worker for Chrome extension

// Handle installation
chrome.runtime.onInstalled.addListener(() => {
  console.log('JobHack extension installed');
});

// Handle messages from popup or content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'authenticate') {
    handleAuthentication(request.data, sendResponse);
    return true;
  }

  if (request.action === 'logout') {
    handleLogout(sendResponse);
    return true;
  }
});

async function handleAuthentication(credentials, sendResponse) {
  try {
    // Call API to authenticate
    const response = await fetch('http://localhost:8000/api/v1/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        username: credentials.email,
        password: credentials.password,
      }),
    });

    if (!response.ok) {
      throw new Error('Authentication failed');
    }

    const data = await response.json();

    // Store auth token
    await chrome.storage.local.set({
      authToken: data.access_token,
    });

    sendResponse({ success: true });
  } catch (error) {
    sendResponse({ success: false, error: error.message });
  }
}

async function handleLogout(sendResponse) {
  await chrome.storage.local.remove(['authToken', 'defaultResume']);
  sendResponse({ success: true });
}

// Context menu for quick actions
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: 'extract-job',
    title: 'Extract Job with JobHack',
    contexts: ['page'],
  });

  chrome.contextMenus.create({
    id: 'quick-apply',
    title: 'Quick Apply with JobHack',
    contexts: ['page'],
  });
});

// Handle context menu clicks
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'extract-job') {
    chrome.tabs.sendMessage(tab.id, { action: 'extractJobInfo' });
  }

  if (info.menuItemId === 'quick-apply') {
    // Open popup
    chrome.action.openPopup();
  }
});
