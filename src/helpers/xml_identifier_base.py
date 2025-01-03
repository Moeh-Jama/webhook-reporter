import logging
import xml.etree.ElementTree as ET


from src.exceptions.file_errors import MalformedFile
class XmlIdentifierBase:
    def __init__(self, xml_file: str):
        self.xml_file = xml_file
        self.root = None
        self.logger = logging.getLogger("webhook-reporter-logger")
    
    def load_xml(self):
        """Loads and sets self.root to xml root"""
        try:
            tree = ET.parse(self.xml_file)
            self.root = tree.getroot()
        except ET.ParseError:
            raise MalformedFile(file=self.xml_file)
        except Exception as e:
            self.logger.error(f"[{e}] occurred trying to load and parse the XML file '{self.xml_file}'")