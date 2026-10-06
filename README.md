# FastAPI Auth0 Authentication

A simple FastAPI application with Auth0 JWT authentication.

## Setup

### 1. Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file with your Auth0 credentials and API proxy configuration:

```env
# Auth0 Configuration
AUTH0_DOMAIN=your-auth0-domain.us.auth0.com
AUTH0_AUDIENCE=your-api-identifier

# API Proxy Configuration (optional defaults)
DEFAULT_API_URL=https://api.example.com
DEFAULT_AUTH_TOKEN=your-default-api-token
DEFAULT_HEADERS={"Content-Type": "application/json"}
```

## Running the Server

Start the FastAPI server with auto-reload:

```bash
uvicorn main:app --reload
```

The server will run on `http://127.0.0.1:8000`

## Web Interface

Visit `http://localhost:8000` to access the web interface for making API calls.

The web interface provides:
- Form to enter API URL, method, headers, and payload
- Pre-loaded default headers (from `.env`)
- Direct API calls from the browser (no backend proxy)
- Real-time response display with status codes
- JSON formatting for easy reading

The interface calls APIs directly from your browser using the provided configuration.

## API Endpoints

### Public Endpoint
Accessible without authentication:

```bash
curl http://localhost:8000/public
```

Response:
```json
{"msg": "anyone can see this"}
```

### Private Endpoint
Requires a valid Auth0 JWT token:

```bash
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/private
```

Response:
```json
{
  "msg": "you're authenticated",
  "claims": {
    "iss": "https://your-domain.auth0.com/",
    "sub": "...",
    "aud": "...",
    "iat": 1234567890,
    "exp": 1234567890
  }
}
```

### Items Endpoints
Endpoints for managing items stored in `data.json`.

**GET /items** - Read items (requires `read:items` scope):
```bash
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/items
```

Response:
```json
{
  "items": ["a", "b", "c"]
}
```

**POST /items** - Create new item (requires `write:items` scope):
```bash
curl -X POST http://localhost:8000/items \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '"new_item"'
```

Response:
```json
{
  "msg": "item created",
  "item": "new_item",
  "items": ["a", "b", "c", "new_item"]
}
```

### Web Interface API Calls
The web interface makes direct API calls from your browser. Configure your API details in the form and click "Send Request".



## Project Structure

```
.
├── main.py              # FastAPI application entry point
├── config.py            # Configuration and environment variables
├── auth.py              # Auth0 JWT verification
├── static/
│   └── index.html      # Web interface (direct API calls)
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not committed)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Configuration Notes

- The web interface makes direct API calls from your browser
- Default headers are pre-loaded from `.env` 
- You can override any field directly in the form
- The interface supports GET, POST, PUT, and DELETE methods
- JSON responses are automatically formatted; other content types display as raw text
