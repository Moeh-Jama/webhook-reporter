import textwrap
from typing import Any, Dict, List
from src.formatters.base_formatter import BaseFormatter
from src.models.teams_model import Column, ColumnSet, Container, Image, Item, TextBlock
from src.models.test_suite import TestCase, TestIcons, TestResult

IGNORED_FIELDS = ["failure_summary", "slowest_tests"]


class TeamsFormatter(BaseFormatter):
    """Formats the Coverage & Tests reports into Slack Message format"""

    def generate_full_message(self) -> List[Item]:
        """Creates Body Items for Coverage Report and Test Report"""
        body_section: List[Item] = []
        coverage_section = self.format_coverage()

        if not coverage_section:
            raise ValueError(
                "Coverage Section failed to generate. Check the coverage report data."
            )

        test_report_section = self.format_test_report()

        # Add header to body
        body_section.append(self.format_header().to_dict())
        # Add Coverage Section
        body_section.extend([col_set.to_dict() for col_set in coverage_section])

        if test_report_section:
            body_section.extend([item.to_dict() for item in test_report_section])

        # Add footer
        body_section.append(self.format_footer().to_dict())

        return self.formatted_teams_message(body=body_section)

    def formatted_teams_message(self, body: List[Dict[str, Any]]):
        return {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "contentUrl": None,
                    "content": {
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "type": "AdaptiveCard",
                        "version": "1.2",
                        "body": body,
                    },
                }
            ],
        }

    def format_coverage(self) -> List[ColumnSet]:
        """Return the Coverage Column Section"""
        overview_set: List[ColumnSet] = []
        overview_set.append(ColumnSet(columns=self.get_base_coverage_fields()))

        other_fields = self._test_report_fields()
        size = len(other_fields)

        if size == 0:
            return overview_set

        num_columns_per_set = max(2, size // 2)

        for i in range(0, size, num_columns_per_set):
            cols = other_fields[i : i + num_columns_per_set]
            overview_set.append(ColumnSet(columns=cols))

        return overview_set

    def get_base_coverage_fields(self) -> List[Column]:
        """Base Column Fields"""
        line_rate = self._name_value_column(
            key="**Line Coverage**", value=self.coverage_report.total_line_rate
        )
        complexity = self._name_value_column(
            key="**Complexity Avg**", value=self.coverage_report.complexity_avg
        )
        total = self._name_value_column(
            key="**Tests Run**", value=self.coverage_report.total
        )

        return [line_rate, complexity, total]

    def _test_report_fields(self) -> List[Column]:
        """Test Report fields"""
        columns: List[Column] = []
        for name, value in self.test_report.get_summary().items():
            if name in IGNORED_FIELDS:
                continue
            formatted_name = name.replace("_", " ").capitalize()
            columns.append(self._name_value_column(key=formatted_name, value=value))
        return columns

    def _name_value_column(self, key: str, value: str) -> Column:
        """Creates a Column with TextBlocks for key and value fields"""

        key_block = TextBlock(text=key, weight="Bolder", wrap=True)
        value_block = TextBlock(text=str(value), wrap=True)

        return Column(width="stretch", items=[key_block, value_block])

    def format_test_report(self) -> List[TextBlock]:
        """Returns all if any TextBlock messages for non-passing test-cases"""
        section: List[TextBlock] = []
        if not self.test_report.failure_summary:
            return section
        header = TextBlock(
            text="\ud83d\udccb **Test Details**",
            weight="Bolder",
            size="Medium",
            spacing="Medium",
            wrap=True,
        )

        section.append(header)

        test_results = self._highlight_messages()
        section += test_results

        return section
    
    def _highlight_messages(self) -> List[Container]:
        output: List[Container] = []
        for status, icon in [
            (TestResult.SKIPPED, TestIcons.SKIPPED.value),
            (TestResult.FAILED, TestIcons.FAILED.value),
            (TestResult.ERROR, TestIcons.ERROR.value),
        ]:
            tests = self.test_report.get_tests_by_status(test_status=status)
            if tests:
                title = f"{icon} *{status.name.capitalize()}* ({len(tests)})"
                container = self.test_message_summary(title=title, tests=tests)
                if container:
                    output.append(container)

        return output
    
    def test_message_summary(self, title: str, tests: List[TestCase]) -> Container:

        header = TextBlock(text=title, wrap=True)

        message = "```javascript"
        for test in tests[:self.MAX_TEST_SHOWN]:
            test_msg = test.message or ""
            test_case_message = f"{textwrap.dedent(test_msg).strip()[:250]}\n" if test_msg else ""
            message += f"\n{test.name}:\n{test_case_message}"
        message += "```"

        messages = TextBlock(text=message, wrap=True)
        return Container(items=[header, messages])

    def format_header(self) -> ColumnSet:
        """Creates header as a ColumnSet"""
        columns: List[Column] = []
        image = Image(
            url=self.github_action.actor_profile_img,
            altText="Github Actor pfp",
            size="Small",
        )
        columns.append(Column(width='auto', items=[image]))


        event_name = TextBlock(
            text=f"\ud83d\ude80 **[{self.github_action.event_name}]({self.github_action.reference_link})**",
            wrap=True,
            size="Large",
            weight="Bolder",
        )
        columns.append(Column(width='stretech', items=[event_name]))

        return ColumnSet(columns=columns)

    def format_footer(self) -> ColumnSet:
        """The footer with application name and image as a Column"""
        footer_info = self._get_footer()

        image = Image(url=footer_info["url"], size="Small", altText="Footer Icon")
        image_column = Column(width="auto", items=[image])

        footer_msg = TextBlock(
            text=footer_info["message"],
            size="Small",
            weight="Lighter",
            horizontalAlignment="Left",
            wrap=True,
        )
        msg_column = Column(width="stretch", items=[footer_msg])

        return ColumnSet(columns=[image_column, msg_column])
