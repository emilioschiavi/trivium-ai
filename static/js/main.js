/**
 * Main Application Module
 * Handles page initialization, UI updates, and event listeners
 */

const WeatherApp = (function () {
    'use strict';

    // Application state
    let forecastData = [];
    let currentPreferences = {};

    /**
     * Initialize the application
     */
    function init() {
        console.log('Weather Sport Planner initializing...');

        // Load forecast data from template (injected by Django)
        if (typeof window.forecastData !== 'undefined') {
            forecastData = window.forecastData;
            console.log('Forecast data loaded:', forecastData);
        }

        // Load and apply preferences
        currentPreferences = PreferencesManager.load();
        PreferencesManager.populateForm(currentPreferences);

        // Set up event listeners
        setupEventListeners();

        // Show success message
        showNotification('Application loaded successfully', 'success');
    }

    /**
     * Set up all event listeners
     */
    function setupEventListeners() {
        // Preferences form submission
        const preferencesForm = document.getElementById('preferencesForm');
        if (preferencesForm) {
            preferencesForm.addEventListener('submit', handlePreferencesSubmit);
        }

        // Reset button
        const resetBtn = document.getElementById('resetBtn');
        if (resetBtn) {
            resetBtn.addEventListener('click', handlePreferencesReset);
        }

        // Real-time preference changes (optional - show preview)
        const preferenceInputs = document.querySelectorAll('#preferencesForm input');
        preferenceInputs.forEach(function (input) {
            input.addEventListener('change', handlePreferenceChange);
        });
    }

    /**
     * Handle preferences form submission
     * @param {Event} event - Form submit event
     */
    function handlePreferencesSubmit(event) {
        event.preventDefault();

        try {
            // Read preferences from form
            const prefs = PreferencesManager.readFromForm();

            // Validate and save
            if (PreferencesManager.save(prefs)) {
                showNotification('✅ Preferences saved successfully!', 'success');

                // Update current preferences
                currentPreferences = prefs;

                // Reload page to apply new preferences
                setTimeout(function () {
                    location.reload();
                }, 1000);
            } else {
                showNotification('❌ Failed to save preferences. Please check your values.', 'error');
            }
        } catch (error) {
            console.error('Error saving preferences:', error);
            showNotification('❌ An error occurred while saving preferences.', 'error');
        }
    }

    /**
     * Handle preferences reset
     */
    function handlePreferencesReset() {
        if (confirm('🔄 Reset all preferences to defaults?')) {
            try {
                PreferencesManager.reset();
                showNotification('✅ Preferences reset to defaults!', 'success');

                // Reload page
                setTimeout(function () {
                    location.reload();
                }, 1000);
            } catch (error) {
                console.error('Error resetting preferences:', error);
                showNotification('❌ Failed to reset preferences.', 'error');
            }
        }
    }

    /**
     * Handle real-time preference changes (preview)
     * @param {Event} event - Input change event
     */
    function handlePreferenceChange(event) {
        // Optional: Could show real-time preview of recommendations
        // For now, just log the change
        console.log('Preference changed:', event.target.name, event.target.value);
    }

    /**
     * Show notification message to user
     * @param {string} message - Notification message
     * @param {string} type - Notification type (success, error, info)
     */
    function showNotification(message, type) {
        type = type || 'info';

        // Check if notification exists, create if not
        let notification = document.getElementById('app-notification');

        if (!notification) {
            notification = document.createElement('div');
            notification.id = 'app-notification';
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 15px 20px;
                border-radius: 8px;
                font-size: 1rem;
                font-weight: 500;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                z-index: 9999;
                animation: slideInRight 0.3s ease-out;
                max-width: 400px;
            `;
            document.body.appendChild(notification);
        }

        // Set notification style based on type
        const colors = {
            success: { bg: '#4caf50', text: '#fff' },
            error: { bg: '#f44336', text: '#fff' },
            info: { bg: '#2196f3', text: '#fff' },
            warning: { bg: '#ff9800', text: '#fff' }
        };

        const color = colors[type] || colors.info;
        notification.style.backgroundColor = color.bg;
        notification.style.color = color.text;
        notification.textContent = message;
        notification.style.display = 'block';

        // Auto-hide after 3 seconds
        setTimeout(function () {
            notification.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(function () {
                notification.style.display = 'none';
            }, 300);
        }, 3000);
    }

    /**
     * Get current forecast data
     * @returns {Array} Forecast data array
     */
    function getForecastData() {
        return forecastData;
    }

    /**
     * Get current preferences
     * @returns {Object} Current preferences
     */
    function getPreferences() {
        return currentPreferences;
    }

    // Add CSS animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInRight {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        @keyframes slideOutRight {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);

    // Public API
    return {
        init: init,
        getForecastData: getForecastData,
        getPreferences: getPreferences,
        showNotification: showNotification
    };
})();

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', WeatherApp.init);
} else {
    WeatherApp.init();
}
