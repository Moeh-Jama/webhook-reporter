"""Abstract reader"""
from abc import ABC, abstractmethod

from src.models.test_suite import TestReport


class BaseTestSuiteReader(ABC):
    """Base reader for all TestSuite files"""

    def read(self, file_path: str) -> TestReport:
        """
            Reads file that contains TestSuite details and returns
            associated generic report
        """
        raise NotImplementedError