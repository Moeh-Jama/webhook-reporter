"""
    Jest based coverage parser
    reference on schema creation:[AggregatedResult] https://raw.githubusercontent.com/jestjs/jest/bd1c6db7c15c23788ca3e09c919138e48dd3b28a/packages/jest-test-result/src/types.ts#L54
    Note: files are only in JSON.
"""

from typing import Any
from src.parsers.schema_parser import SchemaParser
from src.models.data_reports import NormalisedCoverageData


class JestSchemaParser(SchemaParser):
    """Jest Schema parser"""

    def parse_and_normalise(self, coverage_file: str) -> NormalisedCoverageData:
        """Parse the JSON converage_file and generate a normalised coverage"""
        return super().parse_and_normalise(coverage_file)

    def normalise(self, parsed_data: Any) -> NormalisedCoverageData:
        """Reads the parsed data from coverage file and creates Normalised coverage object"""
        return super().normalise(parsed_data)
