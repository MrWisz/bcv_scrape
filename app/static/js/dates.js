/**
 * Date management for historical rates
 */

import { bcvDateToISO, showError, hideError, formatDateDDMMYYYY } from './utils.js';

let availableDates = []; // Array of BCV formatted dates
let dateMapping = {}; // Map: ISO date -> BCV formatted date
let selectedDate = null;

/**
 * Load available dates from history
 * @param {Function} onDateLoaded - Callback when dates are loaded with most recent date
 */
export async function loadAvailableDates(onDateLoaded) {
    try {
        const response = await fetch('/rates/history/dates');
        const data = await response.json();

        if (data.success && data.dates && data.dates.length > 0) {
            availableDates = data.dates;

            // Create mapping from ISO to BCV format
            availableDates.forEach(bcvDate => {
                const isoDate = bcvDateToISO(bcvDate);
                if (isoDate) {
                    dateMapping[isoDate] = bcvDate;
                }
            });

            // Set date range limits
            const isoDatesList = Object.keys(dateMapping).sort();
            const dateInput = document.getElementById('date-select');

            if (isoDatesList.length > 0) {
                // Set min and max dates
                dateInput.min = isoDatesList[0];
                dateInput.max = isoDatesList[isoDatesList.length - 1];

                // Set most recent date as default
                const mostRecent = isoDatesList[isoDatesList.length - 1];
                dateInput.value = mostRecent;
                selectedDate = dateMapping[mostRecent];

                // Display selected date in DD/MM/YYYY format
                document.getElementById('date-display').value = formatDateDDMMYYYY(mostRecent);

                // Update info text with available dates count
                document.getElementById('date-info').textContent =
                    `${isoDatesList.length} fecha(s) con datos disponibles`;

                // Setup click handler to open native date picker
                document.getElementById('date-display').addEventListener('click', () => {
                    document.getElementById('date-select').showPicker();
                });

                // Call callback with the most recent date
                if (onDateLoaded) {
                    onDateLoaded(selectedDate);
                }
            }
        }
    } catch (error) {
        console.error('Error loading dates:', error);
        document.getElementById('date-info').textContent = 'Error al cargar fechas';
    }
}

/**
 * Find most recent available date before or equal to target date
 * @param {string} targetIsoDate - Target date in ISO format
 * @returns {string|null} Closest ISO date or null
 */
export function findClosestAvailableDate(targetIsoDate) {
    const availableIsoDates = Object.keys(dateMapping).sort();

    if (availableIsoDates.length === 0) return null;

    const targetTime = new Date(targetIsoDate).getTime();

    // Find the last date that is <= target date
    let mostRecentBefore = null;

    for (const isoDate of availableIsoDates) {
        const dateTime = new Date(isoDate).getTime();

        // If this date is before or equal to target
        if (dateTime <= targetTime) {
            mostRecentBefore = isoDate;
        } else {
            // Dates are sorted, so we can break here
            break;
        }
    }

    // If no date before target, return the first available date
    return mostRecentBefore || availableIsoDates[0];
}

/**
 * Handle date selection change
 * @param {Function} loadRatesByDate - Callback to load rates for a specific date
 */
export function onDateChange(loadRatesByDate) {
    const isoDate = document.getElementById('date-select').value;
    const bcvDate = dateMapping[isoDate];

    if (bcvDate) {
        selectedDate = bcvDate;
        loadRatesByDate(bcvDate);
        // Update display with DD/MM/YYYY format
        document.getElementById('date-display').value = formatDateDDMMYYYY(isoDate);
        // Clear any previous errors
        hideError();
    } else {
        // Selected date is not in our history - find closest available date
        const closestDate = findClosestAvailableDate(isoDate);

        if (closestDate) {
            // Set to closest date
            document.getElementById('date-select').value = closestDate;
            selectedDate = dateMapping[closestDate];
            loadRatesByDate(dateMapping[closestDate]);

            // Update display with DD/MM/YYYY format
            document.getElementById('date-display').value = formatDateDDMMYYYY(closestDate);

            // Show informative message
            showError(`No hay datos para ${formatDateDDMMYYYY(isoDate)}. Mostrando último día disponible: ${formatDateDDMMYYYY(closestDate)}`);

            // Auto-hide error after 3 seconds
            setTimeout(() => {
                hideError();
            }, 3000);
        } else {
            showError('No hay datos disponibles para esta fecha. Por favor seleccione otra fecha.');
        }
    }
}

export function getSelectedDate() {
    return selectedDate;
}

export function getDateMapping() {
    return dateMapping;
}
