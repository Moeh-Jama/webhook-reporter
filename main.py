"""Main source of project"""

import logging
import os
import sys
from dotenv import load_dotenv
from src.exceptions.configurations import ConfigurationValuesNotFoundError, UnsupportedCoverageType, UnsupportedTestReportType
import asyncio
from src.formatters.discord_formatter import DiscordFormatter
from src.parsers.parser_factory import ParserFactory
from src.test_readers.reader_factory import ReaderFactory
from src.utils import set_provider

logger = logging.getLogger("webhook-reporter")


def setup_provider():
    """Configuration gathering"""
    # Read all required environment values
    provider_name = os.getenv("INPUT_PROVIDER")
    webhook_url = os.getenv("INPUT_WEBHOOK_URL")
    coverage_file = os.getenv("INPUT_COVERAGE_FILE")
    print('GITHUB_REPOSITORY', os.getenv('GITHUB_REPOSITORY', 'unknown'))
    print('GITHUB_EVENT_NAME', os.getenv('GITHUB_EVENT_NAME', 'unknown'))
    print('GITHUB_REF_NAME', os.getenv('GITHUB_REF_NAME', 'unknown'))
    print('GITHUB_ACTION', os.getenv('GITHUB_ACTION', 'unknown'))
    print('GITHUB_ACTION_REPOSITORY', os.getenv('GITHUB_ACTION_REPOSITORY', 'unknown'))
    print('GITHUB_PATH', os.getenv('GITHUB_PATH', 'unknown'))
    print('GITHUB_JOB', os.getenv('GITHUB_JOB', 'unknown'))
    print('GITHUB_REF', os.getenv('GITHUB_REF', 'unknown'))
    print('GITHUB_SHA', os.getenv('GITHUB_SHA', 'unknown'))
    # Verify all required configuration fields are present
    if not (provider_name and webhook_url and coverage_file and coverage_file):
        raise ConfigurationValuesNotFoundError
    # Non-required fields are None and handled subsequently.
    test_file = os.getenv("INPUT_TEST_RESULTS")
    coverage_threshold = os.getenv("INPUT_COVERAGE_THRESHOLD")

    try:
        coverage_threshold = float(coverage_threshold) if coverage_threshold else None
    except Exception:
        logger.error(f"Error reading the threshold value '{coverage_threshold}' with type '{type(coverage_threshold)}'")

    try:
        parser = ParserFactory.get_parser(coverage_file)
    except UnsupportedCoverageType as e:
        print(e)
        sys.exit(1)
    coverage_report = parser.parse_and_normalise(coverage_file=coverage_file)
    try:
        reader = ReaderFactory.get_reader(test_file=test_file)
    except UnsupportedTestReportType as e:
        print(e)
        sys.exit(1)

    test_report = reader.read(test_file)
    formatter = DiscordFormatter(coverage_report=coverage_report, test_report=test_report)
    provider = set_provider(provider_name=provider_name)
    return provider, formatter


def main():
    """Reads the coverage file"""
    provider, formatter = setup_provider()
    message = formatter.generate_full_message()
    asyncio.run(provider.send_report(messages=message))


if __name__ == "__main__":
    load_dotenv()
    main()
