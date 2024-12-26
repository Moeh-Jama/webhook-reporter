"""Returns reader based on given framework"""

from src.exceptions.configurations import UnsupportedTestReportType
from src.helpers.test_suite_xml_identifier import TestSuiteXmlIdentifier
from src.models.file_types import TestSuiteFileType
from src.test_readers.jest_reader import JestJSONReader
from src.test_readers.junit_reader import JUnitReader


class ReaderFactory:
    """Return Reader type based on framework given"""
    @staticmethod
    def get_reader(test_file: str):
        if not test_file:
            return None
        if test_file.endswith('json'):
            return JestJSONReader()
        
        if not test_file.endswith('xml'):
            raise UnsupportedTestReportType()

        test_suite_identifier = TestSuiteXmlIdentifier(xml_file=test_file)
        test_suite_type = test_suite_identifier.identify_suite()

        if test_suite_type == TestSuiteFileType.JUNIT:
            return JUnitReader()
        else:
            raise UnsupportedTestReportType()
