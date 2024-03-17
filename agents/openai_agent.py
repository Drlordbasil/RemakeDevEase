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
            "check browser": self.action_check_browser,
            "navigate": self.action_navigate,
            "search": self.action_search,
            "scrape": self.action_scrape
        }

    def process_input(self, user_input):
        self.conversation_history.append(f"User: {user_input}")
        if user_input.lower().startswith("task:"):
            self.current_task = user_input[5:].strip()
            self.conversation_history.append(f"Assistant: Understood. The current task is: {self.current_task}. I'll break it into smaller manageable tasks for myself. When I do the tasks I'll do 1 task per response.")
            subtasks = self.generate_subtasks(self.current_task)
            for subtask in subtasks:
                self.task_list.add_task(subtask)
            print(f"Generated subtasks: {subtasks}")
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
            self.execute_action(response)
            print(f"Generated response: {response}")

    def generate_response(self):
        if self.task_list.get_tasks():
            next_task = self.task_list.get_tasks()[0]
            response = self.generate_task_response(next_task)
            self.execute_action(response)
            self.task_list.remove_task(next_task)
            print(f"Completed task: {next_task}")
            print(f"Generated response: {response}")
            return response
        else:
            return "All tasks completed. Waiting for new tasks or queries."

    def execute_action(self, action):
        for keyword, handler in self.action_handlers.items():
            if keyword in action.lower():
                handler(action)
                return
        print(f"No valid action found for: {action}")

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
            print(f"Navigated to URL: {url}")
        else:
            print(f"No valid URL found in action: {action}")

    def action_navigate(self, action):
        url = self.extract_url_from_action(action)
        if url:
            self.browser.navigate_to(url)
            print(f"Navigated to URL: {url}")
        else:
            print(f"No valid URL found in action: {action}")

    def action_search(self, action):
        query = self.extract_search_query_from_action(action)
        if query:
            search_url = f"https://www.google.com/search?q={query}"
            self.browser.navigate_to(search_url)
            print(f"Performed web search for: {query}")
        else:
            print(f"No valid search query found in action: {action}")

    def action_scrape(self, action):
        current_url = self.browser.get_current_url()
        page_source = self.browser.scrape_page()
        self.knowledge_base[current_url] = page_source
        print(f"Scraped page source from: {current_url}")
        print(f"Page source length: {len(page_source)}")

    def action_run_command(self, action):
        command = self.extract_command_from_action(action)
        if command:
            self.terminal.execute_command(command)
            print(f"Executed command: {command}")
        else:
            print(f"No valid command found in action: {action}")

    def action_add_task(self, action):
        task = self.extract_task_from_action(action)
        if task:
            self.task_list.add_task(task)
            self.conversation_history.append(f"Assistant: Added task: {task}")
            print(f"Added task: {task}")
        else:
            print(f"No valid task found in action: {action}")

    def action_write_code(self, action):
        code = self.extract_code_from_action(action)
        if code:
            self.code_editor.set_code(code)
            print("Code written to editor.")
        else:
            print(f"No valid code found in action: {action}")

    def action_check_browser(self, action):
        current_url = self.browser.get_current_url()
        page_source = self.browser.scrape_page()
        print(f"Current URL: {current_url}")
        print(f"Page source length: {len(page_source)}")

    def remove_task(self, task_text):
        self.task_list.remove_task(task_text)
        self.conversation_history.append(f"Assistant: Removed task: {task_text}")
        print(f"Removed task: {task_text}")

    def research(self, topic):
        search_query = f"{topic}"
        self.browser.navigate_to(f"https://www.google.com/search?q={search_query}")
        self.conversation_history.append(f"Assistant: Researching '{topic}' on the web.")
        print(f"Researching '{topic}' on the web.")

    def interact_with_terminal(self, command):
        self.terminal.execute_command(command)
        self.conversation_history.append(f"Assistant: Executed command: {command}")
        print(f"Executed command: {command}")

    def create_file(self, filename, content):
        self.code_editor.set_code(content)
        self.code_editor.save_file(filename)
        self.conversation_history.append(f"Assistant: Created file '{filename}'.")
        print(f"Created file '{filename}'.")

    def edit_file(self, filename, content):
        self.code_editor.open_file(filename)
        self.code_editor.set_code(content)
        self.code_editor.save_file(filename)
        self.conversation_history.append(f"Assistant: Edited file '{filename}'.")
        print(f"Edited file '{filename}'.")

    def open_file(self, filename):
        self.code_editor.open_file(filename)
        self.conversation_history.append(f"Assistant: Opened file '{filename}'.")
        print(f"Opened file '{filename}'.")

    def generate_subtasks(self, task):
        prompt = f"Break down the following task into smaller subtasks: {task}"
        response = self.api.api_calls(prompt, "")
        subtasks = response.split("\n")
        return [subtask.strip() for subtask in subtasks if subtask.strip()]

    def generate_task_response(self, task):
        prompt = f"Perform the following task: {task}"
        return self.api.api_calls(prompt, "")

    def extract_url_from_action(self, action):
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        urls = url_pattern.findall(action)
        if urls:
            return urls[0]
        else:
            return None

    def extract_search_query_from_action(self, action):
        query_pattern = re.compile(r'search:\s*(.+)', re.IGNORECASE)
        match = query_pattern.search(action)
        if match:
            return match.group(1)
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