"""Base Schema Parser"""

from abc import ABC, abstractmethod
from typing import Any

from src.models.data_reports import CoverageType, NormalisedCoverageData


class SchemaParser(ABC):
    """Abstract Schema Parser based on Coverage report schema"""

    @abstractmethod
    def parse_and_normalise(self, coverage_file: str) -> NormalisedCoverageData:
        """Parse the data and return the normalised view"""
        super().parse_and
    
    @abstractmethod
    def normalise(self, parsed_data: Any) -> NormalisedCoverageData:
        """Normalised the data from parsed_data into a standard normalised object"""
        raise NotImplementedError
    
    def detect_coverage_type(coverage_file: str) -> CoverageType:
        """detects the xml file coverage type"""
        pass