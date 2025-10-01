/**
 * capsule web interface
 */

class CapsuleApp {
    constructor() {
        this.token = localStorage.getItem('capsule_token');
        this.user_id = localStorage.getItem('capsule_user_id');
        this.api_base = window.location.origin;
        this.mode = 'input';
        this.authMode = 'login';
        
        this.init();
    }
    
    init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.initAfterDOM());
        } else {
            this.initAfterDOM();
        }
    }
    
    initAfterDOM() {
        if (this.token && this.user_id) {
            this.showApp();
        } else {
            this.showAuth();
        }
        
        this.setupKeyboardShortcuts();
    }
    
    setupKeyboardShortcuts() {
        // Auth screen navigation
        const authUsername = document.getElementById('auth-username');
        const authPassword = document.getElementById('auth-password');
        
        if (authUsername) {
            authUsername.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    authPassword.focus();
                }
            });
        }
        
        if (authPassword) {
            authPassword.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    this.handleAuth();
                } else if (e.key === 'ArrowUp') {
                    e.preventDefault();
                    this.switchAuthMode(this.authMode === 'login' ? 'register' : 'login');
                }
            });
        }
        
        if (authUsername) {
            authUsername.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowUp') {
                    e.preventDefault();
                    this.switchAuthMode(this.authMode === 'login' ? 'register' : 'login');
                }
            });
        }
        
        // Main input
        const mainInput = document.getElementById('main-input');
        if (mainInput) {
            mainInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    this.handleSubmit();
                } else if (e.key === 'ArrowUp') {
                    e.preventDefault();
                    // Toggle mode without changing focus
                    if (this.mode === 'input') {
                        this.setMode('output');
                    } else {
                        this.setMode('input');
                    }
                }
            });
        }
        
        // Toggle container navigation
        const toggleContainer = document.getElementById('toggle-container');
        if (toggleContainer) {
            toggleContainer.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowLeft') {
                    e.preventDefault();
                    this.setMode('input');
                } else if (e.key === 'ArrowRight') {
                    e.preventDefault();
                    this.setMode('output');
                } else if (e.key === 'Enter' || e.key === 'ArrowDown') {
                    e.preventDefault();
                    if (mainInput) mainInput.focus();
                }
            });
        }
    }
    
    showAuth() {
        const authScreen = document.getElementById('auth-screen');
        const appScreen = document.getElementById('app-screen');
        if (authScreen) authScreen.classList.remove('hidden');
        if (appScreen) appScreen.classList.add('hidden');
        
        // Auto-focus username field
        setTimeout(() => {
            const authUsername = document.getElementById('auth-username');
            if (authUsername) authUsername.focus();
        }, 100);
    }
    
    showApp() {
        const authScreen = document.getElementById('auth-screen');
        const appScreen = document.getElementById('app-screen');
        const userName = document.getElementById('user-name');
        
        if (authScreen) authScreen.classList.add('hidden');
        if (appScreen) appScreen.classList.remove('hidden');
        if (userName) userName.textContent = this.user_id;
        
        // Load provider info
        this.loadProviders();
        
        setTimeout(() => {
            const mainInput = document.getElementById('main-input');
            if (mainInput) mainInput.focus();
        }, 100);
    }
    
    async loadProviders() {
        try {
            const data = await this.makeRequest('/providers');
            const llmProvider = document.getElementById('llm-provider');
            const storageProvider = document.getElementById('storage-provider');
            if (llmProvider) llmProvider.textContent = data.llm;
            if (storageProvider) storageProvider.textContent = data.storage;
        } catch (error) {
            console.error('Failed to load providers:', error);
        }
    }
    
    switchAuthMode(mode) {
        this.authMode = mode;
        const slider = document.getElementById('auth-slider');
        const submitBtn = document.getElementById('auth-submit-btn');
        const loginToggle = document.getElementById('login-toggle');
        const registerToggle = document.getElementById('register-toggle');
        
        if (mode === 'register') {
            if (slider) slider.classList.add('register');
            if (submitBtn) submitBtn.textContent = 'sign up';
            if (loginToggle) loginToggle.classList.remove('active');
            if (registerToggle) registerToggle.classList.add('active');
        } else {
            if (slider) slider.classList.remove('register');
            if (submitBtn) submitBtn.textContent = 'sign in';
            if (loginToggle) loginToggle.classList.add('active');
            if (registerToggle) registerToggle.classList.remove('active');
        }
    }
    
    setMode(mode) {
        this.mode = mode;
        const slider = document.getElementById('mode-slider');
        const inputBtn = document.getElementById('input-mode-btn');
        const outputBtn = document.getElementById('output-mode-btn');
        
        if (mode === 'output') {
            if (slider) slider.classList.add('output');
            if (inputBtn) inputBtn.classList.remove('active');
            if (outputBtn) outputBtn.classList.add('active');
        } else {
            if (slider) slider.classList.remove('output');
            if (inputBtn) inputBtn.classList.add('active');
            if (outputBtn) outputBtn.classList.remove('active');
        }
        
        const mainInput = document.getElementById('main-input');
        if (mainInput) mainInput.focus();
    }
    
    showStatus(message, isThinking = false) {
        const statusEl = document.getElementById('status-message');
        if (!statusEl) return;
        
        if (isThinking) {
            statusEl.innerHTML = '<span class="thinking"><span class="thinking-dot"></span></span>';
        } else {
            statusEl.textContent = message;
        }
    }
    
    clearStatus() {
        setTimeout(() => {
            const statusEl = document.getElementById('status-message');
            if (statusEl) statusEl.textContent = '';
        }, 2000);
    }
    
    showOutput(text) {
        const outputEl = document.getElementById('output-content');
        if (outputEl) outputEl.textContent = text;
    }
    
    clearOutput() {
        const outputEl = document.getElementById('output-content');
        if (outputEl) outputEl.textContent = '';
    }
    
    async makeRequest(endpoint, options = {}) {
        const url = `${this.api_base}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        if (this.token) {
            defaultOptions.headers['Authorization'] = `Bearer ${this.token}`;
        }
        
        if (options.body instanceof FormData) {
            delete defaultOptions.headers['Content-Type'];
        }
        
        const finalOptions = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(url, finalOptions);
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'unknown error' }));
                throw new Error((errorData.detail || `http ${response.status}`).toLowerCase());
            }
            
            return await response.json();
        } catch (error) {
            throw error;
        }
    }
    
    async handleAuth() {
        const username = document.getElementById('auth-username');
        const password = document.getElementById('auth-password');
        const messageEl = document.getElementById('auth-message');
        
        if (!username || !password) return;
        
        const user_id = username.value.trim().toLowerCase();
        const pass = password.value;
        
        if (!user_id || !pass) {
            if (messageEl) messageEl.textContent = 'please fill in all fields';
            return;
        }
        
        try {
            if (this.authMode === 'register') {
                await this.register(user_id, pass);
            } else {
                await this.login(user_id, pass);
            }
        } catch (error) {
            if (messageEl) messageEl.textContent = `error: ${error.message}`;
        }
    }
    
    async register(user_id, password) {
        const formData = new FormData();
        formData.append('user_id', user_id);
        formData.append('password', password);
        
        await this.makeRequest('/register', {
            method: 'POST',
            body: formData
        });
        
        // Auto-login after registration
        await this.login(user_id, password);
    }
    
    async login(user_id, password) {
        const formData = new FormData();
        formData.append('username', user_id);
        formData.append('password', password);
        
        const result = await this.makeRequest('/login', {
            method: 'POST',
            body: formData
        });
        
        this.token = result.access_token;
        this.user_id = user_id;
        localStorage.setItem('capsule_token', this.token);
        localStorage.setItem('capsule_user_id', this.user_id);
        
        this.showApp();
    }
    
    logout() {
        this.token = null;
        this.user_id = null;
        localStorage.removeItem('capsule_token');
        localStorage.removeItem('capsule_user_id');
        
        const authUsername = document.getElementById('auth-username');
        const authPassword = document.getElementById('auth-password');
        const authMessage = document.getElementById('auth-message');
        const mainInput = document.getElementById('main-input');
        
        if (authUsername) authUsername.value = '';
        if (authPassword) authPassword.value = '';
        if (authMessage) authMessage.textContent = '';
        if (mainInput) mainInput.value = '';
        
        this.clearOutput();
        this.showAuth();
    }
    
    async handleSubmit() {
        const input = document.getElementById('main-input');
        if (!input) return;
        
        const text = input.value.trim();
        if (!text) return;
        
        input.value = '';
        
        if (this.mode === 'input') {
            await this.addMemory(text);
        } else {
            await this.queryMemories(text);
        }
    }
    
    async addMemory(memory) {
        try {
            this.showStatus('', true);
            this.clearOutput();
            
            // Add timestamp context for temporal understanding
            const now = new Date();
            const timestamp = now.toISOString();
            const dayOfWeek = now.toLocaleDateString('en-US', { weekday: 'long' });
            const dateStr = now.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
            const timeStr = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
            
            const contextualMemory = `[${timestamp}] [${dayOfWeek}, ${dateStr} at ${timeStr}] ${memory}`;
            
            const formData = new FormData();
            formData.append('memory', contextualMemory);
            
            await this.makeRequest('/add', {
                method: 'POST',
                body: formData
            });
            
            this.showStatus('memory saved.');
            this.clearStatus();
        } catch (error) {
            this.showStatus(`error: ${error.message}`);
            this.clearStatus();
        }
    }
    
    async queryMemories(query) {
        try {
            this.showStatus('', true);
            this.clearOutput();
            
            const result = await this.makeRequest(`/query?q=${encodeURIComponent(query)}`);
            
            this.showStatus('');
            
            if (!result.results || result.results === "No matching memories found.") {
                this.showOutput("i don't have any memories about that yet.");
            } else {
                this.showOutput(result.results);
            }
        } catch (error) {
            this.showStatus('');
            this.showOutput(`error: ${error.message}`);
        }
    }
}

// global functions
let app;

function switchAuthMode(mode) {
    if (!app) { console.error('App not initialized'); return; }
    app.switchAuthMode(mode);
}

function handleAuth() {
    if (!app) { console.error('App not initialized'); return; }
    app.handleAuth();
}

function logout() {
    if (!app) { console.error('App not initialized'); return; }
    app.logout();
}

function setMode(mode) {
    if (!app) { console.error('App not initialized'); return; }
    app.setMode(mode);
}

function handleSubmit() {
    if (!app) { console.error('App not initialized'); return; }
    app.handleSubmit();
}

// initialize when script loads
app = new CapsuleApp();
