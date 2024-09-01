"""Reads JSON Jest tests"""


import re
from typing import Any, Dict, List, Tuple
from src.models.test_suite import TestCase, TestReport, TestStatus, TestSuite
from src.test_readers.base_reader import BaseTestSuiteReader
import json

from src.utils import get_test_case_status, truncate_text

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
        message = test_case.get('failureMessages', []) # get the first one.
        full_message: str = None
        if len(message) > 0 or status == TestStatus.FAILED:
            full_message, message = self._format_json_details(test_case=test_case)
        else:
            message = ''
            full_message = ''

        duration = test_case.get('duration', 0)
        if not duration:
            duration = 0
        return TestCase(
            name=test_case['title'],
            status=status,
            time=str(round(duration/1000, 2)),
            message=message,
            full_message=full_message
        )
    

    def remove_ansi_formats(self, error_message: str) -> str:
        """Removes the ANSI escape sequences"""
        ansi_escape = re.compile(r'\x1b\[([0-9]+;)*[0-9]*m')

        # substitute the escape sequences with nothing
        return ansi_escape.sub('', error_message)


    def _format_json_details(self, test_case: Dict[str, Any]) -> Tuple[str, str]:
        """Formats the given message into full_message and simple message"""
        full_message, message = '', ''
        error_message = self.remove_ansi_formats(test_case.get('failureMessages', [''])[0])
        if not error_message:
            return full_message, message
        
        message = truncate_text(error_message.split('//')[-1], max_length=50)
        full_message = error_message
        return full_message, message



        