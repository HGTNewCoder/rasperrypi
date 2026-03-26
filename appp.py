import sys
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QGridLayout, 
                             QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
                             QPushButton, QSizePolicy, QMessageBox, QStackedWidget)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, QDate, QTimer

class CommBox(QFrame):
    def __init__(self, title, description, bg_color, icon_file, is_bell=False, callback=None):
        super().__init__()
        self.is_bell = is_bell
        self.title = title 
        self.original_color = bg_color
        self.callback = callback 
        
        # Consistent sizing for cards vs bell
        if is_bell:
            self.setFixedSize(160, 160) 
            radius = "20px"
        else:
            self.setMinimumWidth(260) 
            self.setMinimumHeight(320)
            radius = "20px" # BACK TO CURVED AS REQUESTED
        
        # OUTER BOX STYLE
        self.setStyleSheet(f"QFrame {{ border: none; border-radius: {radius}; background-color: white; }}")
        
        self.main_v_layout = QVBoxLayout(self)
        self.main_v_layout.setContentsMargins(0, 0, 0, 0)
        self.main_v_layout.setSpacing(0)

        if is_bell:
            self.setup_bell_ui(bg_color, icon_file)
        else:
            self.setup_standard_ui(title, description, bg_color, icon_file)

    def setup_bell_ui(self, bg_color, icon_file):
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.bell_inner_frame = QFrame()
        self.bell_inner_frame.setStyleSheet(f"background-color: {bg_color}; border-radius: 20px; border: none;")
        inner_layout = QVBoxLayout(self.bell_inner_frame)
        
        icon_display = QLabel()
        icon_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if icon_file and os.path.exists(icon_file):
            pixmap = QPixmap(icon_file)
            icon_display.setPixmap(pixmap.scaled(110, 110, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        
        inner_layout.addWidget(icon_display)
        self.main_v_layout.addWidget(self.bell_inner_frame)

    def setup_standard_ui(self, title, description, bg_color, icon_file):
        # --- TOP SECTION (Curved top, Flat bottom) ---
        top_half = QFrame()
        top_half.setStyleSheet(f"""
            QFrame {{ 
                background-color: {bg_color}; 
                border-top-left-radius: 20px; 
                border-top-right-radius: 20px; 
                border-bottom-left-radius: 0px; 
                border-bottom-right-radius: 0px; 
                border: none; 
            }}
        """)
        top_layout = QVBoxLayout(top_half)
        top_layout.setContentsMargins(10, 10, 10, 5)
        
        t_label = QLabel(title)
        t_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        t_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        top_layout.addWidget(t_label)

        icon_display = QLabel()
        icon_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if icon_file and os.path.exists(icon_file):
            pixmap = QPixmap(icon_file)
            icon_display.setPixmap(pixmap.scaled(140, 90, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        top_layout.addWidget(icon_display)

        # --- BOTTOM SECTION (Flat top, Curved bottom) ---
        bottom_half = QFrame()
        bottom_half.setStyleSheet("""
            QFrame { 
                background-color: white; 
                border-top-left-radius: 0px; 
                border-top-right-radius: 0px; 
                border-bottom-left-radius: 20px; 
                border-bottom-right-radius: 20px; 
                border: none; 
            }
        """)
        bottom_layout = QVBoxLayout(bottom_half)
        bottom_layout.setContentsMargins(15, 0, 15, 15)

        bottom_layout.addStretch(1) 
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setFont(QFont("Arial", 15, QFont.Weight.Bold))
        desc_label.setStyleSheet("color: #2c3e50;")
        bottom_layout.addWidget(desc_label)
        bottom_layout.addStretch(1) 

        self.btn = QPushButton("TALK WITH US")
        self.btn.setFixedHeight(45)
        self.btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn.clicked.connect(self.handle_click)
        
        # Button keeps a subtle curve for comfort
        self.btn.setStyleSheet("QPushButton { background-color: #4D908E; color: white; border-radius: 12px; font-weight: bold; font-size: 14px; border: none; }")
        bottom_layout.addWidget(self.btn)

        self.main_v_layout.addWidget(top_half, 4)
        self.main_v_layout.addWidget(bottom_half, 6)

    def handle_click(self):
        if self.callback:
            self.callback()

    def mousePressEvent(self, event):
        if self.is_bell:
            self.bell_inner_frame.setStyleSheet("background-color: #900C3F; border-radius: 20px;")
            QTimer.singleShot(200, lambda: self.bell_inner_frame.setStyleSheet(f"background-color: {self.original_color}; border-radius: 20px;"))

class WellBeingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Daily Well-Being")
        self.stack = QStackedWidget(self)
        
        # Build screen instances
        self.main_menu = self.create_main_menu()
        self.response_screen = self.create_response_screen()
        
        self.stack.addWidget(self.main_menu)
        self.stack.addWidget(self.response_screen)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.stack)

    def create_main_menu(self):
        page = QWidget()
        page.setStyleSheet("background-color: #F0F8F7;")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 20)

        # FULL WIDTH HEADER
        header_container = QFrame()
        header_container.setStyleSheet("background-color: #8FC8C2; border: none;")
        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(0, 20, 0, 20)
        
        header = QLabel(f"MY DAILY WELL-BEING\n{QDate.currentDate().toString('dddd, MMMM d, yyyy')}")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        header.setStyleSheet("color: #2C4C49;")
        header_layout.addWidget(header)
        layout.addWidget(header_container)

        grid_container = QWidget()
        grid_layout = QGridLayout(grid_container)
        grid_layout.setContentsMargins(25, 10, 25, 10)
        grid_layout.setSpacing(20)

        cards = [
            ("FOOD", "Request food or specify meal type.", "#AED6F1", "food.png", 0, 0),
            ("FEELING", "Describe current mood and emotion.", "#F9E79F", "feeling.png", 0, 1),
            ("EXERCISE", "Request activity or physical exercise.", "#D6EAF8", "exercise.png", 0, 2),
            ("BATHROOM", "Request bathroom assistance.", "#D1F2EB", "bathroom.png", 0, 3),
            ("YES / NO", "Confirmatory responses for staff.", "#FADBD8", "yes_no.png", 1, 0),
            ("ENTERTAINMENT", "Request leisure activity or TV.", "#D5F5E3", "entertainment.png", 1, 1),
            ("RECOMMEND ANSWER", "Suggestion from staff or system.", "#FCF3CF", "recommend.png", 1, 2),
            ("CLOCK", "Check the time or daily schedule.", "#E8DAEF", "clock.png", 1, 3),
        ]

        for title, desc, col, img, r, c in cards:
            card = CommBox(title, desc, col, img, callback=self.go_to_responses)
            grid_layout.addWidget(card, r, c)

        self.bell = CommBox("", "", "#F1948A", "bell.png", is_bell=True)
        grid_layout.addWidget(self.bell, 2, 2, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(grid_container)
        return page

    def create_response_screen(self):
        page = QWidget()
        page.setStyleSheet("background-color: #F0F8F7;")
        layout = QVBoxLayout(page)
        
        header = QLabel("PLEASE CHOOSE YOUR ANSWER")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        header.setStyleSheet("color: #2C4C49; margin-top: 40px; margin-bottom: 40px;")
        layout.addWidget(header)

        card_layout = QHBoxLayout()
        card_layout.setSpacing(50)
        card_layout.setContentsMargins(100, 0, 100, 0)

        # Yes/No cards also curved
        yes_card = CommBox("YES", "Confirm Choice", "#D4EFDF", "yes.png", callback=lambda: self.show_confirm("YES"))
        no_card = CommBox("NO", "Cancel Choice", "#FADBD8", "no.png", callback=lambda: self.show_confirm("NO"))
        
        card_layout.addWidget(yes_card)
        card_layout.addWidget(no_card)
        layout.addLayout(card_layout)

        layout.addStretch()

        back_btn = QPushButton("GO BACK")
        back_btn.setFixedSize(220, 60)
        back_btn.setStyleSheet("background-color: #2C4C49; color: white; border-radius: 30px; font-weight: bold; font-size: 18px;")
        back_btn.clicked.connect(self.go_to_main)
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(40)

        return page

    def go_to_responses(self):
        self.stack.setCurrentIndex(1)

    def go_to_main(self):
        self.stack.setCurrentIndex(0)

    def show_confirm(self, choice):
        QMessageBox.information(self, "Success", f"Response Recorded: {choice}")
        self.go_to_main()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WellBeingApp()
    window.showMaximized()
    sys.exit(app.exec())
