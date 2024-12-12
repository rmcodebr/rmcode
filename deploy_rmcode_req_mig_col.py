import paramiko
import subprocess
import sys

# Define connection details
HOST = '192.168.0.190'
USER = 'rm'
PORT = 22
SSH_KEY_PATH = '/home/rm/.ssh/deploy_pv_ssh_key'  # Path to your SSH private key

# Define paths
LOCAL_APP_PATH = '/home/rm/www/rmcode'  # Local path to your Django app folder
# Remote path where the app will be uploaded
REMOTE_APP_PATH = '/home/rm/www/rmcode'
# Remote requirements.txt path
REQUIREMENTS_PATH = '/home/rm/www/rmcode/requirements.txt'
VENV_PATH = '/home/rm/venvs/rmcode'  # Path to virtual environment


def create_ssh_client(host, port, user, key_path):
    """Create and return an SSH client using SSH key authentication."""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port, username=user, key_filename=key_path)
        return client
    except Exception as e:
        print(f"Failed to create SSH client: {e}")
        raise


def rsync_files(local_path, remote_path):
    """Sync files from the local system to the remote server using rsync."""
    try:
        rsync_command = [
            "rsync",
            "-avz",  # Archive mode (preserves permissions, timestamps, etc.)
            "--delete",  # Delete files on the remote server that no longer exist locally
            "--rsh=ssh",  # Use SSH for remote shell
            # Ensure the trailing slash to copy contents of the directory
            f"{local_path}/",
            f"{USER}@{HOST}:{remote_path}"
        ]
        subprocess.run(rsync_command, check=True)
        print("Files synchronized successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Rsync failed: {e}")
        raise


def run_ssh_command(ssh_client, command):
    """Run a command on the remote server."""
    try:
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        if output:
            print(output)
        if error:
            print(f"Error: {error}")
    except Exception as e:
        print(f"Failed to execute command: {e}")
        raise


def deploy():
    try:
        # Step 1: Create SSH client
        ssh_client = create_ssh_client(HOST, PORT, USER, SSH_KEY_PATH)

        # Step 2: Sync files (upload only changed files and delete old ones)
        print("Syncing files...")
        rsync_files(LOCAL_APP_PATH, REMOTE_APP_PATH)

        # Step 3: Handle optional commands
        if "req" in sys.argv:
            print("Installing requirements...")
            install_requirements = f"source {VENV_PATH}/bin/activate && pip install -r {REQUIREMENTS_PATH}"
            run_ssh_command(
                ssh_client, f"cd {REMOTE_APP_PATH} && {install_requirements}")

        if "mig" in sys.argv:
            print("Running migrations...")
            run_ssh_command(
                ssh_client, f"cd {REMOTE_APP_PATH} && source {VENV_PATH}/bin/activate && python manage.py makemigrations")
            run_ssh_command(
                ssh_client, f"cd {REMOTE_APP_PATH} && source {VENV_PATH}/bin/activate && python manage.py migrate")

        if "col" in sys.argv:
            print("Collecting static files...")
            run_ssh_command(
                ssh_client, f"cd {REMOTE_APP_PATH} && source {VENV_PATH}/bin/activate && python manage.py collectstatic --noinput")

        # Step 4: Reload daemon and restart Gunicorn socket
        print("Reloading daemon and restarting Gunicorn socket...")
        run_ssh_command(ssh_client, 'sudo systemctl daemon-reload')
        run_ssh_command(
            ssh_client, 'sudo systemctl restart pv_gunicorn.socket')
        run_ssh_command(
            ssh_client, 'sudo systemctl restart pv_gunicorn.service')

        print("Deployment completed successfully.")

    except Exception as e:
        print(f"Deployment failed: {e}")

    finally:
        ssh_client.close()


if __name__ == "__main__":
    # Check if no arguments are passed
    if len(sys.argv) == 1:
        print("No specific commands provided. Syncing files and restarting Gunicorn.")
        deploy()  # Only sync files and restart services
    else:
        deploy()
