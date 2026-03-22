import os
import subprocess
import hashlib

# Get the absolute path to the root project directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# Clone target directory: <project_root>/clonedProject/repos
BASE_CLONE_DIR = os.path.join(PROJECT_ROOT, "clonedProject", "repos")

# Ensure the directory exists
os.makedirs(BASE_CLONE_DIR, exist_ok=True)


def get_project_folder_name(repo_url):
    hashed = hashlib.sha1(repo_url.encode()).hexdigest()
    return hashed  # ensures unique + filesystem-safe folder names

def get_local_repo_path(repo_url):
    folder_name = get_project_folder_name(repo_url)
    return os.path.join(BASE_CLONE_DIR, folder_name)

def run_git_command(args, cwd=None):
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Git command failed: {' '.join(args)}\n{result.stderr}")
    return result.stdout.strip()

def clone_repo(repo_url, username, pat, branch_name="main"):
    if not os.path.exists(BASE_CLONE_DIR):
        os.makedirs(BASE_CLONE_DIR)

    # Authenticated URL (supports PAT)
    auth_url = repo_url.replace("https://", f"https://{username}:{pat}@")
    local_path = get_local_repo_path(repo_url)

    if not os.path.exists(local_path):
        # Clone specific branch
        run_git_command(["git", "clone", "-b", branch_name, "--single-branch", auth_url, local_path])
    else:
        # Fetch latest updates from origin
        run_git_command(["git", "fetch"], cwd=local_path)

        # Checkout the requested branch
        run_git_command(["git", "checkout", branch_name], cwd=local_path)

        try:
            # Compare local and remote hashes
            local_hash = run_git_command(["git", "rev-parse", "HEAD"], cwd=local_path)
            remote_hash = run_git_command(["git", "rev-parse", "@{u}"], cwd=local_path)

            if local_hash != remote_hash:
                run_git_command(["git", "pull"], cwd=local_path)
        except Exception as e:
            # If upstream tracking info not available, attempt to pull anyway
            run_git_command(["git", "pull", "origin", branch_name], cwd=local_path)

    return local_path  # Final usable path to cloned repo

