"""Testing Standard Schema Parser"""

import pytest
from unittest.mock import patch, mock_open
import xml.etree.ElementTree as ET
from src.parsers.standard_schema_parser import StandardSchemaParser
from src.models.data_reports import FileCoverage, NormalisedCoverageData


@pytest.fixture
def sample_coverage_xml():
    """Fixture that provides a sample XML coverage data."""
    return """<?xml version="1.0" ?>
    <coverage line-rate="0.85" branch-rate="0.75" timestamp="1628472326">
        <packages>
            <package>
                <classes>
                    <class filename="file1.py" line-rate="0.9" branch-rate="0.8" complexity="2.5"/>
                    <class filename="file2.py" line-rate="0.7" branch-rate="0.6" complexity="1.5"/>
                </classes>
            </package>
        </packages>
    </coverage>
    """


def test_parse_and_normalise(sample_coverage_xml):
    """Test the parse_and_normalise method of StandardSchemaParser."""
    parser = StandardSchemaParser()

    # Mock open to simulate reading the coverage file
    with patch("builtins.open", mock_open(read_data=sample_coverage_xml)):
        result = parser.parse_and_normalise("mock_coverage.xml")

    # Expected output
    expected_files = [
        FileCoverage(
            filename="file1.py", line_rate=0.9, branch_rate=0.8, complexity=2.5
        ),
        FileCoverage(
            filename="file2.py", line_rate=0.7, branch_rate=0.6, complexity=1.5
        ),
    ]
    expected_data = NormalisedCoverageData(
        total_line_rate=0.85,
        total_branch_rate=0.75,
        files=expected_files,
        timestamp="1628472326",
    )

    # Assertions
    assert result.total_line_rate == expected_data.total_line_rate
    assert result.total_branch_rate == expected_data.total_branch_rate
    assert result.timestamp == expected_data.timestamp
    assert len(result.files) == len(expected_data.files)
    for i, file_coverage in enumerate(result.files):
        assert file_coverage.filename == expected_data.files[i].filename
        assert file_coverage.line_rate == expected_data.files[i].line_rate
        assert file_coverage.branch_rate == expected_data.files[i].branch_rate
        assert file_coverage.complexity == expected_data.files[i].complexity
