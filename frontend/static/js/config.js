/**
 * Web Interface Configuration
 */

const WEB_CONFIG = {
    // API Configuration
    api: {
        base_url: window.location.origin,
        timeout: 30000,
        retry_attempts: 3
    },
    
    // UI Configuration
    ui: {
        theme: 'light',
        auto_save_interval: 30000, // 30 seconds
        message_timeout: 3000,     // 3 seconds
        animation_duration: 200    // 200ms
    },
    
    // Feature Flags
    features: {
        keyboard_shortcuts: true,
        auto_save: false,
        dark_mode: false,
        offline_mode: false
    },
    
    // Local Storage Keys
    storage: {
        token_key: 'capsule_token',
        user_key: 'capsule_user_id',
        theme_key: 'capsule_theme',
        draft_key: 'capsule_draft'
    },
    
    // Error Messages
    messages: {
        connection_error: 'Unable to connect to server. Please check your connection.',
        auth_required: 'Please login to continue.',
        invalid_input: 'Please check your input and try again.',
        server_error: 'Server error occurred. Please try again later.',
        success_save: 'Memory saved successfully!',
        success_login: 'Login successful!',
        success_register: 'Registration successful!'
    }
};

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WEB_CONFIG;
}
