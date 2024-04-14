import anthropic
import base64
import re
import os


key = os.environ.get("ANTHTROPIC_API_KEY")
client = anthropic.Anthropic(api_key=key)

image_path = '/Users/rod13684/Documents/test_note2.jpg'

with open(image_path, "rb") as image_file:
    image_data = base64.b64encode(image_file.read()).decode("utf-8")

message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image_data,
                    },
                },
                {
                    "type": "text",
                    "text": "Convert the handwritten note in this image to Markdown format text. Preserve  characters such as '#' and '[', The first instance of text found in the image should return as '[[<example test>]]'. CRITICAL INSTRUCTION: DO NOT RETURN ANY TEXT OUR OUTPUT EXCEPT WHAT IS DETECTED IN THE IMAGE.",
                },
            ],
        }
    ],
)

markdown_text= message.content[0].text

match = re.search(r"\[\[(.+?)\]\]", markdown_text)
if match:
    file_name = match.group(1)
    markdown_text = markdown_text.replace(match.group(), "")
else:
    file_name = "output"

with open(f"{file_name}.md", "w") as markdown_file:
    markdown_file.write(markdown_text)

print(f"Conversion successful. Markdown file saved as {file_name}.md")

