import sys
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QGridLayout, 
                             QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
                             QPushButton, QMessageBox, QStackedWidget, QTimeEdit)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, QDate, QTimer, QTime, QUrl
from PyQt6.QtMultimedia import QSoundEffect

class CommBox(QFrame):
    def __init__(self, title, description, bg_color, icon_file, is_bell=False, callback=None):
        super().__init__()
        self.is_bell = is_bell
        self.title = title 
        self.original_color = bg_color
        self.callback = callback 
        self.setFrameShape(QFrame.Shape.NoFrame)
        
        if is_bell:
            self.setFixedSize(160, 160) 
        else:
            self.setMinimumWidth(260) 
            self.setMinimumHeight(320)
        
        self.setStyleSheet("QFrame { border: none; border-radius: 20px; background-color: white; }")
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
        self.bell_inner_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.bell_inner_frame.setStyleSheet(f"background-color: {bg_color}; border-radius: 20px; border: none;")
        inner_layout = QVBoxLayout(self.bell_inner_frame)
        icon_display = QLabel()
        icon_display.setFrameShape(QFrame.Shape.NoFrame)
        icon_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if icon_file and os.path.exists(icon_file):
            pixmap = QPixmap(icon_file)
            icon_display.setPixmap(pixmap.scaled(110, 110, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        inner_layout.addWidget(icon_display)
        self.main_v_layout.addWidget(self.bell_inner_frame)

    def setup_standard_ui(self, title, description, bg_color, icon_file):
        top_half = QFrame()
        top_half.setFrameShape(QFrame.Shape.NoFrame)
        top_half.setStyleSheet(f"background-color: {bg_color}; border-top-left-radius: 20px; border-top-right-radius: 20px; border: none;")
        top_layout = QVBoxLayout(top_half)
        t_label = QLabel(title)
        t_label.setFrameShape(QFrame.Shape.NoFrame)
        t_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        t_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        top_layout.addWidget(t_label)
        
        icon_display = QLabel()
        icon_display.setFrameShape(QFrame.Shape.NoFrame)
        icon_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if icon_file and os.path.exists(icon_file):
            pixmap = QPixmap(icon_file)
            icon_display.setPixmap(pixmap.scaled(140, 90, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        top_layout.addWidget(icon_display)

        bottom_half = QFrame()
        bottom_half.setFrameShape(QFrame.Shape.NoFrame)
        bottom_half.setStyleSheet("background-color: white; border-bottom-left-radius: 20px; border-bottom-right-radius: 20px; border: none;")
        bottom_layout = QVBoxLayout(bottom_half)
        bottom_layout.addStretch(1) 
        desc_label = QLabel(description)
        desc_label.setFrameShape(QFrame.Shape.NoFrame)
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setFont(QFont("Arial", 15, QFont.Weight.Bold))
        bottom_layout.addWidget(desc_label)
        bottom_layout.addStretch(1) 

        self.btn = QPushButton("TALK WITH US")
        self.btn.setFixedHeight(45)
        self.btn.setStyleSheet("QPushButton { background-color: #4D908E; color: white; border-radius: 12px; font-weight: bold; border: none; }")
        self.btn.clicked.connect(self.handle_click)
        bottom_layout.addWidget(self.btn)
        
        self.main_v_layout.addWidget(top_half, 4)
        self.main_v_layout.addWidget(bottom_half, 6)

    def handle_click(self):
        if self.callback: self.callback(self.title)

    def mousePressEvent(self, event):
        if self.is_bell:
            self.bell_inner_frame.setStyleSheet("background-color: #900C3F; border-radius: 20px; border: none;")
            QTimer.singleShot(200, lambda: self.bell_inner_frame.setStyleSheet(f"background-color: {self.original_color}; border-radius: 20px; border: none;"))
            if self.callback: self.callback("BELL")


class WellBeingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Daily Well-Being")
        self.active_alarm_time = None
        self.timer_seconds_remaining = 0
        
        self.sound_effect = QSoundEffect()
        self.sound_effect.setLoopCount(-2)
        if os.path.exists("alarm.wav"):
            self.sound_effect.setSource(QUrl.fromLocalFile(os.path.abspath("alarm.wav")))
        
        self.core_timer = QTimer(self)
        self.core_timer.timeout.connect(self.process_time_events)
        self.core_timer.start(1000)

        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.create_main_menu())
        self.stack.addWidget(self.create_response_page())
        self.stack.addWidget(self.create_clock_page())
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stack)

    def create_main_menu(self):
        page = QWidget()
        page.setStyleSheet("background-color: #F0F8F7;")
        layout = QVBoxLayout(page)
        
        header_container = QFrame()
        header_container.setFrameShape(QFrame.Shape.NoFrame)
        header_container.setStyleSheet("background-color: #8FC8C2; border: none;")
        header_layout = QVBoxLayout(header_container)
        
        header = QLabel(f"MY DAILY WELL-BEING\n{QDate.currentDate().toString('dddd, MMMM d, yyyy')}")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        header.setStyleSheet("color: #2C4C49; border: none;")
        
        self.timer_status = QLabel("")
        self.timer_status.setFrameShape(QFrame.Shape.NoFrame)
        self.timer_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_status.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        
        header_layout.addWidget(header)
        header_layout.addWidget(self.timer_status)
        layout.addWidget(header_container)

        grid = QGridLayout()
        grid.setContentsMargins(25, 10, 25, 10)
        grid.setSpacing(20)
        
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
            card = CommBox(title, desc, col, img, callback=self.navigate)
            grid.addWidget(card, r, c)
            
        self.bell = CommBox("", "", "#F1948A", "bell.png", is_bell=True, callback=self.navigate)
        grid.addWidget(self.bell, 2, 0, 1, 4, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addLayout(grid)
        return page

    def create_response_page(self):
        page = QWidget()
        page.setStyleSheet("background-color: white;")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 20, 40, 20)
        layout.setSpacing(20)

        title_lbl = QLabel("CHOOSE ANSWER")
        title_lbl.setFrameShape(QFrame.Shape.NoFrame)
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_lbl.setFont(QFont("Arial", 38, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #2C4C49; border: none;")
        layout.addWidget(title_lbl)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(40)

        yes_card = self.create_styled_response_card(
            title="YES", bg_color="#D5F5E3", icon="yes.png",
            btn_text="CONFIRM CHOICE", btn_color="#4D908E",
            text_color="#2C4C49", btn_text_color="white",
            callback=lambda: self.finish("YES")
        )

        no_card = self.create_styled_response_card(
            title="NO", bg_color="#FADBD8", icon="no.png",
            btn_text="CANCEL CHOICE", btn_color="#FF4C4C",
            text_color="#FF0000", btn_text_color="white",
            callback=lambda: self.finish("NO")
        )

        cards_layout.addWidget(yes_card)
        cards_layout.addWidget(no_card)
        layout.addLayout(cards_layout)

        back_btn = QPushButton("Go Back")
        back_btn.setFixedSize(150, 50)
        back_btn.setStyleSheet("background-color: #BDBDBD; color: white; border-radius: 10px; font-weight: bold; font-size: 16px; border: none;")
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        return page

    def create_styled_response_card(self, title, bg_color, icon, btn_text, btn_color, text_color, btn_text_color, callback):
        card = QFrame()
        card.setFrameShape(QFrame.Shape.NoFrame)
        card.setStyleSheet(f"QFrame {{ background-color: {bg_color}; border-radius: 40px; border: none; }} QLabel {{ border: none; background: transparent; }}")
        
        v_layout = QVBoxLayout(card)
        v_layout.setContentsMargins(20, 10, 20, 20) 
        v_layout.setSpacing(5)

        icon_lbl = QLabel()
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if os.path.exists(icon):
            pix = QPixmap(icon).scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            icon_lbl.setPixmap(pix)
        v_layout.addWidget(icon_lbl)

        t_lbl = QLabel(title)
        t_lbl.setFont(QFont("Arial", 75, QFont.Weight.Bold))
        t_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        t_lbl.setStyleSheet(f"color: {text_color}; border: none;")
        v_layout.addWidget(t_lbl)
        
        v_layout.addStretch()

        btn = QPushButton(btn_text)
        btn.setFixedHeight(80)
        btn.setStyleSheet(f"QPushButton {{ background-color: {btn_color}; color: {btn_text_color}; border-radius: 25px; font-size: 24px; font-weight: bold; border: none; }}")
        btn.clicked.connect(callback)
        v_layout.addWidget(btn)

        return card

    def create_clock_page(self):
        page = QWidget()
        page.setStyleSheet("background-color: #F0F8F7;")
        main_v = QVBoxLayout(page)
        main_v.setContentsMargins(0, 0, 0, 0)
        
        top_bar = QFrame()
        top_bar.setFixedHeight(120)
        top_bar.setStyleSheet("background-color: #8FC8C2; border: none;")
        top_layout = QHBoxLayout(top_bar)
        
        clock_title = QLabel("CLOCK SETTINGS")
        clock_title.setFont(QFont("Arial", 32, QFont.Weight.Bold)) 
        clock_title.setStyleSheet("color: white; border: none;")
        top_layout.addWidget(clock_title, alignment=Qt.AlignmentFlag.AlignCenter)
        main_v.addWidget(top_bar)
        
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(100, 20, 100, 20)
        content_layout.setSpacing(20)
        
        mode_box = QHBoxLayout()
        self.btn_alarm_mode = QPushButton("ALARM")
        self.btn_timer_mode = QPushButton("TIMER")
        
        for b in [self.btn_alarm_mode, self.btn_timer_mode]:
            b.setFixedSize(300, 80)
            b.setCheckable(True)
            b.setStyleSheet("QPushButton { background-color: #D1E8E5; border-radius: 40px; font-weight: bold; font-size: 26px; color: #2C4C49; border: none; } QPushButton:checked { background-color: #2C4C49; color: white; }")
            
        self.btn_alarm_mode.setChecked(True)
        self.btn_alarm_mode.clicked.connect(lambda: self.switch_clock_mode("ALARM"))
        self.btn_timer_mode.clicked.connect(lambda: self.switch_clock_mode("TIMER"))
        mode_box.addWidget(self.btn_alarm_mode)
        mode_box.addWidget(self.btn_timer_mode)
        content_layout.addLayout(mode_box)
        
        center_card = QFrame()
        center_card.setStyleSheet("background-color: white; border-radius: 40px; border: none;")
        card_layout = QVBoxLayout(center_card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        
        spinner_hbox = QHBoxLayout()
        hr_vbox = QVBoxLayout()
        self.hr_up = QPushButton("▲")
        self.hr_down = QPushButton("▼")
        for btn in [self.hr_up, self.hr_down]: 
            btn.setFixedSize(80, 80)
            btn.setStyleSheet("font-size: 40px; color: #8FC8C2; background: transparent; border: 3px solid #8FC8C2; border-radius: 40px;")
        
        self.hr_up.clicked.connect(lambda: self.spin_time(h=1))
        self.hr_down.clicked.connect(lambda: self.spin_time(h=-1))
        hr_vbox.addWidget(self.hr_up)
        hr_vbox.addWidget(self.hr_down)
        
        self.time_spinner = QTimeEdit()
        self.time_spinner.setDisplayFormat("HH:mm")
        self.time_spinner.setFixedSize(450, 200)
        self.time_spinner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_spinner.setStyleSheet("QTimeEdit { background-color: #F9F9F9; border: 3px solid #8FC8C2; border-radius: 30px; font-size: 130px; font-weight: bold; color: #2C4C49; } QTimeEdit::up-button, QTimeEdit::down-button { width: 0px; }")
        
        min_vbox = QVBoxLayout()
        self.min_up = QPushButton("▲")
        self.min_down = QPushButton("▼")
        for btn in [self.min_up, self.min_down]: 
            btn.setFixedSize(80, 80)
            btn.setStyleSheet("font-size: 40px; color: #8FC8C2; background: transparent; border: 3px solid #8FC8C2; border-radius: 40px;")
            
        self.min_up.clicked.connect(lambda: self.spin_time(m=1))
        self.min_down.clicked.connect(lambda: self.spin_time(m=-1))
        min_vbox.addWidget(self.min_up)
        min_vbox.addWidget(self.min_down)
        
        spinner_hbox.addLayout(hr_vbox)
        spinner_hbox.addWidget(self.time_spinner)
        spinner_hbox.addLayout(min_vbox)
        card_layout.addLayout(spinner_hbox)
        
        # --- BIGGER COMMENT/INSTRUCTION ---
        self.mode_label = QLabel("Tap arrows to set alarm")
        self.mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mode_label.setFont(QFont("Arial", 32, QFont.Weight.Bold)) 
        self.mode_label.setStyleSheet("border: none; color: #444444;") 
        card_layout.addWidget(self.mode_label)
        
        content_layout.addWidget(center_card)
        
        act_layout = QHBoxLayout()
        self.start_btn = QPushButton("SET ALARM")
        self.start_btn.setFixedSize(350, 100)
        self.start_btn.setStyleSheet("background-color: #4D908E; color: white; border-radius: 50px; font-weight: bold; font-size: 30px; border: none;")
        self.start_btn.clicked.connect(self.set_clock_action)
        
        back_btn = QPushButton("CANCEL")
        back_btn.setFixedSize(350, 100)
        back_btn.setStyleSheet("background-color: #BDBDBD; color: white; border-radius: 50px; font-weight: bold; font-size: 30px; border: none;")
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        
        act_layout.addWidget(back_btn)
        act_layout.addWidget(self.start_btn)
        content_layout.addLayout(act_layout)
        
        main_v.addLayout(content_layout)
        return page

    def spin_time(self, h=0, m=0):
        current = self.time_spinner.time()
        self.time_spinner.setTime(current.addSecs((h * 3600) + (m * 60)))

    def switch_clock_mode(self, mode):
        if mode == "ALARM":
            self.btn_timer_mode.setChecked(False)
            self.start_btn.setText("SET ALARM")
            self.mode_label.setText("Tap arrows to set alarm")
            self.time_spinner.setTime(QTime.currentTime())
        else:
            self.btn_alarm_mode.setChecked(False)
            self.start_btn.setText("START TIMER")
            self.mode_label.setText("Tap arrows to set duration")
            self.time_spinner.setTime(QTime(0, 0))

    def set_clock_action(self):
        t = self.time_spinner.time()
        if self.btn_alarm_mode.isChecked():
            self.active_alarm_time = t.toString("HH:mm")
        else:
            self.timer_seconds_remaining = (t.hour() * 3600) + (t.minute() * 60)
        self.stack.setCurrentIndex(0)

    def process_time_events(self):
        now_str = QTime.currentTime().toString("HH:mm")
        if self.active_alarm_time and now_str == self.active_alarm_time:
            self.active_alarm_time = None
            self.trigger_alert("ALARM!")
        
        if self.timer_seconds_remaining > 0:
            self.timer_seconds_remaining -= 1
            m, s = divmod(self.timer_seconds_remaining, 60)
            self.timer_status.setText(f"⏳ Timer: {m:02d}:{s:02d} remaining")
            self.timer_status.setStyleSheet("color: white; background-color: #E67E22; border-radius: 10px; padding: 5px; border: none;")
            if self.timer_seconds_remaining == 0:
                self.timer_status.setText("")
                self.trigger_alert("TIMER FINISHED!")
        elif self.timer_status.text() != "":
            self.timer_status.setText("")
            self.timer_status.setStyleSheet("")

    def trigger_alert(self, text):
        self.sound_effect.play()
        QMessageBox.information(self, "Alert", text)
        self.sound_effect.stop()

    def navigate(self, title):
        if title == "YES / NO": self.stack.setCurrentIndex(1)
        elif title == "CLOCK": 
            self.switch_clock_mode("ALARM")
            self.stack.setCurrentIndex(2)
        elif title == "BELL": 
            QMessageBox.warning(self, "Emergency", "Staff Alerted!")

    def finish(self, choice):
        QMessageBox.information(self, "Success", f"Recorded: {choice}")
        self.stack.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WellBeingApp()
    window.showMaximized()
    sys.exit(app.exec())
