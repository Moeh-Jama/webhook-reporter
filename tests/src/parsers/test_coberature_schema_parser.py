"""Tests Coberature file parsing"""

from pathlib import Path

from src.parsers.coberature_schema_parser import CoberatureSchemaParser


xml_file_path = Path(__file__).parent.parent.parent / "data" / "xml" / "coverage"

def test_coberature_coverage_data():
    """Reads sample coverage file correctly"""
    parser = CoberatureSchemaParser()
    file = "sample_coberature_coverage.xml"
    
    coverage_data = parser.parse_and_normalise(f"{xml_file_path}/{file}")

    # Validate coverage rates are expected.
    expected_line_rate = 90
    expected_branch_rate = 75
    assert coverage_data.total_line_rate == expected_line_rate
    assert coverage_data.total_branch_rate == expected_branch_rate
    assert coverage_data.complexity_avg == ((2.5 + 1.5) / 2)

    assert coverage_data.total == 2

    file1 =coverage_data.files[0]
    assert file1.filename == 'file1.py'
    assert file1.line_rate == 0.9
    assert file1.branch_rate == 0.8
    assert file1.complexity == 2.5


    file2 =coverage_data.files[1]
    assert file2.filename == 'file2.py'
    assert file2.line_rate == 0.7
    assert file2.branch_rate == 0.6
    assert file2.complexity == 1.5
