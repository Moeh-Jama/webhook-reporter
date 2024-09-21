"""Microsoft Teams Webhook Provider"""
import os
from typing import Any
import aiohttp

from src.providers.base_provider import Baseprovider

TEST_DATA = {
  "type": "AdaptiveCard",
  "body": [
    {
      "type": "TextBlock",
      "size": "medium",
      "weight": "bolder",
      "text": "${title}",
      "style": "heading",
      "wrap": True
    },
    {
      "type": "ColumnSet",
      "columns": [
        {
          "type": "Column",
          "items": [
            {
              "type": "Image",
              "style": "person",
              "url": "${creator.profileImage}",
              "altText": "${creator.name}",
              "size": "small"
            }
          ],
          "width": "auto"
        },
        {
          "type": "Column",
          "items": [
            {
              "type": "TextBlock",
              "weight": "bolder",
              "text": "${creator.name}",
              "wrap": True
            },
            {
              "type": "TextBlock",
              "spacing": "none",
              "text": "Created {{DATE(${string(createdUtc)}, SHORT)}}",
              "isSubtle": True,
              "wrap": True
            }
          ],
          "width": "stretch"
        }
      ]
    },
    {
      "type": "TextBlock",
      "text": "${description}",
      "wrap": True
    },
    {
      "type": "FactSet",
      "facts": [
        {
          "$data": "${properties}",
          "title": "${key}:",
          "value": "${value}"
        }
      ]
    }
  ],
  "actions": [
    {
      "type": "Action.ShowCard",
      "title": "Set due date",
      "card": {
        "type": "AdaptiveCard",
        "body": [
          {
            "type": "Input.Date",
            "label": "Enter the due date",
            "id": "dueDate"
          },
          {
            "type": "Input.Text",
            "id": "comment",
            "isMultiline": True,
            "label": "Add a comment"
          }
        ],
        "actions": [
          {
            "type": "Action.Submit",
            "title": "OK"
          }
        ],
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json"
      }
    },
    {
      "type": "Action.OpenUrl",
      "title": "View",
      "url": "${viewUrl}",
      "role": "button"
    }
  ],
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "version": "1.5"
}

DATA = {
  "title": "Publish Adaptive Card Schema",
  "description": "Now that we have defined the main rules and features of the format, we need to produce a schema and publish it to GitHub. The schema will be the starting point of our reference documentation.",
  "creator": {
    "name": "Matt Hidinger",
    "profileImage": "https://pbs.twimg.com/profile_images/3647943215/d7f12830b3c17a5a9e4afcc370e3a37e_400x400.jpeg"
  },
  "createdUtc": "2017-02-14T06:08:39Z",
  "viewUrl": "https://adaptivecards.io",
  "properties": [
    { "key": "Board", "value": "Adaptive Cards" },
    { "key": "List", "value": "Backlog" },
    { "key": "Assigned to", "value": "Matt Hidinger" },
    { "key": "Due date", "value": "Not set" }
  ]
}

TEST2 = {
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "type": "AdaptiveCard",
    "version": "1.3",
    "body": [
        {
            "type": "TextBlock",
            "text": "🚀 Test Summary Report",
            "weight": "Bolder",
            "size": "Medium"
        },
        {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "width": "auto",
                    "items": [
                        {
                            "type": "Image",
                            "url": "https://example.com/coverage-icon.png",
                            "size": "Small",
                            "altText": "Coverage Icon"
                        },
                        {
                            "type": "TextBlock",
                            "text": "Line Coverage: 90%",
                            "wrap": True
                        }
                    ]
                },
                {
                    "type": "Column",
                    "width": "auto",
                    "items": [
                        {
                            "type": "Image",
                            "url": "https://example.com/complexity-icon.png",
                            "size": "Small",
                            "altText": "Complexity Icon"
                        },
                        {
                            "type": "TextBlock",
                            "text": "Complexity Avg: 2.75",
                            "wrap": True
                        }
                    ]
                },
                {
                    "type": "Column",
                    "width": "auto",
                    "items": [
                        {
                            "type": "Image",
                            "url": "https://example.com/tests-icon.png",
                            "size": "Small",
                            "altText": "Tests Icon"
                        },
                        {
                            "type": "TextBlock",
                            "text": "Tests Run: 65",
                            "wrap": True
                        }
                    ]
                }
            ]
        }
    ],
    "actions": [],
    "footer": {
        "type": "ColumnSet",
        "columns": [
            {
                "type": "Column",
                "width": "auto",
                "items": [
                    {
                        "type": "Image",
                        "url": "https://example.com/footer-icon.png",
                        "size": "Small",
                        "altText": "Footer Icon"
                    }
                ]
            },
            {
                "type": "Column",
                "width": "stretch",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": "Generated by Webhook Reporter",
                        "size": "Small",
                        "weight": "Lighter",
                        "horizontalAlignment": "Left",
                        "wrap": True
                    }
                ]
            }
        ]
    }
}



PARENT = {
     "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "contentUrl": None,
                "content":TEST2,
            }
        ]
}
class TeamsProvider(Baseprovider):
    """Webhook that sends the report message(s) to Microsoft Teams"""

    async def send_report(self, messages: Any):
        """Send Coverage report back to Microsoft Teams"""
        async with aiohttp.ClientSession() as session:
            async with session.post(self.webhook_url, json=messages) as response:
                if response.status == 200:
                    self.logger.info('Webhook-Reporter sent message to Teams with [200]')
                elif response.status == 400:
                    self.logger.error('Coverage Report was not sent to Teams [400]. Bad Body!')
                else:
                    self.logger.error(f'Coverage Report could not be sent. Return status of [{response.status}]')
