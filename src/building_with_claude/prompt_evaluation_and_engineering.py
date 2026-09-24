import ast
import json
import re

from anthropic import Anthropic
from dotenv import load_dotenv

import building_with_claude.messages_api as API

load_dotenv()  # Load environment variables from .env file

client = Anthropic()
model = "claude-haiku-4-5-20251001"


def generate_dataset():
    prompt = """
Generate an evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects, each representing task that requires Python, JSON, or a Regex to complete.

Example output:
```json
[
  {
    "task": "Description of task",
    "format": json
  },
  ...additional
]
```

* Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a single regex
* Focus on tasks that do not require writing much code

Please generate 3 objects.
"""
    messages = []
    API.add_user_message(messages, prompt)
    API.add_assistant_message(messages, "```json")
    text = API.chat(messages, stop_sequences=["```"])
    return json.loads(text)


def run_prompt(test_case):
    """Merges the prompt and test case input, then returns the result"""
    prompt = f"""
Please solve the following task:

{test_case["task"]}
"""

    messages = []
    API.add_user_message(messages, prompt)
    output = API.chat(messages)
    return output


def run_test_case(test_case):
    """Calls run_prompt, then grades the result"""
    output = run_prompt(test_case)

    # TODO - Grading
    score = 10

    return {"output": output, "test_case": test_case, "score": score}


def run_eval(dataset):
    """Loads the dataset and calls run_test_case with each case"""
    results = []

    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)

    return results


def grade_by_model(test_case, output):
    # Create evaluation prompt
    eval_prompt = """
    You are an expert code reviewer. Evaluate this AI-generated solution.
    
    Task: {test_case}
    Solution: {output}
    
    Provide your evaluation as a structured JSON object with:
    - "strengths": An array of 1-3 key strengths
    - "weaknesses": An array of 1-3 key areas for improvement  
    - "reasoning": A concise explanation of your assessment
    - "score": A number between 1-10
    """

    messages = []
    API.add_user_message(messages, eval_prompt)
    API.add_assistant_message(messages, "```json")

    eval_text = API.chat(messages, stop_sequences=["```"])
    return json.loads(eval_text)


def validate_json(text):
    try:
        json.loads(text.strip())
        return 10
    except json.JSONDecodeError:
        return 0


def validate_python(text):
    try:
        ast.parse(text.strip())
        return 10
    except SyntaxError:
        return 0


def validate_regex(text):
    try:
        re.compile(text.strip())
        return 10
    except re.error:
        return 0


def extract_code_block(text):
    """Returns the contents of the first fenced code block, or the text itself"""
    match = re.search(r"```(?:[a-zA-Z]*)\n(.*?)```", text, re.DOTALL)
    return match.group(1) if match else text


def grade_syntax(output, test_case):
    """Scores the output 0-10 based on whether it parses as the expected format"""
    code = extract_code_block(output)
    validators = {
        "json": validate_json,
        "python": validate_python,
        "regex": validate_regex,
    }
    validator = validators.get(test_case["format"])

    if validator is None:
        raise ValueError(f"Unknown format: {test_case['format']}")

    return validator(code)
