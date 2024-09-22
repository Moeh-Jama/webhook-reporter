"""Microsoft Teams Webhook Provider"""

from typing import Any
import aiohttp

from src.providers.base_provider import Baseprovider


class TeamsProvider(Baseprovider):
    """Webhook that sends the report message(s) to Microsoft Teams"""

    async def send_report(self, messages: Any):
        """Send Coverage report back to Microsoft Teams"""
        async with aiohttp.ClientSession() as session:
            async with session.post(self.webhook_url, json=messages) as response:
                if response.status == 200:
                    self.logger.info(
                        "Webhook-Reporter sent message to Teams with [200]"
                    )
                elif response.status == 400:
                    self.logger.error(
                        "Coverage Report was not sent to Teams [400]. Bad Body!"
                    )
                else:
                    self.logger.error(
                        f"Coverage Report could not be sent. Return status of [{response.status}]"
                    )
