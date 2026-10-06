from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import Body
from auth import verify_token, require_scope
import json
from typing import List, Optional

DATA_FILE = "data.json"


def read_items():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def write_items(items: List[str]):
    with open(DATA_FILE, 'w') as f:
        json.dump(items, f, indent=2)

app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    """Serve the web interface"""
    return FileResponse("static/index.html")


@app.get("/public")
def public_route():
    return {"msg": "anyone can see this"}


@app.get("/private")
def private_route(claims: dict = Depends(verify_token)):
    return {"msg": "you're authenticated", "claims": claims}

@app.get("/items")
def get_items(claims: dict = Depends(require_scope("read:items"))):
    items = read_items()
    return {"items": items}


@app.post("/items")
def create_item(item: str = Body(...), claims: dict = Depends(require_scope("write:items"))):
    items = read_items()
    items.append(item)
    write_items(items)
    return {"msg": "item created", "item": item, "items": items}