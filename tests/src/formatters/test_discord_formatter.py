"""Tests the Normalised Reports into Discord Message Formats"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from discord import Embed, Color
from src.models.data_reports import FileCoverage, NormalisedCoverageData
from src.models.test_suite import TestCase, TestReport, TestResult, TestSuite
from src.formatters.discord_formatter import DiscordFormatter


# Fixtures for test data
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


@pytest.fixture
def mock_test_report_with_insanely_long_failure_message():
    insanely_long_error_message = "An Error" * 21000
    test3 = TestCase(
        name="failing",
        status=TestResult.FAILED,
        time="13",
        message=insanely_long_error_message,
        full_message=insanely_long_error_message,
    )
    suite = TestSuite(name="file_tests", tests=[test3] * 500, time=13.0)
    return TestReport(suites=[suite])


# Tests for generate_full_message
def test_generate_full_message(mock_coverage_data, mock_test_report):
    formatter = DiscordFormatter(mock_coverage_data, mock_test_report)
    embeds = formatter.generate_full_message()
    assert len(embeds) == 2  # Both coverage and test report should be generated
    assert isinstance(embeds[0], Embed)
    assert isinstance(embeds[1], Embed)


def test_generate_full_message_no_test_report(mock_coverage_data):
    formatter = DiscordFormatter(mock_coverage_data)
    embeds = formatter.generate_full_message()
    assert len(embeds) == 1  # Only coverage report should be generated
    assert isinstance(embeds[0], Embed)


def test_generate_full_message_no_coverage_embed(mock_coverage_data, mock_test_report):
    formatter = DiscordFormatter(mock_coverage_data, mock_test_report)
    with patch.object(DiscordFormatter, "format_coverage", return_value=None):
        with pytest.raises(
            Exception,
            match="Coverage embed failed to generate. Check the coverage report data.",
        ):
            formatter.generate_full_message()


# Tests for _coverage_embed
@pytest.fixture
def test_coverage_embed(mock_getenv, mock_coverage_data):
    formatter = DiscordFormatter(mock_coverage_data)
    embed = formatter._coverage_embed()
    assert embed.title == "random title"
    assert embed.color == Color.dark_green()
    assert (
        len(embed.fields) == 3
    )  # Three fields for line coverage, complexity, and total


# Tests for _report_embed
@pytest.fixture
def test_report_embed(mock_getenv, mock_coverage_data, mock_test_report):
    formatter = DiscordFormatter(mock_coverage_data, mock_test_report)
    embed = formatter._report_embed()
    assert embed.title == "Test Report"
    assert embed.color == Color.brand_green()
    assert len(embed.fields) == 4  # Fields from test summary


# Edge case: Test report with failures
@pytest.fixture
def test_report_embed_with_failures(
    mock_getenv, mock_coverage_data, mock_test_report_with_failures
):
    formatter = DiscordFormatter(mock_coverage_data, mock_test_report_with_failures)
    embed = formatter._report_embed()
    assert embed.title == "Test Report"
    assert embed.color == Color.brand_red()
    assert len(embed.fields) == 4  # Fields from test summary


# Tests for _threshold_color
@patch("os.getenv", return_value="80")
def test_threshold_color_high_threshold(mock_coverage_data):
    mock_coverage_data.total_line_rate = 0.75
    formatter = DiscordFormatter(mock_coverage_data)
    color = formatter._threshold_color()
    assert color == Color.yellow()


@patch("os.getenv", return_value="70")
def test_threshold_color_low_threshold(mock_getenv, mock_coverage_data):
    mock_coverage_data.total_line_rate = 0.75
    formatter = DiscordFormatter(mock_coverage_data)
    color = formatter._threshold_color()
    assert color == Color.dark_green()


@patch("os.getenv", return_value="75")
def test_threshold_color_yellow_threshold(mock_getenv, mock_coverage_data):
    mock_coverage_data.total_line_rate = 0.70
    formatter = DiscordFormatter(mock_coverage_data)
    color = formatter._threshold_color()
    assert color == Color.yellow()


# Tests for _fields
def test_fields(mock_coverage_data):
    formatter = DiscordFormatter(mock_coverage_data)
    fields = formatter._fields()
    assert len(fields) == 3
    assert fields[0].name == "Line coverage"
    assert fields[1].name == "Complexity avg"
    assert fields[2].name == "Total"


# Tests for _test_fields
def test_test_fields(mock_test_report):
    formatter = DiscordFormatter(Mock(spec=NormalisedCoverageData), mock_test_report)
    fields = formatter._test_fields(test_report_summary=mock_test_report.get_summary())
    assert len(fields) == 6


# Tests for _format_test_messages and _format_embed_description
def test_format_test_messages(mock_test_report_with_failures):
    formatter = DiscordFormatter(
        Mock(spec=NormalisedCoverageData), mock_test_report_with_failures
    )
    messages = str(formatter.test_report)
    assert "✅ Passed: 2" in messages
    assert "❌ Failed: 1" in messages
    assert "⚠️ Errors: 0" in messages
    assert "⏭️ Skipped: 0" in messages


def test_report_format_embed_description_truncation(
    mock_test_report_with_insanely_long_failure_message,
):
    formatter = DiscordFormatter(
        Mock(spec=NormalisedCoverageData),
        mock_test_report_with_insanely_long_failure_message,
    )
    failed_cases = (
        mock_test_report_with_insanely_long_failure_message.get_tests_by_status(
            test_status=TestResult.FAILED
        )
    )

    formatted_message = formatter.get_test_summary_message()
    assert len(formatted_message) <= 4096


# Ensure that exception or fallback cases are handled appropriately
def test_generate_full_message_no_coverage_report():
    formatter = DiscordFormatter(None)
    with pytest.raises(Exception):
        formatter.generate_full_message()
