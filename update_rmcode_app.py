import os
import subprocess
import sys

# Configuration
REPO_URL = "git@github.com:rmcodebr/rmcode.git"  # Repository SSH URL
REPO_DIR = "/home/rm/www/rmcode"  # Path to your app directory
BRANCH = "main"  # Branch to pull from
VENV_PATH = "/home/rm/venvs/rmcode/bin/activate"  # Path to your virtualenv
GUNICORN_SOCKET = "rmcode_gunicorn.socket"  # Gunicorn socket service name


def run_command(command, cwd=None, use_sudo=False, use_bash=False):
    """Runs a shell command."""
    if use_sudo:
        command = f"sudo {command}"
    if use_bash:
        command = f"bash -c '{command}'"
    result = subprocess.run(command, shell=True, cwd=cwd,
                            capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(result.stdout)
    return result


def clone_or_update_repo():
    """Clones the repository if it doesn't exist, otherwise performs git pull."""
    preserve_files = ["media", "logs", ".env", "update_rmcode_app.py"]

    if os.path.exists(REPO_DIR):
        print(f"Directory {REPO_DIR} exists. Updating repository...")

        # Check for preserved files and move them outside before pulling
        for item in preserve_files:
            item_path = os.path.join(REPO_DIR, item)
            if os.path.exists(item_path):
                subprocess.run(
                    f"mv {item_path} {item_path}_backup", shell=True)

        # Perform git pull if the directory already exists
        os.chdir(REPO_DIR)
        run_command(f"git pull origin {BRANCH}")

        # Restore preserved files
        for item in preserve_files:
            item_path = os.path.join(REPO_DIR, f"{item}_backup")
            if os.path.exists(item_path):
                subprocess.run(
                    f"mv {item_path} {os.path.join(REPO_DIR, item)}", shell=True)
    else:
        print("Directory does not exist. Cloning repository...")
        # Ensure the directory is created
        os.makedirs(REPO_DIR, exist_ok=True)

        # Clone the repository
        run_command(f"git clone -b {BRANCH} {REPO_URL} {REPO_DIR}")

    # Ensure you're in the repository directory
    os.chdir(REPO_DIR)


def install_dependencies():
    """Activates the virtual environment and installs dependencies."""
    print("Installing dependencies...")
    run_command(
        f"source {VENV_PATH} && pip install -r {REPO_DIR}/requirements.txt",
        cwd=REPO_DIR,
        use_bash=True)  # Use bash to execute the command


def collect_static_files():
    """Runs Django's collectstatic command."""
    print("Collecting static files...")
    run_command(
        f"source {VENV_PATH} && python manage.py collectstatic --noinput",
        cwd=REPO_DIR,
        use_bash=True)  # Use bash to execute the command


def restart_gunicorn():
    """Reloads and restarts Gunicorn."""
    print("Reloading and restarting Gunicorn...")
    run_command("systemctl daemon-reload", use_sudo=True)
    run_command(f"systemctl restart {GUNICORN_SOCKET}", use_sudo=True)


def update_app(install_deps=False):
    """Main function to update the app."""
    clone_or_update_repo()

    # Install dependencies only if explicitly told to do so
    if install_deps:
        install_dependencies()

    collect_static_files()
    restart_gunicorn()


if __name__ == "__main__":
    # Check for command-line arguments
    install_deps = "--install-deps" in sys.argv

    # Call update_app with the install_deps flag
    update_app(install_deps=install_deps)
