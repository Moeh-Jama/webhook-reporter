from pathlib import Path

from src.models.test_suite import TestStatus
from src.test_readers.jest_reader import JestJSONReader


json_file_path = Path(__file__).parent.parent.parent / "data" / "json" / "tests"


def test_report_generation():
    """Test that the read/parsed test result is correctly transformed to TestReport"""
    file_name = "test_jest.json"
    reader = JestJSONReader()

    test_report = reader.read(file_path=f"{json_file_path}/{file_name}")

    assert len(test_report.suites) == 1
    assert test_report.total_tests == 6

    assert test_report.success_rate == 1
    assert test_report.total_passed == 6

    assert test_report.total_failed == 0
    assert test_report.total_error == 0
    assert test_report.total_skipped == 0

    testsuite = test_report.suites[0]
    assert testsuite.time == 0.45  # seconds

    assert testsuite.tests[0].name == "should add a new task"
    assert testsuite.tests[1].name == "should complete a task"
    assert (
        testsuite.tests[-1].name
        == "should throw an error when deleting a task with an invalid index"
    )


def test_report_generation_with_fail():
    """Create a TestReport from given junit test file"""
    reader = JestJSONReader()
    file_name = "test_jest_with_failure.json"

    test_report = reader.read(file_path=f"{json_file_path}/{file_name}")

    assert len(test_report.suites) == 1
    assert test_report.total_tests == 7

    assert test_report.total_passed == 6
    assert test_report.total_failed == 1

    failure_summary = test_report.failure_summary

    assert len(failure_summary["suite_test"]) == 1
    assert (
        failure_summary["suite_test"][0]
        == "exception raising for object as title: Error: expect(received).toThrow()\n\nReceived functi..."
    )

    failures = test_report.get_tests_by_status(test_status=TestStatus.FAILED)
    assert len(failures) == 1
