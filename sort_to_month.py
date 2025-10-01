import os
import glob
import shutil
from datetime import datetime

# --- Configuration ---
# The top-level directory where the month folders ('April', 'May', etc.) are located.
# Use '.' for the current directory.
base_directory = '.'
# --- End of Configuration ---

def resort_files_by_month_and_year(directory):
    """
    Finds .nc files inside subdirectories, re-sorts them into new folders
    named 'Month_Year', and cleans up the old, empty directories.
    """
    # The pattern finds files like './April/11_04_2024.nc'
    # The '**' part searches through all subdirectories.
    file_pattern = os.path.join(directory, '**', '??_??_????.nc')
    
    # Use recursive=True to search in subfolders
    files_to_resort = glob.glob(file_pattern, recursive=True)

    if not files_to_resort:
        print("No files matching the 'dd_mm_yyyy.nc' format were found in any subdirectories.")
        return

    print(f"Found {len(files_to_resort)} file(s) to re-sort. Starting process...\n")
    
    # Keep track of the original directories to check for cleanup later
    original_directories = set()

    for filepath in files_to_resort:
        try:
            # Store the parent directory (e.g., './April') for the cleanup step
            parent_dir = os.path.dirname(filepath)
            original_directories.add(parent_dir)

            # --- Determine the new folder name ---
            filename = os.path.basename(filepath)
            date_string = filename.split('.nc')[0]
            date_object = datetime.strptime(date_string, '%d_%m_%Y')
            
            # This is the key change: format the folder name as 'Month_YYYY'
            new_folder_name = date_object.strftime('%B_%Y')
            
            # --- Move the file ---
            # Create the new target directory at the base level (e.g., './April_2024')
            target_dir = os.path.join(directory, new_folder_name)
            os.makedirs(target_dir, exist_ok=True)
            
            # Define the final destination path for the file
            destination_path = os.path.join(target_dir, filename)
            
            shutil.move(filepath, destination_path)
            
            print(f"✅ Moved '{filename}'  ->  '{new_folder_name}/'")

        except ValueError:
            print(f"⚠️ Skipping '{filename}': name does not match 'dd_mm_yyyy.nc' format.")
        except Exception as e:
            print(f"❌ An error occurred with '{filename}': {e}")
    
    # --- Cleanup Step ---
    print("\n--- Cleaning up old, empty directories ---")
    # Sort the list for a clean, predictable output
    for old_dir in sorted(list(original_directories)):
        try:
            # os.listdir() will be empty if only files were in it and we moved them all
            if not os.listdir(old_dir):
                os.rmdir(old_dir)
                print(f"🗑️  Removed empty directory: '{old_dir}'")
        except OSError as e:
            # This handles cases where the directory might not be empty (e.g., hidden files)
            print(f"Could not remove '{old_dir}': {e}")

# Run the re-sorting function
if __name__ == "__main__":
    resort_files_by_month_and_year(base_directory)
    print("\nRe-sorting process finished!")