from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict


class TestStatus(Enum):
    """Test case status [passed, failed, skipped]"""
    PASSED = auto()
    FAILED = auto()
    ERROR = auto()
    SKIPPED = auto()
    UNKNOWN = auto()
    

class TestCase:
    """Information on given Test case"""

    def __init__(self, name: str, status: TestStatus, time: str, message: str = None):
        self.name = name
        self.status = status
        if not time.isalpha():
            self.time = float(time)
        
        self.message = message


@dataclass
class TestSuite:
    """Test Suite information. Aggregates all TestCase(s) and their information"""
    name: str
    tests: List[TestCase]
    time: float
    passed: int = 0
    failed: int = 0
    errored:  int = 0
    skipped: int = 0

    def __post_init__(self):
        """Generate the TestStatus metrics"""
        self.passed = sum(1 for test in self.tests if test.status == TestStatus.PASSED)
        self.failed = sum(1 for test in self.tests if test.status == TestStatus.FAILED)
        self.errored = sum(1 for test in self.tests if test.status == TestStatus.ERROR)
        self.skipped = sum(
            1 for test in self.tests if test.status == TestStatus.SKIPPED
        )


@dataclass
class TestReport:
    """Test report on given test run with total test suites added."""
    suites: List[TestSuite]
    total_time: float = field(init=False)
    total_tests: int = field(init=False)
    total_passed: int = field(init=False)
    total_failed: int = field(init=False)
    total_error:    int = field(init=False)
    total_skipped: int = field(init=False)
    success_rate: float = field(init=False)
    failure_summary: Dict[str, List[str]] = field(default_factory=dict)

    def __post_init__(self):
        self.total_time = sum(suite.time for suite in self.suites)
        self.total_tests = sum(len(suite.tests) for suite in self.suites)
        self.total_passed = sum(suite.passed for suite in self.suites)
        self.total_failed = sum(suite.failed for suite in self.suites)
        self.total_error = sum(suite.errored for suite in self.suites)
        self.total_skipped = sum(suite.skipped for suite in self.suites)
        self.success_rate = (
            self.total_passed / self.total_tests if self.total_tests > 0 else 0
        )
        self.generate_failure_summary()

    def generate_failure_summary(self):
        """Generates the 'failure_summary' for all Failed testcases"""
        for suite in self.suites:
            failed_tests = [
                test for test in suite.tests if test.status == TestStatus.FAILED
            ]
            if failed_tests:
                self.failure_summary[suite.name] = [
                    f"{test.name}: {test.message}" for test in failed_tests
                ]

    def get_slowest_tests(self, n=5) -> List[TestCase]:
        """Returns slowest test cases."""
        all_tests = [test for suite in self.suites for test in suite.tests]
        return sorted(all_tests, key=lambda t: t.time, reverse=True)[:n]

    def get_summary(self):
        return {
            "total_tests": self.total_tests,
            "total_passed": self.total_passed,
            "total_failed": self.total_failed,
            "total_skipped": self.total_skipped,
            "success_rate": self.success_rate,
            "total_time": self.total_time,
            "slowest_tests": self.get_slowest_tests(),
            "failure_summary": self.failure_summary,
        }

    def __str__(self) -> str:
        """Basic string representation"""
        output = ''
        output = f"""Total Tests: {self.total_tests}
        ✅ Passed: {self.total_passed}
        ❌ Failed: {self.total_failed}
        ⚠️ Errors: {self.total_error}
        ⏭️ Skipped: {self.total_skipped}
        -------------------------
        Success Rate: {self.success_rate:.2f}%
        Total Time: {self.total_time:.2f}s"""
        return output