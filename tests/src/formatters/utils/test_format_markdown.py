


import pytest

from src.formatters.utils.format_markdown import generate_test_status_summary
from src.models.test_suite import TestCase, TestReport, TestResult, TestSuite


# Mock TestCase class for testing purposes
class MockTestCase:
    def __init__(self, name: str, message: str):
        self.name = name
        self.message = message

@pytest.fixture
def mock_test_report_with_insanely_long_failure_message():
    insanely_long_error_message = 'An Error' * 21000
    test3 = TestCase(name='failing', status=TestResult.FAILED, time='13', message=insanely_long_error_message, full_message=insanely_long_error_message )
    suite = TestSuite(name="file_tests", tests=[test3]*500, time=13.0)
    return TestReport(suites=[suite])


def test_generate_test_status_summary_multiple_cases():
    tests = [
        MockTestCase(name="Test 1", message="This is the message for test 1"),
        MockTestCase(name="Test 2", message="This is the message for test 2"),
        MockTestCase(name="Test 3", message="This is the message for test 3"),
        MockTestCase(name="Test 4", message="This is the message for test 4"),
        MockTestCase(name="Test 5", message="This is the message for test 5"),
    ]
    result = generate_test_status_summary("test cases", tests, "python")
    expected = (
        "__**Test cases**__ (5)\n"
        "```python\n"
        "Test 1:\nThis is the message for test 1\n"
        "\nTest 2:\nThis is the message for test 2\n"
        "\nTest 3:\nThis is the message for test 3\n"
        "\nTest 4:\nThis is the message for test 4\n"
        "```"
    )
    assert result == expected

def test_generate_test_status_summary_empty_list():
    result = generate_test_status_summary("test cases", [], "python")
    expected = ""
    assert result == expected

def test_generate_test_status_summary_single_case():
    tests = [MockTestCase(name="Test 1", message="This is the message for test 1")]
    result = generate_test_status_summary("single test", tests, "python")
    expected = (
        "__**Single test**__ (1)\n"
        "```python\n"
        "Test 1:\nThis is the message for test 1\n"
        "```"
    )
    assert result == expected

def test_generate_test_status_summary_single_case_javascript_format():
    tests = [MockTestCase(name="Test 1", message="This is the message for test 1")]
    result = generate_test_status_summary("single test", tests, "javascript")
    expected = (
        "__**Single test**__ (1)\n"
        "```javascript\n"
        "Test 1:\nThis is the message for test 1\n"
        "```"
    )
    assert result == expected

def test_generate_test_status_summary_long_message():
    long_message = "A" * 300  # Message longer than 250 characters
    tests = [MockTestCase(name="Test 1", message=long_message)]
    result = generate_test_status_summary("long message test", tests, "python")
    expected = (
        "__**Long message test**__ (1)\n"
        "```python\n"
        "Test 1:\n" + long_message[:250] + "\n"
        "```"
    )
    assert result == expected

def test_generate_test_status_summary_different_markdown_styles():
    tests = [MockTestCase(name="Test 1", message="This is the message for test 1")]
    
    result = generate_test_status_summary("markdown style test", tests, "json")
    expected = (
        "__**Markdown style test**__ (1)\n"
        "```json\n"
        "Test 1:\nThis is the message for test 1\n"
        "```"
    )
    assert result == expected