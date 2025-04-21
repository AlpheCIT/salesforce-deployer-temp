def read_file(file_path):
    """Read the contents of a file and return it as a string."""
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    """Write the given content to a file."""
    with open(file_path, 'w') as file:
        file.write(content)

def file_exists(file_path):
    """Check if a file exists at the given path."""
    return os.path.isfile(file_path)

def create_directory(directory_path):
    """Create a directory if it does not exist."""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def delete_file(file_path):
    """Delete a file at the given path if it exists."""
    if file_exists(file_path):
        os.remove(file_path)