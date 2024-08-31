"""All discord related view information"""

from datetime import datetime
import os
import textwrap
from typing import Dict, List
from discord import Any, Color, Embed, EmbedAuthor, EmbedField, EmbedFooter, EmbedMedia
from src.models.data_reports import NormalisedCoverageData, CoverageMetricType
from src.models.test_suite import TestReport


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
        icon_url = os.getenv("ICON_URL")
        thumbnail = EmbedMedia(url=os.getenv("BOT_IMAGE", ""))
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
        if not self.test_report or self._test_report_contains_messages():
            return None

        summary: Dict[str, Any] = self.test_report.get_summary()

        icon_url = os.getenv("ICON_URL")
        thumbnail = EmbedMedia(url=os.getenv("BOT_IMAGE", ""))
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
                value=str(self.coverage_report.total_line_rate),
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
        test_messages = self.test_report.failure_summary
        formatted_messages = self._format_test_messages(test_messages)
        return self._format_embed_description(formatted_messages)

    def _format_test_messages(self, messages: Dict[str, List[str]]) -> str:
        formatted_messages = []
        for test_suite, test_results in messages.items():
            formatted_messages.append(f"__**{test_suite}**__")
            for idx, result in enumerate(test_results, 1):
                formatted_result = textwrap.dedent(result).strip()
                formatted_messages.append(
                    f"Test {idx}:\n```py\n{formatted_result}\n```"
                )
        return "\n".join(formatted_messages)

    def _format_embed_description(self, message: str) -> str:
        truncated_message = message[:1997] + "..." if len(message) > 2000 else message
        return f"🧪 Test Results Summary:\n\n{truncated_message}"

    def _test_report_contains_messages(self) -> bool:
        """checks if failure/error messages exist"""
        return self.test_report.total_failed > 0 or self.test_report.total_error > 0