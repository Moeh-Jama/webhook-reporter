from pathlib import Path
import pytest

from src.exceptions.configurations import UnsupportedCoverageType
from src.exceptions.file_errors import MalformedFile
from src.helpers.coverage_xml_identifier import CoverageXmlIdentifier
from src.models.file_types import CoverageFileType

xml_file_path = Path(__file__).parent.parent.parent / "data" / "xml" / "coverage"


def test_identify_clover_coverage_file():
    """Test to check if an Clover is validated correctly."""
    coverage_identifier = CoverageXmlIdentifier(
        xml_file=f"{xml_file_path}/sample_clover_coverage.xml"
    )
    result = coverage_identifier.identifiy_report()
    assert result == CoverageFileType.CLOVER


def test_identify_coberature_coverage_file():
    """Test to check if an Coberature is validated correctly."""
    coverage_identifier = CoverageXmlIdentifier(
        xml_file=f"{xml_file_path}/sample_coberature_coverage.xml"
    )
    result = coverage_identifier.identifiy_report()
    assert result == CoverageFileType.COBERATURE


def test_unsupported_coverage_type():
    """Test to check if an unsupported coverage type raises an exception."""
    coverage_identifier = CoverageXmlIdentifier(
        xml_file=f"{xml_file_path}/unsupported.xml"
    )
    with pytest.raises(UnsupportedCoverageType):
        coverage_identifier.identifiy_report()


def test_identify_malformed_xml():
    """Test to check if malformed XML raises an exception."""

    coverage_identifier = CoverageXmlIdentifier(
        xml_file=f"{xml_file_path}/malformed.xml"
    )
    with pytest.raises(MalformedFile):
        coverage_identifier.identifiy_report()


def test_identify_xml_with_missing_attributes():
    """Test XML missing expected attributes for coverage type detection."""
    coverage_identifier = CoverageXmlIdentifier(
        xml_file=f"{xml_file_path}/incomplete_coberature.xml"
    )
    with pytest.raises(UnsupportedCoverageType):
        coverage_identifier.identifiy_report()


def test_identify_unexpected_structure():
    """Test for XML with an unexpected structure."""
    coverage_identifier = CoverageXmlIdentifier(
        xml_file=f"{xml_file_path}/unexpected.xml"
    )
    with pytest.raises(UnsupportedCoverageType):
        coverage_identifier.identifiy_report()


def test_identify_empty_file():
    """Test for an empty file."""
    coverage_identifier = CoverageXmlIdentifier(xml_file=f"{xml_file_path}/empty.xml")
    with pytest.raises(MalformedFile):
        coverage_identifier.identifiy_report()


def test_identify_xml_with_multiple_root_elements():
    """Test XML with multiple root elements."""
    coverage_identifier = CoverageXmlIdentifier(
        xml_file=f"{xml_file_path}/multiple_root_elements.xml"
    )
    with pytest.raises(UnsupportedCoverageType):
        coverage_identifier.identifiy_report()
