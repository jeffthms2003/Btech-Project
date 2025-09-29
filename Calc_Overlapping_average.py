"""FILES SHOULD BE SAVED IN mm_yyyy.nc FORMAT IN THE daily_nc_files folder"""
import xarray as xr
import glob
import os
import pandas as pd

# --- 1. Setup and File Sorting ---
data_directory = 'daily_nc_files/'
file_pattern = os.path.join(data_directory, '*.nc')
file_list_unsorted = glob.glob(file_pattern)

file_list = sorted(
    file_list_unsorted,
    key=lambda f: os.path.basename(f).split('_')[1] + os.path.basename(f).split('_')[0]
)
print("Found and sorted files:")
print(file_list)

# --- 2. Load, Combine, and Select Data ---
variable_name = 'd2m'

print("\nLoading and combining all files into a single dataset...")
# ADDED 'chunks' to manage memory usage efficiently
combined_ds = xr.open_mfdataset(
    file_list,
    combine='by_coords',
    chunks={'valid_time': 10}
)

print("Selecting data from 11th April 2024 to 5th May 2025...")
specific_period_ds = combined_ds.sel(valid_time=slice('2024-04-11', '2025-05-05'))


# --- 3. Calculate the Rolling Average ---
print("Calculating the 7-day rolling average...")
# ADJUSTED: Removed 'center=True' to create a trailing average
rolling_avg_data = specific_period_ds[variable_name].rolling(valid_time=7).mean()

# The .compute() or .load() command is what actually executes the lazy operations
print("Computing the result...")
rolling_avg_data.load() # or .compute()

print("\n--- Rolling Average Calculation Complete ---")
print(rolling_avg_data)


# --- 4. Save the Result While Preserving Global Attributes ---
final_ds = rolling_avg_data.to_dataset(name=variable_name)
final_ds.attrs = combined_ds.attrs
timestamp = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
history_note = f"{timestamp}: Calculated 7-day trailing rolling average. \n"
final_ds.attrs['history'] = history_note + final_ds.attrs.get('history', '')

output_filename = 'dewpoint_7day_trailing_avg.nc'
print(f"\nSaving the result with global attributes to {output_filename}...")
final_ds.to_netcdf(output_filename)

print("\nDone!")