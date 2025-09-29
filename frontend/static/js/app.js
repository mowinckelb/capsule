/**
 * Capsule Web Interface JavaScript
 * Handles all frontend interactions with the API
 */

class CapsuleApp {
    constructor() {
        this.token = localStorage.getItem('capsule_token');
        this.user_id = localStorage.getItem('capsule_user_id');
        this.api_base = window.location.origin;
        this.mode = 'input';

        this.init();
    }

    init() {
        console.log('🚀 Initializing Capsule App');

        if (this.token && this.user_id) {
            this.showApp();
        } else {
            this.showAuth();
        }

        this.setupKeyboardShortcuts();
        this.updateModeUI();
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                const activeElement = document.activeElement;
                if (activeElement.id === 'memory-input') {
                    this.addMemory();
                } else if (activeElement.id === 'query-input') {
                    this.queryMemories();
                }
            }

            if (e.key.toLowerCase() === 'tab' && e.shiftKey) {
                e.preventDefault();
                this.toggleMode();
            }
        });
    }

    showAuth() {
        document.getElementById('auth-section').classList.remove('hidden');
        document.getElementById('app-section').classList.add('hidden');
        const sessionControls = document.getElementById('session-controls');
        if (sessionControls) {
            sessionControls.classList.add('hidden');
        }
        this.mode = 'input';
        this.updateModeUI();
        this.resetWorkspace();
    }

    showApp() {
        document.getElementById('auth-section').classList.add('hidden');
        document.getElementById('app-section').classList.remove('hidden');
        const sessionControls = document.getElementById('session-controls');
        if (sessionControls) {
            sessionControls.classList.remove('hidden');
        }
        document.getElementById('user-name').textContent = this.user_id;
        this.mode = 'input';
        this.updateModeUI();
        this.resetWorkspace();
    }

    resetWorkspace() {
        const results = document.getElementById('query-results');
        if (results) {
            results.classList.add('muted-state');
            results.innerHTML = 'Your answers will appear here once you ask a question.';
            results.style.opacity = '';
        }
        const loading = document.getElementById('loading-indicator');
        if (loading) {
            loading.classList.add('hidden');
        }
        const addMessage = document.getElementById('add-message');
        if (addMessage) {
            addMessage.innerHTML = '';
        }
        const authMessage = document.getElementById('auth-message');
        if (authMessage) {
            authMessage.innerHTML = '';
        }
    }

    showMessage(elementId, message, type = 'info') {
        const element = document.getElementById(elementId);
        if (!element) return;

        const classMap = {
            error: 'alert-error',
            success: 'alert-success',
            info: 'alert-info'
        };
        const alertClass = classMap[type] || classMap.info;

        element.innerHTML = `<div class="alert ${alertClass}">${message}</div>`;

        if (type !== 'error') {
            setTimeout(() => {
                if (element.innerHTML.includes(message)) {
                    element.innerHTML = '';
                }
            }, 2800);
        }
    }

    setLoadingState(isLoading) {
        const indicator = document.getElementById('loading-indicator');
        const results = document.getElementById('query-results');
        if (!indicator || !results) return;

        if (isLoading) {
            indicator.classList.remove('hidden');
            results.innerHTML = '';
            results.style.opacity = '0.35';
        } else {
            indicator.classList.add('hidden');
            results.style.opacity = '';
        }
    }

    updateModeUI() {
        const toggle = document.getElementById('mode-toggle');
        const inputPane = document.getElementById('input-pane');
        const outputPane = document.getElementById('output-pane');
        if (!toggle || !inputPane || !outputPane) {
            return;
        }

        toggle.setAttribute('data-mode', this.mode);
        toggle.setAttribute('aria-checked', String(this.mode === 'output'));
        toggle.setAttribute('aria-label', this.mode === 'output' ? 'Switch workspace to input mode' : 'Switch workspace to output mode');
        inputPane.classList.toggle('hidden', this.mode !== 'input');
        outputPane.classList.toggle('hidden', this.mode !== 'output');
    }

    ensureMode(mode) {
        if (this.mode !== mode) {
            this.mode = mode;
            this.updateModeUI();
        }
    }

    toggleMode() {
        this.mode = this.mode === 'input' ? 'output' : 'input';
        this.updateModeUI();
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
            console.log(`📡 Making request to ${endpoint}`);
            const response = await fetch(url, finalOptions);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
                throw new Error(errorData.detail || `HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('❌ Request failed:', error);
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

            await this.makeRequest('/register', {
                method: 'POST',
                body: formData
            });

            this.showMessage('auth-message', 'Registration successful! You can now login.', 'success');
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

            this.token = result.access_token;
            this.user_id = user_id;
            localStorage.setItem('capsule_token', this.token);
            localStorage.setItem('capsule_user_id', this.user_id);

            this.showMessage('auth-message', 'Login successful!', 'success');

            setTimeout(() => {
                this.showApp();
            }, 600);
        } catch (error) {
            this.showMessage('auth-message', `Login failed: ${error.message}`, 'error');
        }
    }

    logout() {
        this.token = null;
        this.user_id = null;
        localStorage.removeItem('capsule_token');
        localStorage.removeItem('capsule_user_id');

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

            await this.makeRequest('/add', {
                method: 'POST',
                body: formData
            });

            this.showMessage('add-message', '✅ Memory filed. I will recall it for you when asked.', 'success');
            document.getElementById('memory-input').value = '';
        } catch (error) {
            this.showMessage('add-message', `Failed to save memory: ${error.message}`, 'error');
        }
    }

    async queryMemories() {
        const queryInput = document.getElementById('query-input');
        const query = queryInput.value.trim();

        if (!query) {
            const resultsContainer = document.getElementById('query-results');
            if (resultsContainer) {
                resultsContainer.classList.remove('muted-state');
                resultsContainer.innerHTML = 'You need to ask a question before I can recall anything for you.';
            }
            return;
        }

        this.ensureMode('output');
        this.setLoadingState(true);

        try {
            const result = await this.makeRequest(`/query?q=${encodeURIComponent(query)}`);
            this.setLoadingState(false);
            this.displayQueryResults(result.results, query);
            queryInput.value = '';
        } catch (error) {
            this.setLoadingState(false);
            const resultsContainer = document.getElementById('query-results');
            if (resultsContainer) {
                resultsContainer.classList.remove('muted-state');
                resultsContainer.innerHTML = `<div class="alert alert-error">I could not search your memories because ${error.message}.</div>`;
            }
        }
    }

    displayQueryResults(results, query) {
        const resultsContainer = document.getElementById('query-results');
        if (!resultsContainer) return;

        if (!results || results === 'No matching memories found.') {
            resultsContainer.classList.remove('muted-state');
            resultsContainer.innerHTML = `You have not stored anything I can match to "${query}" yet. Add more detail and I will remember it for you.`;
            return;
        }

        const processed = this.formatResponse(results);
        resultsContainer.classList.remove('muted-state');
        resultsContainer.innerHTML = processed;
    }

    formatResponse(response) {
        if (typeof response !== 'string') {
            return '';
        }

        const secondPerson = this.convertToSecondPerson(response);
        return secondPerson
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>');
    }

    convertToSecondPerson(text) {
        let output = text;
        const matchCase = (original, replacement) => {
            if (original.toUpperCase() === original) {
                return replacement.toUpperCase();
            }
            if (original[0] && original[0] === original[0].toUpperCase()) {
                return replacement.charAt(0).toUpperCase() + replacement.slice(1);
            }
            return replacement;
        };

        const replacements = [
            { regex: /\b(I am|I'm)\b/gi, replacement: 'you are' },
            { regex: /\b(I have|I've)\b/gi, replacement: 'you have' },
            { regex: /\b(I will|I'll)\b/gi, replacement: 'you will' },
            { regex: /\b(I would|I'd)\b/gi, replacement: 'you would' },
            { regex: /\bI\b/gi, replacement: 'you' },
            { regex: /\bme\b/gi, replacement: 'you' },
            { regex: /\bmyself\b/gi, replacement: 'yourself' },
            { regex: /\bmy\b/gi, replacement: 'your' },
            { regex: /\bmine\b/gi, replacement: 'yours' }
        ];

        replacements.forEach(({ regex, replacement }) => {
            output = output.replace(regex, (match) => matchCase(match, replacement));
        });

        return output;
    }

    switchTab(tab) {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        const tabs = document.querySelectorAll('.tab');
        if (tab === 'login') {
            tabs[0].classList.add('active');
        } else {
            tabs[1].classList.add('active');
        }

        const loginForm = document.getElementById('login-form');
        const registerForm = document.getElementById('register-form');

        if (tab === 'login') {
            loginForm.classList.remove('hidden');
            registerForm.classList.add('hidden');
        } else {
            loginForm.classList.add('hidden');
            registerForm.classList.remove('hidden');
        }

        const authMessage = document.getElementById('auth-message');
        if (authMessage) {
            authMessage.innerHTML = '';
        }
    }

    handleQueryKeypress(event) {
        if (event.key === 'Enter') {
            this.queryMemories();
        }
    }
}

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

function toggleMode() {
    app.toggleMode();
}

window.addEventListener('DOMContentLoaded', () => {
    app = new CapsuleApp();
});