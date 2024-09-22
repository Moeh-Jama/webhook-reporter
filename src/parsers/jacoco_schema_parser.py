"""
    Jacoco schema parser
    based on: https://raw.githubusercontent.com/jacoco/jacoco/master/org.jacoco.report/src/org/jacoco/report/xml/report.dtd
"""

import xml.etree.ElementTree as ET
from typing import Any
from src.models.data_reports import NormalisedCoverageData, FileCoverage

from src.parsers.schema_parser import SchemaParser


class JacocoSchemaParser(SchemaParser):
    """Parse Jacoco schemas based on reports.dtd definition"""

    def parse_and_normalise(self, coverage_file: str) -> NormalisedCoverageData:
        """Parse the Jacoco XML coverage_file and generate a normalised coverage"""
        tree = ET.parse(coverage_file)
        root = tree.getroot()
        timestamp = root.attrib.get("name")  # There is no timestamp in Jacoco, using name as a fallback

        # Initialize totals
        total_missed_lines = 0
        total_covered_lines = 0
        total_missed_branches = 0
        total_covered_branches = 0

        files = []
        for package in root.findall(".//package"):
            for cls in package.findall(".//class"):
                filename = cls.attrib["sourcefilename"]

                # Collect file-level counter information
                missed_lines = 0
                covered_lines = 0
                missed_branches = 0
                covered_branches = 0
                complexity = 0

                for counter in cls.findall(".//counter"):
                    if counter.attrib["type"] == "LINE":
                        missed_lines = int(counter.attrib["missed"])
                        covered_lines = int(counter.attrib["covered"])
                    if counter.attrib["type"] == "BRANCH":
                        missed_branches = int(counter.attrib["missed"])
                        covered_branches = int(counter.attrib["covered"])
                    if counter.attrib["type"] == "COMPLEXITY":
                        complexity = int(counter.attrib["missed"]) + int(counter.attrib["covered"])

                # Update total counters for the package
                total_missed_lines += missed_lines
                total_covered_lines += covered_lines
                total_missed_branches += missed_branches
                total_covered_branches += covered_branches

                # Calculate file-level line and branch rates
                total_lines = missed_lines + covered_lines
                total_branches = missed_branches + covered_branches

                line_rate = covered_lines / total_lines if total_lines > 0 else 0.0
                branch_rate = covered_branches / total_branches if total_branches > 0 else 0.0

                # Create the file coverage object
                file_coverage = FileCoverage(
                    filename=filename,
                    line_rate=line_rate,
                    branch_rate=branch_rate,
                    complexity=complexity,
                )
                files.append(file_coverage)

        # Calculate total coverage rates
        total_lines = total_missed_lines + total_covered_lines
        total_branches = total_missed_branches + total_covered_branches

        total_line_rate = total_covered_lines / total_lines if total_lines > 0 else 0.0
        total_branch_rate = total_covered_branches / total_branches if total_branches > 0 else 0.0

        return NormalisedCoverageData(
            total_line_rate=total_line_rate,
            total_branch_rate=total_branch_rate,
            files=files,
            timestamp=timestamp,
        )

    def normalise(self, parsed_data: Any) -> NormalisedCoverageData:
        """Reads the parsed data from coverage file and creates Normalised coverage object"""
        return super().normalise(parsed_data)
