# logger.py
LOG_TEMPLATE_WITH_STEP = "\n============================================\n\033[92m[Pipeline]\033[0m (%d/%d) %s"

# def log(msg: str):
#     print(LOG_TEMPLATE % msg)
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