import sys
import asyncio
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor
import qasync

class MascotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self._drag_position = None

    def init_ui(self):

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.SubWindow
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        self.speech_bubble = QLabel("Iniciando... Ligando redes neurais... TAINEL-DROID-26FE online. Me diga, como posso ajudar?")
        self.speech_bubble.setWordWrap(True)
        self.speech_bubble.setFixedWidth(220)
        self.speech_bubble.setStyleSheet("""
            QLabel {
                background-color: rgba(30, 30, 46, 230);
                color: #cdd6f4;
                border: 2px solid #89b4fa;
                border-radius: 12px;
                padding: 10px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
            }
        """)

        self.avatar_label = QLabel("🤖")
        self.avatar_label.setFont(QFont("Arial", 48))
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.speech_bubble)
        layout.addWidget(self.avatar_label)
        self.setLayout(layout)

        self.move_to_bottom_right()

    def move_to_bottom_right(self):
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - 260, screen.height() - 200)

    def set_speech(self, text: str):
        """Atualiza a fala no balão de texto."""
        self.speech_bubble.setText(text)
        self.adjustSize()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self._drag_position:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_position = None