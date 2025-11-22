# logger.py
LOG_TEMPLATE_WITH_STEP = "\n============================================\n\033[92m[Pipeline]\033[0m (%d/%d) %s"
LOG_TEMPLATE_SIMPLE = "%s[Pipeline]%s %s"
LOG_TEMPLATE_INFO = " %s[Info]%s %s"
LOG_TEMPLATE_ERROR = " %s[ERROR]%s %s"

COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_RED = "\033[91m"
COLOR_RESET = "\033[0m"

_current_step = 0
_total_steps = 0

def start_pipeline(total_steps: int):
    global _current_step, _total_steps
    _current_step = 0
    _total_steps = total_steps

def log(msg: str):
    """
    Print the next step message automatically with step counter.
    """
    global _current_step
    _current_step += 1
    print(LOG_TEMPLATE_WITH_STEP % (_current_step, _total_steps, msg))

def info(msg: str):
    """Info log (yellow)"""
    print(LOG_TEMPLATE_INFO % (COLOR_YELLOW, COLOR_RESET, msg))


def error(msg: str):
    """Error log (red)"""
    print(LOG_TEMPLATE_ERROR % (COLOR_RED, COLOR_RESET, msg))