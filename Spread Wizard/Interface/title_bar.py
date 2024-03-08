"""This module contains a single class to define a title bar GUI component."""

# pylint: disable=E0611
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QSizePolicy, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class TitleBar(QWidget):
    """Define a QWidget to act as a title bar for Mapset Statistician"""

    def __init__(self, parent):
        super().__init__(parent)

        self.setStyleSheet("background-color: #0f0f0f;")
        self.setGeometry(0, 0, self.parent().size().width(), 30)
        self.draggable = True
        self.dragging_threshold = 5
        self.drag_position = None

        font = QFont("Nunito", 10)
        font.setBold(True)

        # Create a horizontal layout for the title bar
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Add a spacer to push the buttons to the right
        #left_spacer = QLabel(self)
        #left_spacer.setStyleSheet("background-color: #222222;")
        #left_spacer.setFixedSize(120,40)
        #layout.addWidget(left_spacer)

        self.spacer = QLabel(self)
        self.spacer.setStyleSheet("background-color: #222222; color: #f9d5ff;")
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.spacer.setFixedHeight(30)
        self.spacer.setText("  Spread Wizard by Hugged")
        self.spacer.setFont(font)
        self.spacer.setAlignment(Qt.AlignVCenter)
        layout.addWidget(self.spacer)

        # Add a minimize button
        minimize_button = QPushButton("-", self)
        minimize_button.setStyleSheet(
            "QPushButton       { background-color: #222222; color: #f9d5ff; border: none; }"
            "QPushButton:hover { background-color: #333333; color: #f9d5ff; border: none; }")
        minimize_button.setFixedSize(40, 30)
        minimize_button.clicked.connect(self.parent().showMinimized)
        minimize_button.setFont(font)
        layout.addWidget(minimize_button)

        # Add a maximize/restore button
        #self.maximize_button = QPushButton("□", self)
        #self.maximize_button.setStyleSheet(
        #    "QPushButton       { background-color: #222222; color: #f9d5ff; border: none; }"
        #    "QPushButton:hover { background-color: #333333; color: #f9d5ff; border: none; }")
        #self.maximize_button.setFixedSize(40, 30)
        #self.maximize_button.clicked.connect(self.toggleMaximize)
        #self.maximize_button.setFont(font)
        #layout.addWidget(self.maximize_button)

        # Add a close button
        close_button = QPushButton("X", self)
        close_button.setStyleSheet(
            "QPushButton       { background-color: #222222; color: #f9d5ff; border: none; }"
            "QPushButton:hover { background-color: #333333; color: #f9d5ff; border: none; }")
        close_button.setFixedSize(40, 30)
        close_button.clicked.connect(self.parent().close)
        close_button.setFont(font)
        layout.addWidget(close_button)

        self.setLayout(layout)

    # pylint: disable=C0103
    #(These methods require camelcase cuz PyQt5)
    def mousePressEvent(self, event):
        """Handle left mouse clicks to move the window."""

        if event.button() == Qt.LeftButton and self.draggable:
            self.drag_position = event.globalPos() - self.parent().frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Handle Moving the window."""

        if self.drag_position is not None and self.draggable:
            if event.buttons() == Qt.LeftButton and (event.globalPos() -
                                  self.drag_position).manhattanLength() > self.dragging_threshold:
                self.parent().move(event.globalPos() - self.drag_position)
                self.drag_position = event.globalPos() - self.parent().frameGeometry().topLeft()
                event.accept()

    def mouseReleaseEvent(self, event):
        """Handle Releasing the left button."""

        if event.button() == Qt.LeftButton and self.draggable:
            self.drag_position = None
            event.accept()

    def toggleMaximize(self):
        """Toggle the maximizing of the main window."""

        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setText("□")
        else:
            self.parent().showMaximized()
            self.maximize_button.setText("❐")
