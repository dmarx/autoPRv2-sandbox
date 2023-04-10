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


def extract_functions(source: str) -> list:
    """
    Given a string of source code, extract the names and arguments of all functions defined in that source code.

    1. Parse the source code string into an Abstract Syntax Tree (AST) using the built-in `ast.parse()` function.
    2. Use the built-in `ast.walk()` function to traverse the AST and identify all `FunctionDef` nodes.
    3. For each `FunctionDef` node, extract the name of the function and the names of its arguments using the `node.name` and `node.args.args` attributes, respectively.
    4. Return a list of strings, where each string represents the name of a function followed by a comma-separated list of its arguments.
    """
    functions = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.FunctionDef):
            functions.append(f"{node.name}({', '.join(arg.arg for arg in node.args.args)})")
    return functions


 def map_project() -> dict:
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
        def think_through(directive: str, project_map: dict) -> str: 
            prompt = (
                f"Here's a summary of our codebase: \n\n{project_map}\n\n"
                "Please outline a step-by-step plan to address the directive below. "
                "Each step should appear on a single line, and each such line should begin with \"[STEPINSTRUCTIONS]\" to denote that "
                f"the rest of that line is the complete instructions for the coresponding step of the plan.\n\n{directive}"
            )
            response = generate_response(prompt)
            plan = response.choices[0].text.strip()
            return plan
        directive = self.state['directive']
        project_map = map_project()
        plan = think_through(directive, project_map)
        self.state['project_map'] = project_map
        self.state['plan'] = plan
        self.history.append({'project_map': project_map})
        self.history.append({'plan': plan})

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


def check_changes_applied(notes: str):
    """
    Given a string of notes describing changes to be made to one or more files,
    checks that all changes were made as described.

    1. Split the notes string into a list of individual notes.
    2. For each note in the list:
        a. Extract the relative file path from the note.
        b. Load the file and parse its contents.
        c. Extract the line number and line text to be changed from the note.
        d. Verify that the line number and text in the file match those described in the note.
    3. If any note fails to match, raise an exception indicating which note(s) failed and how.
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
