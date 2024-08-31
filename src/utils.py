"""Utilities module for Parse/Provider logics"""

from src.models.test_suite import TestStatus
from src.parsers.schema_parser import SchemaParser
from src.providers.discord_provider import DiscordProvider


def set_provider(provider_name: str) -> DiscordProvider:
    """Returns the Provider based on provider name"""
    provider_name = process_text_input(text=provider_name)
    if provider_name == "discord":
        return DiscordProvider()
    else:
        raise Exception(
            f"Provider {provider_name} is not supported! raise a ticket on https://github.com/Moeh-Jama/webhook-reporter/issues/new"
        )


def process_text_input(text: str) -> str:
    """Cleans the text to reduce any ambiguousness when comparing"""
    text = text.lower().strip()
    return text


def get_test_case_status(status: str) -> TestStatus:
    """Returns the TestStatus from given status as string"""
    status = status.lower().strip()
    if status.startswith("pass"):
        return TestStatus.PASSED
    elif status.startswith("fail"):
        return TestStatus.FAILED
    elif status.startswith("err"):
        return TestStatus.ERROR
    elif status.startswith("skip"):
        return TestStatus.SKIPPED
    return TestStatus.UNKNOWN
