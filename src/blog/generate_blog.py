import openai
import re
from jinja2 import Template
from datetime import datetime

# Function to read the content from a markdown file
def read_blog_content(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to generate content using GPT-4
def generate_blog_content(prompt, temperature=0.1):
    openai.api_key = 'your_openai_api_key'
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=2048
    )
    return response['choices'][0]['message']['content']

# Function to generate images using DALL-E
def generate_images(descriptions, n=1):
    openai.api_key = 'your_openai_api_key'
    images = []
    for description in descriptions:
        response = openai.Image.create(
            prompt=description,
            n=n,
            size="1024x1024"
        )
        images.append(response['data'][0]['url'])
    return images

# Jinja2 template for the blog post
template_str = """
# {{ title }}
### {{ subtitle }}

{% if images %}
![Generated Image]({{ images[0] }})

{% endif %}
## Why?
{{ why }}

{% for point in points %}
- **{{ point.title }}**: {{ point.description }}
{% endfor %}

{% if images and images|length > 1 %}
![Generated Image]({{ images[1] }})

{% endif %}
## Technical Details
Here’s how the project is being built:

{% for detail in technical_details %}
- **{{ detail.title }}**: {{ detail.description }}
{% endfor %}

## Next Stage of the Journey
Looking ahead, here are the next steps:

{% for step in next_steps %}
- **{{ step.title }}**: {{ step.description }}
{% endfor %}

## TL;DR
{{ tldr }}

{{ closing }}

{% for link in links %}
- [{{ link.text }}]({{ link.url }})
{% endfor %}
"""

# Create a Template object
template = Template(template_str)

# Read the blog content from the markdown file
blog_content = read_blog_content('blog_content.md')

# Extracting title and subtitle from the blog content
title_match = re.search(r'# (.+)', blog_content)
subtitle_match = re.search(r'### (.+)', blog_content)

title = title_match.group(1) if title_match else "Blog Post"
subtitle = subtitle_match.group(1) if subtitle_match else "Subtitle"

# Define the blog content structure
content = {
    "title": title,
    "subtitle": subtitle,
    "image_descriptions": [
        "A high quality professional digital image representing the main theme of the blog post.",
        "Another image capturing the essence of the blog content."
    ],
    "why": re.search(r'## Why\?\n(.+)', blog_content, re.DOTALL).group(1).strip(),
    "points": [
        {"title": match.group(1).strip(), "description": match.group(2).strip()}
        for match in re.finditer(r'- (.+?): (.+)', re.search(r'## Why\?\n(.+?)\n\n##', blog_content, re.DOTALL).group(1), re.DOTALL)
    ],
    "technical_details": [
        {"title": match.group(1).strip(), "description": match.group(2).strip()}
        for match in re.finditer(r'- (.+?): (.+)', re.search(r'## Technical Details\n(.+?)\n\n##', blog_content, re.DOTALL).group(1), re.DOTALL)
    ],
    "next_steps": [
        {"title": match.group(1).strip(), "description": match.group(2).strip()}
        for match in re.finditer(r'- (.+?): (.+)', re.search(r'## Next Stage of the Journey\n(.+?)\n\n##', blog_content, re.DOTALL).group(1), re.DOTALL)
    ],
    "tldr": re.search(r'## TL;DR\n(.+)', blog_content, re.DOTALL).group(1).strip(),
    "closing": re.search(r'## TL;DR\n(.+?)\n\n- ', blog_content, re.DOTALL).group(1).strip(),
    "links": [
        {"text": match.group(1).strip(), "url": match.group(2).strip()}
        for match in re.finditer(r'- \[(.+?)\]\((.+?)\)', blog_content)
    ]
}

# Generate detailed content using GPT-4
content['why'] = generate_blog_content(content['why'])
content['tldr'] = generate_blog_content(content['tldr'])
for point in content['points']:
    point['description'] = generate_blog_content(point['description'])
for detail in content['technical_details']:
    detail['description'] = generate_blog_content(detail['description'])
for step in content['next_steps']:
    step['description'] = generate_blog_content(step['description'])

# Generate images using DALL-E 3
content['images'] = generate_images(content['image_descriptions'])

# Render the template with the content
rendered_blog = template.render(content)

# Generate the filename with current datetime
filename = f"./blog_posts/{content['title'].replace(' ', '_')}_blog_{datetime.now().strftime('%d%m%Y')}.md"

# Save the rendered blog to a Markdown file
with open(filename, "w") as file:
    file.write(rendered_blog)

print(f"Blog post generated and saved as {filename}")
