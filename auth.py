import jwt
from jwt import PyJWKClient
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import DOMAIN, AUDIENCE

# Fetches and caches Auth0's public keys
jwks_client = PyJWKClient(f"https://{DOMAIN}/.well-known/jwks.json")

# Reads the "Authorization: Bearer <token>" header
bearer = HTTPBearer()


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

def require_scope(needed: str):
    def checker(claims: dict = Depends(verify_token)) -> dict:
        granted = set(claims.get("scope", "").split()) | set(claims.get("permissions", []))
        if needed not in granted:
            raise HTTPException(status_code=403, detail=f"Missing permission: {needed}")
        return claims
    return checker
