import subprocess
import os
import shutil

git_dir = os.path.join(os.getcwd(), '.git')

def has_git_initialized():
    return os.path.isdir(git_dir)

git_initialized = has_git_initialized()

def save_git_status():
    if not git_initialized:
        subprocess.run(['git', 'init'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['git', 'add', '.'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def restore_git_status():
    if not git_initialized:
        if has_git_initialized():
            shutil.rmtree(git_dir)

def get_tracked_files():
    save_git_status()
    result = subprocess.run(['git', 'ls-files'], capture_output=True, text=True)
    restore_git_status()
    return result.stdout.strip().split()

def create_tarball(tracked_files, output_filename='tracked_files.tar'):
    if os.path.exists(output_filename):
        os.remove(output_filename)
    for file in tracked_files:
        subprocess.run(['tar', '-rvf', output_filename, file])

def main():
    folder = os.path.basename(os.getcwd())
    tracked_files = [f"{folder}{os.sep}{file}" for file in get_tracked_files()]
    os.chdir('..')
    output = 'standard_lib_checker.tar'
    print("Tracked files:")
    print(tracked_files)

    create_tarball(tracked_files, f"{folder}{os.sep}{output}")
    print(f"All tracked files have been packed into {output}.")

if __name__ == "__main__":
    main()