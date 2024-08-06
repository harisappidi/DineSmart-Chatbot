# DineSmart: Your Personalized Restaurant Concierge

DineSmart is an innovative AI-powered chatbot designed to simplify the process of finding the perfect restaurant. This project leverages Google Vertex AI and Google Maps API to provide users with personalized and real-time restaurant recommendations based on their specific preferences for cuisine and location. The application is deployed on Google Cloud Platform (GCP).

Here is the link to access the application: https://dinesmart-3bij6bnbhq-uc.a.run.app

## Features

- **Restaurant Search**: Find restaurants based on specific cuisine and location.
- **Best Restaurant Recommendation**: Get the best restaurant recommendation based on ratings and number of reviews.
- **Interactive Chat**: Engage in a conversation with the chatbot to get restaurant suggestions.

## Technologies Used

- **Streamlit**: A web application framework for creating the chatbot interface.
- **Google Vertex AI**: For building and managing the generative model.
- **Google Maps API**: For fetching real-time restaurant data.
- **Python**: The primary programming language used for development.
- **Google Cloud Platform (GCP)**: For deploying the application.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Streamlit
- Google Cloud account with Vertex AI and Maps API enabled
- Google Cloud service account credentials
- `.env` file for managing API keys and credentials

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/harisappidi/DineSmart-Chatbot.git
    cd DineSmart-Chatbot
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory and add your API keys and credentials:

    ```env
    MAPS_API_KEY=your_google_maps_api_key
    GOOGLE_APPLICATION_CREDENTIALS=path_to_your_service_account_credentials.json
    ```

4. Ensure that your service account credentials file is correctly set in the environment variable:

    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS=path_to_your_service_account_credentials.json
    ```

### Running the Application

1. Navigate to the project directory:

    ```bash
    cd /path/to/your/folder
    ```

2. Run the Streamlit application:

    ```bash
    streamlit run main.py
    ```

3. Open your web browser and navigate to `http://localhost:8501` to access the DineSmart chatbot.

## Usage

1. Enter your query in the chat input box to find restaurants based on your cuisine and location preferences.
2. The chatbot will respond with restaurant recommendations, including the best restaurant based on ratings and number of reviews.
3. Continue the conversation to refine your search and get more personalized recommendations.

## Project Structure


DineSmart-Chatbot <br />
├── main.py # Main application file <br />
├── requirements.txt # Python dependencies <br />
├── .env # Environment variables <br />
├── README.md # Project documentation <br />


## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Google Vertex AI](https://cloud.google.com/vertex-ai)
- [Google Maps API](https://developers.google.com/maps/documentation)
- [Google Cloud Platform (GCP)](https://cloud.google.com/docs)

## Contact

For any questions or inquiries, please contact:

- Hari Sappidi - [GitHub](https://github.com/harisappidi)
