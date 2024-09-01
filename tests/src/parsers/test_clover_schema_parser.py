"""Tests Clover file parsing"""

from pathlib import Path

from src.parsers.clover_schema_parser import CloverSchemaParser


xml_file_path = Path(__file__).parent.parent.parent / "data" / "xml" / "coverage"


def test_coberature_coverage_data():
    """Reads sample coverage file correctly"""
    parser = CloverSchemaParser()
    file = "sample_clover_coverage.xml"
    
    coverage_data = parser.parse_and_normalise(f"{xml_file_path}/{file}")

    expected_line_rate = 4/12 # coveredstatements / statements
    expected_branch_rate = 0/6 # coveredconditionals / conditionals
    assert coverage_data.total_line_rate == int(expected_line_rate * 100)
    assert coverage_data.total_branch_rate == int(expected_branch_rate * 100)
    assert coverage_data.complexity_avg == 2.5 # See cyclomatic_complexity (use cond values)

    assert coverage_data.total == 2

    file1 = coverage_data.files[0]
    
    assert file1.filename == 'math.js'
    assert file1.line_rate == 1
    assert file1.branch_rate == 0

    file2 = coverage_data.files[1]
    assert file2.filename == 'registration.js'
    assert file2.line_rate == int(0/8)
    assert file2.branch_rate == int(1/6)
