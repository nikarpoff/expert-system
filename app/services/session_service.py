from dataclasses import dataclass


@dataclass
class SessionStats:
    asked_questions: int = 0


class SessionService:
    def __init__(self):
        self.stats = SessionStats()

    def mark_question_asked(self) -> None:
        self.stats.asked_questions += 1
