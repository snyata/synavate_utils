import openai
import os
import json
import ast

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Paths
UTILS_PATH = os.path.join('..', 'generate_tests', 'generate_tests', 'utils.py')
TESTS_PATH = os.path.join('..', 'generate_tests', 'tests', 'test_init_gen_tests.py')
TRACKER_PATH = os.path.join('..', 'generate_tests', 'scripts', 'generate_tests.json')

def get_existing_utilities():
    if os.path.exists(TRACKER_PATH):
        with open(TRACKER_PATH, 'r') as file:
            return json.load(file)
    return {}

def update_existing_utilities(utilities):
    with open(TRACKER_PATH, 'w') as file:
        json.dump(utilities, file, indent=4)

def extract_utilities_from_code(code):
    tree = ast.parse(code)
    utilities = [node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.ClassDef))]
    return utilities

def generate_tests(util_code):
    prompt = f"""
    Below is a utility function or class in Python:

    {util_code}

    Write pytest test cases for the above utility function or class.
    """

    response = openai.Completion.create(
        model="gpt-4o",
        prompt=prompt,
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.0
    )

    return response.choices[0].text.strip()

def main():
    # Load existing utilities from tracker
    existing_utilities = get_existing_utilities()

    # Read utils.py content
    with open(UTILS_PATH, 'r') as file:
        utils_code = file.read()

    # Extract utilities from utils.py
    current_utilities = extract_utilities_from_code(utils_code)

    new_tests = []

    for util in current_utilities:
        if util not in existing_utilities:
            # Generate tests for the new utility
            util_code = f"def {util}(): pass"  # Simplified for illustration
            tests = generate_tests(util_code)
            new_tests.append(tests)
            existing_utilities[util] = True

    # Update the tracker with new utilities
    update_existing_utilities(existing_utilities)

    # Append new tests to test_mylib.py
    if new_tests:
        with open(TESTS_PATH, 'a') as file:
            for test in new_tests:
                file.write('\n\n' + test)

        print("New tests generated and appended to test_mylib.py")
    else:
        print("No new utilities found. No tests generated.")

if __name__ == "__main__":
    main()