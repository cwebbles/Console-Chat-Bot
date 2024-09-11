import hashlib
import os
import subprocess
import shutil

# File paths
REQUIREMENTS_FILE = "requirements.txt"
HASH_FILE = ".requirements_hash"
LAYER_ZIP_DIR = "layer_content"
LAYER_CODE_DIR = "python"

def get_file_hash(file_path):
    """Calculate the SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        hasher.update(f.read())
    return hasher.hexdigest()

def save_hash(hash_value, hash_file):
    """Save the hash to a file."""
    with open(hash_file, "w") as f:
        f.write(hash_value)

def load_hash(hash_file):
    """Load the hash from a file, if it exists."""
    if os.path.exists(hash_file):
        with open(hash_file, "r") as f:
            return f.read().strip()
    return None

def remove_packages():
    """Remove all currently installed packages."""
    subprocess.run(["pip", "freeze"], capture_output=True, text=True)
    subprocess.run(["pip", "uninstall", "-y", "-r", REQUIREMENTS_FILE])

def install_packages():
    """Install packages from the requirements file."""
    subprocess.run(["sh", ".\\1-install.sh"])

def packages_dependencies():
    """Packages dependencies"""
    subprocess.run(["sh", ".\\2-package.sh"])
    shutil.make_archive(LAYER_ZIP_DIR, 'zip', LAYER_CODE_DIR)

def clear():
    """Clear extra files"""
    subprocess.run(["rm", "-r", "create_layer"])
    subprocess.run(["rm", "-r", "python"])

def main():
    # Calculate the current hash of the requirements file
    current_hash = get_file_hash(REQUIREMENTS_FILE)
    saved_hash = load_hash(HASH_FILE)

    if current_hash != saved_hash:
        print("Changes detected in requirements.txt. Reinstalling packages...")
        remove_packages()
        install_packages()
        save_hash(current_hash, HASH_FILE)
        packages_dependencies()
        clear()
    else:
        print("No changes detected in requirements.txt. Skipping reinstall.")

if __name__ == "__main__":
    main()
