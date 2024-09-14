"""Module to hold markdown formatting code units"""

import textwrap
from typing import List
from src.models.test_suite import TestCase, TestIcons, TestReport, TestResult

def generate_test_summary_by_status(test_report: TestReport, markdown_style: str = '') -> str:
    """Generates a formatted message highlighting test results by status.
    
    Args:
        test_report (TestReport): The given test report we get the test_cases from.
        markdown_style (str): The style of the markdown code block. Defaults to an empty string, which means no specific language is specified.
    """
    output = ""

    skipped = generate_test_status_summary(
        title="Skipped Tests",
        tests=test_report.get_tests_by_status(test_status=TestResult.SKIPPED),
        markdown_style=markdown_style,
    )
    if skipped:
        output += TestIcons.SKIPPED.value + skipped

    failures = generate_test_status_summary(
        title="Failed Tests",
        tests=test_report.get_tests_by_status(test_status=TestResult.FAILED),
        markdown_style=markdown_style,
    )
    if failures:
        output += TestIcons.FAILED.value + failures

    errors = generate_test_status_summary(
        title="Errors",
        tests=test_report.get_tests_by_status(test_status=TestResult.ERROR),
        markdown_style=markdown_style,
    )
    if errors:
        output += TestIcons.ERROR.value + errors

    return output



def generate_test_status_summary(title: str, tests: List[TestCase], markdown_style: str = '') -> str:
    """Returns a formatted markdown string with a title and a list of test cases.
    
    Args:
        title (str): The title to be included in the markdown, which will be capitalized.
        tests (List[TestCase]): A list of test cases to be formatted. Only the first few are included in the output.
        markdown_style (str): The style of the markdown code block. Defaults to an empty string, which means no specific language is specified.
    
    Returns:
        str: A markdown-formatted string including the title and the formatted test cases.
    
    The title is capitalized, and the count of test cases is included in parentheses.
    The function iterates over the first few test cases (up to 4) and creates a formatted list of messages.
    """
    
    if not tests:
        return ""

    title = f"__**{title.capitalize()}**__ ({len(tests)})"
    message = f"```{markdown_style}"
    for test in tests[:4]: # TODO: get MAX
        test_msg = test.message or ""
        test_case_message = f"{textwrap.dedent(test_msg).strip()[:250]}\n" if test_msg else ""
        message += f"\n{test.name}:\n{test_case_message}"
    message += "```"
    return f"{title}\n{message}"

