from datetime import datetime
import signal

Openai_API_KEY=""
Claude_API_KEY=""

openai_model_name="gpt-4o"
claude_model_name="claude-3-5-sonnet-20240620"

def timeout_handler(signum, frame):
    raise TimeoutException

signal.signal(signal.SIGALRM, timeout_handler)

def get_current_date_hyphen():
    return datetime.now().strftime('%Y_%m_%d')

def get_current_date_month_en():
    return datetime.today().strftime('%d %B %Y')