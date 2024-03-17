from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QEventLoop

class Browser(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        self.address_bar = QLineEdit()
        self.address_bar.returnPressed.connect(self.load_url)
        self.layout.addWidget(self.address_bar)
        
        self.web_view = QWebEngineView()
        self.layout.addWidget(self.web_view)
        
        self.web_view.load(QUrl("https://www.google.com"))
        
    def load_url(self):
        url = QUrl(self.address_bar.text())
        if url.scheme() == "":
            url.setScheme("http")
        self.web_view.load(url)
        
    def navigate_to(self, url):
        self.address_bar.setText(url)
        self.load_url()
        self.wait_for_page_load()
        
    def execute_script(self, script):
        self.web_view.page().runJavaScript(script)
        
    def get_current_url(self):
        return self.web_view.url().toString()
    
    def get_page_source(self):
        loop = QEventLoop()
        self.web_view.page().toHtml(lambda html: (setattr(self, 'page_source', html), loop.quit()))
        loop.exec_()
        return self.page_source
    
    def search_text(self, text):
        self.web_view.page().findText(text)
        
    def scrape_page(self):
        return self.get_page_source()
    
    def wait_for_page_load(self, timeout=10000):
        loop = QEventLoop()
        self.web_view.loadFinished.connect(loop.quit)
        loop.exec_()
        
    def log_message(self, message):
        print(f"Browser: {message}")
        
    def handle_error(self, error_message):
        self.log_message(f"Error: {error_message}")