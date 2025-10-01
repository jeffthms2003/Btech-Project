import os
import glob
import xarray as xr
import pandas as pd

# --- Configuration ---
# Directory where your .nc files are located.
# Use '.' for the current directory.
file_directory = '.'
# --- End of Configuration ---

def rename_netcdf_files(directory):
    """
    Renames NetCDF files in a given directory from their original name
    to a 'dd_mm_yyyy.nc' format based on the 'valid_time' coordinate.
    """
    # Create a pattern to find all files ending with .nc
    file_pattern = os.path.join(directory, '*.nc')
    
    # Get a list of all NetCDF files in the directory
    netcdf_files = glob.glob(file_pattern)

    if not netcdf_files:
        print("No .nc files found in the specified directory.")
        return

    print(f"Found {len(netcdf_files)} NetCDF file(s). Starting renaming process...\n")

    for original_filepath in netcdf_files:
        try:
            # Open the dataset using a 'with' statement to ensure it's properly closed
            with xr.open_dataset(original_filepath) as xrds:
                # Extract the first timestamp from the 'valid_time' variable
                # Since all times in the file are for the same day, the first one is sufficient
                first_time_stamp = xrds['valid_time'].values[0]

                # Convert the numpy datetime64 object to a pandas Timestamp for easy formatting
                date_object = pd.to_datetime(first_time_stamp)
                
                # Format the date into the desired 'dd_mm_yyyy' string
                new_date_str = date_object.strftime('%d_%m_%Y')
                
                # Construct the new filename and path
                new_filename = f"{new_date_str}.nc"
                new_filepath = os.path.join(directory, new_filename)
                
                # Get just the filename for cleaner print statements
                original_filename = os.path.basename(original_filepath)

                # Check if a file with the new name already exists to avoid overwriting
                if os.path.exists(new_filepath):
                    print(f"Skipping '{original_filename}': a file named '{new_filename}' already exists.")
                    continue
                
                print(f"Renaming '{original_filename}' -> '{new_filename}'")

            # Rename the actual file on the disk
            os.rename(original_filepath, new_filepath)

        except KeyError:
            print(f"Skipping '{os.path.basename(original_filepath)}': Variable 'valid_time' not found.")
        except Exception as e:
            print(f"An error occurred with file '{os.path.basename(original_filepath)}': {e}")

    print("\nProcess finished.")

# Run the function
if __name__ == "__main__":
    rename_netcdf_files(file_directory)