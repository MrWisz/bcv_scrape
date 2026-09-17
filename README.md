# Venezuela Exchange Rate API

A Flask API that serves Venezuelan exchange rates — the official (BCV) rate and the parallel/black-market rate — by consuming the public [DolarAPI](https://dolarapi.com/docs/venezuela/) service.

## Features

- Official (BCV) USD and EUR rates, sourced from DolarAPI
- Parallel/black-market USD rate, sourced from DolarAPI
- Includes applicable date for exchange rates
- Full historical rate lookup (proxied from DolarAPI's own history)
- Interactive Swagger/OpenAPI documentation with API key support
- REST API endpoints for easy integration
- Web App calculator for USD/EUR/Paralelo to VES conversion
- Deployable to Render

## Authentication

All endpoints require an `X-API-Key` header (except for the health endpoint):

```
X-API-Key: your-api-key
```

Set the key as an environment variable named `API_KEY` on your server. Without a valid key, requests will receive a `401 Unauthorized` response.

When using the Swagger UI at `/docs`, click the **Authorize** button at the top right and enter your key there.

## API Endpoints

### Exchange Rates
- `GET /rates` - Get all exchange rates (USD, EUR, and date)
- `GET /rates/usd` - Get only USD rate
- `GET /rates/eur` - Get only EUR rate
- `GET /rates/date` - Get the applicable date for the rates
- `GET /rates/usd/change` - Get USD percentage change vs previous saved day
- `GET /rates/usd/paralelo` - Get the USD parallel (non-official) exchange rate

### Historical Rates
- `GET /rates/history` - Get all historical exchange rates
- `GET /rates/history/dates` - Get list of available dates
- `GET /rates/history/<date>` - Get rates for a specific date

### Web App
- `GET /calculator` - Telegram Web App currency calculator (USD/EUR/Paralelo to VES)

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

## Data Source

All rates and history come from [DolarAPI](https://ve.dolarapi.com) at request time. Responses are cached in-process (30 minutes for current rates, 3 hours for history) to avoid hitting DolarAPI on every request — see `app/services/dolarapi_client.py`. There is no local database; nothing needs to be provisioned or migrated.

## Migrating from the old scraper/MongoDB setup

This project used to scrape bcv.org.ve directly and store history in MongoDB Atlas. If you're updating an existing deployment:

- Remove `MONGODB_URI` and `MONGODB_DB_NAME` from your Render service's environment variables (they're no longer read, and deleting them from `render.yaml` doesn't remove already-configured values on the dashboard).
- `rates_history.json` in the repo root is no longer read or written to; it's safe to delete if you don't want to keep it around.

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
    "USD": "36,50000000",
    "EUR": "39,75000000",
    "date": "Lunes, 30 Diciembre 2025"
  }
}
```

### GET /rates/usd
```json
{
  "success": true,
  "currency": "USD",
  "rate": "36,50000000"
}
```

### GET /rates/eur
```json
{
  "success": true,
  "currency": "EUR",
  "rate": "39,75000000"
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

### GET /rates/usd/paralelo
```json
{
  "success": true,
  "currency": "USD",
  "rate": 934.576908
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
    "USD": "36,50000000",
    "EUR": "39,75000000"
  }
}
```

## Interactive Documentation

Once the API is running, access the interactive Swagger documentation at:
- Local: `http://localhost:5000/docs`
- Production: `https://your-app-name.onrender.com/docs`
(Or whatever deployment server you decide to use)

The Swagger UI allows you to:
- Authenticate using the **Authorize** button (enter your `API_KEY`)
- Browse all endpoints with detailed descriptions
- See request/response schemas with examples
- Test the API directly from your browser
- Download the OpenAPI specification
