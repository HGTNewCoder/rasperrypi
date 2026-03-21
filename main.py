import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLabel, QFrame)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtCore import QUrl

class AACApp(QWidget):
    def __init__(self):
        super().__init__()
        self.navigation_stack = []  # Track navigation path
        self.main_cards = []  # Will be loaded from JSON
        self.card_data = {}  # Will be loaded from JSON
        self.sound_player = QMediaPlayer()  # Initialize sound player
        
        # Load card configuration from JSON
        self.load_cards_from_json()
        
        self.init_ui()

    def load_cards_from_json(self):
        """Load card configuration from cards.json file."""
        try:
            # Get the directory where main.py is located
            app_dir = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(app_dir, 'cards.json')
            
            with open(json_path, 'r') as f:
                data = json.load(f)
            
            self.main_cards = data.get('mainCards', [])
            self.card_data = data.get('categories', {})
            
            print(f"✓ Cards loaded successfully from {json_path}")
        except FileNotFoundError:
            print(f"✗ Error: cards.json not found in {app_dir}")
            print("Using default cards...")
            self._set_default_cards()
        except json.JSONDecodeError:
            print("✗ Error: cards.json is not valid JSON")
            self._set_default_cards()
    
    def _set_default_cards(self):
        """Fallback to default cards if JSON loading fails."""
        self.main_cards = ['I want...', 'Help', 'Yes', 'No', 'Food', 'Water', 'Bathroom', 'Stop']
        self.card_data = {
            'I want...': ['Food', 'Water', 'Rest', 'Play', 'Help', 'Bathroom', 'Sleep', 'Talk'],
            'Help': ['Call Mom', 'Call Dad', 'Call Doctor', 'Emergency', 'Pain', 'Tired', 'Happy', 'Sad'],
            'Yes': ['Agree', 'Good', 'Continue', 'More', 'Again', 'Yes Please', 'Okay', 'Sure'],
            'No': ['Stop', 'No Thanks', 'Wrong', 'Different', 'Not', 'Disagree', 'Later', 'Done'],
            'Food': ['Apple', 'Banana', 'Bread', 'Cheese', 'Chicken', 'Rice', 'Pasta', 'Juice'],
            'Water': ['Cold', 'Warm', 'Ice', 'Drink', 'More', 'Less', 'Now', 'Later'],
            'Bathroom': ['Toilet', 'Wash', 'Shower', 'Wet', 'Dry', 'Help', 'Done', 'Pain'],
            'Stop': ['No More', 'Wait', 'Pause', 'Reset', 'Help', 'Done', 'Tired', 'Stop Now'],
        }

    def init_ui(self):
        # Set window size for a 10-inch screen (commonly 1280x800 or 800x480)
        self.setWindowTitle('AAC Touch Interface')
        self.setGeometry(100, 100, 1024, 600)
        self.setStyleSheet("background-color: #f5f5f5;")

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        # ===== TITLE DISPLAY =====
        self.title_display = QLabel("MAIN CATEGORY")
        self.title_display.setFont(QFont('Arial', 28, QFont.Bold))
        self.title_display.setAlignment(Qt.AlignCenter)
        self.title_display.setMinimumHeight(50)
        self.title_display.setStyleSheet("color: #333333;")
        self.main_layout.addWidget(self.title_display)

        # ===== GRID CONTAINER FOR CARDS =====
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(20)  # Space between cards
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_container.setLayout(self.grid_layout)
        self.main_layout.addWidget(self.grid_container, 1)  # Give it stretch factor
        
        # ===== NAVIGATION BAR (Back Button) =====
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(10)
        
        self.back_button = QPushButton("← Back")
        self.back_button.setFont(QFont('Arial', 14, QFont.Bold))
        self.back_button.setMinimumHeight(45)
        self.back_button.setMinimumWidth(120)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #ff9800;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e68900;
            }
        """)
        self.back_button.clicked.connect(self.go_back)
        self.back_button.hide()
        nav_layout.addWidget(self.back_button)
        nav_layout.addStretch()
        
        self.main_layout.addLayout(nav_layout)
        
        # ===== PAGE INDICATORS (Bottom dots) =====
        self.indicators_container = QWidget()
        self.indicators_layout = QHBoxLayout()
        self.indicators_layout.setContentsMargins(0, 0, 0, 0)
        self.indicators_layout.setSpacing(8)
        self.indicators_layout.addStretch()
        self.indicators_container.setLayout(self.indicators_layout)
        self.main_layout.addWidget(self.indicators_container)
        
        self.setLayout(self.main_layout)
        
        # Display the main cards (loaded from JSON)
        self.display_cards(self.main_cards)

    def display_cards(self, card_titles, parent_title=None):
        """Clear the grid and display a new set of cards."""
        # Clear the existing grid
        while self.grid_layout.count():
            widget = self.grid_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()
        
        # Clear page indicators
        while self.indicators_layout.count() > 1:  # Keep the stretch factor
            widget = self.indicators_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()
        
        # Add new cards
        row = 0
        col = 0
        for title in card_titles:
            card = self.create_card(title)
            self.grid_layout.addWidget(card, row, col)
            
            col += 1
            if col > 3: # Reset to next row after 4 columns
                col = 0
                row += 1
        
        # Update title display
        if parent_title:
            self.title_display.setText(parent_title.upper())
            self.navigation_stack.append(parent_title)
            self.back_button.show()
        else:
            self.title_display.setText("MAIN CATEGORY")
            self.navigation_stack = []
            self.back_button.hide()

    def go_back(self):
        """Navigate back to the previous card set."""
        if self.navigation_stack:
            self.navigation_stack.pop()
        
        if self.navigation_stack:
            # Go back to a subcategory
            parent_title = self.navigation_stack[-1]
            self.display_cards(self.card_data[parent_title], parent_title)
        else:
            # Go back to main menu
            self.display_cards(self.main_cards)

    def create_card(self, title):
        """Builds a single card with an image placeholder and a title button."""
        card_frame = QFrame()
        card_frame.setStyleSheet("""
            QFrame { 
                border: 3px solid #d0d0d0; 
                border-radius: 12px; 
                background-color: #ffffff;
                padding: 0px;
            }
        """)
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)
        
        # Placeholder for the future image
        image_placeholder = QLabel("Image")
        image_placeholder.setAlignment(Qt.AlignCenter)
        image_placeholder.setStyleSheet("""
            QLabel {
                border: 2px dashed #b0b0b0;
                background-color: #f0f0f0;
                border-radius: 8px;
                color: #888888;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        image_placeholder.setMinimumHeight(120)
        
        # The clickable text button
        btn = QPushButton(title)
        btn.setFont(QFont('Arial', 16, QFont.Bold))
        btn.setMinimumHeight(50)
        btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                color: #333333;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #e8f5e9;
                border-radius: 5px;
            }
            QPushButton:pressed {
                background-color: #c8e6c9;
            }
        """)
        
        # Connect the button click to our logic function
        btn.clicked.connect(lambda checked, t=title: self.card_clicked(t))
        
        # Assemble the card
        card_layout.addWidget(image_placeholder, 1)
        card_layout.addWidget(btn)
        card_frame.setLayout(card_layout)
        
        return card_frame

    def card_clicked(self, title):
        """Updates the top display when a card is tapped and shows subcards if available."""
        # Play sound when card is clicked
        self.play_sound()
        
        # Check if this card has subcategories
        if title in self.card_data:
            # Display the 8 subcategory cards
            self.display_cards(self.card_data[title], title)
    
    def play_sound(self):
        """Play a sound when a card is clicked."""
        try:
            # Get the directory where main.py is located
            app_dir = os.path.dirname(os.path.abspath(__file__))
            sound_path = os.path.join(app_dir, 'assets', 'sound.mp3')
            
            # Check if the sound file exists
            if os.path.exists(sound_path):
                self.sound_player.setMedia(QUrl.fromLocalFile(sound_path))
                self.sound_player.play()
            else:
                # Optional: Print debug message
                print(f"Sound file not found: {sound_path}")
        except Exception as e:
            print(f"Error playing sound: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AACApp()
    window.show()
    sys.exit(app.exec_())