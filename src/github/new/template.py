import os
from typing import Dict, Optional
from pydantic import BaseModel
from dotenv import load_dotenv


class TemplateModel(BaseModel):
    repo_name: str = "new_repo"
    description: str
    author: str = "snyata"
    email: str = "core@synavate.tech"
    model: str = "gpt-4o"

if os.path.isfile('.env'):
    load_dotenv()
    print(".ENV FILE LOADED")
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Read from the template file
def read_template_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        template_data = {}
        for line in lines:
            key, value = line.strip().split(': ', 1)
            template_data[key] = value
    return template_data

# Get the base path from environment variables
base_path = os.getenv('BASE_PATH')
if base_path is None:
    raise ValueError("BASE_PATH environment variable is not set")

# Construct the full path to the template file
template_file_path = os.path.join(base_path, "README_template.md")

# Read the template data from the file
template_data = read_template_file(template_file_path)

# Create an instance of TemplateModel with the read data
readme_template = TemplateModel(
    repo_name=template_data['repo_name'],
    description=template_data['description'],
    author=template_data['author'],
    email=template_data['email'],
    model=template_data['model']
)

def read_project_description(file_path=template_file_path):
    """
    Reads the project description from a file and returns a dictionary containing the project information.

    Args:
        file_path (str, optional): The path to the file containing the project description. Defaults to the value of the environment variable 'BASE_PATH'.

    Returns:
        dict: A dictionary containing the project information. The keys are 'repo_name', 'description', 'email', 'author', and 'model'. The values are the corresponding values from the file.

    Raises:
        FileNotFoundError: If the file specified by `file_path` does not exist.

    Example:
        >>> read_project_description('/path/to/project_description.txt')
        {'repo_name': 'my_repo', 'description': 'This is my project', 'email': 'user@example.com', 'author': 'John Doe', 'model': 'model_name'}
    """
    # Use ENV Variable for BASE_PATH
    if not os.path.exists(file_path):
        os.mkdir(file_path)
        
        with open(file_path, 'r') as file:
            lines = file.readlines()
            project_info = {}
            for line in lines:
                if line.startswith('1. repo_name:'):
                    project_info['repo_name'] = line.split(':')[1].strip()
                elif line.startswith('2. description:'):
                    project_info['description'] = line.split(':')[1].strip()
                elif line.startswith('3. email:'):
                    project_info['email'] = line.split(':')[1].strip()
                elif line.startswith('4. author:'):
                    project_info['author'] = line.split(':')[1].strip()
                elif line.startswith('5. model:'):
                    project_info['model'] = line.split(':')[1].strip()
            return project_info
    
        

def generate_readme(project_info):
    """
    A function that generates a README.md file for a given project based on the project information provided. 
    The README includes sections such as the repo name, description, contact email, and specific formatting requirements.
    """
    prompt = (
        f"Create a simple README.md file for the following project:\n\n"
        f"Repo Name: {project_info['repo_name']}\n"
        f"Description: {project_info['description']}\n"
        f"Contact Email: {project_info['email']}\n\n"
        f"Contact Email: {project_info['author']}\n\n"
        f"The README should include the following sections:\n"
        f"1. Name of repo\n"
        f"2. Short 1-2 Sentence description including the fact it is in a new project.\n"
        f"3. Contact Us: {{Email}}\n\n"
        f"Use a formal tone"
        f"Output the content of README.md with strict markdown format, headings and sparse emojis."
    )

    response = openai.Completion.create(
        model="gpt-4o",  # Or any other model you are using
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.0,
    )

    readme_content = response.choices[0].text.strip()
    return readme_content

def write_readme(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def main():
    """
    A function that orchestrates the initialization of a project repository by reading project description,
    navigating to the project directory, initializing the repository, creating a blank README file,
    generating README content, and committing the README to the repository.
    """

    project_path = read_project_description(file_path=os.getenv('BASE_PATH'))
    # Step 4: Navigate to the project directory
    if os.path.exists(os.join(project_path,project_path["repo_name"])):
        os.chdir(os.join(project_path,project_path["repo_name"]))
    else:
        os.mkdir(os.join(project_path,project_path["repo_name"]))

    # Step 5: Initialize the repo locally, create a blank README, add and commit
    subprocess.run(['git', 'init'])
    readme_path = os.path.join(project_path, 'README.md')
    open(readme_path, 'w').close()  # Create an empty README.md file

    # Generate README content
    readme_content = generate_readme(project_path[:])

    # Write README content to README.md file
    write_readme(readme_path, readme_content)
    subprocess.run(['git', 'add', 'README.md'])
    subprocess.run(['git', 'commit', '-m', 'Initial commit with README'])

    print("README.md has been generated and committed successfully.")

if __name__ == "__main__":
    import openai
    openai.api_key = os.getenv('OPENAI_API_KEY')
    main()

