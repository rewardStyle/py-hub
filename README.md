# py-hub
Python3 library which wraps common GitHub API operations used across a lot of tooling

## Installation

```bash
pipenv install git+git://github.com/rewardStyle/py-hub.git#egg=hub
# To install and lock all dependencies properly, install a specific sha:
pipenv install -e git+git://github.com/rewardStyle/py-hub.git@<GIT_SHA>#egg=hub
```

## Use Cases

Use when creating a Python3 tool which requires sensitive information ( such as API tokens )
to be supplied to the application at runtime.
This information can be supplied as an environment variable, in an `.env` file,
or with flags as direct arguments to the application on the command line.

```python
import hub

# Normally this would be supplied via command line, .env file, or env var
github_token='a valid github auth token'

def main():
    # Instantiate an object capable of performing the necessary operations
    # NOTE - To avoid hitting API rate limits, each API operation has a delay,
    #        as defined by API_RATE_LIMIT_PAUSE_SECONDS in github/main.py
    gh = hub.GitHub(github_token)

    active_repos = gh.get_all_repos()

    all_repos = gh.get_all_repos(ignore_archived=False)

    active_repos_sorted = gh.get_all_repos(sort_by_last_push=True)

    repo = gh.get_repo('ltk-web')
    print( f"{repo.name} was created at {repo.created_at}" )
    dir(repo)

    cf_template = repo.get_file_contents('cloudformation/template.yml')

    print( f"It has been {repo.get_days_since_last_push()} days since anyone's pushed to the repo" )


if __name__ == '__main__':
    main()
```

### Testing
```bash
pipenv run python test.py
```

## The WHYs

### Why was this module developed ?

DevOps tooling, particularly in the context of metrics and reporting,
often requires up-to-date information on the state of the Engineering
organization's repos.

In fact, a common pattern is to dynamically generate a list of 
active ( non-archived ) repos, either to perform operations on,
or to test against.

This pattern relies on pygithub and gitpython,
and pops up in a number of devops-tools. By developing this library,
the functionality can be added to whichever tools need it,
while ensuring a consistent experience. This also ensures that
maintenance is simplified, as this library becomes the one
source of truth for this functionality.

