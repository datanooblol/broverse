from broverse.action import Action
import requests
import re

def clean_up_markdown_link(markdown):
    cleaned_text = re.sub(r'!\[.*?\]\(.*?\)|\[(.*?)\]\(.*?\)', r'\1', markdown)
    return cleaned_text

class HTMLParsing(Action):
    def run(self, shared):
        source = shared.get("source", None)
        response = requests.get(f"https://r.jina.ai/{source}")
        markdown_str = clean_up_markdown_link(response.text)
        shared["raw_context"] = markdown_str
        shared["action"] = "chunk"
        return shared