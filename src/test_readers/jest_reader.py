"""Reads JSON Jest tests"""


from typing import Any, Dict, List
from src.models.test_suite import TestCase, TestReport, TestStatus, TestSuite
from src.test_readers.base_reader import BaseTestSuiteReader
import json

from src.utils import get_test_case_status

class JestJSONReader(BaseTestSuiteReader):
    """Reading JSON Test data"""

    def read(self, file_path: str) -> TestReport:
        """Reads the JSON file and transforms it to TestReport file"""
        f = open(file_path, encoding='utf-8')
        test_results = json.load(f)

        testsuites: List[TestSuite] = []
        for test_suite in test_results['testResults']:
            test_case_list: List[TestCase] = []
            for test_case in test_suite['assertionResults']:
                test_case_list.append(self.create_test_case(test_case=test_case))
            
            duration = float(test_suite.get('endTime')) - float(test_suite.get('startTime'))
            print('duration', duration)
            testsuite = TestSuite(
                name=test_suite.get('name', ''),
                tests=test_case_list,
                time=round(duration/1000, 2)

            )
            testsuites.append(testsuite)

        f.close()
        return TestReport(suites=testsuites)


    def create_test_case(self, test_case: Dict[str, Any]) -> TestCase:
        """transforms given JSON Element for testcase into TestCase"""

        status = get_test_case_status(test_case['status'])
        message = test_case.get('failure_messages', [''])[0] # get the first one.

        duration = test_case.get('duration', 0)
        if not duration:
            duration = 0
        return TestCase(
            name=test_case['title'],
            status=status,
            time=str(round(duration/1000, 2)),
            message=message
        )