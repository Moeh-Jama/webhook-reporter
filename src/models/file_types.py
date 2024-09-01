


from enum import Enum, auto


class CoverageFileType(Enum):
    CLOVER = auto()
    COBERATURE = auto()
    JACOCO = auto()

class TestSuiteFileType(Enum):
    JUNIT = 'JUnit'
    TESTNG = 'TestNG'
    NUNIT = 'NUnit'
