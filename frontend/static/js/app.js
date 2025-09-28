/**
 * Capsule Web Interface JavaScript
 * Handles all frontend interactions with the API
 */

class CapsuleApp {
    constructor() {
        this.token = localStorage.getItem('capsule_token');
        this.user_id = localStorage.getItem('capsule_user_id');
        this.api_base = window.location.origin;
        
        // Initialize app
        this.init();
    }
    
    init() {
        console.log('🚀 Initializing Capsule App');
        
        // Check if user is already logged in
        if (this.token && this.user_id) {
            this.showApp();
        } else {
            this.showAuth();
        }
        
        // Add keyboard shortcuts
        this.setupKeyboardShortcuts();
    }
    
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + Enter to submit forms
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                const activeElement = document.activeElement;
                if (activeElement.id === 'memory-input') {
                    this.addMemory();
                } else if (activeElement.id === 'query-input') {
                    this.queryMemories();
                }
            }
        });
    }
    
    showAuth() {
        document.getElementById('auth-section').classList.remove('hidden');
        document.getElementById('app-section').classList.add('hidden');
    }
    
    showApp() {
        document.getElementById('auth-section').classList.add('hidden');
        document.getElementById('app-section').classList.remove('hidden');
        document.getElementById('user-name').textContent = this.user_id;
    }
    
    showMessage(elementId, message, type = 'info') {
        const element = document.getElementById(elementId);
        const alertClass = type === 'error' ? 'alert-error' : 'alert-success';
        element.innerHTML = `<div class="alert ${alertClass}">${message}</div>`;
        
        // Auto-hide success messages after 3 seconds
        if (type !== 'error') {
            setTimeout(() => {
                element.innerHTML = '';
            }, 3000);
        }
    }
    
    async makeRequest(endpoint, options = {}) {
        const url = `${this.api_base}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        // Add auth token if available
        if (this.token) {
            defaultOptions.headers['Authorization'] = `Bearer ${this.token}`;
        }
        
        // Handle form data
        if (options.body instanceof FormData) {
            delete defaultOptions.headers['Content-Type'];
        }
        
        const finalOptions = { ...defaultOptions, ...options };
        
        try {
            console.log(`📡 Making request to ${endpoint}`);
            const response = await fetch(url, finalOptions);
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
                throw new Error(errorData.detail || `HTTP ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error(`❌ Request failed:`, error);
            throw error;
        }
    }
    
    async register() {
        const user_id = document.getElementById('register-user').value.trim();
        const password = document.getElementById('register-password').value;
        
        if (!user_id || !password) {
            this.showMessage('auth-message', 'Please fill in all fields', 'error');
            return;
        }
        
        try {
            const formData = new FormData();
            formData.append('user_id', user_id);
            formData.append('password', password);
            
            const result = await this.makeRequest('/register', {
                method: 'POST',
                body: formData
            });
            
            this.showMessage('auth-message', 'Registration successful! You can now login.', 'success');
            
            // Switch to login tab and pre-fill user ID
            this.switchTab('login');
            document.getElementById('login-user').value = user_id;
            
        } catch (error) {
            this.showMessage('auth-message', `Registration failed: ${error.message}`, 'error');
        }
    }
    
    async login() {
        const user_id = document.getElementById('login-user').value.trim();
        const password = document.getElementById('login-password').value;
        
        if (!user_id || !password) {
            this.showMessage('auth-message', 'Please fill in all fields', 'error');
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
            
            // Store token and user info
            this.token = result.access_token;
            this.user_id = user_id;
            localStorage.setItem('capsule_token', this.token);
            localStorage.setItem('capsule_user_id', this.user_id);
            
            this.showMessage('auth-message', 'Login successful!', 'success');
            
            // Show main app after brief delay
            setTimeout(() => {
                this.showApp();
            }, 1000);
            
        } catch (error) {
            this.showMessage('auth-message', `Login failed: ${error.message}`, 'error');
        }
    }
    
    logout() {
        this.token = null;
        this.user_id = null;
        localStorage.removeItem('capsule_token');
        localStorage.removeItem('capsule_user_id');
        
        // Clear forms
        document.getElementById('login-user').value = '';
        document.getElementById('login-password').value = '';
        document.getElementById('memory-input').value = '';
        document.getElementById('query-input').value = '';
        
        this.showAuth();
    }
    
    async addMemory() {
        const memory = document.getElementById('memory-input').value.trim();
        
        if (!memory) {
            this.showMessage('add-message', 'Please enter a memory to save', 'error');
            return;
        }
        
        try {
            this.showMessage('add-message', '💾 Saving memory...', 'info');
            
            const formData = new FormData();
            formData.append('memory', memory);
            
            const result = await this.makeRequest('/add', {
                method: 'POST',
                body: formData
            });
            
            this.showMessage('add-message', '✅ Memory saved successfully!', 'success');
            document.getElementById('memory-input').value = '';
            
        } catch (error) {
            this.showMessage('add-message', `Failed to save memory: ${error.message}`, 'error');
        }
    }
    
    async queryMemories() {
        const query = document.getElementById('query-input').value.trim();
        
        if (!query) {
            this.showMessage('query-results', '<div class="alert alert-error">Please enter a question</div>');
            return;
        }
        
        try {
            // Show loading state
            document.getElementById('query-results').innerHTML = 
                '<div class="loading">🔍 Searching your memories...</div>';
            
            const result = await this.makeRequest(`/query?q=${encodeURIComponent(query)}`);
            
            // Display results
            this.displayQueryResults(result.results, query);
            
            // Clear input
            document.getElementById('query-input').value = '';
            
        } catch (error) {
            document.getElementById('query-results').innerHTML = 
                `<div class="alert alert-error">Search failed: ${error.message}</div>`;
        }
    }
    
    displayQueryResults(results, query) {
        const resultsContainer = document.getElementById('query-results');
        
        if (!results || results === "No matching memories found.") {
            resultsContainer.innerHTML = `
                <div class="memory-result">
                    <h3>🤔 No Results Found</h3>
                    <p>I couldn't find any memories related to "${query}". Try asking about something you've saved before, or save some memories first!</p>
                </div>
            `;
            return;
        }
        
        resultsContainer.innerHTML = `
            <div class="memory-result">
                <h3>💡 Answer</h3>
                <p>${this.formatResponse(results)}</p>
            </div>
        `;
    }
    
    formatResponse(response) {
        // Basic formatting for better readability
        return response
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>');
    }
    
    switchTab(tab) {
        // Update tab appearance
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelector(`.tab:nth-child(${tab === 'login' ? '1' : '2'})`).classList.add('active');
        
        // Show/hide forms
        const loginForm = document.getElementById('login-form');
        const registerForm = document.getElementById('register-form');
        
        if (tab === 'login') {
            loginForm.classList.remove('hidden');
            registerForm.classList.add('hidden');
        } else {
            loginForm.classList.add('hidden');
            registerForm.classList.remove('hidden');
        }
        
        // Clear any previous messages
        document.getElementById('auth-message').innerHTML = '';
    }
    
    handleQueryKeypress(event) {
        if (event.key === 'Enter') {
            this.queryMemories();
        }
    }
}

// Global functions for HTML onclick handlers
let app;

function switchTab(tab) {
    app.switchTab(tab);
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

function addMemory() {
    app.addMemory();
}

function queryMemories() {
    app.queryMemories();
}

function handleQueryKeypress(event) {
    app.handleQueryKeypress(event);
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    app = new CapsuleApp();
});
