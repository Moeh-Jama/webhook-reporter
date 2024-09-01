"""Test that parser is returning parser"""


from pathlib import Path

import pytest

from src.exceptions.configurations import UnsupportedCoverageType
from src.exceptions.file_errors import MalformedFile
from src.parsers.clover_schema_parser import CloverSchemaParser
from src.parsers.coberature_schema_parser import CoberatureSchemaParser
from src.parsers.parser_factory import ParserFactory


xml_file_path = Path(__file__).parent.parent.parent / "data" / "xml" / "coverage"

def test_get_parser_coberature_parser():
    """get_parser identifies clover file as CoberatureSchemaParser"""
    parser_factory = ParserFactory()
    file = 'sample_coberature_coverage.xml'
    parser = parser_factory.get_parser(file_name=f"{xml_file_path}/{file}")

    assert isinstance(parser, CoberatureSchemaParser)

def test_get_parser_clover_parser():
    """get_parser identifies clover file as CloverSchemaParser"""
    parser_factory = ParserFactory()
    file = 'sample_clover_coverage.xml'
    parser = parser_factory.get_parser(file_name=f"{xml_file_path}/{file}")

    assert isinstance(parser, CloverSchemaParser)

def test_get_parser_raises_unsupported():
    """get parser raises for unknown coverage file"""
    parser_factory = ParserFactory()
    file = 'unsupported.xml'

    with pytest.raises(UnsupportedCoverageType):
        parser_factory.get_parser(file_name=f"{xml_file_path}/{file}")

def test_raises_malformed_coberature():
    """For incomplete coberature coverage file raises"""
    parser_factory = ParserFactory()
    file = 'malformed.xml'

    with pytest.raises(MalformedFile):
        parser_factory.get_parser(file_name=f"{xml_file_path}/{file}")