/**
 * Utility functions for the calculator
 */

/**
 * Truncate to specified decimals without rounding
 * @param {number} num - Number to truncate
 * @param {number} decimals - Number of decimal places (default: 2)
 * @returns {number} Truncated number
 */
export function truncateDecimals(num, decimals = 2) {
    const multiplier = Math.pow(10, decimals);
    return Math.trunc(num * multiplier) / multiplier;
}

/**
 * Convert BCV date format to ISO (YYYY-MM-DD)
 * @param {string} bcvDate - Date in format "Martes, 30 Diciembre 2025"
 * @returns {string|null} Date in ISO format "2025-12-30" or null if error
 */
export function bcvDateToISO(bcvDate) {
    const months = {
        'Enero': '01', 'Febrero': '02', 'Marzo': '03', 'Abril': '04',
        'Mayo': '05', 'Junio': '06', 'Julio': '07', 'Agosto': '08',
        'Septiembre': '09', 'Octubre': '10', 'Noviembre': '11', 'Diciembre': '12'
    };

    try {
        const parts = bcvDate.split(' ');
        const day = parts[1].padStart(2, '0');
        const month = months[parts[2]];
        const year = parts[3];

        return `${year}-${month}-${day}`;
    } catch (error) {
        console.error('Error converting date:', error);
        return null;
    }
}

/**
 * Show error message to user
 * @param {string} message - Error message to display
 */
export function showError(message) {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('error').textContent = message;
    document.getElementById('error').classList.add('show');
}

/**
 * Hide error message
 */
export function hideError() {
    document.getElementById('error').classList.remove('show');
}

/**
 * Format ISO date to DD/MM/YYYY
 * @param {string} isoDate - Date in ISO format (YYYY-MM-DD)
 * @returns {string} Date in DD/MM/YYYY format
 */
export function formatDateDDMMYYYY(isoDate) {
    if (!isoDate) return '';
    const [year, month, day] = isoDate.split('-');
    return `${day}/${month}/${year}`;
}
