import asana
from asana.rest import ApiException
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import json
import os
    
load_dotenv()

base_url = "https://api.aimlapi.com/v1"
api_key = os.getenv('API_KEY', '')

client = OpenAI(api_key=api_key, base_url=base_url)
model = os.getenv('AI_MODEL', 'gpt-4')

configuration = asana.Configuration()
configuration.access_token = os.getenv('ASANA_ACCESS_TOKEN', '')
api_client = asana.ApiClient(configuration)

task_api_instance = asana.TasksApi(api_client)

def create_asana_task(task_name, due_on='today'):
    """
    Creates a task in Asana given the name of the task and when it is due

    Example call:

    create_asana_task("Test Task", "2024-06-24")
    Args:
        task_name (str): The name of the task in Asana
        due_on (str): The date the task is due in the format YYYY-MM-DD. If not given, the current day is used
    Returns:
        str: The API response of adding the task to Asana or an error message if the API call threw an error
    """
    if due_on == 'today':
        due_on = str(datetime.now().date())
        
    task_body = {
        'data': {
            'name': task_name,
            'due_on': due_on,
            'projects': [os.getenv('ASANA_PROJECT_ID', '')]
        }
    }
    
    try:
        api_response = task_api_instance.create_task(task_body, {})
        return json.dumps(api_response, indent=2)
    except ApiException as e:
        return f"Error when calling TasksApi->create_task: {e}"
    
def get_tools():
    """
    Returns a list of tools that can be used by the AI in the chat

    The tools are defined as objects with a type of "function" and have a function property
    that contains the name, description, and parameters of the function

    The parameters are defined as objects with a type of "object" and have a properties
    property that contains the name, type, and description of each parameter

    The required property is a list of the names of the required parameters

    Args:
        None

    Returns:
        list: A list of tools that can be used by the AI in the chat
    """
    tools = [
        {
            'type': 'function',
            'function': {
                'name': 'create_asana_task',
                'description': 'Creates a task in Asana given the name of the task and when it is due',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'task_name': {'type': 'string', 'description': 'The name of the task in Asana'},
                        'due_on': {'type': 'string', 'description': 'The date the task is due in the format YYYY-MM-DD. If not given, the current day is usedThe date the task is due in the format YYYY-MM-DD. If not given, the current day is used'}
                    },
                    'required': ['task_name']
                }
            }
        }
    ]
    return tools

def prompt_ai(messages):
    """
    Prompts the AI with a given list of messages and processes the response. If the AI response includes tool calls, 
    it invokes the specified tools and appends the results back to the messages. Finally, it returns the AI's response 
    content.

    Args:
        messages (list): A list of messages to prompt the AI, where each message is a dictionary containing 
                         'role' and 'content' keys.

    Returns:
        str: The content of the AI's response message.
    """
    # First, prompt the AI with the latest user message
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=get_tools(),
        temperature=0.7,
        max_tokens=256,
    )
    
    response_message = completion.choices[0].message
    tool_calls = response_message.tool_calls
    
    # Second, see if the AI decided it needs to invoke a tool
    if tool_calls:
        # If the AI decided to invoke a tool, invoke it
        available_functions = {
            'create_asana_task': create_asana_task
        }
        
        # Add the tool request to the list of messages so the AI knows later it invoked the tool
        messages.append({
            'role': 'assistant',
            'content': response_message.content if response_message.content else '',
            'tool_calls': [
                {
                    'id': tool_call.id,
                    'type': 'function',
                    'function': {
                        'name': tool_call.function.name,
                        'arguments': tool_call.function.arguments
                    }
                } for tool_call in tool_calls
            ]
        })
        
        # Invoke the tool
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            # Invoke the function
            function_response = function_to_call(**function_args)
            
            # Add the function response to the list of messages
            messages.append({
                'tool_call_id': tool_call.id,
                'role': 'tool',
                'name': function_name,
                'content': function_response
            })
            
            # Call the AI again so it can produce a response with the result of calling the tool(s)
            second_completion = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=256,
            )
            
            return second_completion.choices[0].message.content
    
    return response_message.content

def main():
    messages = [
        {
            'role': 'system',
            'content': f'You are a personal assistant who helps manage tasks in Asana. The current date is: {datetime.now().date()}'
        }
    ]
    
    while True:
        user_input = input('Chat with AI (q to quit): ').strip()
        
        if user_input == 'q':
            break
        
        messages.append({'role': 'user', 'content': user_input})
        ai_response = prompt_ai(messages)
        
        print('Assistant:', ai_response)
        messages.append({'role': 'assistant', 'content': ai_response})
    
if __name__ == "__main__":
    main()