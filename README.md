# BCV Exchange Rate Scraper API

A Flask API that scrapes exchange rates from the Banco Central de Venezuela (BCV) and fetches cryptocurrency prices from Binance P2P marketplace.

## Features

- Scrapes USD and EUR exchange rates from BCV official website
- Fetches real-time USDT/VES prices from Binance P2P marketplace
- Includes applicable date for exchange rates
- Interactive Swagger/OpenAPI documentation
- REST API endpoints for easy integration
- Deployable to Render

## API Endpoints

### Exchange Rates (BCV)
- `GET /rates` - Get all exchange rates (USD, EUR, and date)
- `GET /rates/usd` - Get only USD rate
- `GET /rates/eur` - Get only EUR rate
- `GET /rates/date` - Get the applicable date for the rates

### P2P Cryptocurrency Prices
- `GET /p2p/usdt` - Get Binance P2P USDT/VES buy price

### Documentation
- `GET /` - API information and available endpoints
- `GET /docs` - Interactive Swagger UI documentation
- `GET /apispec.json` - OpenAPI specification

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the API:
```bash
python api.py
```

3. Access at `http://localhost:5000`

## Deployment to Render

1. Push this code to a GitHub repository
2. Connect your GitHub account to Render
3. Create a new Web Service
4. Select this repository
5. Render will automatically detect the `render.yaml` and deploy

## Response Examples

### GET /rates
```json
{
  "success": true,
  "data": {
    "USD": 36.50,
    "EUR": 39.75,
    "date": "2025-12-30"
  }
}
```

### GET /rates/usd
```json
{
  "success": true,
  "currency": "USD",
  "rate": 36.50
}
```

### GET /rates/eur
```json
{
  "success": true,
  "currency": "EUR",
  "rate": 39.75
}
```

### GET /rates/date
```json
{
  "success": true,
  "date": "2025-12-30"
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

Once the API is running, you can access the interactive Swagger documentation at:
- Local: `http://localhost:5000/docs`
- Production: `https://your-app-name.onrender.com/docs`

The Swagger UI allows you to:
- Browse all endpoints with detailed descriptions
- See request/response schemas with examples
- Test the API directly from your browser
- Download the OpenAPI specification
