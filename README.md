# BCV Exchange Rate Scraper API

A simple Flask API that scrapes exchange rates (USD and EUR) from the Banco Central de Venezuela website.

## Features

- Scrapes USD and EUR exchange rates from BCV
- REST API endpoints for easy integration
- Deployable to Render

## API Endpoints

- `GET /` - API documentation
- `GET /rates` - Get all exchange rates (USD and EUR)
- `GET /rates/usd` - Get only USD rate
- `GET /rates/eur` - Get only EUR rate

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

## Response Format

```json
{
  "success": true,
  "data": {
    "USD": "XX.XX",
    "EUR": "XX.XX"
  }
}
```
