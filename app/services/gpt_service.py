import openai
import os


from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def fetch_word_from_gpt(focus_sound, difficulty_level):
    """
    Fetch a word containing the specified focus_sound and for the given difficulty_level using OpenAI GPT.
    """
    try:
        print(f"Fetching word with focus_sound: {focus_sound}, difficulty_level: {difficulty_level}")

        # Call OpenAI's chat completions API
        completion = client.chat.completions.create(
            model="gpt-4o",  # Replace with your correct model (e.g., gpt-4)
            messages=[
                {
                    "role": "developer",
                    "content": "You are a helpful assistant that generates single words containing specific sounds.",
                },
                {
                    "role": "user",
                    "content": f"Give me a word containing the sound '{focus_sound}' at difficulty level {difficulty_level}.",
                },
            ],
        )

        # Access the message content properly
        word = completion.choices[0].message.content.strip()
        print(f"GPT Response: {word}")
        return word

    except Exception as e:
        # Handle errors gracefully
        print(f"Error in fetch_word_from_gpt: {e}")
        return None



print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
