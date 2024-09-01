"""All discord related view information"""

from datetime import datetime
import os
import textwrap
from typing import Dict, List
from discord import Any, Color, Embed, EmbedAuthor, EmbedField, EmbedFooter, EmbedMedia
from config import BOT_IMAGE
from src.models.data_reports import NormalisedCoverageData, CoverageMetricType
from src.models.test_suite import TestCase, TestIcons, TestReport, TestStatus


class DiscordFormatter:
    """Formats the Coverage & Tests reports into Discord Message format"""

    def __init__(
        self, coverage_report: NormalisedCoverageData, test_report: TestReport = None
    ):
        self.coverage_report = coverage_report
        self.test_report = test_report

    def generate_full_message(self) -> List[Embed]:
        """Creates Embeds for Coverage Report and Test Report"""
        coverage_embed = self._coverage_embed()
        test_report_embed = self._report_embed()
        embeds: List[Embed] = []

        if coverage_embed:
            embeds.append(coverage_embed)
        else:
            raise Exception("idk something happened bro")  # TODO: lets fix this later

        if test_report_embed:
            embeds.append(test_report_embed)
        else:
            print("No test report generated")  # TODO: make this logged warning

        return embeds

    def _coverage_embed(self) -> Embed:
        """Create coverage report as an Embed"""
        icon_url = BOT_IMAGE
        thumbnail = EmbedMedia(url=BOT_IMAGE)
        footer = EmbedFooter(text="Notified via Webhook Reporter", icon_url=icon_url)
        message = f"```{(self.test_report)} ```"
        return Embed(
            timestamp=datetime.now(),
            title="random title",  # LIMIT title Size
            url="https://example.com",
            description=message,
            color=self._threshold_color(),
            thumbnail=thumbnail,
            fields=self._fields(),
            author=EmbedAuthor(
                name="webhook-reporter",
                url="https://github.com/Moeh-Jama/webhook-reporter",
            ),
            footer=footer,
        )

    def _report_embed(self):
        """Create test report as an embed"""
        if not self.test_report:
            return None

        summary: Dict[str, Any] = self.test_report.get_summary()

        icon_url = BOT_IMAGE
        thumbnail = EmbedMedia(url=BOT_IMAGE)
        footer = EmbedFooter(text="Notified via Webhook Reporter", icon_url=icon_url)

        fields = self._test_fields(test_report_summary=summary)
        color_status = Color.brand_green()
        if self.test_report.success_rate < 1:
            color_status = Color.brand_red()
        return Embed(
            timestamp=datetime.now(),
            title="Test Report",
            url="",
            description=self._test_message(),
            color=color_status,
            thumbnail=thumbnail,
            fields=fields,
            author=EmbedAuthor(
                name="webhook-reporter",
                url="https://github.com/Moeh-Jama/webhook-reporter",
            ),
            footer=footer,
        )

    def _threshold_color(self) -> Color:
        """
        Returns color value based on threshold or default of 0.8

        if a current coverage is less than coverage by 20% it is highlighted red, else yellow
        """
        env_threshold = float(os.getenv("COVERAGE_THRESHOLD", "0")) / 100.0
        if not self.coverage_report.total_line_rate:
            return Color.brand_red()
        if env_threshold <= self.coverage_report.total_line_rate:
            return Color.dark_green()
        elif env_threshold * 0.8 > self.coverage_report.total_line_rate:
            return Color.brand_red()
        else:
            return Color.yellow()

    def _fields(self) -> List[EmbedField]:
        """Returns all Embed fields based on given coverage_report"""

        field_metrics: List[EmbedField] = []
        # Line Rate
        field_metrics.append(
            EmbedField(
                name=self._format_field_name(CoverageMetricType.LINE_COVERAGE),
                value=str(self.coverage_report.total_line_rate) + "%",
                inline=True,
            )
        )
        # Complexity
        field_metrics.append(
            EmbedField(
                name=self._format_field_name(CoverageMetricType.COMPLEXITY_AVG),
                value=str(self.coverage_report.complexity_avg),
                inline=True,
            )
        )
        # Total
        field_metrics.append(
            EmbedField(
                name=self._format_field_name(CoverageMetricType.TOTAL),
                value=str(self.coverage_report.total),
                inline=True,
            )
        )
        return field_metrics

    def _format_field_name(self, field: CoverageMetricType) -> str:
        """Gets prettified name"""
        return field.name.lower().replace("_", " ").capitalize()

    def _test_fields(self, test_report_summary: Dict[str, Any]) -> List[EmbedField]:
        """Fields using TestReport summary attributes"""
        embed_list: List[EmbedField] = []
        for name, value in test_report_summary.items():

            if name in ["failure_summary", "slowest_tests"]:
                continue

            embed_field = EmbedField(
                name=name.replace("_", " ").capitalize(), value=str(value), inline=True
            )
            embed_list.append(embed_field)

        return embed_list

    def _test_message(self) -> str:
        """Test Report metrics"""
        highlight = self._highlight_tests_message()
        if highlight:
            highlight = textwrap.dedent(highlight).strip()
        return highlight

    def _highlight_tests_message(self) -> str:
        """Creates list of message blocks based on TestStatus with formatted blocks"""
        output = ""

        skipped = self._format_lists(
            title="skipped",
            tests=self.test_report.get_tests_by_status(test_status=TestStatus.SKIPPED),
        )
        if skipped:
            output += TestIcons.SKIPPED.value + skipped

        failures = self._format_lists(
            title="failures",
            tests=self.test_report.get_tests_by_status(test_status=TestStatus.FAILED),
        )
        if failures:
            output += TestIcons.FAILED.value + failures

        errors = self._format_lists(
            title="errors",
            tests=self.test_report.get_tests_by_status(test_status=TestStatus.ERROR),
        )
        if errors:
            output += TestIcons.ERROR.value + errors

        return (output + "")[:4096] # Max discord embed description size

    def _format_lists(self, title: str, tests: List[TestCase]) -> str:
        """Returns formatted markdown sections with formatted title section"""
        if not tests:
            return ''
        title = f"__**{title.capitalize()}**__ ({len(tests)})"
        message = "```javascript"
        for test in tests[:4]:
            test_msg = test.message or ''
            test_case_message = ''
            if test_msg:
                test_case_message = f"{textwrap.dedent(test_msg).strip()[:250]}:\n"
                print('message type', type(test_case_message))
            message += f"\n{test.name.strip()}:\n{test_case_message}"
        message += "```"
        return title + "\n" + message

    def _test_report_contains_messages(self) -> bool:
        """checks if failure/error messages exist"""
        return self.test_report.total_failed > 0 or self.test_report.total_error > 0
