import pytest
from httpx import AsyncClient

from src.app import app


@pytest.mark.asyncio
async def test_get_bets_empty():
    """
    Test check status_code when bets are empty.
    """
    async with AsyncClient(app=app, base_url="http://localhost:8000/api/v1") as client:
        response = await client.get("/bets/bets")
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Bets not found!"
