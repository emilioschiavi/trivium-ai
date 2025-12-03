/**
 * Preferences Management Module
 * Handles loading, saving, and validating user preferences in localStorage
 */

const PreferencesManager = (function () {
    'use strict';

    // Default preference values
    const DEFAULTS = {
        cycling: true,
        running: true,
        cyclingTempMin: 0,
        cyclingTempMax: 25,
        runningTempMin: 10,
        runningTempMax: 20,
        windMax: 30,
        cyclingRainMax: 0,
        runningRainMax: 3
    };

    const STORAGE_KEY = 'weatherPreferences';

    /**
     * Load preferences from localStorage
     * @returns {Object} Preferences object
     */
    function loadPreferences() {
        try {
            const saved = localStorage.getItem(STORAGE_KEY);
            if (saved) {
                const parsed = JSON.parse(saved);
                // Merge with defaults to handle any missing keys
                return Object.assign({}, DEFAULTS, parsed);
            }
        } catch (error) {
            console.error('Error loading preferences:', error);
        }
        return Object.assign({}, DEFAULTS);
    }

    /**
     * Save preferences to localStorage
     * @param {Object} prefs - Preferences object to save
     * @returns {boolean} Success status
     */
    function savePreferences(prefs) {
        try {
            const validated = validatePreferences(prefs);
            if (validated) {
                localStorage.setItem(STORAGE_KEY, JSON.stringify(prefs));
                return true;
            }
        } catch (error) {
            console.error('Error saving preferences:', error);
        }
        return false;
    }

    /**
     * Validate preference values
     * @param {Object} prefs - Preferences to validate
     * @returns {boolean} Validation result
     */
    function validatePreferences(prefs) {
        const errors = [];

        // Temperature validation
        if (prefs.cyclingTempMin >= prefs.cyclingTempMax) {
            errors.push('🚴 Cycling: Minimum temperature must be less than maximum');
        }
        if (prefs.runningTempMin >= prefs.runningTempMax) {
            errors.push('🏃 Running: Minimum temperature must be less than maximum');
        }

        // Range validation
        if (prefs.cyclingTempMin < -20 || prefs.cyclingTempMax > 40) {
            errors.push('🚴 Cycling: Temperature must be between -20°C and 40°C');
        }
        if (prefs.runningTempMin < -20 || prefs.runningTempMax > 40) {
            errors.push('🏃 Running: Temperature must be between -20°C and 40°C');
        }

        // Wind validation
        if (prefs.windMax < 0 || prefs.windMax > 100) {
            errors.push('💨 Wind threshold must be between 0 and 100 km/h');
        }

        // Rain validation
        if (prefs.cyclingRainMax < 0 || prefs.cyclingRainMax > 50) {
            errors.push('🚴 Cycling: Rain threshold must be between 0 and 50 mm/h');
        }
        if (prefs.runningRainMax < 0 || prefs.runningRainMax > 50) {
            errors.push('🏃 Running: Rain threshold must be between 0 and 50 mm/h');
        }

        if (errors.length > 0) {
            alert('❌ Validation Errors:\n\n' + errors.join('\n'));
            return false;
        }

        return true;
    }

    /**
     * Reset preferences to defaults
     */
    function resetPreferences() {
        try {
            localStorage.removeItem(STORAGE_KEY);
            return true;
        } catch (error) {
            console.error('Error resetting preferences:', error);
            return false;
        }
    }

    /**
     * Get default preferences
     * @returns {Object} Default preferences
     */
    function getDefaults() {
        return Object.assign({}, DEFAULTS);
    }

    /**
     * Populate form with preference values
     * @param {Object} prefs - Preferences to populate
     */
    function populateForm(prefs) {
        const fields = [
            { id: 'cyclingEnabled', key: 'cycling', type: 'checkbox' },
            { id: 'runningEnabled', key: 'running', type: 'checkbox' },
            { id: 'cyclingTempMin', key: 'cyclingTempMin', type: 'number' },
            { id: 'cyclingTempMax', key: 'cyclingTempMax', type: 'number' },
            { id: 'runningTempMin', key: 'runningTempMin', type: 'number' },
            { id: 'runningTempMax', key: 'runningTempMax', type: 'number' },
            { id: 'windMax', key: 'windMax', type: 'number' },
            { id: 'cyclingRainMax', key: 'cyclingRainMax', type: 'number' },
            { id: 'runningRainMax', key: 'runningRainMax', type: 'number' }
        ];

        fields.forEach(function (field) {
            const element = document.getElementById(field.id);
            if (element) {
                if (field.type === 'checkbox') {
                    element.checked = prefs[field.key];
                } else {
                    element.value = prefs[field.key];
                }
            }
        });
    }

    /**
     * Read preferences from form
     * @returns {Object} Preferences object from form values
     */
    function readFromForm() {
        return {
            cycling: document.getElementById('cyclingEnabled').checked,
            running: document.getElementById('runningEnabled').checked,
            cyclingTempMin: parseFloat(document.getElementById('cyclingTempMin').value),
            cyclingTempMax: parseFloat(document.getElementById('cyclingTempMax').value),
            runningTempMin: parseFloat(document.getElementById('runningTempMin').value),
            runningTempMax: parseFloat(document.getElementById('runningTempMax').value),
            windMax: parseFloat(document.getElementById('windMax').value),
            cyclingRainMax: parseFloat(document.getElementById('cyclingRainMax').value),
            runningRainMax: parseFloat(document.getElementById('runningRainMax').value)
        };
    }

    // Public API
    return {
        load: loadPreferences,
        save: savePreferences,
        validate: validatePreferences,
        reset: resetPreferences,
        getDefaults: getDefaults,
        populateForm: populateForm,
        readFromForm: readFromForm
    };
})();
