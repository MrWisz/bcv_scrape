/**
 * Main entry point for the calculator app
 */

import { initTelegram, calculate, setupEventListeners } from './calculator.js';
import { loadRatesByDate, scheduleNextUpdate, loadBinanceRate, applyRates, getRates, applyBinanceRate, getBinanceRate } from './rates.js';
import { loadAvailableDates, applyAvailableDates, onDateChange, getAvailableDates } from './dates.js';
import { getCachedBootstrap, cacheBootstrap } from './cache.js';

// Initialize Telegram WebApp
initTelegram();

// Make calculate function globally available for inline onclick
window.calculate = calculate;

/**
 * Cache the initial bootstrap data once all three pieces have loaded, so the
 * next page load (within the cache window) can skip the network calls entirely.
 */
function maybeCacheBootstrap() {
    const dates = getAvailableDates();
    const rates = getRates();
    const binanceRate = getBinanceRate();

    if (dates.length > 0 && rates.USD && binanceRate !== null) {
        cacheBootstrap({ dates, rates, binanceRate });
    }
}

// Initialize app on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    const cached = getCachedBootstrap();

    if (cached) {
        // Populate everything from cache - no network calls on this load
        applyAvailableDates(cached.dates, () => {});
        applyRates(cached.rates);
        applyBinanceRate(cached.binanceRate);
    } else {
        // Load available dates first, then load rates for the most recent date
        loadAvailableDates((mostRecentDate) => {
            loadRatesByDate(mostRecentDate).then(maybeCacheBootstrap);
        });

        // Load the live Binance P2P rate (independent of the selected history date)
        loadBinanceRate().then(maybeCacheBootstrap);
    }

    // Schedule automatic updates at 4:30 PM
    scheduleNextUpdate();

    // Date selector change event
    document.getElementById('date-select').addEventListener('change', () => {
        onDateChange(loadRatesByDate);
    });

    // Setup calculator event listeners
    setupEventListeners();
});
