from datetime import datetime


class Logger:
    @staticmethod
    def write(message, break_line=False):
        content = ""

        if break_line:
            content = "\n"

        content += f"[{datetime.now().strftime('%Y-%m-%d@%H:%M:%S')}]: {message}"
        print(f"{content}")
