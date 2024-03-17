from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

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
        
    def execute_script(self, script):
        self.web_view.page().runJavaScript(script)
        
    def get_current_url(self):
        return self.web_view.url().toString()
    
    def get_page_source(self):
        def callback(html):
            self.page_source = html
        self.web_view.page().toHtml(callback)
        
    def search_text(self, text):
        self.web_view.page().findText(text)
        
    def scrape_page(self):
        self.get_page_source()
        self.execute_script("document.documentElement.outerHTML")
        return self.page_source