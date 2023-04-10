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
    
# this is gonna be a super spaghetti code way of doing things but it might be a helpful way to keep information
# within a helpfully readable context for the LLM
class Agent:
    def __init__(self, issue):
        self.issue = issue
        self.directive = prompt_from_issue(issue)
        self.history = []
        self.state = {"directive": self.directive}  # keys: directive, plan

    def address_issue(self):
        self.summarize_directive()
        self.make_a_plan()
        self.step_through_plan()
        self.validate_solution()
        self.submit_pr()

    def summarize_directive(self):
        def summarize(directive):
            prompt = f"Please restate the following GitHub issue as a directive:\n\n{directive}"
            response = generate_response(prompt)
            summarized_directive = response.choices[0].text.strip()
            return summarized_directive

        self.state['directive'] = summarize(self.state['directive'])
        self.history.append({'directive': self.state['directive']})

    def make_a_plan(self):
        def think_through(directive):
            prompt = f"Please generate a plan to address the following directive:\n\n{directive}"
            response = generate_response(prompt)
            plan = response.choices[0].text.strip()
            return plan

        self.state['plan'] = think_through(self.state['directive'])
        self.history.append({'plan': self.state['plan']})

    def step_through_plan(self):
        def think_about_files(plan_step):
            #relevant_files_to_read, new_filenames_to_create = None, None
            relevant_files_to_read = []
            for file in Path('.').rglob('*.*'):
                file_notes = take_notes(plan_step, file)
                # TO DO: add notes to plan sub-state and history
                self.state['notes']
            # TO DO: review notes to infer new files to create, write new notes, update states/history
            return relevant_files_to_read, new_filenames_to_create
            
        def execute_plan(plan_step):
            #prompt = f"Please generate code to execute the following plan step:\n\n{plan_step}"
            #response = generate_response(prompt)
            #code = response.choices[0].text.strip()
            relevant_files_to_read, new_filenames_to_create = think_about_files(plan_step)
            for file in relevant_files_to_read:
                if necessary_to_modify(file):
                    make_changes(file)
            for file_name in new_filenames_to_create:
                

        for step in self.state['plan']:
            execute_plan(step)

    def validate_solution(self):
        prompt = f"Please test the code you have generated to ensure that it meets certain quality and functionality standards."
        response = generate_response(prompt)
        feedback = response.choices[0].text.strip()
        self.history.append({'feedback':feedback})

    def submit_pr(self):
        prompt = f"Please submit a pull request with the generated code, along with a message summarizing the changes made and explaining how they address the issue."
        response = generate_response(prompt)
        pr_message = response.choices[0].text.strip()
        # create pull request here
        self.history.append(pr_message)



if __name__ == '__main__':
    issue = json.loads(sys.argv[1])
    author_role = issue['author_association']
    if author_role != 'OWNER':
        exit()
    agent = Agent(issue)
    agent.address_issue()
