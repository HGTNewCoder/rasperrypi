import sys
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QGridLayout, 
                             QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
                             QPushButton, QSizePolicy, QMessageBox, QStackedWidget)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, QDate, QTimer


class Bell(QFrame):
    def __init__(self, bg_color, icon_file, radius="50px", callback=None):
        super().__init__()

        self.radius = radius
        self.callback = callback

        self.setStyleSheet(f"background-color: {bg_color}; border-radius: 20px; border: none;")
        self.setStyleSheet(f"QFrame {{ border: none; border-radius: {self.radius}; background-color: white; }}")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)  

        #Add Icon
        icon_display = QLabel()
        icon_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if icon_file and os.path.exists(icon_file):
            pixmap = QPixmap(icon_file)
            icon_display.setPixmap(pixmap.scaled(110, 110, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

        self.main_layout.addWidget(icon_display)

    
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
        self.main_layout.addWidget(self.bell_inner_frame)

        def handle_click(self):
            if self.callback:
                self.callback()

        def mousePressEvent(self, event):
            if self.is_bell:
                self.bell_inner_frame.setStyleSheet("background-color: #900C3F; border-radius: 20px;")
                QTimer.singleShot(200, lambda: self.bell_inner_frame.setStyleSheet(f"background-color: {self.bg_color}; border-radius: 20px;"))


class Card(QFrame):
    def __init__(self, title, description, bg_color, icon_file, callback=None):
        super().__init__()
        self.title = title 
        self.bg_color = bg_color
        self.callback = callback 
        self.radius = "50px"
        self.icon_file = icon_file

        
        # OUTER BOX STYLE
        self.setStyleSheet(f"QFrame {{ border: none; border-radius: {self.radius}; background-color: white; }}")
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0) 
        self.main_layout.setSpacing(0)  

        # --- TOP SECTION (Curved top, Flat bottom) ---
        self.top_half = QFrame()
        self.top_half.setStyleSheet(f"""
            QFrame {{ 
                background-color: {self.bg_color}; 
                border-top-left-radius: 20px; 
                border-top-right-radius: 20px; 
                border-bottom-left-radius: 0px; 
                border-bottom-right-radius: 0px; 
                border: none; 
            }}
        """)
        self.top_layout = QVBoxLayout(self.top_half)
        self.top_layout.setContentsMargins(10, 10, 10, 5)
        
        self.title_label = QLabel(self.title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.top_layout.addWidget(self.title_label)

        #Add Icon
        self.icon_display = QLabel()
        self.icon_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.icon_file and os.path.exists(self.icon_file):
            pixmap = QPixmap(self.icon_file)
            self.icon_display.setPixmap(pixmap.scaled(140, 90, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.top_layout.addWidget(self.icon_display)

        # --- BOTTOM SECTION (Flat top, Curved bottom) ---
        self.bottom_half = QFrame()
        self.bottom_half.setStyleSheet("""
            QFrame { 
                background-color: white; 
                border-top-left-radius: 0px; 
                border-top-right-radius: 0px; 
                border-bottom-left-radius: 20px; 
                border-bottom-right-radius: 20px; 
                border: none; 
            }
        """)

        #Define Bottom Layout
        self.bottom_layout = QVBoxLayout(self.bottom_half)
        self.bottom_layout.setContentsMargins(15, 0, 15, 15)
        self.bottom_layout.addStretch(1) 
        
        #Description text for each card, centered and styled
        self.desc_label = QLabel(description)
        self.desc_label.setWordWrap(True)
        self.desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.desc_label.setFont(QFont("Arial", 15, QFont.Weight.Bold))
        self.desc_label.setStyleSheet("color: #2c3e50;")

        self.bottom_layout.addWidget(self.desc_label)
        self.bottom_layout.addStretch(1)

       #Talk with us button, only visible on cards that have a callback function defined
        self.talk_with_us_btn = QPushButton("TALK WITH US")
        self.talk_with_us_btn.setFixedHeight(45)
        self.talk_with_us_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.talk_with_us_btn.clicked.connect(self.callback)
        self.talk_with_us_btn.setStyleSheet("QPushButton { background-color: #4D908E; color: white; border-radius: 12px; font-weight: bold; font-size: 14px; border: none; }")
        if not self.callback:
            self.talk_with_us_btn.hide()  

        
        self.bottom_layout.addWidget(self.talk_with_us_btn)

        self.main_layout.addWidget(self.top_half, 4)
        self.main_layout.addWidget(self.bottom_half, 6)

class WellBeingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Daily Well-Being")
        
        # Build screen instances
        self.main_menu = self.create_main_menu()
        self.response_screen = self.create_response_screen()
        
        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.main_menu)
        self.stack.addWidget(self.response_screen)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.stack)

    def create_main_menu(self):
        main_menu = QWidget()
        main_menu.setStyleSheet("background-color: #F0F8F7;")
        main_menu_layout = QVBoxLayout(main_menu)
        main_menu_layout.setContentsMargins(0, 0, 0, 20)

        # FULL WIDTH HEADER
        header_container = QFrame()
        header_container.setStyleSheet("background-color: #8FC8C2; border: none;")
        
        header = QLabel(f"MY DAILY WELL-BEING\n{QDate.currentDate().toString('dddd, MMMM d, yyyy')}")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        header.setStyleSheet("color: #2C4C49;")
        
        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(0, 20, 0, 20)
        header_layout.addWidget(header)

        main_menu_layout.addWidget(header_container)

        grid_container = QWidget()
        grid_layout = QGridLayout(grid_container)
        grid_layout.setContentsMargins(25, 10, 25, 10)
        grid_layout.setSpacing(20)

        #Convert to JSON file later
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

        for title, desc, color, img, row, column in cards:
            card = Card(title, desc, color, img, callback=self.go_to_responses)
            grid_layout.addWidget(card, row, column)

        
        bell = Bell("#F1948A", "bell.png")
        grid_layout.addWidget(bell, 2, 2, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        
        main_menu_layout.addWidget(grid_container)
        return main_menu

    def create_response_screen(self):
        response_screen = QWidget()
        response_screen.setStyleSheet("background-color: #F0F8F7;")
        
        header = QLabel("PLEASE CHOOSE YOUR ANSWER")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        header.setStyleSheet("color: #2C4C49; margin-top: 40px; margin-bottom: 40px;")
        
        card_layout = QHBoxLayout()
        card_layout.setSpacing(50)
        card_layout.setContentsMargins(100, 0, 100, 0)

        # Yes/No cards also curved
        yes_card = Card("YES", "Confirm Choice", "#D4EFDF", "yes.png", callback=lambda: self.show_confirm("YES"))
        no_card = Card("NO", "Cancel Choice", "#FADBD8", "no.png", callback=lambda: self.show_confirm("NO"))
        
        card_layout.addWidget(yes_card)
        card_layout.addWidget(no_card)

        back_btn = QPushButton("GO BACK")
        back_btn.setFixedSize(220, 60)
        back_btn.setStyleSheet("background-color: #2C4C49; color: white; border-radius: 30px; font-weight: bold; font-size: 18px;")
        back_btn.clicked.connect(self.go_to_main)

        response_screen_layout = QVBoxLayout(response_screen)
        response_screen_layout.addWidget(header)
        response_screen_layout.addLayout(card_layout)
        response_screen_layout.addStretch()
        response_screen_layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        response_screen_layout.addSpacing(40)


        return response_screen

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
