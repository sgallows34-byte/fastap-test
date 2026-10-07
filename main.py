import os
import json
import sqlite3
from typing import List

import httpx
from dotenv import load_dotenv
from fastapi import Body, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.staticfiles import StaticFiles

from auth import require_scope, verify_token

load_dotenv()
DOMAIN = os.environ["AUTH0_DOMAIN"]
bearer = HTTPBearer()

DATA_FILE = "data.json"


def read_items():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def write_items(items: List[str]):
    with open(DATA_FILE, "w") as f:
        json.dump(items, f, indent=2)


app = FastAPI()

db = sqlite3.connect("app.db", check_same_thread=False)
db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        auth0_sub TEXT PRIMARY KEY,
        email TEXT,
        email_verified INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
""")
db.commit()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    """Serve the web interface"""
    return FileResponse("static/index.html")


@app.get("/me")
def me(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
    claims: dict = Depends(verify_token),
):
    sub = claims["sub"]
    if sub.endswith("@clients"):
        raise HTTPException(status_code=400, detail="Machine tokens have no user account")

    query = "SELECT auth0_sub, email, email_verified, created_at FROM users WHERE auth0_sub = ?"
    row = db.execute(query, (sub,)).fetchone()
    created = False

    if row is None:
        try:
            resp = httpx.get(
                f"https://{DOMAIN}/userinfo",
                headers={"Authorization": f"Bearer {creds.credentials}"},
                timeout=10,
            )
            resp.raise_for_status()
            info = resp.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Could not fetch profile from Auth0: {e}")

        db.execute(
            "INSERT INTO users (auth0_sub, email, email_verified) VALUES (?, ?, ?)",
            (sub, info.get("email"), int(info.get("email_verified", False))),
        )
        db.commit()
        created = True
        row = db.execute(query, (sub,)).fetchone()

    return {
        "account_created_now": created,
        "account": dict(zip(["auth0_sub", "email", "email_verified", "created_at"], row)),
    }


@app.get("/public")
def public_route():
    return {"msg": "anyone can see this"}


@app.get("/private")
def private_route(claims: dict = Depends(verify_token)):
    return {"msg": "you're authenticated", "claims": claims}


@app.get("/items")
def get_items(claims: dict = Depends(require_scope("read:items"))):
    return {"items": read_items()}


@app.post("/items")
def create_item(item: str = Body(...), claims: dict = Depends(require_scope("write:items"))):
    items = read_items()
    items.append(item)
    write_items(items)
    return {"msg": "item created", "item": item, "items": items}