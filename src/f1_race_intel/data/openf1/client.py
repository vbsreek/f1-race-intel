from typing import Any

import httpx

from f1_race_intel.config import settings
from f1_race_intel.data.openf1.schemas import OpenF1Driver, OpenF1Lap, OpenF1Session, OpenF1Stint


class OpenF1Client:
    def __init__(self, base_url: str | None = None, timeout: float = 30.0) -> None:
        self.base_url = base_url or settings.openf1_base_url
        self.timeout = timeout

    async def _get(self, path: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
            response = await client.get(path, params=params or {})
            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict) and data.get("detail"):
                return []
            return data if isinstance(data, list) else []

    async def get_session(self, session_key: int) -> OpenF1Session | None:
        rows = await self._get("/sessions", {"session_key": session_key})
        return OpenF1Session.model_validate(rows[0]) if rows else None

    async def list_sessions(
        self,
        *,
        year: int | None = None,
        session_type: str | None = None,
    ) -> list[OpenF1Session]:
        params: dict[str, Any] = {}
        if year is not None:
            params["year>="] = year
            params["year<="] = year
        if session_type is not None:
            params["session_type"] = session_type
        rows = await self._get("/sessions", params)
        return [OpenF1Session.model_validate(row) for row in rows]

    async def get_drivers(self, session_key: int) -> list[OpenF1Driver]:
        rows = await self._get("/drivers", {"session_key": session_key})
        return [OpenF1Driver.model_validate(row) for row in rows]

    async def get_stints(self, session_key: int) -> list[OpenF1Stint]:
        rows = await self._get("/stints", {"session_key": session_key})
        return [OpenF1Stint.model_validate(row) for row in rows]

    async def get_laps(self, session_key: int) -> list[OpenF1Lap]:
        rows = await self._get("/laps", {"session_key": session_key})
        return [OpenF1Lap.model_validate(row) for row in rows]
