from agents.base_agent import BaseAgent
from utils.openai_api import OpenAIAPI
import re

class OpenAIAgent(BaseAgent):
    def __init__(self, browser, terminal, task_list, code_editor):
        super().__init__()
        self.browser = browser
        self.terminal = terminal
        self.task_list = task_list
        self.code_editor = code_editor
        self.action_handlers = {
            "clear": self.action_clear,
            "exit": self.action_exit,
            "open website": self.action_open_website,
            "run command": self.action_run_command,
            "add task": self.action_add_task,
            "write code": self.action_write_code,
            "check browser": self.action_check_browser
        }

    def process_input(self, user_input):
        action_detected = False
        for action in ["clear", "exit", "open website", "research", "look up", "run command", "add task", "write code", "check browser"]:
            if action in user_input.lower():
                self.execute_action(user_input)
                action_detected = True
                break
        if action_detected:
            return
        self.conversation_history.append(f"User: {user_input}")
        if user_input.lower().startswith("task:"):
            self.current_task = user_input[5:].strip()
            self.conversation_history.append(f"Assistant: Understood. The current task is: {self.current_task}. I'll break it into smaller manageable tasks for myself. When I do the tasks I'll do 1 task per response.")
        else:
            context = f"Current Task: {self.current_task}\n\n" if self.current_task else ""
            if self.knowledge_base:
                knowledge_base_context = "\n".join([f"{key}: {value}" for key, value in self.knowledge_base.items()])
                context += f"Knowledge Base:\n{knowledge_base_context}\n\n"
            task_list_context = "\n".join([f"Task {i+1}: {task}" for i, task in enumerate(self.get_task_list())])
            context += f"Task List:\n{task_list_context}\n\n"
            context += "\n".join(self.conversation_history[-5:])
            response = self.api.api_calls(user_input, context)
            self.conversation_history.append(f"Assistant: {response}")

    def generate_response(self):
        if self.conversation_history:
            return self.conversation_history[-1][11:]
        else:
            return "I'm ready to assist you. Please provide me with a task or query."

    def execute_action(self, action):
        for keyword, handler in self.action_handlers.items():
            if keyword in action:
                handler(action)
                return
        print("No valid action found for:", action)

    def action_clear(self, action):
        self.conversation_history = []
        self.current_task = None
        print("Conversation history and current task cleared.")

    def action_exit(self, action):
        print("Exiting the program...")
        exit()

    def action_open_website(self, action):
        url = self.extract_url_from_action(action)
        if url:
            self.browser.navigate_to(url)
            print("Navigated to URL:", url)
        else:
            print("No valid URL found in action:", action)

    def action_run_command(self, action):
        command = self.extract_command_from_action(action)
        if command:
            self.terminal.execute_command(command)
            print("Executed command:", command)
        else:
            print("No valid command found in action:", action)

    def action_add_task(self, action):
        task = self.extract_task_from_action(action)
        if task:
            self.task_list.add_task(task)
            
            print("Added task:", task)
        else:
            print("No valid task found in action:", action)

    def action_write_code(self, action):
        code = self.extract_code_from_action(action)
        if code:
            self.code_editor.set_code(code)
            print("Code written to editor.")
        else:
            print("No valid code found in action:", action)

    def action_check_browser(self, action):
        current_url = self.browser.get_current_url()
        page_source = self.browser.scrape_page()
        print("Current URL:", current_url)
        print("Page source length:", len(page_source))

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
