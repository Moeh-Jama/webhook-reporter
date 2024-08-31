"""Test utils"""

import pytest
from src.models.test_suite import TestStatus
from src.providers.discord_provider import DiscordProvider
from src.utils import get_test_case_status, process_text_input, set_provider


def test_process_text_input():
    assert process_text_input(' PyTest ') == 'pytest'
    assert process_text_input('DISCORD') == 'discord'
    assert process_text_input(' Some Random Text ') == 'some random text'


def test_set_provider_discord():
    provider = set_provider('discord')
    assert isinstance(provider, DiscordProvider)

def test_set_provider_unsupported():
    with pytest.raises(Exception) as exc_info:
        set_provider('unsupported_provider')
    assert 'Provider unsupported_provider is not supported' in str(exc_info.value)


def test_test_case_status():
    status = 'SkIpPeD'
    test_status = get_test_case_status(status=status)

    assert TestStatus.SKIPPED, test_status


@pytest.mark.parametrize(
        'status_str, test_status',
        [
            ('', TestStatus.UNKNOWN),
            ('error', TestStatus.ERROR),
            (' FAIL ', TestStatus.FAILED),
            ('failed', TestStatus.FAILED),
            (' skip', TestStatus.SKIPPED),
            ('pass ', TestStatus.PASSED)
        ]
)
def test_statuses_edge_cases(status_str, test_status):
    resulting_status = get_test_case_status(status=status_str)

    assert resulting_status == test_status