"""Base Webhook Provider"""

import logging
import os


class Baseprovider:
    """Base provider for given webhook"""

    def __init__(self):
        self.webhook_url = os.getenv("INPUT_WEBHOOK_URL")
        self.logger = logging.getLogger("webhook-reporter-logger")

    async def send_report():
        """Sends report via webhook"""
        raise NotImplementedError("Provider send report not implemented")
