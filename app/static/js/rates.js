/**
 * Exchange rates management
 */

import { truncateDecimals, showError } from './utils.js';
import { getCachedRates, cacheRates } from './cache.js';

const SCHEDULED_UPDATE_HOUR = 16; // 4 PM
const SCHEDULED_UPDATE_MINUTE = 30; // 4:30 PM Venezuela time

let rates = {};

/**
 * Load exchange rates (from cache or API)
 * @param {boolean} forceRefresh - Force refresh from API
 */
export async function loadRates(forceRefresh = false) {
    // Try to use cached data first
    if (!forceRefresh) {
        const cachedRates = getCachedRates();
        if (cachedRates) {
            rates = cachedRates;
            displayRates();
            return;
        }
    }

    // If no cache or force refresh, fetch from API
    console.log('Fetching rates from API...');
    try {
        const response = await fetch('/rates');
        const data = await response.json();

        if (data.success) {
            rates = data.data;
            cacheRates(rates); // Save to cache
            displayRates();
        } else {
            throw new Error('API returned unsuccessful response');
        }
    } catch (error) {
        console.error('Error:', error);

        // Try to use cached data as fallback
        const cachedRates = getCachedRates();
        if (cachedRates) {
            rates = cachedRates;
            displayRates();
        } else {
            showError('Error de conexión: ' + error.message);
        }
    }
}

/**
 * Load rates for a specific date
 * @param {string} date - Date in BCV format
 */
export async function loadRatesByDate(date) {
    try {
        // URL encode the date
        const encodedDate = encodeURIComponent(date);
        const response = await fetch(`/rates/history/${encodedDate}`);
        const data = await response.json();

        if (data.success) {
            rates = {
                USD: data.data.USD,
                EUR: data.data.EUR,
                date: date
            };
            displayRates();
        } else {
            showError('No se encontraron datos para esta fecha');
        }
    } catch (error) {
        console.error('Error loading rates for date:', error);
        showError('Error al cargar las tasas para esta fecha');
    }
}

/**
 * Display rates in UI
 */
function displayRates() {
    // Convert comma to dot for proper number parsing (BCV uses European format)
    const usdRateNum = parseFloat(rates.USD.replace(',', '.'));
    const eurRateNum = parseFloat(rates.EUR.replace(',', '.'));

    // Truncate to 2 decimals without rounding
    const usdRate = truncateDecimals(usdRateNum).toFixed(2);
    const eurRate = truncateDecimals(eurRateNum).toFixed(2);

    document.getElementById('usd-rate').textContent = usdRate + ' VES';
    document.getElementById('eur-rate').textContent = eurRate + ' VES';
    document.getElementById('date-rate').textContent = rates.date;

    // Show app
    document.getElementById('loading').style.display = 'none';
    document.getElementById('app').style.display = 'block';
}

/**
 * Schedule next update at 4:30 PM Venezuela time
 */
export function scheduleNextUpdate() {
    const now = new Date();

    // Convert to Venezuela time (UTC-4 / GMT-4)
    const venezuelaTime = new Date(now.toLocaleString('en-US', { timeZone: 'America/Caracas' }));

    // Calculate next 4:30 PM
    const nextUpdate = new Date(venezuelaTime);
    nextUpdate.setHours(SCHEDULED_UPDATE_HOUR, SCHEDULED_UPDATE_MINUTE, 0, 0);

    // If it's already past 4:30 PM today, schedule for tomorrow
    if (venezuelaTime >= nextUpdate) {
        nextUpdate.setDate(nextUpdate.getDate() + 1);
    }

    const timeUntilUpdate = nextUpdate - venezuelaTime;
    const minutesUntilUpdate = Math.round(timeUntilUpdate / 1000 / 60);

    // Debug logs
    console.log('=== Scheduled Update Info ===');
    console.log('System time:', now.toLocaleString());
    console.log('Venezuela time (GMT-4):', venezuelaTime.toLocaleString('es-VE', { timeZone: 'America/Caracas' }));
    console.log('Next update at:', nextUpdate.toLocaleString('es-VE', { timeZone: 'America/Caracas' }));
    console.log('Time until update:', minutesUntilUpdate, 'minutes');
    console.log('============================');

    // Schedule the update
    setTimeout(() => {
        console.log('Scheduled update triggered at 4:30 PM Venezuela time');
        loadRates(true); // Force refresh
        scheduleNextUpdate(); // Schedule next update
    }, timeUntilUpdate);
}

/**
 * Get current rates
 * @returns {Object} Current rates
 */
export function getRates() {
    return rates;
}
