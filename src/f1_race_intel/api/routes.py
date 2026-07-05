import httpx
from fastapi import APIRouter, HTTPException

from f1_race_intel.config import settings

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/sessions")
async def list_sessions(year: int | None = None, limit: int = 10) -> list[dict]:
    """Proxy recent sessions from OpenF1 (scaffold — no local persistence yet)."""
    params: dict[str, str | int] = {"limit": limit}
    if year is not None:
        params["year"] = year

    async with httpx.AsyncClient(base_url=settings.openf1_base_url, timeout=15.0) as client:
        try:
            response = await client.get("/sessions", params=params)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=f"OpenF1 request failed: {exc}") from exc

    data = response.json()
    return data if isinstance(data, list) else []
