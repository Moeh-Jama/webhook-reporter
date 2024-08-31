"""Base Webhook Provider"""


class Baseprovider:
    """Base provider for given webhook"""

    async def send_report():
        """Sends report via webhook"""
        raise NotImplementedError("Provider send report not implemented")
