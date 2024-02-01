from flask import Flask, request, jsonify, render_template
import openai
import asyncio
import os
from dotenv import load_dotenv
from datetime import date

app = Flask(__name__)


# Load the environment variables from the .env file
load_dotenv()

# Get the API key from the environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# Set up OpenAI API credentials
openai.api_key = openai_api_key

# Define the rest of your code below

# Define the HTML page to render
@app.route("/")
def home():
    return render_template("index.html")

# Define the JSON API endpoint
@app.route("/api/chat", methods=["POST"])
def chat():
    # Get the user input from the request
    user_input = request.form["user_input"]
    
    # Call the OpenAI API to get the chatbot's response
    response = asyncio.run(get_chatbot_response(user_input))
    
    # Return the response as a JSON object
    return jsonify(response)

# Define an async function to get the chatbot's response
async def get_chatbot_response(user_input):
    # Set up the OpenAI API request
    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
            {"role": "system", "content": f"You are a conversion system, you convert markdown lists into a comma-separated format that can be easily pasted into Excel, No header in the first row. Format: today's date {date.today().isoformat()} in the first column, the time without the check-mark bullets in the second column, then three empty columns, and the text in the last column. Provide the output as a code block without any additional comments."},
            {"role": "user", "content": """
- [x] 08:30 check-in\n
- [x] 09:00 merges\n
- [x] 10:00 Hiper\n
- [] 10:30 PS checkin\n
- [ ] 11:00 test meeting\n
- [x] 11:30 BREAK\n
- 12:30 merges\n
- 13:00 all-hands\n
- 13:15 break\n
- [x] 13:30 merges\n
- 14:45 break
"""
             },
            {"role": "assistant", "content": """
```\n
2023-05-01, 08:30, , , , check-in\n
2023-05-01, 09:00, , , , merges\n
2023-05-01, 10:00, , , , Hiper\n
2023-05-01, 10:30, , , , PS checkin\n
2023-05-01, 11:00, , , , test meeting\n
2023-05-01, 11:30, , , , BREAK\n
2023-05-01, 12:30, , , , merges\n
2023-05-01, 13:00, , , , all-hands\n
2023-05-01, 13:15, , , , BREAK\n
2023-05-01, 13:30, , , , merges\n
2023-05-01, 14:45, , , , BREAK\n
```
"""
             },
            {"role": "user", "content": f"{user_input}"}
        ]
    )

    # Extract the chatbot's response from the API response
    result = response['choices'][0]['message']['content']
    # Return a JSON-encoded response
    return result

if __name__ == "__main__":
    app.run(debug=True)
