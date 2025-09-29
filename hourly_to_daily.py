"""PLEASE CREATE 2 FOLDERS hourly_nc_files(with the downloaded data where the hourly data is stored in monthly manner) and daily_nc_files
(where the required daily data is stored) """
import xarray as xr
import os
import glob

# --- Configuration ---
# Directory containing your monthly hourly .nc files
input_directory = "hourly_nc_files"

# Directory where the new daily .nc files will be saved
output_directory = "daily_nc_files"
# --- End of Configuration ---

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Find all NetCDF files in the input directory
nc_files = glob.glob(os.path.join(input_directory, '*.nc'))

if not nc_files:
    print(f"Error: No .nc files found in '{input_directory}'. Please check the path.")
else:
    print(f"Found {len(nc_files)} files to process...")

# Loop through each file
for file_path in nc_files:
    try:
        with xr.open_dataset(file_path) as ds:
            print(f"\nProcessing '{os.path.basename(file_path)}'...")

            # --- The Core Conversion Step (MODIFIED LINE) ---
            # Resample using your 'valid_time' dimension
            daily_ds = ds.resample(valid_time='D').mean()

            # Copy the global attributes from the original file to the new one
            daily_ds.attrs = ds.attrs
            
            # Construct the output filename
            base_name = os.path.basename(file_path)
            output_name = f"{os.path.splitext(base_name)[0]}_daily.nc"
            output_path = os.path.join(output_directory, output_name)
            
            # Save the new daily dataset to a NetCDF file
            daily_ds.to_netcdf(output_path)
            
            print(f"  -> Successfully converted and saved to '{output_path}'")

    except Exception as e:
        print(f"  -> Failed to process {os.path.basename(file_path)}. Error: {e}")

print("\nConversion complete! ✨")