from app.ui.main_window import run_app
from app.utils.logger import configure_logger


def main() -> None:
    configure_logger()
    run_app()


if __name__ == '__main__':
    main()
