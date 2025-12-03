/**
 * Charts Module
 * Handles Chart.js initialization and rendering for weather forecast visualization
 */

const WeatherCharts = (function () {
    'use strict';

    // Chart instances
    let temperatureChart = null;
    let precipitationChart = null;
    let windChart = null;

    // Chart colors
    const COLORS = {
        temperature: {
            line: 'rgb(255, 99, 132)',
            background: 'rgba(255, 99, 132, 0.1)',
            border: 'rgba(255, 99, 132, 0.5)'
        },
        precipitation: {
            bar: 'rgb(54, 162, 235)',
            background: 'rgba(54, 162, 235, 0.5)',
            border: 'rgba(54, 162, 235, 1)'
        },
        wind: {
            line: 'rgb(75, 192, 192)',
            background: 'rgba(75, 192, 192, 0.1)',
            border: 'rgba(75, 192, 192, 0.5)'
        }
    };

    /**
     * Initialize all charts
     */
    function init() {
        console.log('Initializing weather charts...');

        // Get forecast data
        const forecastData = window.forecastData || [];

        if (!forecastData || forecastData.length === 0) {
            console.warn('No forecast data available for charts');
            return;
        }

        // Initialize each chart
        initTemperatureChart(forecastData);
        initPrecipitationChart(forecastData);
        initWindChart(forecastData);

        console.log('Charts initialized successfully');
    }

    /**
     * Format timestamp to readable time
     * @param {string} timestamp - ISO timestamp
     * @returns {string} Formatted time (HH:MM)
     */
    function formatTime(timestamp) {
        try {
            const date = new Date(timestamp);
            const hours = date.getHours().toString().padStart(2, '0');
            const minutes = date.getMinutes().toString().padStart(2, '0');
            return hours + ':' + minutes;
        } catch (error) {
            console.error('Error formatting time:', error);
            return '';
        }
    }

    /**
     * Initialize temperature chart
     * @param {Array} data - Forecast data array
     */
    function initTemperatureChart(data) {
        const canvas = document.getElementById('temperatureChart');
        if (!canvas) {
            console.error('Temperature chart canvas not found');
            return;
        }

        const ctx = canvas.getContext('2d');

        // Extract data
        const labels = data.map(function (item) { return formatTime(item.timestamp); });
        const temperatures = data.map(function (item) { return item.temperature; });

        // Destroy existing chart if any
        if (temperatureChart) {
            temperatureChart.destroy();
        }

        // Create chart
        temperatureChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Temperature (°C)',
                    data: temperatures,
                    borderColor: COLORS.temperature.line,
                    backgroundColor: COLORS.temperature.background,
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    pointBackgroundColor: COLORS.temperature.line,
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            font: {
                                size: 12,
                                weight: 'bold'
                            }
                        }
                    },
                    title: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        titleFont: {
                            size: 14
                        },
                        bodyFont: {
                            size: 13
                        },
                        callbacks: {
                            label: function (context) {
                                return 'Temperature: ' + context.parsed.y.toFixed(1) + '°C';
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        ticks: {
                            callback: function (value) {
                                return value + '°C';
                            },
                            font: {
                                size: 11
                            }
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        ticks: {
                            font: {
                                size: 11
                            },
                            maxRotation: 45,
                            minRotation: 0
                        },
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    /**
     * Initialize precipitation chart
     * @param {Array} data - Forecast data array
     */
    function initPrecipitationChart(data) {
        const canvas = document.getElementById('precipitationChart');
        if (!canvas) {
            console.error('Precipitation chart canvas not found');
            return;
        }

        const ctx = canvas.getContext('2d');

        // Extract data
        const labels = data.map(function (item) { return formatTime(item.timestamp); });
        const precipitation = data.map(function (item) { return item.precipitation; });

        // Destroy existing chart if any
        if (precipitationChart) {
            precipitationChart.destroy();
        }

        // Create chart
        precipitationChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Precipitation (mm/h)',
                    data: precipitation,
                    backgroundColor: COLORS.precipitation.background,
                    borderColor: COLORS.precipitation.border,
                    borderWidth: 2,
                    borderRadius: 4,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            font: {
                                size: 12,
                                weight: 'bold'
                            }
                        }
                    },
                    title: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        titleFont: {
                            size: 14
                        },
                        bodyFont: {
                            size: 13
                        },
                        callbacks: {
                            label: function (context) {
                                return 'Precipitation: ' + context.parsed.y.toFixed(1) + ' mm/h';
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function (value) {
                                return value + ' mm';
                            },
                            font: {
                                size: 11
                            }
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        ticks: {
                            font: {
                                size: 11
                            },
                            maxRotation: 45,
                            minRotation: 0
                        },
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    /**
     * Initialize wind speed chart
     * @param {Array} data - Forecast data array
     */
    function initWindChart(data) {
        const canvas = document.getElementById('windChart');
        if (!canvas) {
            console.error('Wind chart canvas not found');
            return;
        }

        const ctx = canvas.getContext('2d');

        // Extract data
        const labels = data.map(function (item) { return formatTime(item.timestamp); });
        const windSpeeds = data.map(function (item) { return item.wind_speed; });

        // Destroy existing chart if any
        if (windChart) {
            windChart.destroy();
        }

        // Create chart
        windChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Wind Speed (km/h)',
                    data: windSpeeds,
                    borderColor: COLORS.wind.line,
                    backgroundColor: COLORS.wind.background,
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    pointBackgroundColor: COLORS.wind.line,
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            font: {
                                size: 12,
                                weight: 'bold'
                            }
                        }
                    },
                    title: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        titleFont: {
                            size: 14
                        },
                        bodyFont: {
                            size: 13
                        },
                        callbacks: {
                            label: function (context) {
                                return 'Wind Speed: ' + context.parsed.y.toFixed(1) + ' km/h';
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function (value) {
                                return value + ' km/h';
                            },
                            font: {
                                size: 11
                            }
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        ticks: {
                            font: {
                                size: 11
                            },
                            maxRotation: 45,
                            minRotation: 0
                        },
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    /**
     * Update all charts with new data
     * @param {Array} data - New forecast data
     */
    function updateCharts(data) {
        if (!data || data.length === 0) {
            console.warn('No data provided for chart update');
            return;
        }

        // Reinitialize charts with new data
        initTemperatureChart(data);
        initPrecipitationChart(data);
        initWindChart(data);
    }

    /**
     * Destroy all charts
     */
    function destroy() {
        if (temperatureChart) {
            temperatureChart.destroy();
            temperatureChart = null;
        }
        if (precipitationChart) {
            precipitationChart.destroy();
            precipitationChart = null;
        }
        if (windChart) {
            windChart.destroy();
            windChart = null;
        }
    }

    // Public API
    return {
        init: init,
        update: updateCharts,
        destroy: destroy
    };
})();

// Initialize charts when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', WeatherCharts.init);
} else {
    WeatherCharts.init();
}
