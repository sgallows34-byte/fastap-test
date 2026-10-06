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

Create a `.env` file with your Auth0 credentials:

```env
AUTH0_DOMAIN=your-auth0-domain.us.auth0.com
AUTH0_AUDIENCE=your-api-identifier
```

## Running the Server

Start the FastAPI server with auto-reload:

```bash
uvicorn main:app --reload
```

The server will run on `http://127.0.0.1:8000`

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

## Getting an Auth0 Token

To get a token for testing, use the Auth0 Management API or client credentials flow. Example:

```bash
export TOKEN=$(curl -X POST https://your-domain.auth0.com/oauth/token \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "your-client-id",
    "client_secret": "your-client-secret",
    "audience": "your-api-identifier",
    "grant_type": "client_credentials"
  }' | jq -r '.access_token')
```

## Project Structure

```
.
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not committed)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```
