from agents.base_agent import BaseAgent
from utils.openai_api import OpenAIAPI

class OpenAIAgent(BaseAgent):
    def __init__(self, model, api_key):
        self.api = OpenAIAPI(model=model, api_key=api_key)
        self.conversation_history = []
        self.current_task = None

    def process_input(self, user_input):
        # Add the user input to the conversation history
        self.conversation_history.append(f"User: {user_input}")

        # Check if the user input is a task assignment
        if user_input.lower().startswith("task:"):
            self.current_task = user_input[5:].strip()
            self.conversation_history.append(f"Assistant: Understood. The current task is: {self.current_task}")
        else:
            # If there is a current task, add it to the context
            if self.current_task:
                context = f"Current Task: {self.current_task}\n\n"
            else:
                context = ""

            # Add the conversation history to the context
            context += "\n".join(self.conversation_history[-5:])

            # Call the OpenAI API to process the user input
            response = self.api.generate_response(context + f"\nUser: {user_input}")

            # Add the assistant's response to the conversation history
            self.conversation_history.append(f"Assistant: {response}")

    def generate_response(self):
        if self.conversation_history:
            return self.conversation_history[-1][11:]  # Extract the assistant's response
        else:
            return "I'm ready to assist you. Please provide me with a task or query."

    def execute_action(self, action):
        # Placeholder implementation for executing actions
        # You can extend this method to handle specific actions based on the generated response
        print(f"Executing action: {action}")

        # Example: If the action is a clear instruction, clear the conversation history
        if action.lower() == "clear":
            self.conversation_history = []
            self.current_task = None