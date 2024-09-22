import os

def pytest_generate_tests(metafunc):
    """Set all environments for tests"""
    os.environ['ICON_URL'] = "https://icon_url.com/icon.png"
    os.environ['BOT_IMAGE'] = "https://icon_url.com/bot_icon.png"
    os.environ['GITHUB_REPOSITORY'] = 'random-repo'
    os.environ['GITHUB_SHA'] = 'RAN2223DOM'
    os.environ['GITHUB_RUN_ID'] = "555225525"
    os.environ['GITHUB_REF'] = 'refs/pull/38/merge'
    os.environ['GITHUB_ACTOR_ID'] = "10217249"