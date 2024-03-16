from abc import ABC, abstractmethod

class BaseAgent(ABC):
    @abstractmethod
    def process_input(self, user_input):
        """
        Process the user input and update the agent's internal state.

        Args:
            user_input (str): The user input string.
        """
        raise NotImplementedError("Subclasses must implement the process_input method.")

    @abstractmethod
    def generate_response(self):
        """
        Generate a response based on the agent's current state.

        Returns:
            str: The generated response.
        """
        raise NotImplementedError("Subclasses must implement the generate_response method.")

    @abstractmethod
    def execute_action(self, action):
        """
        Execute an action based on the generated response.

        Args:
            action (str): The action to be executed.
        """
        raise NotImplementedError("Subclasses must implement the execute_action method.")

    def reset(self):
        """
        Reset the agent's internal state to its initial values.
        """
        pass

    def load_knowledge_base(self, knowledge_base):
        """
        Load a knowledge base into the agent's memory.

        Args:
            knowledge_base (dict): The knowledge base dictionary.
        """
        pass

    def train(self, training_data):
        """
        Train the agent using the provided training data.

        Args:
            training_data (list): A list of training examples.
        """
        pass

    def evaluate(self, evaluation_data):
        """
        Evaluate the agent's performance using the provided evaluation data.

        Args:
            evaluation_data (list): A list of evaluation examples.

        Returns:
            float: The evaluation score.
        """
        pass

    def save_state(self, file_path):
        """
        Save the agent's current state to a file.

        Args:
            file_path (str): The path to the file where the state will be saved.
        """
        pass

    def load_state(self, file_path):
        """
        Load the agent's state from a file.

        Args:
            file_path (str): The path to the file containing the agent's state.
        """
        pass