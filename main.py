import streamlit as st
import requests
import os
import vertexai
from google.oauth2 import service_account
from dotenv import load_dotenv
import os

load_dotenv()

# Google Maps API key
MAPS_API_KEY = os.getenv('MAPS_API_KEY')


from vertexai.generative_models import (
    FunctionDeclaration,
    GenerationConfig,
    GenerativeModel,
    Part,
    Tool,
)

# Function to get restaurant content via API
def getcontent_via_api(location, cuisine):
    """
    Fetch restaurant information based on location and cuisine from Google Places API.

    Args:
        location (str): The location to search for restaurants.
        cuisine (str): The type of cuisine to search for.

    Returns:
        dict: A dictionary containing restaurant information if the request is successful.
        dict: A dictionary containing error information if the request fails.
    """

    endpoint = 'https://places.googleapis.com/v1/places:searchText'

    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': MAPS_API_KEY,
        'X-Goog-FieldMask': 'places.id,places.displayName,places.formattedAddress,places.priceLevel,places.rating'
    }
    data = {
        "textQuery": location + " " + cuisine + " restaurants"
    }

    response = requests.post(endpoint, headers=headers, json=data)
    if response.status_code == 200:
        results = response.json()
        return results
    else:
        #return error information to the model
        return response.json()

# Streamlit app
def run_conversation():

    """
    Handle user conversation within the Streamlit app.
    Manages user input, maintains context, and interacts with the generative model.
    """

    # Function declarations for the generative model
    check_restaurants = FunctionDeclaration(
        name="check_restaurants",
        description="Check if there are restaurants based on Cuisine in a specific location",
        parameters={
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "Location to search for restaurants"},
                "cuisine": {"type": "string", "description": "Cuisine type"}
            },
            "required": ["location","cuisine"]
        },
    )

    get_best_restaurant = FunctionDeclaration(
        name="get_best_restaurant",
        description="Get the best restaurant of user requested cuisine based on rating and number of reviews",
        parameters={
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "Location to search for the best restaurant"},
                "cuisine": {"type": "string", "description": "Cuisine type"},
                "min_reviews": {"type": "integer", "description": "Minimum number of reviews", "default": 100}
            },
            "required": ["location", "cuisine"]
        },
    )

    # Define tools with function declarations
    resta_tool = Tool(
        function_declarations=[
            check_restaurants,
            get_best_restaurant
        ],
    )

    # Initialize the generative model with the defined tools
    model = GenerativeModel(
        "gemini-1.0-pro-vision",
        generation_config=GenerationConfig(temperature=0.3),
        tools=[resta_tool],
    )
    chat = model.start_chat()
    st.header("Find the restaurants based on cuisine and location")


    # Handle user input
    user_query = st.chat_input("Enter your message here...")
    if user_query:
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # Concatenate only the last 5 messages to maintain context
        last_five_messages = st.session_state.chat_history[-5:]
        full_context = "\n".join([msg["content"] for msg in last_five_messages])

        # Send message to the generative model
        response = chat.send_message(full_context)
        function_name = response.candidates[0].content.parts[0].function_call

        if function_name:
            response_part = response.candidates[0].content.parts[0].function_call.args
            location = response_part["location"]
            cuisine = response_part["cuisine"]

            # Get restaurant content via API based on the function call
            llm_response = chat.send_message(
                Part.from_function_response(
                    name=response.candidates[0].content.parts[0].function_call.name,
                    response={
                        "content": getcontent_via_api(location,cuisine),
                    },
                ),
            )
            
            response_text = llm_response.candidates[0].content.parts[0].text
        else:
            response_text = response.candidates[0].content.parts[0].text

        # Append the assistant's response to chat history and display it
        st.session_state.chat_history.append({"role": "assistant", "content": response_text})
        with st.chat_message("assistant"):
            st.write(response_text)

def main():
    """
    Main function to run the Streamlit app.
    It sets up the UI, initializes credentials, and starts the conversation handling.
    """

    st.set_page_config(page_title="Dinesmart", page_icon="🍽️")
    st.title("Dinesmart: Your personal restaurant concierge")

    # Get Google Cloud credentials from environment variable
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise Exception("The GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")

    credentials = service_account.Credentials.from_service_account_file(credentials_path)

    PROJECT_ID = "dinesmart-430016"
    LOCATION = "us-east4"

    # Initialize Vertex AI with the project credentials
    vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=credentials)

    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hi there! How can I help you today with restaurants ?"}
        ]

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    run_conversation()

if __name__ == "__main__":
    main()