from agents.base_agent import BaseAgent
from utils.openai_api import OpenAIAPI
import re

class OpenAIAgent(BaseAgent):
    def __init__(self, browser, terminal, task_list, code_editor):
        super().__init__()  # Call the __init__ method of the parent class (BaseAgent)
        self.browser = browser
        self.terminal = terminal
        self.task_list = task_list
        self.code_editor = code_editor


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

            # Add the loaded knowledge base to the context
            if self.knowledge_base:
                knowledge_base_context = "\n".join([f"{key}: {value}" for key, value in self.knowledge_base.items()])
                context += f"Knowledge Base:\n{knowledge_base_context}\n\n"

            # Add the current task list to the context
            task_list_context = "\n".join([f"Task {i+1}: {task}" for i, task in enumerate(self.get_task_list())])
            context += f"Task List:\n{task_list_context}\n\n"

            # Add the conversation history to the context
            context += "\n".join(self.conversation_history[-5:])

            # Call the OpenAI API to process the user input
            response = self.api.api_calls(user_input, context)

            # Add the assistant's response to the conversation history
            self.conversation_history.append(f"Assistant: {response}")

    def generate_response(self):
        if self.conversation_history:
            return self.conversation_history[-1][11:]  # Extract the assistant's response
        else:
            return "I'm ready to assist you. Please provide me with a task or query."

    def execute_action(self, action):
        # Execute the action based on the generated response
        if action.lower() == "clear":
            self.conversation_history = []
            self.current_task = None
        elif action.lower() == "exit":
            print("Exiting the program...")
            exit()
        else:
            print(f"Executing action: {action}")
            
            if "open website" or "research" or "look up" in action.lower():
                url = self.extract_url_from_action(action)
                if url:
                    self.browser.navigate_to(url)
                else:
                    print("No valid URL found in the action.")
            
            elif "run command" in action.lower():
                command = self.extract_command_from_action(action)
                if command:
                    self.terminal.execute_command(command)
                else:
                    print("No valid command found in the action.")
            
            elif "add task" in action.lower():
                task = self.extract_task_from_action(action)
                if task:
                    self.task_list.add_task(task)
                else:
                    print("No valid task found in the action.")
            
            elif "write code" in action.lower():
                code = self.extract_code_from_action(action)
                if code:
                    self.code_editor.set_code(code)
                else:
                    print("No valid code found in the action.")

    def extract_url_from_action(self, action):
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        urls = url_pattern.findall(action)
        if urls:
            return urls[0]
        else:
            return None

    def extract_command_from_action(self, action):
        command_pattern = re.compile(r'run command:\s*(.+)', re.IGNORECASE)
        match = command_pattern.search(action)
        if match:
            return match.group(1)
        else:
            return None

    def extract_task_from_action(self, action):
        task_pattern = re.compile(r'add task:\s*(.+)', re.IGNORECASE)
        match = task_pattern.search(action)
        if match:
            return match.group(1)
        else:
            return None

    def extract_code_from_action(self, action):
        code_pattern = re.compile(r'write code:\s*(.+)', re.IGNORECASE)
        match = code_pattern.search(action)
        if match:
            return match.group(1)
        else:
            return None