import re
import time
import subprocess
import word2number

def parse_text_task(text):
    # Define regular expressions to match different types of tasks
    action_patterns = {
        'schedule_meeting': r"schedule a meeting (.+?) (?:at|on) (\d{1,2}(?::\d{2})?(?:AM|PM)?)",
        'timer': r"start(?:ing)?(?: a)? timer(?: for)?(?: (\d+) hours?)?(?:,? (\d+) minutes?)?(?:,? (\d+) seconds?)?",
        #'timer': r"start(?:ing)?(?: a)?(?: (\d+) hour?)?(?:,? (\d+) minute?)?(?:,? (\d+) second?)? timer",
        'stopwatch': r"start(?:ing)?(?: a)? stopwatch?",
        'stats': r"show(?: me)?(?: the)?(?: device| glasses| glass| your)? (stats|statistics)",
        'nsolve': r"(?:help me )?(solve|evaluate)(?: a| an)?(?: math(?:ematics|ematical)?| numerical)? equation",
        'settings': r"(?:open)?(?:\s+(?:the|your))?(\s+settings|\s+preferences|\s+system\s+settings|\s+system\s+preferences|\s+device\s+settings|\s+device\s+preferences)",
        'time': r"what(?:'s| is)?(?: the)?(?: current| right| correct)? time(?: is it| right now| currently)?",
        'time2': r"what time is it",
        # Add more action patterns as needed
    }
    for action, pattern in action_patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # Extract parameters based on the matched groups
            parameters = match.groups()
            return action, parameters
    return None, None


def start_timer(parameters):
    starttime = time.time()
    print(f"time={time.time()}")
    parameters = list(parameters)  # Convert parameters tuple to a list
    if parameters[0] is None:
        parameters[0] = 0
    if parameters[1] is None:
        parameters[1] = 0
    if parameters[2] is None:
        parameters[2] = 0
    print(f"Timer for {parameters[0]}h, {parameters[1]}m, {parameters[2]}s")
    totalsec = 3600 * int(parameters[0]) + 60 * int(parameters[1]) + int(parameters[2])
    print(f"Total seconds: {totalsec}")


# Example usage
text_task = input("> ")
action, parameters = parse_text_task(text_task)
if action:
    print("Action:", action)
    print("Parameters:", parameters)
    if action == "timer":
        start_timer(parameters)
    if action == "nsolve":
        subprocess.run(["python", "mathwordtoeq.py"])
else:
    print("No action detected.")
