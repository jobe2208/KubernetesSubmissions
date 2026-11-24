import time
import uuid
from datetime import datetime, timezone

FILE_PATH = "/usr/src/app/files/log.txt"
random_string = str(uuid.uuid4())

while True:
    timestamp = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    log_line = f"{timestamp}: {random_string}\n"

    with open(FILE_PATH, "a") as file:
        file.write(log_line)

    print(log_line.strip(), flush=True)
    time.sleep(5)