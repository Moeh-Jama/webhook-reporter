"""Utilities module for Parse/Provider logics"""

import difflib
import logging
from typing import List
from src.exceptions.configurations import InvalidProviderError
from src.formatters.base_formatter import BaseFormatter
from src.formatters.discord_formatter import DiscordFormatter
from src.formatters.slack_formatter import SlackFormatter
from src.formatters.teams_formatter import TeamsFormatter
from src.models.data_reports import NormalisedCoverageData
from src.models.test_suite import TestReport, TestResult
from src.providers.base_provider import Baseprovider
from src.providers.discord_provider import DiscordProvider
from src.providers.slack_provider import SlackProvider
from src.providers.teams_provider import TeamsProvider

logger = logging.getLogger("webhook-reporter-logger")

def set_provider(provider_name: str) -> Baseprovider:
    """Returns the Provider based on provider name"""
    provider_name = process_text_input(text=provider_name)
    if provider_name == "discord":
        return DiscordProvider()
    elif provider_name == "slack":
        return SlackProvider()
    elif provider_name == "teams":
        return TeamsProvider()
    else:
        log_incorrect_provider_name(provider_name=provider_name)
        logger.error(f"Provider {provider_name} is not supported! raise a ticket on https://github.com/Moeh-Jama/webhook-reporter/issues/new")
        raise InvalidProviderError


def closest_approx_name(allowed_names: List[str], given_name: str) -> str:
    """Returns the closest approximate name to provided name. If none match to cutoff we return empty string"""
    close_matches = difflib.get_close_matches(given_name, allowed_names, n=1, cutoff=0.6)
    return f"Did you mean '{close_matches[0]}'?" if close_matches else ""

def set_formatter(
    provider_name: str, coverage_report: NormalisedCoverageData, test_report: TestReport
) -> BaseFormatter:
    """Generates a Formatter based on the type of provider given"""
    provider_name = process_text_input(text=provider_name)
    if provider_name == "discord":
        formatter = DiscordFormatter(
            coverage_report=coverage_report, test_report=test_report
        )
    elif provider_name == "slack":
        formatter = SlackFormatter(
            coverage_report=coverage_report, test_report=test_report
        )
    elif provider_name == "teams":
        formatter = TeamsFormatter(
            coverage_report=coverage_report, test_report=test_report
        )
    else:
        log_incorrect_provider_name(provider_name=provider_name)
        logger.error(f"Provider {provider_name} is not supported! raise a ticket on https://github.com/Moeh-Jama/webhook-reporter/issues/new")
        raise InvalidProviderError

    return formatter


def process_text_input(text: str) -> str:
    """Cleans the text to reduce any ambiguousness when comparing"""
    text = text.lower().strip()
    return text

def log_incorrect_provider_name(provider_name: str):
    allowed_provider_names = ['discord', 'slack', 'teams']
    message = closest_approx_name(allowed_names=allowed_provider_names, given_name=provider_name)
    if message:
        logger.debug(message)

def get_test_case_status(status: str) -> TestResult:
    """Returns the TestResult from given status as string"""
    status = status.lower().strip()
    if status.startswith("pass"):
        return TestResult.PASSED
    elif status.startswith("fail"):
        return TestResult.FAILED
    elif status.startswith("err"):
        return TestResult.ERROR
    elif status.startswith("skip") or status.startswith("pend"):
        return TestResult.SKIPPED
    return TestResult.UNKNOWN


def truncate_text(text: str, max_length: int = 25) -> str:
    """Truncate text to maximum length and append an ellipsis if truncated"""
    if not text:
        return text
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text
