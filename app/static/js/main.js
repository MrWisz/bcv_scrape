/**
 * Main entry point for the calculator app
 */

import { initTelegram, calculate, setupEventListeners } from './calculator.js';
import { loadRates, loadRatesByDate, scheduleNextUpdate } from './rates.js';
import { loadAvailableDates, onDateChange } from './dates.js';

// Initialize Telegram WebApp
initTelegram();

// Make calculate function globally available for inline onclick
window.calculate = calculate;

// Initialize app on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    // Load available dates first, then load rates for the most recent date
    loadAvailableDates((mostRecentDate) => {
        // Load rates for the most recent date
        loadRatesByDate(mostRecentDate);
    });

    // Also load current rates (for caching/fallback)
    loadRates();

    // Schedule automatic updates at 4:30 PM
    scheduleNextUpdate();

    // Date selector change event
    document.getElementById('date-select').addEventListener('change', () => {
        onDateChange(loadRatesByDate);
    });

    // Setup calculator event listeners
    setupEventListeners();
});
