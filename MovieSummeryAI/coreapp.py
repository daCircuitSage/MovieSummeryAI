from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI

from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser
from typing import List, Optional


load_dotenv()

model = ChatMistralAI(model = 'mistral-small-2506', temperature=0.3)



class Movie(BaseModel):
    title : str
    genre : list[str]
    relese_year : Optional[int]
    director : str
    casts : list[str]
    ratings : float
    summery :str

parser = PydanticOutputParser(pydantic_object=Movie)




prompt = ChatPromptTemplate.from_messages([
    ('system', """
Extract structured information from the paragraph.

If any field is missing, use:
- ratings: 0.0
- director: "Unknown"
- casts: []

{format_instructions}
"""),
    ('human', "{paragraph}")
])

user_text = input("Enter Your Paragraph: ")

final_prompt = prompt.invoke({
    'paragraph':user_text,
    'format_instructions':parser.get_format_instructions()
})

response = model.invoke(final_prompt)

parsed_output = parser.parse(response.content)

print(parsed_output)

