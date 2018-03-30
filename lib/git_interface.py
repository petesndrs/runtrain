'''Module git_interface
'''
import git


def git_sha():
    '''Function git_sha
    '''
    repo = git.Repo()
    sha = repo.head.object.hexsha
    short_sha = repo.git.rev_parse(sha, short=7)
    return short_sha


def git_branch():
    '''Function git_sha
    '''
    repo = git.Repo()
    return repo.active_branch.name
