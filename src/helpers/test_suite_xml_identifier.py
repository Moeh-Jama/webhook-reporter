from src.exceptions.configurations import UnsupportedTestReportType
from src.helpers.xml_identifier_base import XmlIdentifierBase
from src.models.file_types import TestSuiteFileType


class TestSuiteXmlIdentifier(XmlIdentifierBase):
    """Identifies the type of Test Suite we are dealing with"""

    __test__ = False

    def identify_suite(self) -> TestSuiteFileType:
        if self.root is None:
            self.load_xml()

        # Check for JUnit
        if self.root.tag == "testsuites":
            # JUnit and similar formats (e.g. Jest, Pytest using JUnit reporter)
            if any(child.tag == "testsuite" for child in self.root):
                return TestSuiteFileType.JUNIT
        elif self.root.tag == "testsuite":
            # Single <testsuite> root, which is valid for JUnit as well
            return TestSuiteFileType.JUNIT
        # Check for TestNG
        if self.root.tag == "testng-results":
            return TestSuiteFileType.TESTNG

        # Check for NUnit
        if self.root.tag == "test-results" and "total" in self.root.attrib:
            return TestSuiteFileType.NUNIT

        raise UnsupportedTestReportType()
