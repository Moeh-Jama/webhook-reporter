"""
Reader for all JUNIT type XMLS

utilization: pytest, surefire
"""

from typing import List
from src.models.test_suite import TestCase, TestReport, TestResult, TestSuite
from src.test_readers.base_reader import BaseTestSuiteReader
import xml.etree.ElementTree as ET

from src.utils import get_test_case_status


class JUnitReader(BaseTestSuiteReader):
    def read(self, file_path: str) -> TestReport:
        """Read JUnit type file with associated TestSuites"""

        tree = ET.parse(file_path)
        root = tree.getroot()

        # Parsing the JUnit XML
        suites: List[TestSuite] = []
        if root.findall(".//testsuite"):
            for testsuite in root.findall(".//testsuite"):
                test_cases: List[TestCase] = self._test_suite_collection(
                    testsuite=testsuite
                )

                suite = TestSuite(
                    name=testsuite.attrib["name"],
                    tests=test_cases,
                    time=float(testsuite.attrib.get("time", 0)),
                )
                suites.append(suite)
        else:
            testsuite = root
            test_cases: List[TestCase] = self._test_suite_collection(
                testsuite=testsuite
            )
            suite = TestSuite(
                name=testsuite.attrib["name"],
                tests=test_cases,
                time=float(testsuite.attrib.get("time", 0)),
            )
            suites.append(suite)

        return TestReport(suites=suites)

    def _test_suite_collection(self, testsuite: ET.Element) -> List[TestCase]:
        test_cases: List[TestCase] = []
        for test_case in testsuite.findall(".//testcase"):
            testcase = self.create_test_case(test_case)
            test_cases.append(testcase)
        return test_cases

    def create_test_case(self, test_case: ET.Element) -> TestCase:
        """transforms given JUnit Element for testcase into TestCase"""
        message: str = None
        full_message: str = None
        status: TestResult = TestResult.PASSED
        cases = test_case.findall(".//")
        if len(cases) > 0:
            case = cases[0]
            status = get_test_case_status(case.tag)
            message = case.attrib.get("message", "")
            full_message = case.text

        testcase = TestCase(
            name=test_case.attrib["name"],
            status=status,
            time=test_case.attrib["time"],
            message=message,
            full_message=full_message,
        )

        return testcase
