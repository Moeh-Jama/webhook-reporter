"""Test that parser is returning parser"""

from pathlib import Path

import pytest

from src.exceptions.configurations import UnsupportedTestReportType
from src.exceptions.file_errors import MalformedFile

from src.test_readers.jest_reader import JestJSONReader
from src.test_readers.junit_reader import JUnitReader
from src.test_readers.reader_factory import ReaderFactory


xml_file_path = Path(__file__).parent.parent.parent / "data" / "xml" / "tests"

json_file_path = Path(__file__).parent.parent.parent / "data" / "json" / "tests"


def test_get_reader_junit_parser():
    """get_reader identifies test file for JUnitReader"""
    parser_factory = ReaderFactory()
    file = "single_suite.xml"
    parser = parser_factory.get_reader(test_file=f"{xml_file_path}/{file}")

    assert isinstance(parser, JUnitReader)


def test_get_reader_jest_json_parser():
    """get_reader identifies test file for Jest JSON Reader"""
    parser_factory = ReaderFactory()
    file = "test_jest.json"
    parser = parser_factory.get_reader(test_file=f"{json_file_path}/{file}")

    assert isinstance(parser, JestJSONReader)


def test_get_reader_raises_unsupported():
    """get parser raises for unknown test file"""
    parser_factory = ReaderFactory()
    file = "unsupported.xml"

    with pytest.raises(UnsupportedTestReportType):
        parser_factory.get_reader(test_file=f"{xml_file_path}/{file}")


def test_raises_malformed_coberature():
    """For incomplete junit test file raises"""
    parser_factory = ReaderFactory()
    file = "malformed.xml"

    with pytest.raises(MalformedFile):
        parser_factory.get_reader(test_file=f"{xml_file_path}/{file}")
