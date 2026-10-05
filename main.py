import os
import jwt
from jwt import PyJWKClient
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()
DOMAIN = os.environ["AUTH0_DOMAIN"]
AUDIENCE = os.environ["AUTH0_AUDIENCE"]

# Fetches and caches Auth0's public keys
jwks_client = PyJWKClient(f"https://{DOMAIN}/.well-known/jwks.json")

# Reads the "Authorization: Bearer <token>" header
bearer = HTTPBearer()

app = FastAPI()


def verify_token(creds: HTTPAuthorizationCredentials = Depends(bearer)) -> dict:
    token = creds.credentials
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token).key
        return jwt.decode(
            token,
            signing_key,
            algorithms=["RS256"],
            audience=AUDIENCE,
            issuer=f"https://{DOMAIN}/",
        )
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")


@app.get("/public")
def public():
    return {"msg": "anyone can see this"}


@app.get("/private")
def private(claims: dict = Depends(verify_token)):
    return {"msg": "you're authenticated", "claims": claims}