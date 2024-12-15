from httpx import AsyncClient


class HTTPClient:

    def __init__(self) -> None:
        self.client = None

    async def init_client(self) -> None:
        """
        Method initialize the http client.
        """
        self.client = AsyncClient(timeout=None)

    async def close_client(self) -> None:
        """
        Method close the http client.
        """
        await self.client.aclose()

    def get_client(self) -> AsyncClient:
        """
        Method return the http client.
        """
        return self.client


http_client = HTTPClient()
