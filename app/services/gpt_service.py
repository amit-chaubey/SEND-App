from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("WARNING: No OpenAI API key found!")

# Initialize OpenAI client with API key
client = OpenAI(
    api_key=api_key,
    http_client=None  # This ensures we don't use any custom HTTP client
)

def fetch_word_from_gpt(focus_sound, difficulty_level=1, recent_words=None):
    if not api_key:
        print("No OpenAI API key found, using fallback words")
        return None
        
    print(f"GPT Service: Fetching word for sound '{focus_sound}'")
    recent_words = recent_words or []
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": f"You are a word generator. Generate ONE simple word containing the '{focus_sound}' sound. Respond with ONLY the word, no punctuation or explanation."
                },
                {
                    "role": "user", 
                    "content": f"Give me a word with '{focus_sound}' sound. Don't use: {', '.join(recent_words)}"
                }
            ],
            max_tokens=10,
            temperature=0.7
        )
        word = response.choices[0].message.content.strip().lower().rstrip('.,!?')
        if focus_sound not in word:
            print(f"Generated word '{word}' doesn't contain '{focus_sound}', skipping")
            return None
        print(f"GPT Service: Generated word '{word}'")
        return word
    except Exception as e:
        print(f"GPT Service Error: {str(e)}")
        return None 