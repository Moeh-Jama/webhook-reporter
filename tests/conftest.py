import os

def pytest_generate_tests(metafunc):
    """Set all environments for tests"""
    os.environ['ICON_URL'] = "https://icon_url.com/icon.png"
    os.environ['BOT_IMAGE'] = "https://icon_url.com/bot_icon.png"
    # os.environ['COVERAGE_THRESHOLD'] = "50"