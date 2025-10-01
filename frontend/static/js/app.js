/**
 * capsule web interface
 */

class CapsuleApp {
    constructor() {
        this.token = localStorage.getItem('capsule_token');
        this.user_id = localStorage.getItem('capsule_user_id');
        this.api_base = window.location.origin;
        this.mode = 'input'; // 'input' or 'output'
        
        this.init();
    }
    
    init() {
        if (this.token && this.user_id) {
            this.showApp();
        } else {
            this.showAuth();
        }
        
        this.setupKeyboardShortcuts();
    }
    
    setupKeyboardShortcuts() {
        const input = document.getElementById('main-input');
        if (input) {
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.handleSubmit();
                }
            });
        }
        
        const loginPassword = document.getElementById('login-password');
        if (loginPassword) {
            loginPassword.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.login();
                }
            });
        }
        
        const registerPassword = document.getElementById('register-password');
        if (registerPassword) {
            registerPassword.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.register();
                }
            });
        }
    }
    
    showAuth() {
        document.getElementById('auth-screen').classList.remove('hidden');
        document.getElementById('app-screen').classList.add('hidden');
    }
    
    showApp() {
        document.getElementById('auth-screen').classList.add('hidden');
        document.getElementById('app-screen').classList.remove('hidden');
        document.getElementById('user-name').textContent = this.user_id;
        
        // Focus input
        setTimeout(() => {
            document.getElementById('main-input').focus();
        }, 100);
    }
    
    setMode(mode) {
        this.mode = mode;
        document.getElementById('input-mode').classList.toggle('active', mode === 'input');
        document.getElementById('output-mode').classList.toggle('active', mode === 'output');
        
        const input = document.getElementById('main-input');
        if (mode === 'input') {
            input.placeholder = 'type here...';
        } else {
            input.placeholder = 'ask something...';
        }
        
        input.focus();
    }
    
    showStatus(message, isThinking = false) {
        const statusEl = document.getElementById('status-message');
        statusEl.textContent = message;
        if (isThinking) {
            statusEl.classList.add('thinking');
        } else {
            statusEl.classList.remove('thinking');
        }
    }
    
    clearStatus() {
        setTimeout(() => {
            const statusEl = document.getElementById('status-message');
            statusEl.textContent = '';
            statusEl.classList.remove('thinking');
        }, 2000);
    }
    
    showOutput(text) {
        const outputEl = document.getElementById('output-content');
        outputEl.textContent = text;
    }
    
    clearOutput() {
        document.getElementById('output-content').textContent = '';
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
                throw new Error(errorData.detail || `http ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            throw error;
        }
    }
    
    switchAuthMode(mode) {
        const loginForm = document.getElementById('login-form');
        const registerForm = document.getElementById('register-form');
        
        if (mode === 'login') {
            loginForm.classList.remove('hidden');
            registerForm.classList.add('hidden');
        } else {
            loginForm.classList.add('hidden');
            registerForm.classList.remove('hidden');
        }
        
        document.getElementById('auth-message').textContent = '';
    }
    
    async register() {
        const user_id = document.getElementById('register-user').value.trim().toLowerCase();
        const password = document.getElementById('register-password').value;
        
        if (!user_id || !password) {
            document.getElementById('auth-message').textContent = 'please fill in all fields';
            return;
        }
        
        try {
            const formData = new FormData();
            formData.append('user_id', user_id);
            formData.append('password', password);
            
            await this.makeRequest('/register', {
                method: 'POST',
                body: formData
            });
            
            document.getElementById('auth-message').textContent = 'account created. signing in...';
            
            // Auto-login
            setTimeout(() => {
                document.getElementById('login-user').value = user_id;
                document.getElementById('login-password').value = password;
                this.switchAuthMode('login');
                this.login();
            }, 1000);
            
        } catch (error) {
            document.getElementById('auth-message').textContent = `error: ${error.message}`;
        }
    }
    
    async login() {
        const user_id = document.getElementById('login-user').value.trim().toLowerCase();
        const password = document.getElementById('login-password').value;
        
        if (!user_id || !password) {
            document.getElementById('auth-message').textContent = 'please fill in all fields';
            return;
        }
        
        try {
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
            
            document.getElementById('auth-message').textContent = 'welcome back.';
            
            setTimeout(() => {
                this.showApp();
            }, 500);
            
        } catch (error) {
            document.getElementById('auth-message').textContent = `error: ${error.message}`;
        }
    }
    
    logout() {
        this.token = null;
        this.user_id = null;
        localStorage.removeItem('capsule_token');
        localStorage.removeItem('capsule_user_id');
        
        document.getElementById('login-user').value = '';
        document.getElementById('login-password').value = '';
        document.getElementById('main-input').value = '';
        this.clearOutput();
        
        this.showAuth();
    }
    
    async handleSubmit() {
        const input = document.getElementById('main-input');
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
            this.showStatus('thinking', true);
            this.clearOutput();
            
            const formData = new FormData();
            formData.append('memory', memory);
            
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
            this.showStatus('thinking', true);
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
    app.switchAuthMode(mode);
}

function register() {
    app.register();
}

function login() {
    app.login();
}

function logout() {
    app.logout();
}

function setMode(mode) {
    app.setMode(mode);
}

// initialize
document.addEventListener('DOMContentLoaded', () => {
    app = new CapsuleApp();
});
