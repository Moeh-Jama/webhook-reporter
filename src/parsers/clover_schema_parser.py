"""
    Jest based coverage parser
    reference on schema creation:[AggregatedResult] https://raw.githubusercontent.com/jestjs/jest/bd1c6db7c15c23788ca3e09c919138e48dd3b28a/packages/jest-test-result/src/types.ts#L54
    Note: files are only in JSON.
"""

from typing import Any
from src.parsers.schema_parser import SchemaParser
from src.models.data_reports import FileCoverage, NormalisedCoverageData
import xml.etree.ElementTree as ET


class CloverSchemaParser(SchemaParser):
    """Jest Schema parser"""

    def parse_and_normalise(self, coverage_file: str) -> NormalisedCoverageData:
        """Parse the JSON converage_file and generate a normalised coverage"""
        # <metrics statements="12" coveredstatements="4" conditionals="6" coveredconditionals="0" methods="4" coveredmethods="3" elements="22" coveredelements="7" complexity="0" loc="12" ncloc="12" packages="1" files="2" classes="2"/>
        # coverage/line_rate = coveredstatements/statements
        tree = ET.parse(coverage_file)
        root = tree.getroot()
        timestamp = root.attrib["generated"]

        files = []
        statements = 0
        covered_statements = 0

        conditionals  = 0
        covered_conditionals  = 0
        for file in root.findall(".//file"):
            metric = file.find('.//metrics')
            filename = file.attrib["name"]
            statement = float(metric.attrib['statements'])
            covered_statement = float(metric.attrib['coveredstatements'])
            line_rate = covered_statement / statement
            conditional = float(metric.attrib['conditionals'])
            covered_conditional = float(metric.attrib['coveredconditionals'])
            branch_rate = 0
            if conditional != 0:
                branch_rate = covered_conditional / conditional
            complexity = self._calculate_cyclomatic_complexity(element=file)

            statements += statement
            covered_statements += covered_statement
            conditionals += conditional
            covered_conditionals += covered_conditional

            file_coverage = FileCoverage(
                filename=filename,
                line_rate=line_rate,
                branch_rate=branch_rate,
                complexity=complexity,
            )
            files.append(file_coverage)

        line_rate = covered_statements / statements
        branch_rate = covered_conditionals / conditionals
        return NormalisedCoverageData(
            total_line_rate=round(line_rate, 4),
            total_branch_rate=round(branch_rate, 4),
            files=files,
            timestamp=timestamp,
        )

    def normalise(self, parsed_data: Any) -> NormalisedCoverageData:
        """Reads the parsed data from coverage file and creates Normalised coverage object"""
        return super().normalise(parsed_data)


    def _calculate_cyclomatic_complexity(self,element: ET.Element) -> int:
        """Calculates per Cyclomatic Complexity=Number of Decision Points+1 """
        decision_point = 0
        for line in element.findall('.//line'):
            # We only check for conditional (decision points)
            if line.get('type') == 'cond':
                decision_point += 1

        return decision_point + 1