"""Returns reader based on given framework"""

from src.test_readers.jest_reader import JestJSONReader
from src.test_readers.junit_reader import JUnitReader


class ReaderFactory:
    """Return Reader type based on framework given"""
    @staticmethod
    def get_reader(framework):
        if framework == 'junit':
            return JUnitReader()
        elif framework == 'pytest':
            return JUnitReader()
        elif framework == 'jest':
            return JestJSONReader()
        else:
            raise ValueError(f"Unsupported framework: {framework}")