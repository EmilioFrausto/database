import os

DB_FILE = "data.db"

# Our in-memory index (list instead of dictionary)
store = []


def find_key(key):
    for i in range(len(store)):
        if store[i][0] == key:
            return i
    return -1


def set_value(key, value):
    index = find_key(key)

    if index == -1:
        store.append((key, value))
    else:
        store[index] = (key, value)

    # Append to disk immediately
    with open(DB_FILE, "a") as f:
        f.write(f"SET {key} {value}\n")


def get_value(key):
    index = find_key(key)

    if index == -1:
        print("NULL")
    else:
        print(store[index][1])


def load_database():
    if not os.path.exists(DB_FILE):
        return

    with open(DB_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(" ", 2)

            if len(parts) == 3 and parts[0] == "SET":
                key = parts[1]
                value = parts[2]

                index = find_key(key)

                if index == -1:
                    store.append((key, value))
                else:
                    store[index] = (key, value)


def main():
    load_database()

    while True:
        try:
            command = input().strip()
        except EOFError:
            break

        parts = command.split(" ", 2)

        if parts[0] == "SET" and len(parts) == 3:
            set_value(parts[1], parts[2])

        elif parts[0] == "GET" and len(parts) == 2:
            get_value(parts[1])

        elif parts[0] == "EXIT":
            break


if __name__ == "__main__":
    main()