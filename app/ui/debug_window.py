from PyQt6.QtWidgets import QTextEdit, QVBoxLayout, QWidget


class DebugWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Отладка экспертной системы')
        self.text = QTextEdit(self)
        self.text.setReadOnly(True)
        layout = QVBoxLayout(self)
        layout.addWidget(self.text)

    def add_trace(self, line: str) -> None:
        self.text.append(line)
