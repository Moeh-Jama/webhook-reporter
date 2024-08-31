"""
    Jacoco schema parser
    based on: https://raw.githubusercontent.com/jacoco/jacoco/master/org.jacoco.report/src/org/jacoco/report/xml/report.dtd
"""

from typing import Any
from src.parsers.schema_parser import SchemaParser
from src.models.data_reports import NormalisedCoverageData


class JacocoSchemaParser(SchemaParser):
    """Parse Jacoco schemas based on reports.dtd definition"""

    def parse_and_normalise(self, coverage_file: str) -> NormalisedCoverageData:
        """Parse the JSON converage_file and generate a normalised coverage"""
        return super().parse_and_normalise(coverage_file)

    def normalise(self, parsed_data: Any) -> NormalisedCoverageData:
        """Reads the parsed data from coverage file and creates Normalised coverage object"""
        return super().normalise(parsed_data)
