/**
 * Cache management for exchange rates
 */

const CACHE_KEY = 'bcv_rates_cache';
const CACHE_DURATION = 4 * 60 * 60 * 1000; // 4 hours in milliseconds

/**
 * Check if cache is valid and return cached data
 * @returns {Object|null} Cached rates data or null if invalid/expired
 */
export function getCachedRates() {
    try {
        const cached = localStorage.getItem(CACHE_KEY);
        if (!cached) return null;

        const { data, timestamp } = JSON.parse(cached);
        const now = Date.now();

        // Check if cache is still valid (less than 4 hours old)
        if (now - timestamp < CACHE_DURATION) {
            console.log('Using cached rates');
            return data;
        }

        console.log('Cache expired');
        return null;
    } catch (error) {
        console.error('Error reading cache:', error);
        return null;
    }
}

/**
 * Save rates to cache
 * @param {Object} data - Rates data to cache
 */
export function cacheRates(data) {
    try {
        const cacheData = {
            data: data,
            timestamp: Date.now()
        };
        localStorage.setItem(CACHE_KEY, JSON.stringify(cacheData));
        console.log('Rates cached successfully');
    } catch (error) {
        console.error('Error caching rates:', error);
    }
}
