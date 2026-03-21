import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, 
                             QPushButton, QLabel, QLineEdit, QMessageBox, QSplitter, QInputDialog, QDialog, 
                             QFormLayout, QSpinBox)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

class CardManagerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.cards_file = os.path.join(os.path.dirname(__file__), 'cards.json')
        self.card_data = {}
        self.main_cards = []
        self.current_category = None
        
        # Load cards
        self.load_cards()
        
        self.init_ui()
    
    def load_cards(self):
        """Load cards from JSON file."""
        try:
            with open(self.cards_file, 'r') as f:
                data = json.load(f)
            self.main_cards = data.get('mainCards', [])
            self.card_data = data.get('categories', {})
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load cards: {e}")
    
    def save_cards(self):
        """Save cards to JSON file."""
        try:
            data = {
                'mainCards': self.main_cards,
                'categories': self.card_data
            }
            with open(self.cards_file, 'w') as f:
                json.dump(data, f, indent=2)
            QMessageBox.information(self, "Success", "Cards saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save cards: {e}")
    
    def init_ui(self):
        """Initialize the UI."""
        self.setWindowTitle('Card Manager - Edit cards.json')
        self.setGeometry(100, 100, 1200, 700)
        self.setStyleSheet("background-color: #f5f5f5;")
        
        main_layout = QVBoxLayout()
        
        # ===== TITLE =====
        title = QLabel("Card Manager")
        title.setFont(QFont('Arial', 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # ===== MAIN CONTENT (Splitter) =====
        splitter = QSplitter(Qt.Horizontal)
        
        # --- LEFT PANEL: Main Categories ---
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        left_layout.addWidget(QLabel("MAIN CATEGORIES:"))
        self.main_list = QListWidget()
        self.main_list.itemClicked.connect(self.on_main_category_selected)
        left_layout.addWidget(self.main_list)
        
        # Main category buttons
        main_btn_layout = QHBoxLayout()
        add_main_btn = QPushButton("+ Add")
        add_main_btn.clicked.connect(self.add_main_category)
        remove_main_btn = QPushButton("- Remove")
        remove_main_btn.clicked.connect(self.remove_main_category)
        rename_main_btn = QPushButton("✎ Rename")
        rename_main_btn.clicked.connect(self.rename_main_category)
        main_btn_layout.addWidget(add_main_btn)
        main_btn_layout.addWidget(remove_main_btn)
        main_btn_layout.addWidget(rename_main_btn)
        left_layout.addLayout(main_btn_layout)
        
        left_panel.setLayout(left_layout)
        splitter.addWidget(left_panel)
        splitter.setStretchFactor(0, 1)
        
        # --- RIGHT PANEL: Subcategories ---
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        self.category_label = QLabel("Select a category")
        self.category_label.setFont(QFont('Arial', 14, QFont.Bold))
        right_layout.addWidget(self.category_label)
        
        right_layout.addWidget(QLabel("SUBCATEGORIES:"))
        self.sub_list = QListWidget()
        right_layout.addWidget(self.sub_list)
        
        # Subcategory buttons
        sub_btn_layout = QHBoxLayout()
        add_sub_btn = QPushButton("+ Add Subcard")
        add_sub_btn.clicked.connect(self.add_subcard)
        remove_sub_btn = QPushButton("- Remove Subcard")
        remove_sub_btn.clicked.connect(self.remove_subcard)
        edit_sub_btn = QPushButton("✎ Edit Subcard")
        edit_sub_btn.clicked.connect(self.edit_subcard)
        sub_btn_layout.addWidget(add_sub_btn)
        sub_btn_layout.addWidget(remove_sub_btn)
        sub_btn_layout.addWidget(edit_sub_btn)
        right_layout.addLayout(sub_btn_layout)
        
        right_panel.setLayout(right_layout)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(splitter)
        
        # ===== BOTTOM BUTTONS =====
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        
        save_btn = QPushButton("💾 Save Changes")
        save_btn.setFont(QFont('Arial', 12, QFont.Bold))
        save_btn.setMinimumWidth(150)
        save_btn.setMinimumHeight(40)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        save_btn.clicked.connect(self.save_cards)
        bottom_layout.addWidget(save_btn)
        
        reload_btn = QPushButton("🔄 Reload")
        reload_btn.setFont(QFont('Arial', 12, QFont.Bold))
        reload_btn.setMinimumWidth(150)
        reload_btn.setMinimumHeight(40)
        reload_btn.clicked.connect(self.reload_ui)
        bottom_layout.addWidget(reload_btn)
        
        main_layout.addLayout(bottom_layout)
        
        self.setLayout(main_layout)
        
        # Load initial data
        self.reload_ui()
    
    def reload_ui(self):
        """Reload the UI from current data."""
        self.load_cards()
        self.main_list.clear()
        self.sub_list.clear()
        self.category_label.setText("Select a category")
        
        for card in self.main_cards:
            self.main_list.addItem(card)
    
    def on_main_category_selected(self, item):
        """Handle main category selection."""
        self.current_category = item.text()
        self.category_label.setText(f"{self.current_category.upper()}")
        self.sub_list.clear()
        
        if self.current_category in self.card_data:
            for subcard in self.card_data[self.current_category]:
                self.sub_list.addItem(subcard)
    
    def add_main_category(self):
        """Add a new main category."""
        name, ok = QInputDialog.getText(self, "Add Category", "Enter category name:")
        if ok and name:
            if name in self.main_cards:
                QMessageBox.warning(self, "Warning", "This category already exists!")
                return
            self.main_cards.append(name)
            self.card_data[name] = []
            self.main_list.addItem(name)
    
    def remove_main_category(self):
        """Remove a main category."""
        if not self.current_category:
            QMessageBox.warning(self, "Warning", "Please select a category first!")
            return
        
        reply = QMessageBox.question(self, "Confirm", 
                                     f"Delete '{self.current_category}' and all its subcards?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.main_cards.remove(self.current_category)
            del self.card_data[self.current_category]
            self.current_category = None
            self.reload_ui()
    
    def rename_main_category(self):
        """Rename a main category."""
        if not self.current_category:
            QMessageBox.warning(self, "Warning", "Please select a category first!")
            return
        
        new_name, ok = QInputDialog.getText(self, "Rename Category", 
                                           "Enter new category name:", text=self.current_category)
        if ok and new_name and new_name != self.current_category:
            if new_name in self.main_cards:
                QMessageBox.warning(self, "Warning", "A category with this name already exists!")
                return
            
            # Update main_cards list
            index = self.main_cards.index(self.current_category)
            self.main_cards[index] = new_name
            
            # Update card_data dictionary
            self.card_data[new_name] = self.card_data.pop(self.current_category)
            
            # Update current category
            self.current_category = new_name
            
            # Refresh UI
            self.reload_ui()
            
            # Re-select the renamed category
            for i in range(self.main_list.count()):
                if self.main_list.item(i).text() == new_name:
                    self.main_list.setCurrentRow(i)
                    break
    
    def add_subcard(self):
        """Add a subcard to the selected category."""
        if not self.current_category:
            QMessageBox.warning(self, "Warning", "Please select a category first!")
            return
        
        name, ok = QInputDialog.getText(self, "Add Subcard", "Enter subcard name:")
        if ok and name:
            if name in self.card_data[self.current_category]:
                QMessageBox.warning(self, "Warning", "This subcard already exists in this category!")
                return
            self.card_data[self.current_category].append(name)
            self.sub_list.addItem(name)
    
    def remove_subcard(self):
        """Remove a subcard."""
        if not self.current_category:
            QMessageBox.warning(self, "Warning", "Please select a category first!")
            return
        
        current_item = self.sub_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select a subcard to remove!")
            return
        
        subcard_name = current_item.text()
        reply = QMessageBox.question(self, "Confirm", f"Delete '{subcard_name}'?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.card_data[self.current_category].remove(subcard_name)
            self.sub_list.takeItem(self.sub_list.row(current_item))
    
    def edit_subcard(self):
        """Edit a subcard name."""
        if not self.current_category:
            QMessageBox.warning(self, "Warning", "Please select a category first!")
            return
        
        current_item = self.sub_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select a subcard to edit!")
            return
        
        old_name = current_item.text()
        new_name, ok = QInputDialog.getText(self, "Edit Subcard", 
                                           "Enter new name:", text=old_name)
        if ok and new_name and new_name != old_name:
            index = self.card_data[self.current_category].index(old_name)
            self.card_data[self.current_category][index] = new_name
            current_item.setText(new_name)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CardManagerApp()
    window.show()
    sys.exit(app.exec_())
