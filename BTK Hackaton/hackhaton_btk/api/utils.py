import os
import google.generativeai as genai

genai.configure(api_key="AIzaSyBzz-mPuEHIEftIDogexuPLn5gy734ERgU")

# Model yapılandırma
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 5096,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def call_gemini_api(prompt):
    
    response = model.generate_content(prompt)
    return response


