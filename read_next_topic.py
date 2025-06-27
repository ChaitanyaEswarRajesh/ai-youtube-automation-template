
import os

TOPICS_FILE = "topics.txt"
ARCHIVE_FILE = "topics_archive.txt"

def read_next_topic():
    if not os.path.exists(TOPICS_FILE):
        print("No topics.txt file found.")
        return None

    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        print("topics.txt is empty.")
        return None

    next_topic = lines[0]
    with open(TOPICS_FILE, "w", encoding="utf-8") as f:
        f.writelines(line + "\n" for line in lines[1:])

    with open(ARCHIVE_FILE, "a", encoding="utf-8") as archive:
        archive.write(next_topic + "\n")

    return next_topic

if __name__ == "__main__":
    topic = read_next_topic()
    if topic:
        print(topic)
