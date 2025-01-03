"""Parser Factory"""

import logging
from src.exceptions.configurations import UnsupportedCoverageType
from src.helpers.coverage_xml_identifier import CoverageXmlIdentifier
from src.models.file_types import CoverageFileType
from src.parsers.clover_schema_parser import CloverSchemaParser
from src.parsers.jacoco_schema_parser import JacocoSchemaParser
from src.parsers.schema_parser import SchemaParser
from src.parsers.coberature_schema_parser import CoberatureSchemaParser

logger = logging.getLogger("webhook-reporter-logger")
class ParserFactory:
    """Creates a SchemaParser parser"""

    @staticmethod
    def get_parser(file_name: str) -> SchemaParser:
        """Returns parser from given test_framework"""
        file_name = file_name
        coverage_identifier = CoverageXmlIdentifier(xml_file=file_name)
        coverage_type = coverage_identifier.identifiy_report()
        logger.debug(f'Coverage file was identified as [{coverage_type.name}]')

        if coverage_type == CoverageFileType.COBERATURE:
            return CoberatureSchemaParser()
        elif coverage_type == CoverageFileType.CLOVER:
            return CloverSchemaParser()
        elif coverage_type == CoverageFileType.JACOCO:
            return JacocoSchemaParser()
        else:
            raise UnsupportedCoverageType()
