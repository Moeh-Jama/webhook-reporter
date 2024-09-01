"""All report file data objects"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import List
from math import floor

class CoverageType(Enum):
    STANDARD = auto()
    JACOCO = auto()
    JEST = auto()

FRAMEWORK_TO_COVERAGE = {
    'pytest': CoverageType.STANDARD,
    'coberature': CoverageType.STANDARD,
    'jacoco': CoverageType.JACOCO,
    'jest': CoverageType.JEST
}

@dataclass
class FileCoverage:
    filename: str
    line_rate: float
    branch_rate: float
    complexity: float

@dataclass
class NormalisedCoverageData:
    total_line_rate: float
    total_branch_rate: float
    files: List[FileCoverage]
    timestamp: str
    complexity_avg: float = 0.0
    total: int = 0

    def __post_init__(self):
        self.total_line_rate  = floor(self.total_line_rate * 100)
        self.total_branch_rate  = floor(self.total_branch_rate * 100)
        self.total = len(self.files)
        complexity_avg = sum([file.complexity for file in self.files]) /  self.total
        self.complexity_avg = round(complexity_avg, 4) # 0.0000 per DTDs of Schemas


class CoverageMetricType(Enum):
    """Coverage Enum Metric Type"""

    LINE_COVERAGE = auto()
    BRANCH_COVERAGE = auto()
    COMPLEXITY_AVG = auto()
    TOTAL = auto()
    FAILURES = auto()
    ERRORS = auto()
    SKIPPED = auto()
    TIME = auto()