import os


def create_test_files(folder_path):
    os.makedirs(folder_path, exist_ok=True)

    extensions = ["txt", "jpg", "png", "pdf"]
    for i in range(100):
        for ext in extensions:
            file_path = os.path.join(folder_path, f"file_{i}.{ext}")
            with open(file_path, "w") as f:
                f.write(f"Test content for file {i} with extension {ext}")


if __name__ == "__main__":
    create_test_files("hw_5/test_source")
