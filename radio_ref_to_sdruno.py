import csv
import os

# --- Configuration ---

# The name of the input CSV file downloaded from radioreference.com
INPUT_FILENAME = 'ctid_1855_1751041884.csv'

# The name of the output file that will be created.
# You can rename this to .s1b after the script runs.
OUTPUT_FILENAME = 'converted_output.csv'

# List of modulation types to include in the output file.
# SDRPlay supports modes like: 'AM', 'FM', 'NFM', 'WFM', 'CW'
# The script will only process rows from the input file that match these types.
# Note: 'FMN' from the input file is treated as 'NFM'.
ALLOWED_MODULATIONS = ['AM', 'FM', 'NFM']

# --- End of Configuration ---


def convert_file():
    """
    Reads the input CSV file, filters by modulation type, converts the data
    to the .s1b format, and writes it to the output file.
    """
    # Check if the input file exists
    if not os.path.exists(INPUT_FILENAME):
        print(f"Error: Input file '{INPUT_FILENAME}' not found.")
        print("Please make sure the file is in the same directory as the script.")
        return

    # Keep track of row counts
    rows_read = 0
    rows_written = 0

    print(f"Starting conversion of '{INPUT_FILENAME}'...")
    print(f"Including only these modulation types: {', '.join(ALLOWED_MODULATIONS)}")

    # Open the input and output files
    with open(INPUT_FILENAME, mode='r', encoding='utf-8') as infile, \
         open(OUTPUT_FILENAME, mode='w', newline='', encoding='utf-8') as outfile:

        # Use DictReader to easily access columns by their header name
        reader = csv.DictReader(infile)
        
        # Writer for the output CSV file
        writer = csv.writer(outfile)

        # Process each row in the input file
        for row in reader:
            rows_read += 1
            input_mode = row.get('Mode', '').strip()

            # --- Filtering Logic ---
            # Determine the standardized mode for filtering purposes
            standard_mode = ''
            if input_mode in ['FM', 'WFM']:
                standard_mode = 'FM'
            elif input_mode == 'FMN':
                standard_mode = 'NFM'
            elif input_mode == 'AM':
                standard_mode = 'AM'
            # Add other mappings if needed, e.g., 'CW'

            # Skip the row if its modulation type is not in the allowed list
            if standard_mode not in ALLOWED_MODULATIONS:
                continue

            # --- Transformation Logic ---
            try:
                # Column 1: Frequency (convert from MHz to Hz)
                freq_hz = int(float(row['Frequency Output']) * 1_000_000)

                # Column 2: Store Flag (defaulted to 'Y')
                store_flag = 'Y'

                # Column 4: Name/Description
                name = row.get('Description', '')

                # Columns 3 & 6: Mode and Filter
                if standard_mode == 'AM':
                    mode_col3 = 'AM'
                    filter_col6 = 'AM'
                else: # Handles FM, NFM, WFM
                    mode_col3 = 'FM'
                    filter_col6 = 'NFM' # Default to NFM as per the sample file's consistency

                # Columns 5, 7, 8, 9: Default values based on the sample .s1b file
                empty_col5 = ''
                bandwidth_col7 = '12K'
                antenna_col8 = 'AntA'
                empty_col9 = ''

                # Assemble the new row for the .s1b file
                output_row = [
                    freq_hz,
                    store_flag,
                    mode_col3,
                    name,
                    empty_col5,
                    filter_col6,
                    bandwidth_col7,
                    antenna_col8,
                    empty_col9
                ]

                # Write the converted row to the output file
                writer.writerow(output_row)
                rows_written += 1

            except (ValueError, TypeError) as e:
                # This will catch errors if 'Frequency Output' is not a valid number
                print(f"Warning: Skipping row due to data error (row {rows_read + 1}): {e}")
                continue

    print("\n--- Conversion Complete ---")
    print(f"Total rows read: {rows_read}")
    print(f"Rows written to '{OUTPUT_FILENAME}': {rows_written}")

# --- Run the conversion ---
if __name__ == "__main__":
    convert_file()
