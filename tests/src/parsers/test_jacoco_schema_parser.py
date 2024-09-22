"""Tests Jacoco file parsing"""

from pathlib import Path

from src.parsers.jacoco_schema_parser import JacocoSchemaParser


xml_file_path = Path(__file__).parent.parent.parent / "data" / "xml" / "coverage"

def test_jacoco_coverage_data():
    """Reads sample coverage file correctly"""
    parser = JacocoSchemaParser()
    file = "sample_jacoco_coverage.xml"
    
    coverage_data = parser.parse_and_normalise(f"{xml_file_path}/{file}")

    # Validate coverage rates are expected.
    expected_line_rate = 50
    expected_branch_rate = 0
    assert coverage_data.total_line_rate == expected_line_rate
    assert coverage_data.total_branch_rate == expected_branch_rate
    assert coverage_data.complexity_avg == 4.0

    assert coverage_data.total == 2

    file1 =coverage_data.files[0]
    assert file1.filename == 'Main.java'
    assert file1.line_rate == 0.0
    assert file1.branch_rate == 0
    assert file1.complexity == 3


    file2 =coverage_data.files[1]
    assert file2.filename == 'Calculator.java'
    assert file2.line_rate == 1.0
    assert file2.branch_rate == 0.0
    assert file2.complexity == 5.0