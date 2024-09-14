import textwrap
from typing import Any, Dict, List

from src.formatters.base_formatter import BaseFormatter
from src.models.test_suite import TestCase, TestIcons, TestResult

IGNORED_FIELDS = ["failure_summary", "slowest_tests"]


class SlackFormatter(BaseFormatter):
    """Formats the Coverage & Tests reports into Slack Message format"""

    def generate_full_message(self) -> List[Dict[str, Any]]:
        """Creates Block for Coverage Report and Test Report"""
        coverage_section = self.format_coverage()
        test_report_section = self.format_test_report()

        blocks = [
            self._header_block(text=':rocket: Test and Coverage Report'),
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f"<{self.github_action.reference_link}|{self.github_action.event_name}>"
                }
            }
        ]


        if coverage_section:
            blocks.extend(coverage_section)
        else:
            raise ValueError(
                "Coverage Section failed to generate. Check the coverage report data."
            )

        blocks.append({"type": "divider"})

        if self.test_report:
            blocks.extend(test_report_section)

        blocks.append(self.format_footer())

        return blocks

    def _header_block(self, text: str) -> Dict[str, Any]:
        return {
            "type": "header",
            "text": {"type": "plain_text", "text": text, "emoji": True},
        }

    def format_coverage(self) -> List[Dict[str, Any]]:
        """Generate the Coverage Section"""
        section = []
        coverage_color = self._get_coverage_color()
        fields = [
            {
                "type": "mrkdwn",
                "text": f"*Line Coverage:*\n{self.coverage_report.total_line_rate}%",
            },
            {
                "type": "mrkdwn",
                "text": f"*Complexity Average:*\n{self.coverage_report.complexity_avg}",
            },
            {
                "type": "mrkdwn",
                "text": f"*Total:*\n{self.coverage_report.total}",
            },
        ]

        if self.test_report:
            fields += self._test_fields(
                test_report_summary=self.test_report.get_summary()
            )

        section.append(
            {"type": "section", "fields": fields, "accessory": self._action_image()}
        )

        coverage_status = (
            {
                "type": "context",
                "elements": [
                    {"type": "mrkdwn", "text": f"Coverage Status: {coverage_color}"}
                ],
            },
        )

        section.extend(coverage_status)

        return section

    def _action_image(self) -> Dict[str, str | Dict[str, str]]:
        """Returns the associated image of the given triggered action"""
        return {
            "type": "image",
            "image_url": self.github_action.actor_profile_img,
            "alt_text": "alt git_action_image for image",
        }

    def _coverage_fields(self) -> List[Dict[str, str]]:
        """The coverage summary fields like Passed, Failed, etc..."""
        pass

    def format_test_report(self) -> List[Dict[str, Any]]:
        sections = []
        if not self.test_report:
            return sections

        highlight = self._highlight_tests_message()
        if highlight:
            sections.extend(
                [
                    self._header_block(":clipboard: Test Details"),
                    {"type": "section", "text": {"type": "mrkdwn", "text": highlight}},
                ]
            )

        return sections

    def _highlight_tests_message2(self) -> str:
        output = ""

        for status, icon in [
            (TestResult.SKIPPED, ":fast_forward:"),
            (TestResult.FAILED, ":x:"),
            (TestResult.ERROR, ":warning:"),
        ]:
            tests = self.test_report.get_tests_by_status(test_status=status)
            if tests:
                title = f"{icon} *{status.name.capitalize()}* ({len(tests)})"
                output += f"{title}\n"
                for test in tests[: self.MAX_TEST_SHOWN]:
                    test_msg = test.message or ""
                    test_case_message = (
                        f"{textwrap.dedent(test_msg).strip()[:250]}" if test_msg else ""
                    )
                    output += f"• `{test.name.strip()}`: {test_case_message}\n"
                output += "\n"

        return output.strip()

    def _highlight_tests_message(self) -> str:
        """Creates list of message blocks based on TestResult with formatted blocks"""
        output = ""

        skipped = self._format_lists(
            title="skipped",
            tests=self.test_report.get_tests_by_status(test_status=TestResult.SKIPPED),
        )
        if skipped:
            output += TestIcons.SKIPPED.value + skipped

        failures = self._format_lists(
            title="failures",
            tests=self.test_report.get_tests_by_status(test_status=TestResult.FAILED),
        )
        if failures:
            output += TestIcons.FAILED.value + failures

        errors = self._format_lists(
            title="errors",
            tests=self.test_report.get_tests_by_status(test_status=TestResult.ERROR),
        )
        if errors:
            output += TestIcons.ERROR.value + errors

        return output + ""

    def _format_lists(self, title: str, tests: List[TestCase]) -> str:
        """Returns formatted markdown sections with formatted title section"""
        if not tests:
            return ""
        title = f"__**{title.capitalize()}**__ ({len(tests)})"
        message = "```"
        for test in tests[:4]:
            test_msg = test.message or ""
            test_case_message = ""
            if test_msg:
                test_case_message = f"{textwrap.dedent(test_msg)[:250]}:\n"
            message += f"\n{test.name}:\n{test_case_message}"
        message += "```"
        return title + "\n" + message

    def _get_coverage_color(self) -> str:
        """returns the coverage status"""
        status = self.calculate_coverage_status()
        icon_map = {
            "good": ":large_green_circle:",
            "needs_improvement": ":large_yellow_circle:",
            "critical": ":red_circle:",
        }
        return f"{icon_map[status]} {status.capitalize()}"

    def format_footer(self) -> Dict[str, Any]:
        footer_info = self._get_footer()
        return {
            "type": "context",
            "elements": [
                {
                    "type": "image",
                    "image_url": footer_info["icon_url"],
                    "alt_text": "webhook-reporter image",
                },
                {
                    "type": "mrkdwn",
                    "text": f"{footer_info['message']}",
                },
            ],
        }

    def _test_fields(self, test_report_summary: Dict[str, Any]) -> List[Dict[str, str]]:
        """Fields using TestReport summary attributes"""
        embed_list: List[Dict[str, str]] = []
        for name, value in test_report_summary.items():
            if name in IGNORED_FIELDS:
                continue
            formatted_name = name.replace("_", " ").capitalize()

            field = {
                "type": "mrkdwn",
                "text": f"*{formatted_name}*\n{value}",
            }
            embed_list.append(field)

        return embed_list
