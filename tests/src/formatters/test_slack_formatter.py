"""Tests the Normalised Reports into Slack Message Formats"""


# Fixtures for test data
from datetime import datetime
from unittest.mock import patch
import pytest

from src.formatters.slack_formatter import SlackFormatter
from src.models.data_reports import FileCoverage, NormalisedCoverageData
from src.models.test_suite import TestCase, TestReport, TestResult, TestSuite


@pytest.fixture
def mock_coverage_data():
    return NormalisedCoverageData(
        total_line_rate=0.85,
        total_branch_rate=0.9,
        complexity_avg=3.5,
        total=500,
        files=[
            FileCoverage(
                **{
                    "filename": "file1.py",
                    "line_rate": 0.8,
                    "branch_rate": 0.9,
                    "complexity": 0.0,
                }
            ),
            FileCoverage(
                **{
                    "filename": "file2.py",
                    "line_rate": 0.9,
                    "branch_rate": 0.85,
                    "complexity": 0.0,
                }
            ),
        ],
        timestamp=datetime.now(),
    )


@pytest.fixture
def mock_test_report():
    test1 = TestCase(name="file1.py", status=TestResult.PASSED, time="5")
    test2 = TestCase(name="file2.py", status=TestResult.PASSED, time="6")

    suite = TestSuite(name="file_tests", tests=[test1, test2], time=11.0)
    return TestReport(suites=[suite])


@pytest.fixture
def mock_test_report_with_failures():
    test1 = TestCase(name="file1.py", status=TestResult.PASSED, time="5")
    test2 = TestCase(name="file2.py", status=TestResult.PASSED, time="6")
    test3 = TestCase(
        name="failing",
        status=TestResult.FAILED,
        time="13",
        message="Exception occurred",
        full_message="Exception occurred but longer...",
    )
    suite = TestSuite(name="file_tests", tests=[test1, test2, test3], time=24.0)
    return TestReport(suites=[suite])

def test_generate_full_message(mock_coverage_data: NormalisedCoverageData, mock_test_report: TestReport):
    formatter = SlackFormatter(mock_coverage_data, mock_test_report)
    message_block = formatter.generate_full_message()
    assert len(message_block) > 0

    assert message_block[0]['text']['text'] == ':rocket: Test and Coverage Report'
    fields = message_block[2]['fields']
    assert len(fields) == 9
    assert fields[0]['text'].endswith('85%') # Line Coverage

def test_generate_full_message_no_test_report(mock_coverage_data: NormalisedCoverageData):
    formatter = SlackFormatter(mock_coverage_data)
    message_block = formatter.generate_full_message()
    assert len(message_block) == 6  # Only coverage report should be generated
    fields = message_block[2]['fields']
    assert len(fields) == 3

def test_generate_full_message_no_coverage_section(mock_coverage_data: NormalisedCoverageData, mock_test_report: TestReport):
    formatter = SlackFormatter(mock_coverage_data, mock_test_report)
    with patch.object(SlackFormatter, "format_coverage", return_value=None):
        with pytest.raises(
            Exception,
            match="Coverage Section failed to generate. Check the coverage report data.",
        ):
            formatter.generate_full_message()

def test_coverage_section(monkeypatch, mock_coverage_data: NormalisedCoverageData):
    monkeypatch.setenv('INPUT_COVERAGE_THRESHOLD', mock_coverage_data.total_line_rate)
    formatter = SlackFormatter(mock_coverage_data)
    coverage_section = formatter.format_coverage()
    assert (
        len(coverage_section[0]['fields']) == 3
    )  # Three fields for line coverage, complexity, and total

    assert coverage_section[1]['elements'][0]['text'] == 'Coverage Status: :large_green_circle: Good'

def test_report_embed(mock_coverage_data: NormalisedCoverageData, mock_test_report_with_failures: TestReport):
    formatter = SlackFormatter(mock_coverage_data, mock_test_report_with_failures)
    test_report_section = formatter.format_test_report()
    assert test_report_section[0]['text']['text'] == ':clipboard: Test Details'
    assert test_report_section[1]['text']['text'] == ':x: *Failed* (1)\n```\nfailing:\nException occurred:\n```'

def test_threshold_slightly_below(monkeypatch, mock_coverage_data: NormalisedCoverageData):
    monkeypatch.setenv('INPUT_COVERAGE_THRESHOLD', '0.8')
    mock_coverage_data.total_line_rate = 0.75
    formatter = SlackFormatter(mock_coverage_data)
    coverage_value = formatter._get_coverage_color()
    assert coverage_value == ':large_yellow_circle: Needs_improvement'


def test_threshold_is_exceeded(monkeypatch, mock_coverage_data: NormalisedCoverageData):
    monkeypatch.setenv('INPUT_COVERAGE_THRESHOLD', '0.7')
    mock_coverage_data.total_line_rate = 0.75
    formatter = SlackFormatter(mock_coverage_data)
    coverage_value = formatter._get_coverage_color()
    assert coverage_value == ':large_green_circle: Good'


def test_threshold_color_much_lower(monkeypatch, mock_coverage_data: NormalisedCoverageData):
    monkeypatch.setenv('INPUT_COVERAGE_THRESHOLD', '0.9')
    mock_coverage_data.total_line_rate = 0.70
    formatter = SlackFormatter(mock_coverage_data)
    coverage_value = formatter._get_coverage_color()
    assert coverage_value == ':red_circle: Critical'

def test_generate_full_message_no_coverage_report():
    formatter = SlackFormatter(None)
    with pytest.raises(Exception):
        formatter.generate_full_message()