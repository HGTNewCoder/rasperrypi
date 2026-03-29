import sys
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QGridLayout, 
                             QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
                             QPushButton, QMessageBox, QStackedWidget, QTimeEdit,
                             QGraphicsDropShadowEffect)
from PyQt6.QtGui import QFont, QPixmap, QColor
from PyQt6.QtCore import Qt, QDate, QTimer, QTime, QUrl
from PyQt6.QtMultimedia import QSoundEffect

class CommBox(QFrame):
    def __init__(self, title, description, bg_color, media_file, is_bell=False, show_btn=True, large_text=False, add_shadow=False, use_picture=False, hide_title=False, callback=None):
        super().__init__()
        self.is_bell = is_bell
        self.title = title 
        self.original_color = bg_color
        self.media_file = media_file
        self.callback = callback 
        self.show_btn = show_btn
        self.large_text = large_text
        self.add_shadow = add_shadow
        self.use_picture = use_picture
        self.hide_title = hide_title 
        self.setFrameShape(QFrame.Shape.NoFrame)
        
        if is_bell or not show_btn:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        if is_bell:
            self.setFixedSize(160, 160) 
        else:
            self.setMinimumWidth(260) 
            self.setMinimumHeight(320)
        
        self.setStyleSheet("QFrame { border: none; border-radius: 20px; background-color: white; }")
        
        if self.add_shadow:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(20)
            shadow.setColor(QColor(0, 0, 0, 40))
            shadow.setOffset(0, 6)
            self.setGraphicsEffect(shadow)

        self.main_v_layout = QVBoxLayout(self)
        self.main_v_layout.setContentsMargins(0, 0, 0, 0)
        self.main_v_layout.setSpacing(0)

        if is_bell:
            self.setup_bell_ui(media_file)
        else:
            self.setup_standard_ui(title, description, bg_color, media_file)

    def setup_bell_ui(self, media_file):
        self.bell_inner_frame = QFrame()
        self.bell_inner_frame.setStyleSheet(f"background-color: {self.original_color}; border-radius: 20px; border: none;")
        inner_layout = QVBoxLayout(self.bell_inner_frame)
        self.bell_display = QLabel()
        self.bell_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if media_file and os.path.exists(media_file):
            pixmap = QPixmap(media_file)
            self.bell_display.setPixmap(pixmap.scaled(130, 130, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            self.bell_display.setText("🔔")
            self.bell_display.setFont(QFont("Arial", 60))
        inner_layout.addWidget(self.bell_display)
        self.main_v_layout.addWidget(self.bell_inner_frame)

    def setup_standard_ui(self, title, description, bg_color, media_file):
        self.top_half = QFrame()
        self.top_half.setStyleSheet(f"background-color: {bg_color}; border-top-left-radius: 20px; border-top-right-radius: 20px; border: none;")
        top_layout = QVBoxLayout(self.top_half)
        
        if self.use_picture:
            top_layout.setContentsMargins(0, 0, 0, 0)
            top_layout.setSpacing(0)
        
        if not self.hide_title:
            t_label = QLabel(title)
            t_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            if self.large_text:
                t_label.setFont(QFont("Arial", 26, QFont.Weight.Bold))
                t_label.setStyleSheet("color: #2C4C49; padding: 15px;" if self.use_picture else "color: #2C4C49; padding-top: 10px;")
            else:
                t_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
                if self.use_picture: t_label.setStyleSheet("padding: 10px;")
                
            top_layout.addWidget(t_label)
        
        if self.use_picture and media_file and os.path.exists(media_file):
            self.pic_frame = QFrame()
            safe_path = media_file.replace('\\', '/')
            self.pic_frame.setStyleSheet(f"QFrame {{ border-image: url({safe_path}) 0 0 0 0 stretch stretch; border-top-left-radius: 20px; border-top-right-radius: 20px; border: none; }}")
            top_layout.addWidget(self.pic_frame, 1) 
        else:
            self.media_display = QLabel()
            self.media_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            if media_file and os.path.exists(media_file):
                pixmap = QPixmap(media_file)
                self.media_display.setPixmap(pixmap.scaled(140, 90, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            else:
                emoji_map = {"TOILET": "🚽", "SHOWER": "🚿", "WASH": "🧼", "CLOTHES": "👕", "FOOD": "🥪", "FEELING": "😊", "EXERCISE": "💪", "ENTERTAINMENT": "📺", "YES / NO": "✅", "RECOMMEND ANSWER": "💡", "CLOCK": "⏰"}
                self.media_display.setText(emoji_map.get(title, "✨"))
                self.media_display.setFont(QFont("Arial", 70 if self.large_text else 40))
                
            top_layout.addWidget(self.media_display)

        self.bottom_half = QFrame()
        self.bottom_half.setStyleSheet("background-color: white; border-bottom-left-radius: 20px; border-bottom-right-radius: 20px; border: none;")
        bottom_layout = QVBoxLayout(self.bottom_half)
        bottom_layout.addStretch(1) 
        
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setFont(QFont("Arial", 18 if (self.large_text or self.hide_title) else 15, QFont.Weight.Bold))
        desc_label.setStyleSheet("color: #444444;" if (self.large_text or self.hide_title) else "") 
            
        bottom_layout.addWidget(desc_label)
        bottom_layout.addStretch(1) 

        if self.show_btn:
            self.btn = QPushButton("TALK WITH US")
            self.btn.setFixedHeight(45)
            self.btn.setStyleSheet("QPushButton { background-color: #4D908E; color: white; border-radius: 12px; font-weight: bold; border: none; }")
            self.btn.clicked.connect(self.handle_click)
            bottom_layout.addWidget(self.btn)
        
        # Layout weight adjustments
        if self.hide_title: weights = (75, 25)
        elif self.large_text: weights = (60, 40)
        else: weights = (40, 60)
        self.main_v_layout.addWidget(self.top_half, weights[0])
        self.main_v_layout.addWidget(self.bottom_half, weights[1])

    def handle_click(self):
        if self.callback: self.callback(self.title)

    def mousePressEvent(self, event):
        if self.is_bell:
            self.bell_inner_frame.setStyleSheet("background-color: #900C3F; border-radius: 20px; border: none;")
            QTimer.singleShot(200, lambda: self.bell_inner_frame.setStyleSheet(f"background-color: {self.original_color}; border-radius: 20px; border: none;"))
            if self.callback: self.callback("BELL")
        elif not self.show_btn:
            if self.hide_title and self.use_picture and hasattr(self, 'pic_frame'):
                safe_path = self.media_file.replace('\\', '/')
                self.pic_frame.setStyleSheet(f"QFrame {{ border-image: url({safe_path}) 0 0 0 0 stretch stretch; border-top-left-radius: 20px; border-top-right-radius: 20px; border: 6px solid #8FC8C2; }}")
            else:
                self.top_half.setStyleSheet(f"background-color: #BDBDBD; border-top-left-radius: 20px; border-top-right-radius: 20px; border: none;")
            
            self.bottom_half.setStyleSheet("background-color: #E0E0E0; border-bottom-left-radius: 20px; border-bottom-right-radius: 20px; border: none;")
            QTimer.singleShot(150, self.restore_colors)
            if self.callback: self.callback(self.title)

    def restore_colors(self):
        if self.hide_title and self.use_picture and hasattr(self, 'pic_frame'):
            safe_path = self.media_file.replace('\\', '/')
            self.pic_frame.setStyleSheet(f"QFrame {{ border-image: url({safe_path}) 0 0 0 0 stretch stretch; border-top-left-radius: 20px; border-top-right-radius: 20px; border: none; }}")
        else:
            self.top_half.setStyleSheet(f"background-color: {self.original_color}; border-top-left-radius: 20px; border-top-right-radius: 20px; border: none;")
        self.bottom_half.setStyleSheet("background-color: white; border-bottom-left-radius: 20px; border-bottom-right-radius: 20px; border: none;")


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
        self.stack.addWidget(self.create_main_menu())      # Index 0
        self.stack.addWidget(self.create_response_page())   # Index 1
        self.stack.addWidget(self.create_clock_page())      # Index 2
        self.stack.addWidget(self.create_bathroom_page())   # Index 3
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stack)

    def create_main_menu(self):
        page = QWidget()
        page.setStyleSheet("background-color: #F0F8F7;")
        layout = QVBoxLayout(page)
        
        header_container = QFrame()
        header_container.setStyleSheet("background-color: #8FC8C2; border: none;")
        header_layout = QVBoxLayout(header_container)
        header = QLabel(f"MY DAILY WELL-BEING\n{QDate.currentDate().toString('dddd, MMMM d, yyyy')}")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        header.setStyleSheet("color: #2C4C49;")
        
        self.timer_status = QLabel("")
        self.timer_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(header)
        header_layout.addWidget(self.timer_status)
        layout.addWidget(header_container)

        grid = QGridLayout()
        grid.setContentsMargins(25, 10, 25, 10); grid.setSpacing(20)
        
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
        
        for title, desc, col, icon_file, r, c in cards:
            card = CommBox(title=title, description=desc, bg_color=col, media_file=icon_file, callback=self.navigate)
            grid.addWidget(card, r, c)
            
        self.bell = CommBox(title="", description="", bg_color="#F1948A", media_file="bell.png", is_bell=True, callback=self.navigate)
        grid.addWidget(self.bell, 2, 0, 1, 4, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addLayout(grid)
        return page

    def create_bathroom_page(self):
        page = QWidget(); page.setStyleSheet("background-color: #F0F8F7;")
        layout = QVBoxLayout(page)
        header = QLabel("BATHROOM ASSISTANCE")
        header.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter); header.setStyleSheet("padding: 20px; color: #2C4C49;")
        layout.addWidget(header)

        grid = QGridLayout(); grid.setSpacing(35); grid.setContentsMargins(40, 10, 40, 10)
        options = [
            ("TOILET", "I need to use the toilet.", "#AED6F1", "toilet_pic.png", 0, 0), 
            ("SHOWER", "I would like to take a shower.", "#A2D9CE", "shower_pic.png", 0, 1), 
            ("WASH", "I need to wash my hands/face.", "#F9E79F", "wash_pic.jpg", 1, 0), 
            ("CLOTHES", "I need help changing clothes.", "#D7BDE2", "clothes_pic.jpg", 1, 1), 
        ]
        for t, d, c, mf, r, col in options:
            card = CommBox(title=t, description=d, bg_color=c, media_file=mf, show_btn=False, add_shadow=True, use_picture=True, hide_title=True, callback=self.finish)
            grid.addWidget(card, r, col)

        layout.addLayout(grid)
        back_btn = QPushButton("Go Back")
        back_btn.setFixedSize(200, 60); back_btn.setStyleSheet("background-color: #BDBDBD; color: white; border-radius: 15px; font-weight: bold; font-size: 20px; border: none;")
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)
        return page

    def create_response_page(self):
        page = QWidget(); page.setStyleSheet("background-color: white;")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 20, 40, 20); layout.setSpacing(20)

        self.resp_title = QLabel("CHOOSE ANSWER")
        self.resp_title.setAlignment(Qt.AlignmentFlag.AlignCenter); self.resp_title.setFont(QFont("Arial", 38, QFont.Weight.Bold))
        self.resp_title.setStyleSheet("color: #2C4C49; border: none;")
        layout.addWidget(self.resp_title)

        self.resp_cards_container = QHBoxLayout(); self.resp_cards_container.setSpacing(40)
        yes_card = self.create_styled_response_card("YES", "#D5F5E3", "#4D908E", "yes.png", lambda: self.finish("YES"))
        no_card = self.create_styled_response_card("NO", "#FADBD8", "#A93226", "no.png", lambda: self.finish("NO"))

        self.resp_cards_container.addWidget(yes_card); self.resp_cards_container.addWidget(no_card)
        layout.addLayout(self.resp_cards_container)

        self.back_btn_resp = QPushButton("Go Back")
        self.back_btn_resp.setFixedSize(150, 50); self.back_btn_resp.setStyleSheet("background-color: #BDBDBD; color: white; border-radius: 10px; font-weight: bold; border: none;")
        self.back_btn_resp.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(self.back_btn_resp, alignment=Qt.AlignmentFlag.AlignCenter)

        self.result_container = QFrame(); self.result_container.hide()
        self.result_layout = QVBoxLayout(self.result_container)
        self.result_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.result_icon = QLabel(); self.result_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_layout.addWidget(self.result_icon)
        layout.addWidget(self.result_container)
        return page

    def create_styled_response_card(self, title, bg_color, btn_color, icon, callback):
        card = QFrame(); card.setStyleSheet(f"background-color: {bg_color}; border-radius: 40px; border: none;")
        shadow = QGraphicsDropShadowEffect(); shadow.setBlurRadius(20); shadow.setColor(QColor(0, 0, 0, 40)); shadow.setOffset(0, 6)
        card.setGraphicsEffect(shadow)

        v = QVBoxLayout(card); v.setContentsMargins(20, 10, 20, 20)
        lbl_icon = QLabel()
        if os.path.exists(icon):
            lbl_icon.setPixmap(QPixmap(icon).scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            lbl_icon.setText("✅" if title == "YES" else "❌"); lbl_icon.setFont(QFont("Arial", 150))
        lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter); v.addWidget(lbl_icon)

        t_lbl = QLabel(title); t_lbl.setFont(QFont("Arial", 75, QFont.Weight.Bold)); t_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter); t_lbl.setStyleSheet(f"color: {btn_color}; border: none;")
        v.addWidget(t_lbl); v.addStretch()

        btn = QPushButton("CONFIRM"); btn.setFixedHeight(80); btn.setStyleSheet(f"background-color: {btn_color}; color: white; border-radius: 25px; font-size: 24px; font-weight: bold; border: none;")
        btn.clicked.connect(callback); v.addWidget(btn)
        return card

    def create_clock_page(self):
        page = QWidget(); page.setStyleSheet("background-color: #F0F8F7;")
        main_v = QVBoxLayout(page); main_v.setContentsMargins(0, 0, 0, 0)
        top_bar = QFrame(); top_bar.setFixedHeight(120); top_bar.setStyleSheet("background-color: #8FC8C2; border: none;")
        top_layout = QHBoxLayout(top_bar)
        
        clock_title = QLabel("CLOCK SETTINGS"); clock_title.setFont(QFont("Arial", 32, QFont.Weight.Bold)); clock_title.setStyleSheet("color: white; border: none;")
        top_layout.addWidget(clock_title, alignment=Qt.AlignmentFlag.AlignCenter); main_v.addWidget(top_bar)
        
        content_layout = QVBoxLayout(); content_layout.setContentsMargins(100, 20, 100, 20); content_layout.setSpacing(20)
        mode_box = QHBoxLayout(); self.btn_alarm_mode = QPushButton("ALARM"); self.btn_timer_mode = QPushButton("TIMER")
        
        for b in [self.btn_alarm_mode, self.btn_timer_mode]:
            b.setFixedSize(300, 80); b.setCheckable(True); b.setStyleSheet("QPushButton { background-color: #D1E8E5; border-radius: 40px; font-weight: bold; font-size: 26px; color: #2C4C49; border: none; } QPushButton:checked { background-color: #2C4C49; color: white; }")
            
        self.btn_alarm_mode.setChecked(True); self.btn_alarm_mode.clicked.connect(lambda: self.switch_clock_mode("ALARM")); self.btn_timer_mode.clicked.connect(lambda: self.switch_clock_mode("TIMER"))
        mode_box.addWidget(self.btn_alarm_mode); mode_box.addWidget(self.btn_timer_mode); content_layout.addLayout(mode_box)
        
        center_card = QFrame(); center_card.setStyleSheet("background-color: white; border-radius: 40px; border: none;")
        shadow = QGraphicsDropShadowEffect(); shadow.setBlurRadius(20); shadow.setColor(QColor(0, 0, 0, 40)); shadow.setOffset(0, 6); center_card.setGraphicsEffect(shadow)
        card_layout = QVBoxLayout(center_card); card_layout.setContentsMargins(40, 40, 40, 40)
        
        spinner_hbox = QHBoxLayout(); hr_vbox = QVBoxLayout(); self.hr_up = QPushButton("▲"); self.hr_down = QPushButton("▼")
        for btn in [self.hr_up, self.hr_down]: 
            btn.setFixedSize(80, 80); btn.setStyleSheet("font-size: 40px; color: #8FC8C2; background: transparent; border: 3px solid #8FC8C2; border-radius: 40px;")
        
        self.hr_up.clicked.connect(lambda: self.spin_time(h=1)); self.hr_down.clicked.connect(lambda: self.spin_time(h=-1))
        hr_vbox.addWidget(self.hr_up); hr_vbox.addWidget(self.hr_down)
        
        self.time_spinner = QTimeEdit(QTime.currentTime()); self.time_spinner.setDisplayFormat("HH:mm"); self.time_spinner.setFixedSize(450, 200); self.time_spinner.setAlignment(Qt.AlignmentFlag.AlignCenter); self.time_spinner.setStyleSheet("QTimeEdit { background-color: #F9F9F9; border: 3px solid #8FC8C2; border-radius: 30px; font-size: 130px; font-weight: bold; color: #2C4C49; } QTimeEdit::up-button, QTimeEdit::down-button { width: 0px; }")
        
        min_vbox = QVBoxLayout(); self.min_up = QPushButton("▲"); self.min_down = QPushButton("▼")
        for btn in [self.min_up, self.min_down]: 
            btn.setFixedSize(80, 80); btn.setStyleSheet("font-size: 40px; color: #8FC8C2; background: transparent; border: 3px solid #8FC8C2; border-radius: 40px;")
            
        self.min_up.clicked.connect(lambda: self.spin_time(m=1)); self.min_down.clicked.connect(lambda: self.spin_time(m=-1))
        min_vbox.addWidget(self.min_up); min_vbox.addWidget(self.min_down)
        
        spinner_hbox.addLayout(hr_vbox); spinner_hbox.addWidget(self.time_spinner); spinner_hbox.addLayout(min_vbox)
        card_layout.addLayout(spinner_hbox)
        
        self.mode_label = QLabel("Tap arrows to set alarm"); self.mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter); self.mode_label.setFont(QFont("Arial", 32, QFont.Weight.Bold)); self.mode_label.setStyleSheet("border: none; color: #444444;") 
        card_layout.addWidget(self.mode_label); content_layout.addWidget(center_card)
        
        act_layout = QHBoxLayout(); self.start_btn = QPushButton("SET ALARM"); self.start_btn.setFixedSize(350, 100); self.start_btn.setStyleSheet("background-color: #4D908E; color: white; border-radius: 50px; font-weight: bold; font-size: 30px; border: none;")
        self.start_btn.clicked.connect(self.set_clock_action)
        
        back_btn = QPushButton("CANCEL"); back_btn.setFixedSize(350, 100); back_btn.setStyleSheet("background-color: #BDBDBD; color: white; border-radius: 50px; font-weight: bold; font-size: 30px; border: none;")
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        act_layout.addWidget(back_btn); act_layout.addWidget(self.start_btn); content_layout.addLayout(act_layout)
        main_v.addLayout(content_layout)
        return page

    def spin_time(self, h=0, m=0):
        current = self.time_spinner.time()
        self.time_spinner.setTime(current.addSecs((h * 3600) + (m * 60)))

    def switch_clock_mode(self, mode):
        if mode == "ALARM":
            self.btn_timer_mode.setChecked(False); self.start_btn.setText("SET ALARM")
            self.mode_label.setText("Tap arrows to set alarm"); self.time_spinner.setTime(QTime.currentTime())
        else:
            self.btn_alarm_mode.setChecked(False); self.start_btn.setText("START TIMER")
            self.mode_label.setText("Tap arrows to set duration"); self.time_spinner.setTime(QTime(0, 0))

    def set_clock_action(self):
        t = self.time_spinner.time()
        if self.btn_alarm_mode.isChecked(): self.active_alarm_time = t.toString("HH:mm")
        else: self.timer_seconds_remaining = (t.hour() * 3600) + (t.minute() * 60)
        self.stack.setCurrentIndex(0)

    def process_time_events(self):
        now_str = QTime.currentTime().toString("HH:mm")
        if self.active_alarm_time and now_str == self.active_alarm_time:
            self.active_alarm_time = None; self.trigger_alert("ALARM!")
        if self.timer_seconds_remaining > 0:
            self.timer_seconds_remaining -= 1
            m, s = divmod(self.timer_seconds_remaining, 60)
            self.timer_status.setText(f"⏳ Timer: {m:02d}:{s:02d} remaining")
            self.timer_status.setStyleSheet("color: white; background-color: #E67E22; border-radius: 10px; padding: 5px; border: none;")
            if self.timer_seconds_remaining == 0:
                self.timer_status.setText(""); self.trigger_alert("TIMER FINISHED!")
        elif self.timer_status.text() != "":
            self.timer_status.setText(""); self.timer_status.setStyleSheet("")

    def trigger_alert(self, text):
        self.sound_effect.play(); QMessageBox.information(self, "Alert", text); self.sound_effect.stop()

    def navigate(self, title):
        if title == "YES / NO": self.stack.setCurrentIndex(1)
        elif title == "CLOCK": 
            self.btn_alarm_mode.setChecked(True); self.switch_clock_mode("ALARM"); self.stack.setCurrentIndex(2)
        elif title == "BATHROOM": self.stack.setCurrentIndex(3)
        elif title == "BELL": QMessageBox.warning(self, "Emergency", "Staff Alerted!")

    def finish(self, choice):
        icon_map = {"YES": "yes.png", "NO": "no.png", "TOILET": "toilet_pic.png", "SHOWER": "shower_pic.png", "WASH": "wash_pic.jpg", "CLOTHES": "clothes_pic.jpg"}
        icon_path = icon_map.get(choice, "")

        self.stack.setCurrentIndex(1)
        self.resp_title.hide(); self.back_btn_resp.hide()
        for i in range(self.resp_cards_container.count()):
            w = self.resp_cards_container.itemAt(i).widget()
            if w: w.hide()

        # Update full background color logic
        # Red for 'NO', Green for 'YES' and Bathroom options
        bg = "#D5F5E3" if choice in ["YES", "TOILET", "SHOWER", "WASH"] else "#A93226"
        self.stack.widget(1).setStyleSheet(f"background-color: {bg}; border: none;")

        if os.path.exists(icon_path):
            pix = QPixmap(icon_path).scaled(800, 800, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.result_icon.setPixmap(pix)
            self.result_icon.show(); self.result_container.show()
        else:
            self.result_icon.setText("✅" if choice == "YES" else "❌")
            self.result_icon.setFont(QFont("Arial", 200))
            self.result_icon.show(); self.result_container.show()

        QTimer.singleShot(3000, self.reset_and_go_home)

    def reset_and_go_home(self):
        self.stack.widget(1).setStyleSheet("background-color: white; border: none;")
        self.result_container.hide(); self.resp_title.show(); self.back_btn_resp.show()
        for i in range(self.resp_cards_container.count()):
            w = self.resp_cards_container.itemAt(i).widget()
            if w: w.show()
        self.stack.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WellBeingApp()
    window.showMaximized()
    sys.exit(app.exec())
