"""
Uses an AI agent simulating an SDE to respond to a github issue and generate a PR.
"""

import sys
import json
from loguru import logger
from utils import map_project

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
        self.history = []
        self.state = {"directive": self.directive}  # keys: directive, plan
    def address_issue(self):
        self.make_a_plan()
        #self.step_through_plan()
        #self.validate_solution()
        #self.submit_pr()
    def make_a_plan(self):
        def think_through(directive: str, project_map: dict) -> str: 
            prompt = (
                f"Here's a summary of our codebase: \n\n{project_map}\n\n"
                "Please outline a step-by-step plan to address the directive below. "
                "Each step should appear on a single line, and each such line should begin with \"[STEPINSTRUCTIONS]\" to denote that "
                f"the rest of that line is the complete instructions for the coresponding step of the plan.\n\n{directive}"
            )
            plan = prompt # this is just a passthrough while this is still under development
            # response = generate_response(prompt) # TO DO: define generate_response
            # plan = response.choices[0].text.strip()
            return plan
        directive = self.state['directive']
        logger.debug(directive)
        project_map = map_project()
        logger.debug(project_map)
        plan = think_through(directive, project_map)
        logger.debug(plan)
        self.state['project_map'] = project_map
        self.state['plan'] = plan
        self.history.append({'project_map': project_map})
        self.history.append({'plan': plan})

if __name__ == '__main__':
    issue = json.loads(sys.argv[1])
    author_role = issue['author_association']
    if author_role != 'OWNER':
        exit()
    agent = Agent(issue)
    agent.address_issue()
