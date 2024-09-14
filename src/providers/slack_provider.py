"""Slack Webhook Provider"""

from slack_sdk.webhook import WebhookClient
from src.models.slack_models import SlackMessage
from src.providers.base_provider import Baseprovider


class SlackProvider(Baseprovider):
    """Webhoko that sends the report message(s) to Slack"""

    async def send_report(self, messages: SlackMessage):
        """Send Coverage report back to Slack"""
        webhook = WebhookClient(self.webhook_url)
        import json
        f = open('example_slack_message.json', 'w', encoding='utf-8')
        json.dump(messages, f)
        f.close()
        response = webhook.send(
            text='Test and Coverage Report',
            blocks=messages
        )
        
        if response.status_code == 200:
            self.logger.info('Webhook-Reporter sent message to slack with [200]')
        elif response.status_code == 400:
            self.logger.error('Coverage Report was not sent to slack [400]. Bad Body!')
        else:
            self.logger.error(f'Coverage Report could not be sent. Return status of [{response.status_code}]')
