import xarray as xr
import os
import glob
from datetime import datetime

# --- User Configuration ---
# Set the path to the directory containing your month folders (e.g., 'April_2024').
# Use '.' if the script is in the same directory as the month folders.
base_directory = '.'
# --- End of Configuration ---


def combine_daily_netcdf_files():
    """
    Finds monthly subdirectories, combines the daily .nc files within each,
    and saves a new monthly .nc file, preserving global attributes.
    """
    print("Starting the process...")

    # Find all subdirectories in the base directory
    try:
        subdirectories = [d for d in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, d))]
    except FileNotFoundError:
        print(f"❌ Error: The base directory '{os.path.abspath(base_directory)}' was not found.")
        return

    if not subdirectories:
        print("❌ Error: No monthly data folders found in the specified directory.")
        return

    print(f"✅ Found {len(subdirectories)} month folders to process.")

    # Loop through each monthly folder
    for folder_name in subdirectories:
        folder_path = os.path.join(base_directory, folder_name)
        print(f"\n--- Processing folder: {folder_name} ---")

        # Step 1: Find all daily NetCDF files in the folder
        search_pattern = os.path.join(folder_path, '*.nc')
        daily_files = glob.glob(search_pattern)

        if not daily_files:
            print(f"⚠️ Warning: No .nc files found in '{folder_name}'. Skipping.")
            continue

        # Step 2: Sort files chronologically based on filename (dd_mm_yyyy.nc)
        try:
            # The key extracts the date from the filename and converts it to a datetime object for robust sorting
            sorted_files = sorted(daily_files, key=lambda f: datetime.strptime(os.path.basename(f).replace('.nc', ''), '%d_%m_%Y'))
            print(f"Found and sorted {len(sorted_files)} daily files.")
        except ValueError:
            print(f"❌ Error: Could not parse date from filenames in '{folder_name}'. Ensure they are in 'dd_mm_yyyy.nc' format. Skipping.")
            continue

        # Step 3: Combine all sorted daily files into a single xarray Dataset
        print("Combining files...")
        # 'combine="by_coords"' merges files based on their coordinates, which is perfect for time series data.
        combined_ds = xr.open_mfdataset(sorted_files, combine='by_coords')

        # Step 4: Preserve global attributes from the first daily file
        print("Preserving global attributes...")
        with xr.open_dataset(sorted_files[0]) as first_ds:
            # Copy the attributes from the first file to the new combined dataset
            combined_ds.attrs = first_ds.attrs

        # Step 5: Create the output filename (mm_yyyy.nc) and save the result
        try:
            # Extract month and year from the folder name (e.g., "April_2024")
            month_name, year_str = folder_name.split('_')
            month_num = datetime.strptime(month_name, '%B').month
            output_filename = f"{month_num:02d}_{year_str}.nc"
            output_path = os.path.join(base_directory, output_filename)

            print(f"💾 Saving combined file to: {output_path}")
            combined_ds.to_netcdf(output_path)
            print("✨ Success!")

        except Exception as e:
            print(f"❌ Error creating output file for '{folder_name}': {e}")

        # Clean up by closing the dataset
        combined_ds.close()

    print("\nProcess complete.")


if __name__ == "__main__":
    combine_daily_netcdf_files()