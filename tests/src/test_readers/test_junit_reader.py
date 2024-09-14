"""JUnit test reader tests"""

from pathlib import Path

from src.models.test_suite import TestResult
from src.test_readers.junit_reader import JUnitReader


xml_file_path = Path(__file__).parent.parent.parent / "data" / "xml" / "tests"


def test_report_generation_single_suite():
    """Create a TestReport from given junit test file"""
    reader = JUnitReader()
    file_name = "single_suite.xml"

    test_report = reader.read(file_path=f"{xml_file_path}/{file_name}")

    assert len(test_report.suites) == 1
    assert test_report.total_tests == 2

    assert test_report.success_rate == 1
    assert test_report.total_passed == 2

    assert test_report.total_failed == 0
    assert test_report.total_error == 0
    assert test_report.total_skipped == 0

    testsuite = test_report.suites[0]
    assert testsuite.time == 3.525  # seconds

    assert testsuite.tests[0].name == "test_adds"
    assert testsuite.tests[1].name == "test_adds2"


def test_report_generation_with_fail():
    """Create a TestReport from given junit test file"""
    reader = JUnitReader()
    file_name = "junit_with_fails.xml"

    test_report = reader.read(file_path=f"{xml_file_path}/{file_name}")

    assert len(test_report.suites) == 2

    assert test_report.total_tests == 6
    assert test_report.total_passed == 5
    assert test_report.total_failed == 1

    failure_summary = test_report.failure_summary

    assert len(failure_summary["pytest2"]) == 1
    assert failure_summary["pytest2"][0] == "test_failing_test: assert 1 == 2"

    failures = test_report.get_tests_by_status(test_status=TestResult.FAILED)
    assert len(failures) == 1
