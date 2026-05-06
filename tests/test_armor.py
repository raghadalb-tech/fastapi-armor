import asyncio

from fastapi import FastAPI, HTTPException
from httpx import ASGITransport, AsyncClient

from fastapi_armor import Armor


def _request(app: FastAPI, method: str, path: str):
    async def _run():
        transport = ASGITransport(app=app, raise_app_exceptions=False)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.request(method, path)

    return asyncio.run(_run())


def test_armor_initializes_without_errors():
    app = FastAPI()
    armor = Armor(app)
    assert armor.app is app
    assert armor.logger.name == "fastapi_armor"


def test_http_exception_returns_clean_json():
    app = FastAPI()
    Armor(app)

    @app.get("/http-error")
    async def raise_http_error():
        raise HTTPException(status_code=404, detail="Not found")

    response = _request(app, "GET", "/http-error")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}


def test_unhandled_exception_returns_internal_server_error():
    app = FastAPI()
    Armor(app)

    @app.get("/boom")
    async def raise_runtime_error():
        raise RuntimeError("unexpected")

    response = _request(app, "GET", "/boom")
    assert response.status_code == 500
    assert response.json() == {"error": "Internal server error"}


def test_validation_error_returns_validation_failed():
    app = FastAPI()
    Armor(app)

    @app.get("/items/{item_id}")
    async def get_item(item_id: int):
        return {"item_id": item_id}

    response = _request(app, "GET", "/items/not-an-int")
    assert response.status_code == 422
    body = response.json()
    assert body["error"] == "Validation failed"
    assert isinstance(body["detail"], list)
