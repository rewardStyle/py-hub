import unittest
import os
import hub

class TestGitHub(unittest.TestCase):
    github_token = os.getenv('GITHUB_TOKEN')
    gh = hub.GitHub(github_token)

    def test_init(self):
        """Test that the GitHub object can be instantiated."""
        self.assertIsInstance(self.gh, hub.GitHub)
        self.assertTrue(self.gh.organization is not None)
    
    def test_get_all_repos(self):
        """Tests the functionality of using the GitHub
        object to return a list of all repos in the org."""
        repos = self.gh.get_all_repos()
        self.assertGreater(len(repos), 1, msg="The GitHub org should have more than 1 repo present")
    
    def test_get_all_repos_sorted(self):
        """Tests the functionality of using the GitHub
        object to return a list of all repos in the org,
        sorted by their last push datetime."""
        repos = self.gh.get_all_repos(sort_by_last_push=True)
        self.assertTrue(repos is not None)
        self.assertGreater(len(repos), 1, msg="The GitHub org should have more than 1 repo present")
    
    def test_get_repo(self):
        """Tests the functionality of getting a single repo."""
        name = 'py-hub'
        repo = self.gh.get_repo(name)
        self.assertIsInstance(repo, hub.Repository)
        self.assertEqual(repo.name, name)
        self.assertTrue(repo.repo_obj is not None)
    
    
if __name__ == '__main__':
    unittest.main()
