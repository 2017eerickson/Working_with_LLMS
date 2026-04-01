from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import json
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_INSTRUCTION="""
You are an interviewer who works at Pintrest interviewing me for the software engineering apprenticeship role.
Your role:
- Ask me basic questions that would come up in a behavioral interview for this role based on company culture and values
- Ask me basic questions that would come up in a technical interview
- Give feedback on answers I give you and ask follow up questions to my answers and also how to improve them 


Your contraints:
- Do not ask me questions that are not relevant to the role
- Do not ask me questions that are too complex for an apprenticeship role
- only ask 3 questions in total, 1 behavioral, 1 technical and 1 follow up question based on my answer to the first two questions
- Do not ask me questions that are too simple and do not give you enough information to give me feedback on my answer

Your Tone: 
- Friendly and encouraging but technically precise 
"""

class InterviewRequest(BaseModel):
    question: str = Field(description="The question to be asked in the interview", example="Can you tell me about a time you faced a challenge and how you overcame it?")       
    feedback: str = Field(description="The feedback to be given on the answer provided", example="Your answer is good but you could improve it by giving more specific examples and explaining your thought process more clearly.")
    follow_up: str = Field(description="The follow up question to be asked based on the answer provided")
    
chat_instance = client.chats.create(
    model="gemini-2.5-flash",
    config=genai.types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        response_mime_type="application/json",
        response_schema=InterviewRequest,
        thinking_config=genai.types.ThinkingConfig(
            include_thoughts=True,
            )
        )
    )

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the interview. Goodbye!")
        break
    response = chat_instance.send_message(user_input)
    for part in response.candidates[0].content.parts:
        if not part.text:
            continue
        if part.thought:
            print("Thought summary:")
            print(part.text)
            print()
        else:
            print("Answer:")
            print(part.text)
            print()
    print(f"Interviewer: {json.loads(response.text)}")