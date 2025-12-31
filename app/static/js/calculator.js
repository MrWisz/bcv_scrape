/**
 * Calculator functionality
 */

import { truncateDecimals, showError, hideError } from './utils.js';
import { getRates } from './rates.js';

let tg = null;

/**
 * Initialize Telegram WebApp
 */
export function initTelegram() {
    tg = window.Telegram.WebApp;
    tg.ready();
    tg.expand();
}

/**
 * Calculate conversion
 */
export function calculate() {
    const currency = document.getElementById('currency').value;
    const amount = parseFloat(document.getElementById('amount').value);

    if (isNaN(amount) || amount <= 0) {
        showError('Por favor ingresa un monto válido');
        return;
    }

    // Hide error
    hideError();

    const rates = getRates();

    // Get rate and convert comma to dot (BCV uses European format)
    const rate = parseFloat(rates[currency].replace(',', '.'));
    const result = amount * rate;

    // Truncate to 2 decimals without rounding
    const truncatedAmount = truncateDecimals(amount);
    const truncatedRate = truncateDecimals(rate);
    const truncatedResult = truncateDecimals(result);

    // Format numbers with proper decimal places
    const formattedAmount = truncatedAmount.toFixed(2);
    const formattedRate = truncatedRate.toFixed(2);

    // Show result with thousands separator
    const resultWithSeparator = truncatedResult.toLocaleString('es-VE', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });

    document.getElementById('result-value').textContent = resultWithSeparator + ' VES';
    document.getElementById('result-detail').textContent =
        `${formattedAmount} ${currency} × ${formattedRate} = ${resultWithSeparator} VES`;
    document.getElementById('result').classList.add('show');

    // Haptic feedback
    if (tg && tg.HapticFeedback) {
        tg.HapticFeedback.notificationOccurred('success');
    }
}

/**
 * Set up event listeners
 */
export function setupEventListeners() {
    // Auto-calculate on input change
    document.getElementById('amount').addEventListener('input', function() {
        if (this.value) {
            calculate();
        }
    });

    document.getElementById('currency').addEventListener('change', function() {
        const amount = document.getElementById('amount').value;
        if (amount) {
            calculate();
        }
    });

    // Enter key to calculate
    document.getElementById('amount').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            calculate();
        }
    });
}
