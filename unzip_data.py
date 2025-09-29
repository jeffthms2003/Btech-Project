"""THE ZIPPED DATA SHOULD BE IN zip_files AND THE UNZIPPED FILES WILL BE STORED TO extracted_nc_files"""
import os
import zipfile

# --- Configuration ---
# 1. Set the path to the folder containing your zip files.
source_directory = "zip_files"

# 2. Set the path where you want to save the extracted .nc files.
destination_directory = "extracted_nc_files"
# --- End of Configuration ---

# Ensure the destination directory exists
os.makedirs(destination_directory, exist_ok=True)

print(f"Searching for zip files in '{source_directory}'...")

# Loop through every file in the source directory
for filename in os.listdir(source_directory):
    # Check if the file is a .zip file
    if filename.endswith(".zip"):
        print(f"Processing '{filename}'...")
        
        # Construct the full path to the zip file
        zip_path = os.path.join(source_directory, filename)
        
        try:
            # Open the zip file in read mode
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Extract the specific member 'data_0.nc' to the destination
                zip_ref.extract("data_0.nc", path=destination_directory)
                
                # --- Renaming Logic ---
                # Path of the file after extraction
                extracted_file_path = os.path.join(destination_directory, "data_0.nc")
                
                # Create the new filename by replacing the .zip extension with .nc
                base_name = os.path.splitext(filename)[0]  # This gets "01_2025" from "01_2025.zip"
                new_filename = f"{base_name}.nc"
                new_file_path = os.path.join(destination_directory, new_filename)
                
                # Rename the extracted file
                os.rename(extracted_file_path, new_file_path)
                
                print(f"  -> Extracted and saved as '{new_filename}'")

        except KeyError:
            print(f"  -> ERROR: 'data_0.nc' was not found inside '{filename}'.")
        except FileExistsError:
            print(f"  -> ERROR: The file '{new_filename}' already exists. Skipping.")
        except Exception as e:
            print(f"  -> An unexpected error occurred: {e}")

print("\nExtraction process complete. ✨")