"""The Base Formatter used by all Providers to format their messages"""

from abc import ABC, abstractmethod
import os
from config import BOT_IMAGE
from src.helpers.github_action import GitHubActionInfo
from src.models.data_reports import NormalisedCoverageData
from src.models.test_suite import TestReport


class BaseFormatter(ABC):
    """Parent class for Formatters"""

    def __init__(
        self,
        coverage_report: NormalisedCoverageData,
        test_report: TestReport = None,
    ):
        self.coverage_report = coverage_report
        self.test_report = test_report
        self.github_action = GitHubActionInfo()
        self.MAX_TEST_SHOWN = 4
    
    @abstractmethod
    def generate_full_message(self):
        """Generates the full message. To be implemented by subclasses."""
        pass

    @abstractmethod
    def format_coverage(self):
        """Formats the coverage section specific to each platform."""
        pass

    @abstractmethod
    def format_test_report(self):
        """Formats the test report section specific to each platform."""
        pass
    
    @abstractmethod
    def format_footer(self):
        """Formats the footer of the message(s) to each platform"""
        pass

    def _get_footer(self):
        """All formatters might share a similar footer structure."""
        
        return {
            "message": "Notified via Webhook Reporter",
            "url": "example.com",
            "icon_url": BOT_IMAGE
        }

    def calculate_coverage_status(self) -> str:
        """Returns color value based on threshold or default of 0.8
        if a current coverage is less than coverage by 20% it is highlighted critical, else needs_improvement
        """
        threshold = float(os.getenv("COVERAGE_THRESHOLD", "0")) / 100.0
        rate = self.coverage_report.total_line_rate

        if rate >= threshold:
            return "good"
        elif rate < threshold * 0.8:
            return "critical"
        return "needs_improvement"
