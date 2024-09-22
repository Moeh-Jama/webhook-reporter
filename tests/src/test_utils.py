"""Test utils"""

import pytest
from src.models.test_suite import TestResult
from src.providers.discord_provider import DiscordProvider
from src.utils import closest_approx_name, get_test_case_status, process_text_input, set_provider


def test_process_text_input():
    assert process_text_input(" PyTest ") == "pytest"
    assert process_text_input("DISCORD") == "discord"
    assert process_text_input(" Some Random Text ") == "some random text"


def test_set_provider_discord():
    provider = set_provider("discord")
    assert isinstance(provider, DiscordProvider)


def test_set_provider_unsupported():
    with pytest.raises(Exception):
        set_provider("unsupported_provider")


def test_test_case_status():
    status = "SkIpPeD"
    test_status = get_test_case_status(status=status)

    assert TestResult.SKIPPED, test_status


@pytest.mark.parametrize(
    "status_str, test_status",
    [
        ("", TestResult.UNKNOWN),
        ("error", TestResult.ERROR),
        (" FAIL ", TestResult.FAILED),
        ("failed", TestResult.FAILED),
        (" skip", TestResult.SKIPPED),
        ("pass ", TestResult.PASSED),
    ],
)
def test_statuses_edge_cases(status_str, test_status):
    resulting_status = get_test_case_status(status=status_str)

    assert resulting_status == test_status

@pytest.mark.parametrize(
    "given_name, expected_message",
    [
        ('discord', "Did you mean 'discord'?"),
        ('cord', "Did you mean 'discord'?"),
        ('team', "Did you mean 'teams'?"),
        ('ack', "Did you mean 'slack'?"),
        ('shack', "Did you mean 'slack'?"),
        ('homer simpson', ""),
        ('bread', ""),
    ],
)
def test_closest_approx_name(given_name, expected_message):
    names = ['discord', 'slack', 'teams']
    message = closest_approx_name(allowed_names=names, given_name=given_name)
    
    assert message == expected_message