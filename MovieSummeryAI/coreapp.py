from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI


load_dotenv()

model = ChatMistralAI(model = 'mistral-small-2506', temperature=0.3)

prompt = ChatPromptTemplate.from_messages([
    ('system', """
You are an advanced AI that analyzes and summarizes movie descriptions.

Your task is to extract structured and meaningful information from the given paragraph and enrich it with general knowledge if needed.

Extract the following fields:

1. Title (if mentioned)
2. Release Year
3. Main Characters
4. Setting (location, world, or environment)
5. Main Goal or Objective
6. Main Conflict (external and internal if applicable)
7. Key Plot Summary (short and clear)
8. Core Theme(s)
9. Genre
10. Tone (e.g., dark, emotional, suspenseful, inspiring)
11. Key Concepts (e.g., dream, time travel, space, crime, etc.)
12. IMDb Rating (approximate if known)
13. Rotten Tomatoes Score (if known)
14. Overall Review Summary (1–2 sentences about critical reception)

Rules:
- Keep each field concise (1 sentence max).
- Do NOT copy text directly; rewrite in simple words.
- If any field is not clearly available, use general knowledge OR write "Not specified".
- Ratings can be approximate but should be realistic.
- Avoid unnecessary explanation.
- Output must be clean and structured.

Output strictly in this format (no extra text):

Title: ...
Release Year: ...
Main Characters: ...
Setting: ...
Goal: ...
Conflict: ...
Plot: ...
Theme: ...
Genre: ...
Tone: ...
Key Concepts: ...
IMDb Rating: ...
Rotten Tomatoes: ...
Review: ..."""),
('human',
 """
Extract information from the paragraph:
{paragraph}
""")
])

user_text = input("Enter Your Paragraph: ")

final_prompt = prompt.invoke({
    'paragraph':user_text
})

response = model.invoke(final_prompt)

print(response.content)

