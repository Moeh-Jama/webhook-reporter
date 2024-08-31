
from src.parsers.jest_schema_parser import JestCloveredSchemaParser

parser = JestCloveredSchemaParser()

data = parser.parse_and_normalise(coverage_file='./data/jest_clover_longer_coverage.xml')
print(data)