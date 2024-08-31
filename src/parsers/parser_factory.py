"""Parser Factory"""

from src.exceptions.configurations import UnknownCoverageSchema, UnsupportedCoverageType
from src.parsers.jest_schema_parser import JestCloveredSchemaParser
from src.parsers.schema_parser import SchemaParser
from src.parsers.standard_schema_parser import StandardSchemaParser
from src.utils import process_text_input
from src.models.data_reports import FRAMEWORK_TO_COVERAGE, CoverageType


class ParserFactory:
    """Creates a SchemaParser parser"""

    @staticmethod
    def get_parser(test_framework: str) -> SchemaParser:
        """Returns parser from given test_framework"""
        test_framework = process_text_input(text=test_framework)
        coverage_schema = FRAMEWORK_TO_COVERAGE.get(
            test_framework
        )  # TODO: add 'detect' instead.

        if not coverage_schema:
            raise UnsupportedCoverageType(test_framework)

        if coverage_schema == CoverageType.STANDARD:
            return StandardSchemaParser()
        elif coverage_schema == CoverageType.JEST:
            return JestCloveredSchemaParser()
        else:
            raise UnknownCoverageSchema(
                f"No parser implemented for schema: {coverage_schema}\ncoverage_format not supported! raise a Ticket on https://github.com/Moeh-Jama/webhook-reporter/issues/new"
            )
