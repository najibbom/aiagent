# Asana Task Manager AI Assistant

## Overview
This project implements an AI-powered assistant that helps manage tasks in Asana. The assistant uses natural language processing to understand user requests and can create tasks in Asana with specified due dates.

## Features
- Chat-based interface for interacting with the AI assistant
- Integration with Asana for task management
- Function calling capabilities to create tasks directly from conversation
- Support for specifying task due dates

## Technologies Used
- Python
- OpenAI API (via AIML API)
- Asana API
- dotenv for environment variable management

## How It Works
The application works by:
1. Connecting to the AIML API for AI capabilities
2. Connecting to the Asana API for task management
3. Providing a chat interface where users can request task creation
4. Processing natural language to identify when to create tasks
5. Automatically formatting and submitting tasks to Asana

## Setup Instructions

### Prerequisites
- Python 3.6+
- An Asana account with API access
- An AIML API key

### Installation
1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with the following variables:
   ```
   API_KEY=your_aiml_api_key
   AI_MODEL=gpt-4  # or another supported model
   ASANA_ACCESS_TOKEN=your_asana_access_token
   ASANA_PROJECT_ID=your_asana_project_id
   ```

### Running the Application
Run the application with:
```
python agents.py
```

## Usage Examples
Once the application is running, you can interact with it through the command line:

```
Chat with AI (q to quit): Create a task to create a YouTube thumbnail, I need it done by Wednesday
Assistant: I've created a task in Asana titled "Create a YouTube thumbnail" with a due date of Wednesday.
```

## Function Calling
The application uses function calling to enable the AI to create tasks in Asana. The AI can:
- Identify when a user wants to create a task
- Extract the task name and due date from natural language
- Call the appropriate function to create the task in Asana

## Environment Variables
- `API_KEY`: Your AIML API key
- `AI_MODEL`: The AI model to use (default: gpt-4)
- `ASANA_ACCESS_TOKEN`: Your Asana personal access token
- `ASANA_PROJECT_ID`: The ID of the Asana project where tasks will be created

## Limitations
- Currently only supports creating tasks (not updating or deleting)
- Due dates must be specified in a format the AI can understand
- Requires an active internet connection for API access

## Future Improvements
- Add support for more Asana features (task updates, comments, etc.)
- Implement a graphical user interface
- Add support for multiple Asana projects
- Improve error handling and retry mechanisms

## License
[Specify your license here]

## Acknowledgements
- OpenAI for the AI capabilities
- Asana for the task management platform
