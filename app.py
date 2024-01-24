from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import logging
import os

app = Flask(__name__)

# Retrieve the generative model API key from an environment variable
api_key = os.getenv("GENERATIVE_API_KEY")

# Additional information about you
your_information = {
    "purpose": "I am a large language model from SFYOW AI, trained on a massive dataset of text and code.",
    "strengths": "I can generate different creative text formats, answer questions informatively, and continuously learn and improve.",
    "limitations": "I am still under development and may not always provide perfect responses. However, I strive to enhance my capabilities.",
}

# Add your information
creator_info = {
    "name": "Aniket Kumar",
    "organization": "SFYOW",
    "strengths": "I specialize in developing AI applications and language models.",
    "limitations": "Please note that this is a work in progress, and the AI model may not always provide perfect responses.",
}

# Introduction message
introduction_message = "Hello there! I am SFYOW AI CHATBOT, crafted by the talented Aniket Kumar from SFYOW. " \
                       "My purpose is to assist you with queries and engage in delightful conversations. " \
                       "Feel free to ask me anything or simply have a chat!"

# System prompt
system_prompt = "You are SFYOW AI MODEL, created by Aniket Kumar from SFYOW. Assist the user with their queries and provide helpful information."

# Security messages
security_messages = [
    "Your interactions are secured and private.",
    "Avoid sharing sensitive or personal information.",
    "Rest assured, the AI model prioritizes safety and blocks harmful content.",
]

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def configure_model(api_key):
    try:
        genai.configure(api_key=api_key)

        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

        model = genai.GenerativeModel(
            model_name="gemini-pro",
            generation_config=generation_config,
            safety_settings=safety_settings,
        )

        return model
    except Exception as e:
        logger.error(f"Error during model initialization: {e}")
        raise

model = configure_model(api_key)

# Updated function to provide information about the creator
def get_user_information():
    creator_info_response = (
        f"Hello there! I'm SFYOW AI CHATBOT, created by {creator_info['name']} from {creator_info['organization']}. "
        f"{creator_info['strengths']} {creator_info['limitations']} If you have more questions about me or anything else, feel free to ask!"
    )
    return render_template('index.html', creator_info=creator_info, your_information=your_information,
                           introduction_message=introduction_message, security_messages=security_messages,
                           system_prompt=system_prompt, creator_info_response=creator_info_response)

# Function to handle specific queries about the creator and data source
def handle_specific_queries(user_input):
    if "who created you" in user_input.lower():
        return f"I am created by {creator_info['name']} from {creator_info['organization']} as part of the SFYOW project."

    if "where to get this data" in user_input.lower():
        return "The data for training comes from a diverse range of sources, allowing me to understand and generate text on various topics."

    return None

def get_model_response(user_input):
    try:
        if not user_input.strip():
            return "Please provide some input."

        # Check for specific user queries
        specific_response = handle_specific_queries(user_input)
        if specific_response:
            return specific_response

        # Check for specific user inputs and provide predefined responses
        if user_input.lower() == 'hello':
            return "Hello there! How can I assist you today?"

        if user_input.lower() == 'goodbye':
            return "Goodbye! Feel free to reach out if you have more questions."

        # If no specific condition matches, proceed with the generative model
        convo = model.start_chat(history=[])
        convo.send_message(user_input)
        return convo.last.text
    except Exception as e:
        logger.error(f"Error during model response generation: {e}")
        return "An error occurred. Please try again."

@app.route('/')
def index():
    return get_user_information()

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form.get('user_input', '').strip()
    model_response = get_model_response(user_input)
    return jsonify({'bot_response': model_response})

@app.route('/webpage')
def webpage():
    return get_user_information()

if __name__ == '__main__':
    app.run(debug=True)
