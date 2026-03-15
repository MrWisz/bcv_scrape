# BCV Exchange Rate Scraper API

A Flask API that scrapes exchange rates from the Banco Central de Venezuela (BCV) and fetches cryptocurrency prices from Binance P2P marketplace.

## Features

- Scrapes USD and EUR exchange rates from BCV official website
- Fetches real-time USDT/VES prices from Binance P2P marketplace
- Includes applicable date for exchange rates
- Historical rate storage and lookup
- Interactive Swagger/OpenAPI documentation with API key support
- REST API endpoints for easy integration
- Telegram Web App calculator for USD/EUR to VES conversion
- Deployable to Render

## Authentication

All endpoints require an `X-API-Key` header:

```
X-API-Key: your-api-key
```

Set the key as an environment variable named `API_KEY` on your server. Without a valid key, requests will receive a `401 Unauthorized` response.

When using the Swagger UI at `/docs`, click the **Authorize** button at the top right and enter your key there.

## API Endpoints

### Exchange Rates (BCV)
- `GET /rates` - Get all exchange rates (USD, EUR, and date)
- `GET /rates/usd` - Get only USD rate
- `GET /rates/eur` - Get only EUR rate
- `GET /rates/date` - Get the applicable date for the rates
- `GET /rates/usd/change` - Get USD percentage change vs previous saved day

### Historical Rates
- `GET /rates/history` - Get all historical exchange rates
- `GET /rates/history/dates` - Get list of available dates
- `GET /rates/history/<date>` - Get rates for a specific date

### P2P Cryptocurrency Prices
- `GET /p2p/usdt` - Get Binance P2P USDT/VES buy price

### Web App
- `GET /calculator` - Telegram Web App currency calculator (USD/EUR to VES)

### Documentation
- `GET /` - API information and available endpoints
- `GET /docs` - Interactive Swagger UI documentation
- `GET /apispec.json` - OpenAPI specification

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root:
```
API_KEY=your-secret-api-key
```

3. Run the API:
```bash
python api.py
```

4. Access at `http://localhost:5000`

## Deployment to Render

1. Push this code to a GitHub repository
2. Connect your GitHub account to Render
3. Create a new Web Service
4. Select this repository
5. Add `API_KEY` as an environment variable in the Render dashboard
6. Render will automatically detect the `render.yaml` and deploy

## Response Examples

### GET /rates
```json
{
  "success": true,
  "data": {
    "USD": "36,50",
    "EUR": "39,75",
    "date": "Lunes, 30 Diciembre 2025"
  }
}
```

### GET /rates/usd
```json
{
  "success": true,
  "currency": "USD",
  "rate": "36,50"
}
```

### GET /rates/eur
```json
{
  "success": true,
  "currency": "EUR",
  "rate": "39,75"
}
```

### GET /rates/date
```json
{
  "success": true,
  "date": "Lunes, 30 Diciembre 2025"
}
```

### GET /rates/usd/change
```json
{
  "success": true,
  "data": {
    "previous_date": "Viernes, 27 Diciembre 2025",
    "previous_rate": 36.25,
    "current_date": "Lunes, 30 Diciembre 2025",
    "current_rate": 36.50,
    "percentage_change": 0.689,
    "change_direction": "increase"
  }
}
```

### GET /rates/history/dates
```json
{
  "success": true,
  "dates": ["Lunes, 30 Diciembre 2025", "Viernes, 27 Diciembre 2025"]
}
```

### GET /rates/history/Lunes, 30 Diciembre 2025
```json
{
  "success": true,
  "date": "Lunes, 30 Diciembre 2025",
  "data": {
    "USD": "36,50",
    "EUR": "39,75"
  }
}
```

### GET /p2p/usdt
```json
{
  "success": true,
  "currency": "USDT",
  "fiat": "VES",
  "price": 36.85,
  "source": "Binance P2P"
}
```

## Interactive Documentation

Once the API is running, access the interactive Swagger documentation at:
- Local: `http://localhost:5000/docs`
- Production: `https://your-app-name.onrender.com/docs`

The Swagger UI allows you to:
- Authenticate using the **Authorize** button (enter your `API_KEY`)
- Browse all endpoints with detailed descriptions
- See request/response schemas with examples
- Test the API directly from your browser
- Download the OpenAPI specification
