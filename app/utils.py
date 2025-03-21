import httpx
import toml

from .config import config


async def get_access_token(server, client_id, client_secret):
    url = f"https://{server}/oauth2/v1/token"
    data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        }
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(url, json=data)
    access_token = response.json()["access_token"]
    return access_token



async def handle_server_error(response, server):
    """
    Обрабатывает ошибки сервера и обновляет токен при необходимости

    Args:
        response: Ответ от сервера
        server: URL сервера

    Returns:
        str: Новый токен, если он был обновлен
        None: Если обновление токена не требуется
    """

    if response.status_code != 200:
        new_token = await get_access_token(
            server,
            config.monitoring_bot.client_id,
            config.monitoring_bot.client_secret,
        )
        config.monitoring_bot.access_token = new_token
        toml.dump(config.model_dump(), open("config.toml", "w", encoding="UTF-8"))
        return new_token
    return None


