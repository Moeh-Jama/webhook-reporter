


from pathlib import Path

import pytest

from src.exceptions.configurations import UnsupportedTestReportType
from src.exceptions.file_errors import MalformedFile
from src.helpers.test_suite_xml_identifier import TestSuiteXmlIdentifier
from src.models.file_types import TestSuiteFileType


xml_file_path = Path(__file__).parent.parent.parent / "data" / "xml" / "tests"


def test_identify_junit_singular_suite_file():
    suite_identifier = TestSuiteXmlIdentifier(
        xml_file=f"{xml_file_path}/single_suite.xml"
    )

    result = suite_identifier.identify_suite()
    assert result == TestSuiteFileType.JUNIT

def test_identify_junit_multiple_suites_file():
    suite_identifier = TestSuiteXmlIdentifier(
        xml_file=f"{xml_file_path}/multiple_suites.xml"
    )

    result = suite_identifier.identify_suite()
    assert result == TestSuiteFileType.JUNIT

def test_unsupported_coverage_type():
    """Test to check if an unsupported coverage type raises an exception."""
    suite_identifier = TestSuiteXmlIdentifier(
        xml_file=f"{xml_file_path}/unsupported.xml"
    )
    with pytest.raises(UnsupportedTestReportType):
        suite_identifier.identify_suite()


def test_identify_malformed_xml():
    """Test to check if malformed XML raises an exception."""

    suite_identifier = TestSuiteXmlIdentifier(
        xml_file=f"{xml_file_path}/malformed.xml"
    )
    with pytest.raises(MalformedFile):
        suite_identifier.identify_suite()


def test_identify_xml_with_missing_attributes():
    """Test XML missing expected attributes for coverage type detection."""
    suite_identifier = TestSuiteXmlIdentifier(
        xml_file=f"{xml_file_path}/incomplete_junit_results.xml"
    )
    with pytest.raises(UnsupportedTestReportType):
        suite_identifier.identify_suite()


def test_identify_unexpected_structure():
    """Test for XML with an unexpected structure."""
    suite_identifier = TestSuiteXmlIdentifier(
        xml_file=f"{xml_file_path}/unexpected.xml"
    )
    with pytest.raises(UnsupportedTestReportType):
        suite_identifier.identify_suite()


def test_identify_empty_file():
    """Test for an empty file."""
    suite_identifier = TestSuiteXmlIdentifier(xml_file=f"{xml_file_path}/empty.xml")
    with pytest.raises(MalformedFile):
        suite_identifier.identify_suite()


def test_identify_xml_with_multiple_root_elements():
    """Test XML with multiple root elements."""
    suite_identifier = TestSuiteXmlIdentifier(
        xml_file=f"{xml_file_path}/multiple_root_tests.xml"
    )
    with pytest.raises(UnsupportedTestReportType):
        suite_identifier.identify_suite()