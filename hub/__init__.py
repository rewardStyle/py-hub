from time import sleep
from datetime import datetime
from git import Repo
from github import Github


# Prevent getting API rate limited by GitHub
API_RATE_LIMIT_PAUSE_SECONDS = 0.2


class Repository:
    """Simple class representing a data structure responsible for
    holding key pieces of info about a repo, used throughout the library."""
    def __init__(self, repo_obj):
        # The instance of the repo via PyGitHub's authenticated git client
        self.repo_obj = repo_obj
        self.name = self.repo_obj.name
        self.created_at = self.repo_obj.created_at
        self.pushed_at = self.repo_obj.pushed_at
        self.archived = self.repo_obj.archived
        self.org = 'rewardStyle'
        self.deployments_api = f"https://api.github.com/repos/{self.org}/{self.name}/deployments"

    def get_file_contents(self, filename):
        """Tries to get the decoded file contents of the specified file from this repository,
        else returns None if the file cannot be decoded or does not exist."""
        sleep(API_RATE_LIMIT_PAUSE_SECONDS)
        try:
            return self.repo_obj.get_file_contents(filename).decoded_content
        except:
            return None
    
    def get_days_since_last_push(self):
        """Returns the amount of time, in days, since the last time there was
        a push to the repo."""
        return (datetime.date.today() - self.pushed_at).days
        

class GitHub:
    """The GitHub class represents an object capable of performing
    all the necessary git / GitHub actions with an authenticated client."""
    def __init__(self, github_token=None, organization='rewardStyle'):
        sleep(API_RATE_LIMIT_PAUSE_SECONDS)
        if not github_token:
            raise Exception('no github token supplied')
        self._client = Github(github_token)
        self.organization = self._client.get_organization(organization)

    def get_all_repos(self, ignore_archived=True, sort_by_last_push=False):
        """Returns a list of proprietary Repository instances, optionally sorted by date of last push"""
        sleep(API_RATE_LIMIT_PAUSE_SECONDS)
        repos = [Repository(r) for r in self.organization.get_repos() if not (ignore_archived and r.archived)]
        return repos.sort(key=lambda r: r.pushed_at, reverse=True) if sort_by_last_push else repos
    
    def get_repo(self, name):
        """Returns a single proprietary instance of a Repository"""
        sleep(API_RATE_LIMIT_PAUSE_SECONDS)
        return Repository(self.organization.get_repo(name))
