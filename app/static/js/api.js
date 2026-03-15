/**
 * Authenticated fetch wrapper - injects X-API-Key from page meta tag
 */

const API_KEY = document.querySelector('meta[name="api-key"]')?.content || '';

export function apiFetch(url, options = {}) {
    return fetch(url, {
        ...options,
        headers: {
            'X-API-Key': API_KEY,
            ...(options.headers || {}),
        },
    });
}
