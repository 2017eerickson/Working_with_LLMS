from rest_framework.response import Response
from rest_framework.views import APIView
import os
from dotenv import load_dotenv
from google import genai
from PIL import Image
from pydantic import BaseModel, Field
from .models import StoryRequest
import json

load_dotenv()

from pydantic import BaseModel, Field

# class StoryRequest(BaseModel):
#     story: str = Field(description="The story to be generated, should not be more than 500 words, should be a friendly tone intened for children", example="Once upon a time, in a land far away..." )
#     lesson: str = Field(description="The lesson to be included in the story", example="The importance of kindness")
#     age_group: str = Field(description="The age group for which the story is intended", example="3-5 years old")
    

class Story_Generator(APIView):
    
        def post(self,request):
            api_key = os.getenv("GEMINI_API_KEY")   
            if not api_key:
                raise Exception('api key must be provided')   
            data = request.data.get("Lesson:", "") 
            client = genai.Client(api_key=api_key)

            
            gemini_cofig = {
                "model": "gemini-2.5-flash",
                "contents": data,
                "config":genai.types.GenerateContentConfig(
                    system_instruction= "You are a storyteller teaching children about the lesson provided by telling a story.",
                    response_mime_type= "application/json",
                    response_schema= StoryRequest
                )}
            response = client.models.generate_content(**gemini_cofig)  
            return Response({'Gemini':json.loads(response.text)})  
        
{
"Lesson": "Courage"
}
