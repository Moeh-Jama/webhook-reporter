"""
    Standard Coverage Schema parser

    based on: https://raw.githubusercontent.com/cobertura/web/master/htdocs/xml/coverage-04.dtd
"""

from typing import Any
import xml.etree.ElementTree as ET
from src.parsers.schema_parser import SchemaParser
from src.models.data_reports import FileCoverage, NormalisedCoverageData


class StandardSchemaParser(SchemaParser):
    def parse_and_normalise(self, coverage_file: str) -> NormalisedCoverageData:
        """parses coverage file and return its normalised object"""
        tree = ET.parse(coverage_file)
        root = tree.getroot()
        timestamp = root.attrib["timestamp"]
        total_line_rate = float(root.attrib["line-rate"])
        total_branch_rate = float(root.attrib["branch-rate"])

        files = []
        for package in root.findall(".//package"):
            for cls in package.findall(".//class"):
                filename = cls.attrib["filename"]
                line_rate = float(cls.attrib["line-rate"])
                branch_rate = float(cls.attrib["branch-rate"])
                complexity = float(cls.attrib["complexity"])

                file_coverage = FileCoverage(
                    filename=filename,
                    line_rate=line_rate,
                    branch_rate=branch_rate,
                    complexity=complexity,
                )
                files.append(file_coverage)
        return NormalisedCoverageData(
            total_line_rate=total_line_rate,
            total_branch_rate=total_branch_rate,
            files=files,
            timestamp=timestamp,
        )

    def normalise(self, parsed_data: Any) -> NormalisedCoverageData:
        """Normalises the parsed 'coverage' data"""
        pass