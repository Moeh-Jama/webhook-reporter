"""Discord Webhook Provider"""

import os
from typing import List
import aiohttp
from discord import Embed, Webhook
from config import BOT_IMAGE


class DiscordProvider:
    """Webhook that sends the coverage report back to discord"""

    def __init__(self):
        self.webhook_url = os.getenv("INPUT_WEBHOOK_URL")

    async def send_report(self, messages: List[Embed]):
        """Send CoverageReport back to Discord"""
        avatar_url = BOT_IMAGE
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(self.webhook_url, session=session)
            await webhook.send(
                'format 2',
                embeds=messages,
                username='webhook-reporter',
                avatar_url=avatar_url,
            )
        await session.close()
