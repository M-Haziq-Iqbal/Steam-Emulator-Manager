import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFileDialog, QHBoxLayout, QScrollArea
from PySide6.QtGui import QGuiApplication

class PageWidget(QWidget):
    def __init__(self, index, parent=None):
        super().__init__(parent)
        self.index = index
        self.layout = QVBoxLayout(self)
        # self.setMinimumHeight(MainWindow.minimumSize)
        
        self.setLayout(self.layout)

class Page1(PageWidget):
    def __init__(self, parent=None):
        super().__init__(0, parent)
        
        # Label
        self.label = QLabel("SELECT STEAM GAME FOLDER", alignment=Qt.AlignCenter)
        self.layout.addWidget(self.label)
        
        # Scroll Area
        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(self.scroll_area)

        # Browse Button
        self.browse_button = QPushButton("Browse Folder")
        self.browse_button.clicked.connect(self.browse_folder)
        self.layout.addWidget(self.browse_button)

        self.selected_folders = []

    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.add_folder(folder_path)

    def add_folder(self, folder_path):
        folder_widget = QWidget()
        folder_layout = QHBoxLayout(folder_widget)

        folder_label = QLabel(folder_path)
        folder_layout.addWidget(folder_label)

        remove_button = QPushButton("X")
        remove_button.setFixedSize(20, 20)  # Set fixed size for the button
        remove_button.clicked.connect(lambda: self.remove_folder(folder_widget))
        folder_layout.addWidget(remove_button)

        folder_widget.setLayout(folder_layout)
        self.scroll_layout.addWidget(folder_widget)
        self.selected_folders.append(folder_widget)

    def remove_folder(self, folder_widget):
        self.scroll_layout.removeWidget(folder_widget)
        folder_widget.deleteLater()
        self.selected_folders.remove(folder_widget)

class Page2(PageWidget):
    def __init__(self, parent=None):
        super().__init__(1, parent)
        self.label = QLabel("Page 2", alignment=Qt.AlignCenter)
        self.layout.addWidget(self.label)

class Page3(PageWidget):
    def __init__(self, parent=None):
        super().__init__(2, parent)
        self.label = QLabel("Page 3", alignment=Qt.AlignCenter)
        self.layout.addWidget(self.label)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-page GUI")
        
        # Get screen resolution
        primary_screen = QGuiApplication.primaryScreen()
        screen_geometry = primary_screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        
        # Set minimum and maximum sizes based on screen resolution
        min_width = int(screen_width * 0.4)
        min_height = int(screen_height * 0.5)
        max_width = int(screen_width * 0.8)
        max_height = int(screen_height * 1.0)
        
        # size = {"min":{"width":min_width, "height":min_height}, 
        #         "max": {"width":max_width, "height":max_height}}
                
        self.setMinimumSize(min_width, min_height)
        self.setMaximumSize(max_width, max_height)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.pages = [Page1(), Page2(), Page3()]
        self.current_page_index = 0
        self.layout.addWidget(self.pages[self.current_page_index])

        self.previous_button = QPushButton("Previous")
        self.previous_button.clicked.connect(self.previous_page)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.previous_button)
        self.button_layout.addWidget(self.next_button)
        self.layout.addLayout(self.button_layout)

    def next_page(self):
        if self.current_page_index < len(self.pages) - 1:
            self.layout.removeWidget(self.pages[self.current_page_index])
            self.current_page_index += 1
            self.layout.addWidget(self.pages[self.current_page_index])

    def previous_page(self):
        if self.current_page_index > 0:
            self.layout.removeWidget(self.pages[self.current_page_index])
            self.current_page_index -= 1
            self.layout.addWidget(self.pages[self.current_page_index])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
