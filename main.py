"""Main source of project"""

import logging
import os
import sys
from typing import Tuple
from dotenv import load_dotenv
from src.exceptions.configurations import (
    ConfigurationValuesNotFoundError,
    InvalidProviderError,
    UnsupportedCoverageType,
    UnsupportedTestReportType,
)
import asyncio
from src.formatters.base_formatter import BaseFormatter
from src.logger import setup_logging
from src.parsers.parser_factory import ParserFactory
from src.providers.base_provider import Baseprovider
from src.test_readers.reader_factory import ReaderFactory
from src.utils import set_formatter, set_provider

setup_logging()
logger = logging.getLogger("webhook-reporter-logger")


def setup_provider() -> Tuple[Baseprovider, BaseFormatter]:
    """Configuration gathering"""
    # Read all required environment values
    logger.debug("fetching Webhook configuration data")
    provider_name = os.getenv("INPUT_PROVIDER")
    webhook_url = os.getenv("INPUT_WEBHOOK_URL")
    coverage_file = os.getenv("INPUT_COVERAGE_FILE")

    # Verify all required configuration fields are present
    if not (provider_name and webhook_url and coverage_file and coverage_file):
        raise ConfigurationValuesNotFoundError

    # Non-required fields are None and handled subsequently.
    test_file = os.getenv("INPUT_TEST_RESULTS")
    coverage_threshold = os.getenv("INPUT_COVERAGE_THRESHOLD")

    try:
        coverage_threshold = float(coverage_threshold) if coverage_threshold else None
    except Exception:
        logger.error(
            f"Error reading the threshold value '{coverage_threshold}' with type '{type(coverage_threshold)}'"
        )

    try:
        parser = ParserFactory.get_parser(coverage_file)
    except UnsupportedCoverageType as e:
        print(e)
        sys.exit(1)
    coverage_report = parser.parse_and_normalise(coverage_file=coverage_file)
    logger.debug("Coverage report parsed")

    try:
        reader = ReaderFactory.get_reader(test_file=test_file)
    except UnsupportedTestReportType as e:
        print(e)
        sys.exit(1)

    test_report = reader.read(test_file)
    logger.debug("Test Suites report parsed")

    try:
        formatter = set_formatter(provider_name=provider_name, coverage_report=coverage_report, test_report=test_report)
        provider = set_provider(provider_name=provider_name)
    except InvalidProviderError:
        sys.exit(1)

    logger.debug("Webhook configured")
    return provider, formatter


def main():
    """Reads the coverage file"""
    provider, formatter = setup_provider()
    message = formatter.generate_full_message()

    logger.info("Sending report via webhook")
    asyncio.run(provider.send_report(messages=message))


if __name__ == "__main__":
    load_dotenv()
    main()
