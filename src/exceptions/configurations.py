"""Configuration related errors"""
import urllib

class ConfigurationValuesNotFoundError(Exception):
    """Required fields exceotion"""

    pass

class InvalidProviderError(Exception):
    """Custom exception for invalid provider errors."""
    pass


class UnsupportedCoverageType(Exception):
    """The given coverage is not supported"""
    def __init__(self):
        self.issue_url = self.generate_issue_url()

        # Custom exception message
        message = (
            f"Coverage format not supported! Raise a Ticket here: {self.issue_url}"
        )
        super().__init__(message)

    def generate_issue_url(self) -> str:
        """Generates the Issue with already configured Ticket data."""
        issue_title = "Unsupported Coverage Format"
        issue_body = (
            "### Framework: '<ENTER TEST FRAMEWORK>' is not supported\n"
            "Please check the configuration or extend the support for this framework.\n\n"
            "<Please any format and configurations for the test-framework here>\n"
            "##### Error Details:\n"
            "- Coverage Format: not supported\n"
            "- Triggered by: Parser creation\n"
            "Please look into this at the earliest."
        )
        # Encoding the issue body for url transmission.
        issue_body = urllib.parse.quote(issue_body)
        # Construct the URL to create an issue with pre-filled details
        issue_url = (
            f"https://github.com/Moeh-Jama/webhook-reporter/issues/new?"
            f"title={issue_title.replace(' ', '+')}&"
            f"body={issue_body}&"
            "labels=new_coverage_support&"
            "assignee=Moeh-Jama"
        )

        return issue_url

class UnsupportedTestReportType(Exception):
    """Unsupprted framework file type i.e. pytest with test_file='file.txt'"""
    def __init__(self):
        self.issue_url = self.generate_issue_url()

        # Custom exception message
        message = (
            f"Test Suite format not supported! Raise a Ticket here: {self.issue_url}"
        )
        super().__init__(message)
    
    def generate_issue_url(self) -> str:
        """Generates the Issue with already configured Ticket data."""
        issue_title = "Unsupported Coverage Format"
        issue_body = (
            "### Test File Type '<ADD FILENAME.EXTENSION>' for Framework '<YOUR TESTING FRAMEWORK>' is not supported\n"
            "Please check the configuration or extend the support for this framework.\n\n"
            "<Please any format and configurations for the test-framework here>\n"
            "##### Error Details:\n"
            "- Test Suite Format: not supported\n"
            "- Triggered by: Reader creation\n"
            "Please look into this at the earliest."
        )
        # Encoding the issue body for url transmission.
        issue_body = urllib.parse.quote(issue_body)
        # Construct the URL to create an issue with pre-filled details
        issue_url = (
            f"https://github.com/Moeh-Jama/webhook-reporter/issues/new?"
            f"title={issue_title.replace(' ', '+')}&"
            f"body={issue_body}&"
            "labels=new_test_file_supprot&"
            "assignee=Moeh-Jama"
        )

        return issue_url


class UnknownCoverageSchema(Exception):
    """The given coverage_tool does not have associated known coverage schema"""
    pass