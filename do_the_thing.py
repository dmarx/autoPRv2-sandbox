"""
Uses an AI agent simulating an SDE to respond to a github issue and generate a PR.
"""

import sys
import json
from loguru import logger

def prompt_from_issue(issue: dict):
    """
    Given a github issue object, returns a simplified prompt.
    """
    prompt = f"issue title: {issue['title']}\nissue description: {issue['body']}"
    logger.info(f"<prompt>{prompt}</prompt>")
    return prompt
    
class Agent:
    def __init__(self, issue):
        self.issue = issue
        self.directive = prompt_from_issue(issue)
    def address_issue(self):
        self.summarize_directive()
        self.make_a_plan()
        self.step_through_plan()
        self.validate_solution()
        self.submit_pr()


if __name__ == '__main__':
    issue = json.loads(sys.argv[1])
    author_role = issue['author_association']
    if author_role != 'OWNER':
        exit()
    agent = Agent(issue)
    #agent.address_issue()
