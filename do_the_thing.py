import ast

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


def extract_functions(source)
    functions = []
    for node in ast.walk(ast.parse(f.read())):
        if isinstance(node, ast.FunctionDef):
            functions.append(f"{node.name}({', '.join(arg.arg for arg in node.args.args)})")
    return functions


 def map_project():
    mapping = {}
    for file in Path('.').rglob('*.*'):
        with open(file) as f:
            source = f.read()
        num_tokens = len(source)
        functions = extract_functions(source)
        docstring = ast.get_docstring(ast.parse(source))

        record = f"relative path: {file.relative_to(Path.cwd())}\n" \
                 f"number of tokens: {num_tokens}\n"
        if docstring:
            record += f"docstring: {docstring}\n"
        record += f"functions: {', '.join(functions)}\n"

        mapping[file.stem] = record
   return mapping

    
# this is gonna be a super spaghetti code way of doing things but it might be a helpful way to keep information
# within a helpfully readable context for the LLM
class Agent:
    def __init__(self, issue):
        self.issue = issue
        self.directive = prompt_from_issue(issue)
        self.history = []
        self.state = {"directive": self.directive}  # keys: directive, plan

    def address_issue(self):
        self.make_a_plan()
        self.step_through_plan()
        self.validate_solution()
        self.submit_pr()

        
    def make_a_plan(self):
        def think_through(directive):
            prompt = f"Please generate a plan to address the following directive:\n\n{directive}"
            response = generate_response(prompt)
            plan = response.choices[0].text.strip()
            return plan
        self.state['project_map'] = map_project()
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

        
#########################################################################################

def take_notes(plan_step, file_path):
    """
    Given a plan step and a file path, returns a dictionary of notes about the file relevant to the plan step.
    
    The function should perform the following operations:
    
    1. Parse the file at the given file path using the `ast` module.
    2. Extract all function definitions from the parsed code using the `extract_functions` function.
    3. Create a dictionary of notes with the following keys:
        - "file_path": the file path
        - "num_tokens": the number of tokens in the code
        - "docstring": the docstring of the module (if any)
        - "functions": a list of function names and arguments extracted from the code
        - "relevant": a boolean indicating whether any of the functions in the file are relevant to the current plan step
        - "changes": a list of planned changes to the file for the current plan step
    
    The function should return the dictionary of notes.
    """
    pass


def necessary_to_modify(file_path):
    """
    Given a file path, returns a boolean indicating whether it is necessary to modify the file to address the current plan step.
    
    The function should perform the following operations:
    
    1. Check if the file at the given file path was marked as relevant in the plan notes.
    2. If the file was marked as relevant, check if any planned changes were made to the file.
    3. If any planned changes were made to the file, return True; otherwise, return False.
    
    The function should return a boolean.
    """
    pass


def make_changes(file_path):
    """
    Given a file path, modifies the file to address the current plan step.
    
    The function should perform the following operations:
    
    1. Check if the file at the given file path was marked as relevant in the plan notes.
    2. If the file was marked as relevant, apply any planned changes to the file using the `ast` module.
    3. Write the modified code back to the file.
    
    The function should not return anything.
    """
    pass


#########################################################################################


if __name__ == '__main__':
    issue = json.loads(sys.argv[1])
    author_role = issue['author_association']
    if author_role != 'OWNER':
        exit()
    agent = Agent(issue)
    agent.address_issue()
