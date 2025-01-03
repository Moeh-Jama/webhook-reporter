"""All discord related view information"""

from datetime import datetime
import textwrap
from typing import Dict, List
from discord import Any, Color, Embed, EmbedAuthor, EmbedField, EmbedFooter, EmbedMedia
from src.formatters.base_formatter import BaseFormatter
from src.formatters.utils.format_markdown import (
    generate_test_summary_by_status,
)
from src.models.data_reports import CoverageMetricType

MAX_DISCORD_EMBED_SIZE = 4096
IGNORED_FIELDS = ["failure_summary", "slowest_tests"]


class DiscordFormatter(BaseFormatter):
    """Formats the Coverage & Tests reports into Discord Message format"""

    def generate_full_message(self) -> Embed:
        """Creates Embeds for Coverage Report and Test Report"""
        coverage_embed = self.format_coverage()
        embed: Embed = None

        if coverage_embed:
            embed = self.format_coverage()
        else:
            raise ValueError(
                "Coverage embed failed to generate. Check the coverage report data."
            )

        # if test_report_embed:
        #     embeds.append(test_report_embed)

        return embed

    def format_coverage(self) -> Embed:
        """Create coverage report as an Embed"""
        thumbnail = EmbedMedia(url=self.github_action.actor_profile_img)
        message = self.get_test_summary_message() if self.test_report else ''
        return Embed(
            timestamp=datetime.now(),
            title=self.github_action.event_name,  # LIMIT title Size
            url=self.github_action.reference_link,
            description=message,
            color=self._threshold_color(),
            thumbnail=thumbnail,
            fields=self._fields(),
            author=EmbedAuthor(
                name="webhook-reporter",
                url="https://github.com/Moeh-Jama/webhook-reporter",
            ),
            footer=self.format_footer(),
        )

    def format_test_report(self):
        """Create test report as an embed"""
        pass

    def format_footer(self) -> EmbedFooter:
        """Returns the discord footer"""
        footer_info = self._get_footer()
        return EmbedFooter(
            text=footer_info["message"], icon_url=footer_info["icon_url"]
        )

    def _threshold_color(self) -> Color:
        """Gets the Color based on coverage status."""
        status = self.calculate_coverage_status()

        if status == "good":
            return Color.dark_green()
        elif status == "needs_improvement":
            return Color.yellow()
        return Color.brand_red()

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

        if self.test_report:
            test_fields = self._test_fields(self.test_report.get_summary())
            field_metrics.extend(test_fields)

        return field_metrics

    def _format_field_name(self, field: CoverageMetricType) -> str:
        """Gets prettified name"""
        return field.name.lower().replace("_", " ").capitalize()

    def _test_fields(self, test_report_summary: Dict[str, Any]) -> List[EmbedField]:
        """Fields using TestReport summary attributes"""
        embed_list: List[EmbedField] = []
        for name, value in test_report_summary.items():
            if name in IGNORED_FIELDS:
                continue

            embed_field = EmbedField(
                name=name.replace("_", " ").capitalize(), value=str(value), inline=True
            )
            embed_list.append(embed_field)

        return embed_list

    def get_test_summary_message(self) -> str:
        """Generates a summary message for test report metrics.

        Uses the `generate_test_summary_by_status` utility function to create a markdown-formatted
        summary of the test report's statuses (skipped, failed, errors). Cleans up any indentation
        from the resulting markdown string.

        Returns:
            str: The cleaned markdown-formatted test summary message.
        """
        # Generate the test summary highlight
        highlight = generate_test_summary_by_status(
            test_report=self.test_report, markdown_style="javascript"
        )

        # Remove unnecessary indentation
        if highlight:
            highlight = textwrap.dedent(highlight)

        return highlight
