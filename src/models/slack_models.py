from slack_sdk.models.blocks.blocks import Block

class SlackMessage:
    """Slack message model"""
    
    def __init__(self, title: str, overview: str):
        self.title = title
        self.overview = overview
        self.block: Block = None
    
    def set_block(self, block: Block):
        """Sets the block"""
        self.block = block