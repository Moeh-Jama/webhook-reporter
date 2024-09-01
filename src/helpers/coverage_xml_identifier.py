from src.exceptions.configurations import UnsupportedCoverageType
from src.helpers.xml_identifier_base import XmlIdentifierBase
from src.models.file_types import CoverageFileType


class CoverageXmlIdentifier(XmlIdentifierBase):
    """Identifies the XML file type"""

    def identifiy_report(self) -> CoverageFileType:
        if self.root is None:
            self.load_xml()

        # Check for Clover
        if self.root.tag == "coverage" and "clover" in self.root.attrib:
            return CoverageFileType.CLOVER

        # Check for Cobertura
        elif self.root.tag == "coverage" and all(
            attr in self.root.attrib for attr in ["line-rate", "branch-rate"]
        ):
            return CoverageFileType.COBERATURE

        # Check for JaCoCo
        elif self.root.tag == "report" and "name" in self.root.attrib:
            return CoverageFileType.JACOCO

        raise UnsupportedCoverageType()
