from openai import OpenAI

with open("/Users/anthonywang/.langchain", "r") as f:
    api_key = f.read().strip()

client = OpenAI(api_key=api_key)
