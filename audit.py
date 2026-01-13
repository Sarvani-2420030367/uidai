import datetime

def log_action(username, action):
    with open("audit_log.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} | {username} | {action}\n")
