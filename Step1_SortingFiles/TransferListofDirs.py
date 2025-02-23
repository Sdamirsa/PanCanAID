## THis code will get 
# 1- list of direcotries containing files you want to copy
# 2- Destination that you want to copy these files
# 3- number of levels of folders you want to maintain in your strucutre of folder-trees
# Then it will copy the list of direcotries, each in a new line, to destination wiht the desired structure.


import os
import shutil
from tqdm import tqdm

def main():
    # Prompt user to input directories
    print("Paste the list of directories (each directory on a new line), then press Ctrl+D (Unix) or Ctrl+Z (Windows) and Enter:")
    input_directories = []
    while True:
        try:
            line = input().strip()
            if line:
                input_directories.append(line)
            else:
                break
        except EOFError:
            break

    # Prompt user to input destination directory
    destination = input("Enter the destination directory: ").strip()

    # Create destination directory if it does not exist
    os.makedirs(destination, exist_ok=True)

    # Prompt user to input number of subdirectories to include
    while True:
        try:
            n = int(input("Enter the number of subdirectories to include (N): ").strip())
            if n > 0:
                break
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Please enter a valid integer.")

    # Process each directory
    for dir_path in input_directories:
        try:
            # Check if input directory exists
            if not os.path.exists(dir_path):
                print(f"Directory does not exist: {dir_path}")
                continue

            # Split directory path and take the last N parts
            subdirs = dir_path.split(os.sep)[-n:]

            # Construct new path
            new_path = os.path.join(destination, *subdirs)

            # Create new directory structure
            os.makedirs(new_path, exist_ok=True)
            if os.path.exists(new_path):
                print(f"Directory already exists: {new_path}")
            else:
                print(f"Created directory: {new_path}")

            # Copy files from source directory to new directory
            for file_name in tqdm(os.listdir(dir_path), desc=f'copying from {dir_path} to {new_path}'):
                full_file_name = os.path.join(dir_path, file_name)
                if os.path.isfile(full_file_name):
                    shutil.copy(full_file_name, new_path)

        except Exception as e:
            print(f"Error processing directory: {dir_path}. {str(e)}")

if __name__ == "__main__":
    main()