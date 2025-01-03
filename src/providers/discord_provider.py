"""Discord Webhook Provider"""

from typing import List
import aiohttp
from discord import Embed, Forbidden, NotFound, Webhook
from config import BOT_IMAGE
from src.providers.base_provider import Baseprovider


class DiscordProvider(Baseprovider):
    """Webhook that sends the coverage report back to discord"""

    async def send_report(self, messages: List[Embed]):
        """Send CoverageReport back to Discord"""
        avatar_url = BOT_IMAGE
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(self.webhook_url, session=session)
            try:
                await webhook.send(
                    embed=messages,
                    username="webhook-reporter",
                    avatar_url=avatar_url,
                )
                self.logger.info("Webhook Reporter message was sent.")
            except NotFound:
                self.logger.error("This webhook was not found")
            except Forbidden:
                self.logger.error("Access was forbidden with given webhook")
