from abc import ABC, abstractmethod
from utils.openai_api import OpenAIAPI
import re
import pickle
from gui.browser import Browser
from gui.code_editor import CodeEditor
from gui.terminal import Terminal
from gui.task_list import TaskList

class BaseAgent(ABC):
    def __init__(self):
        self.api = OpenAIAPI()
        self.conversation_history = []
        self.current_task = None
        self.knowledge_base = {}  # Initialize the knowledge_base as an empty dictionary
        self.browser = Browser()
        self.code_editor = CodeEditor()
        self.terminal = Terminal()
        self.task_list = TaskList()
    @abstractmethod
    def process_input(self, user_input):
        """
        Process the user input and update the agent's internal state.

        Args:
            user_input (str): The user input string.
        """
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

            # Add the conversation history to the context
            context += "\n".join(self.conversation_history[-5:])

            # Call the OpenAI API to process the user input
            response = self.api.api_calls(user_input, context)

            # Add the assistant's response to the conversation history
            self.conversation_history.append(f"Assistant: {response}")

    @abstractmethod
    def generate_response(self):
        """
        Generate a response based on the agent's current state.

        Returns:
            str: The generated response.
        """
        if self.conversation_history:
            return self.conversation_history[-1][11:]  # Extract the assistant's response
        else:
            return "I'm ready to assist you. Please provide me with a task or query."

    @abstractmethod
    def execute_action(self, action):
        """
        Execute an action based on the generated response.

        Args:
            action (str): The action to be executed.
        """
        # Execute the action based on the generated response
        if action.lower() == "clear":
            self.conversation_history = []
            self.current_task = None
        elif action.lower() == "exit":
            print("Exiting the program...")
            exit()
        else:
            print(f"Executing action: {action}")

            if "open website" in action.lower():
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

    def reset(self):
        """
        Reset the agent's internal state to its initial values.
        """
        self.conversation_history = []
        self.current_task = None
        self.knowledge_base = {}

    def load_knowledge_base(self, knowledge_base):
        """
        Load a knowledge base into the agent's memory.

        Args:
            knowledge_base (dict): The knowledge base dictionary.
        """
        if not isinstance(knowledge_base, dict):
            raise ValueError("The knowledge base must be a dictionary.")

        self.knowledge_base = knowledge_base

        # Update the conversation history to include the loaded knowledge base
        knowledge_base_context = "\n".join([f"{key}: {value}" for key, value in knowledge_base.items()])
        self.conversation_history.append(f"Assistant: Loaded knowledge base:\n{knowledge_base_context}")

    def save_state(self, file_path):
        """
        Save the agent's current state to a file.

        Args:
            file_path (str): The path to the file where the state will be saved.
        """
        state = {
            "conversation_history": self.conversation_history,
            "current_task": self.current_task,
            "knowledge_base": self.knowledge_base
        }

        with open(file_path, "wb") as f:
            pickle.dump(state, f)

    def load_state(self, file_path):
        """
        Load the agent's state from a file.

        Args:
            file_path (str): The path to the file containing the agent's state.
        """
        with open(file_path, "rb") as f:
            state = pickle.load(f)

        self.conversation_history = state["conversation_history"]
        self.current_task = state["current_task"]
        self.knowledge_base = state["knowledge_base"]

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
    def get_task_list(self):
        return self.task_list.get_tasks()
    def extract_code_from_action(self, action):
        code_pattern = re.compile(r'write code:\s*(.+)', re.IGNORECASE)
        match = code_pattern.search(action)
        if match:
            return match.group(1)
        else:
            return None