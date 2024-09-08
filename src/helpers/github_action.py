"""Github Action environment data getter"""
import os


class GitHubActionInfo:
    """Get the action environment details and return full urls."""
    def __init__(self):
        self.repo = os.getenv('GITHUB_REPOSITORY')
        self.sha = os.getenv('GITHUB_SHA')
        self.ref = os.getenv('GITHUB_REF')
        self.actor = os.getenv('GITHUB_ACTOR')
        self.actor_id = os.getenv('GITHUB_ACTOR_ID')
        self.run_id = os.getenv('GITHUB_RUN_ID')
        self.action = os.getenv('GITHUB_ACTION')
        self.event_name = os.getenv('GITHUB_EVENT_NAME')

    @property
    def commit_url(self):
        return f"https://github.com/{self.repo}/commit/{self.sha}"
    
    @property
    def run_url(self):
        return f"https://github.com/{self.repo}/actions/runs/{self.run_id}"
    
    @property
    def reference_link(self):
        """The link associated with this action run"""
        ref = self.ref.split('refs/')[-1]
        return f"https://github.com/{self.repo}/{ref}"
    
    @property
    def actor_profile_img(self):
        return f"https://avatars.githubusercontent.com/u/{self.actor_id}"
