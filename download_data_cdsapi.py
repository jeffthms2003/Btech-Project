"""Change the variable name in line 48"""
import cdsapi
import calendar
from datetime import date

# --- Configuration ---
dataset = "reanalysis-era5-land"
start_date = date(2024, 4, 11)
end_date = date(2025, 5, 5)

# --- Initialize CDS API Client ---
# Make sure your API key is configured in the ~/.cdsapirc file
client = cdsapi.Client()

# --- Loop through each month in the specified timeline ---
year = start_date.year
month = start_date.month

while (year, month) <= (end_date.year, end_date.month):
    
    # Determine the list of days to download for the current month
    if year == start_date.year and month == start_date.month:
        # First month: Start from the specified day
        start_day = start_date.day
        end_day = calendar.monthrange(year, month)[1]
    elif year == end_date.year and month == end_date.month:
        # Last month: End on the specified day
        start_day = 1
        end_day = end_date.day
    else:
        # Intermediate months: Get all days
        start_day = 1
        end_day = calendar.monthrange(year, month)[1]
        
    days = [str(day) for day in range(start_day, end_day + 1)]
    
    # Format the month and year for the request and filename
    month_str = f"{month:02d}"
    year_str = str(year)
    
    # Define the output filename as per "mm_yyyy.zip" format
    target_file = f"{month_str}_{year_str}.zip"
    
    print(f"Requesting data for {month_str}/{year_str}...")
    
    # --- API Request Dictionary ---
    request = {
        "variable": ["surface_pressure"],
        "year": year_str,
        "month": month_str,
        "day": days,
        "time": [
            "00:00", "01:00", "02:00", "03:00", "04:00", "05:00",
            "06:00", "07:00", "08:00", "09:00", "10:00", "11:00",
            "12:00", "13:00", "14:00", "15:00", "16:00", "17:00",
            "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"
        ],
        "data_format": "netcdf",
        "download_format": "zip" # Request data in NetCDF format
    }

    # --- Retrieve and Download Data ---
    client.retrieve(dataset, request).download(target_file)
    
    print(f"Successfully downloaded: {target_file}\n")
    
    # --- Increment to the next month ---
    month += 1
    if month > 12:
        month = 1
        year += 1