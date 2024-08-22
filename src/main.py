"""Main source of project"""

import logging
import os
import xml.etree.ElementTree as ET

from dotenv import load_dotenv

from exceptions.configurations import ConfigurationValuesNotFoundError

logger = logging.getLogger("webhook-reporter")
COVERAGE_THRESHOLD = 65


def setup():
    """Configuration gathering"""
    provider = os.getenv("INPUT_PROVIDER")  # Discord for example
    webhook_url = os.getenv("INPUT_WEBHOOK_URL")
    coverage_format = os.getenv("INPUT_COVERAGE_FORMAT")
    coverage_file = os.getenv("INPUT_COVERAGE_FILE")
    if not (provider and webhook_url and coverage_file and coverage_file):
        raise ConfigurationValuesNotFoundError

    coverage_threshold = os.getenv("INPUT_COVERAGE_THRESHOLD")
    print(provider, webhook_url, coverage_format, coverage_file, coverage_threshold)


def parse_coverage_report(coverage_file):
    """parses the coverage report at line rate"""
    tree = ET.parse(coverage_file)
    root = tree.getroot()
    coverage = root.attrib.get("line-rate")  # Line Rate is the coverage for pytest
    return float(coverage) * 100


def main():
    """Reads the coverage file"""
    setup()
    coverage_file_name = os.getenv("INPUT_COVERAGE_FILE")
    try:
        coverage = parse_coverage_report(coverage_file_name)
    except FileNotFoundError:
        # TODO: what should we do when no coverage was created?
        # This could be because of the different
        #   1. naming
        #   2. error at pytest. -> Do we report to user?
        logger.error(
            "[WEBHOOK-REPORTER] - coverage file '%s' was not produced. Cannot report.",
            coverage_file_name,
        )
        return None
    payload = {
        "coverage": coverage,
        "status": "success" if coverage >= COVERAGE_THRESHOLD else "failure",
    }
    print(payload)


if __name__ == "__main__":
    load_dotenv()
    main()
