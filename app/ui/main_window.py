from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QMessageBox, QPushButton, QTextEdit, QVBoxLayout, QWidget

from app.config import settings
from app.database.connection import SessionLocal
from app.services.diagnosis_service import DiagnosisService
from app.services.session_service import SessionService
from app.ui.debug_window import DebugWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Медицинская экспертная система')
        self.resize(800, 500)

        self.session_service = SessionService()
        self.debug_window = DebugWindow()

        db_session = SessionLocal()
        self.diagnosis_service = DiagnosisService(db_session)
        self.state = self.diagnosis_service.start()
        self.current_symptom_id = None

        container = QWidget(self)
        self.setCentralWidget(container)
        layout = QVBoxLayout(container)

        self.status_label = QLabel('Нажмите "Следующий вопрос" для начала диагностики')
        self.question_label = QLabel('')
        self.results_box = QTextEdit()
        self.results_box.setReadOnly(True)

        self.next_button = QPushButton('Следующий вопрос')
        self.yes_button = QPushButton('Да')
        self.no_button = QPushButton('Нет')
        self.debug_button = QPushButton('Показать отладку')

        self.next_button.clicked.connect(self.next_question)
        self.yes_button.clicked.connect(lambda: self.answer(True))
        self.no_button.clicked.connect(lambda: self.answer(False))
        self.debug_button.clicked.connect(self.debug_window.show)

        layout.addWidget(self.status_label)
        layout.addWidget(self.question_label)
        layout.addWidget(self.next_button)
        layout.addWidget(self.yes_button)
        layout.addWidget(self.no_button)
        layout.addWidget(self.debug_button)
        layout.addWidget(self.results_box)

        self.update_results()

    def next_question(self):
        symptom_id = self.diagnosis_service.engine.choose_next_symptom(self.state)
        if symptom_id is None:
            self.finish_diagnosis()
            return
        self.current_symptom_id = symptom_id
        question = self.diagnosis_service.symptom_by_id[symptom_id].question
        self.question_label.setText(question)
        self.session_service.mark_question_asked()
        self.status_label.setText(f'Задано вопросов: {self.session_service.stats.asked_questions}')

    def answer(self, answer_yes: bool):
        if self.current_symptom_id is None:
            QMessageBox.warning(self, 'Ошибка', 'Сначала выберите вопрос.')
            return
        self.diagnosis_service.engine.apply_answer(self.state, self.current_symptom_id, answer_yes)
        trace = self.state.traces[-1]
        self.debug_window.add_trace(
            f"Вопрос: {trace.question}; Ответ: {'Да' if trace.answer_yes else 'Нет'}; {trace.probabilities}"
        )
        self.current_symptom_id = None
        self.question_label.setText('')
        self.update_results()
        self.try_finish_early()

    def try_finish_early(self):
        best_id = max(self.state.probabilities, key=self.state.probabilities.get)
        if self.state.probabilities[best_id] >= settings.decision_threshold:
            self.finish_diagnosis(best_id)

    def finish_diagnosis(self, forced_id: str | None = None):
        if not self.state.probabilities:
            QMessageBox.information(self, 'Итог', 'Диагнозы были исключены.')
            return
        best_id = forced_id or max(self.state.probabilities, key=self.state.probabilities.get)
        best = self.diagnosis_service.diagnosis_by_id[best_id]
        prob = self.state.probabilities[best_id]
        QMessageBox.information(self, 'Результат', f'Наиболее вероятный диагноз: {best.name}\nВероятность: {prob:.4f}')

    def update_results(self):
        rows = ['Текущие вероятности диагнозов:']
        for d_id, prob in sorted(self.state.probabilities.items(), key=lambda p: p[1], reverse=True):
            name = self.diagnosis_service.diagnosis_by_id[d_id].name
            rows.append(f'- {name}: {prob:.4f}')
        self.results_box.setText('\n'.join(rows))


def run_app():
    app = QApplication([])
    w = MainWindow()
    w.show()
    app.exec()
