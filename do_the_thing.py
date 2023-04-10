import sys
import json
from loguru import logger

def prompt_from_issue(issue: dict):
    """
    Given a github issue object, returns a simplified prompt.
    """
    return f"issue title: {issue['title']}\nissue description: {issue['body']}"
    

if __name__ == '__main__':
    issue = json.loads(sys.argv[1])
    author_role = issue['author_association']
    if author_role != 'OWNER':
        exit()
    prompt = prompt_from_issue(issue)
    logger.info(f"<prompt>{prompt}</prompt>")
