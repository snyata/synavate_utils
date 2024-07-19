import openai
import os
import json
import ast
import shutil

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Load configuration
with open('config.json', 'r') as file:
    config = json.load(file)

# Load prompt examples
from prompt_examples import python_examples, ts_examples, rs_examples

examples = {
    "python3": python_examples,
    "ts": ts_examples,
    "rs": rs_examples
}

def get_existing_utilities(tracker_path):
    if os.path.exists(tracker_path):
        with open(tracker_path, 'r') as file:
            return json.load(file)
    return {}

def update_existing_utilities(tracker_path, utilities):
    with open(tracker_path, 'w') as file:
        json.dump(utilities, file, indent=4)

def extract_utilities_from_code(lang, code):
    if lang == "python3":
        tree = ast.parse(code)
        return [node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.ClassDef))]
    # Add other language parsing if necessary
    return []

def generate_tests(lang, util_code, examples):
    prompt = f"""
    Below is a utility function or class in {lang}:

    {util_code}

    Write test cases for the above utility function or class using {config['languages'][lang]['test_framework']}.

    {examples}
    """

    response = openai.Completion.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.7
    )

    return response.choices[0].text.strip()

def main():
    for lang, settings in config['languages'].items():
        source_dir = settings['source_dir']
        test_dir = settings['test_dir']
        tracker_path = os.path.join(test_dir, 'utils_tracker.json')

        # Load existing utilities from tracker
        existing_utilities = get_existing_utilities(tracker_path)

        # Read source code
        utils_files = [f for f in os.listdir(source_dir) if f.endswith(('.py', '.ts', '.rs'))]
        for utils_file in utils_files:
            with open(os.path.join(source_dir, utils_file), 'r') as file:
                utils_code = file.read()

            # Extract utilities from source code
            current_utilities = extract_utilities_from_code(lang, utils_code)

            new_tests = []

            for util in current_utilities:
                if util not in existing_utilities:
                    # Generate tests for the new utility
                    util_code = f"def {util}(): pass"  # Simplified for illustration
                    tests = generate_tests(lang, util_code, examples[lang])
                    new_tests.append(tests)
                    existing_utilities[util] = True

            # Update the tracker with new utilities
            update_existing_utilities(tracker_path, existing_utilities)

            # Append new tests to the appropriate test file
            if new_tests:
                test_file_path = os.path.join(test_dir, f'test_{os.path.splitext(utils_file)[0]}.py' if lang == 'python3' else f'test_{os.path.splitext(utils_file)[0]}.ts')
                with open(test_file_path, 'a') as file:
                    for test in new_tests:
                        file.write('\n\n' + test)

                print(f"New tests generated and appended to {test_file_path}")
            else:
                print(f"No new utilities found in {utils_file}. No tests generated.")

if __name__ == "__main__":
    main()