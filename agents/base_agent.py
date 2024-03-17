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
        self.knowledge_base = {}
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
        pass

    @abstractmethod
    def generate_response(self):
        """
        Generate a response based on the agent's current state.

        Returns:
            str: The generated response.
        """
        pass

    @abstractmethod
    def execute_action(self, action):
        """
        Execute an action based on the generated response.

        Args:
            action (str): The action to be executed.
        """
        pass

    def reset(self):
        """
        Reset the agent's internal state to its initial values.
        """
        self.conversation_history = []
        self.current_task = None
        self.knowledge_base = {}
        print("Agent's internal state has been reset.")

    def load_knowledge_base(self, knowledge_base):
        """
        Load a knowledge base into the agent's memory.

        Args:
            knowledge_base (dict): The knowledge base dictionary.
        """
        if not isinstance(knowledge_base, dict):
            raise ValueError("The knowledge base must be a dictionary.")

        self.knowledge_base = knowledge_base

        knowledge_base_context = "\n".join([f"{key}: {value}" for key, value in knowledge_base.items()])
        self.conversation_history.append(f"Assistant: Loaded knowledge base:\n{knowledge_base_context}")
        print(f"Loaded knowledge base:\n{knowledge_base_context}")

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
        print(f"Agent's state saved to {file_path}")

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
        print(f"Agent's state loaded from {file_path}")

    def get_task_list(self):
        tasks = self.task_list.get_tasks()
        print(f"Current task list: {tasks}")
        return tasks

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