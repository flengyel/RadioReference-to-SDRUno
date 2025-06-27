import csv
import os
import argparse

def convert_file(input_filename, output_filename, allowed_modulations, ham_only, add_callsign):
    """
    Reads the input CSV file from radioreference.com, filters and transforms the data
    based on user-provided arguments, and writes it to an SDRUno-compatible .s1b file.

    Args:
        input_filename (str): The path to the input CSV file.
        output_filename (str): The path for the output .s1b file.
        allowed_modulations (list): A list of modulation types (e.g., ['AM', 'NFM']) to include.
        ham_only (bool): If True, only include rows related to amateur radio.
        add_callsign (bool): If True, append the callsign to the description field.
    """
    if not os.path.exists(input_filename):
        print(f"Error: Input file '{input_filename}' not found.")
        return

    rows_read = 0
    rows_written = 0

    print(f"Starting conversion of '{input_filename}'...")
    print(f"Output will be written to '{output_filename}'")
    if allowed_modulations:
        print(f"Including only these modulation types: {', '.join(allowed_modulations)}")
    if ham_only:
        print("Filtering for Amateur Radio frequencies only.")
    if add_callsign:
        print("Appending callsign to the description field.")

    with open(input_filename, mode='r', encoding='utf-8') as infile, \
         open(output_filename, mode='w', newline='', encoding='utf-8') as outfile:

        reader = csv.DictReader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            rows_read += 1
            input_mode = row.get('Mode', '').strip()
            
            # --- Filtering Logic ---

            # Filter for Amateur Radio if specified
            if ham_only and 'Ham' not in row.get('Tag', ''):
                continue

            # Standardize modulation mode
            standard_mode = ''
            if input_mode in ['FM', 'WFM']:
                standard_mode = 'FM'
            elif input_mode == 'FMN':
                standard_mode = 'NFM'
            elif input_mode == 'AM':
                standard_mode = 'AM'
            
            # Skip if modulation is not in the allowed list
            if allowed_modulations and standard_mode not in allowed_modulations:
                continue

            # --- Transformation Logic ---
            try:
                freq_hz = int(float(row['Frequency Output']) * 1_000_000)
                
                name = row.get('Description', '')
                if add_callsign:
                    callsign = row.get('FCC Callsign', '').strip()
                    if callsign:
                        name = f"{name} {callsign}"

                if standard_mode == 'AM':
                    mode_col3 = 'AM'
                    filter_col6 = 'AM'
                else:
                    mode_col3 = 'FM'
                    filter_col6 = 'NFM'

                output_row = [
                    freq_hz,
                    'Y',
                    mode_col3,
                    name,
                    '',
                    filter_col6,
                    '12K',
                    'AntA',
                    ''
                ]

                writer.writerow(output_row)
                rows_written += 1

            except (ValueError, TypeError) as e:
                print(f"Warning: Skipping row due to data error (row {rows_read + 1}): {e}")
                continue

    print("\n--- Conversion Complete ---")
    print(f"Total rows read: {rows_read}")
    print(f"Rows written to '{output_filename}': {rows_written}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a RadioReference.com CSV file to an SDRUno .s1b format.",
        epilog="Example: python radio_ref_to_sdruno.py -i my_freqs.csv -o sdr_import.s1b -m AM NFM --ham-only --add-callsign"
    )
    
    parser.add_argument(
        '-i', '--input-file',
        dest='input_filename',
        required=True,
        help="The input CSV file downloaded from radioreference.com."
    )
    
    parser.add_argument(
        '-o', '--output-file',
        dest='output_filename',
        required=True,
        help="The name of the output .s1b file to be created."
    )
    
    parser.add_argument(
        '-m', '--modulation',
        dest='allowed_modulations',
        nargs='+',
        choices=['AM', 'FM', 'NFM'],
        default=['AM', 'FM', 'NFM'],
        help="One or more modulation types to include. SDRUno supports AM, FM, NFM. Default is all."
    )
    
    parser.add_argument(
        '--ham-only',
        dest='ham_only',
        action='store_true',
        help="Include this flag to process only amateur radio frequencies."
    )
    
    parser.add_argument(
        '--add-callsign',
        dest='add_callsign',
        action='store_true',
        help="Include this flag to append the FCC callsign to the description field."
    )

    args = parser.parse_args()
    
    convert_file(
        args.input_filename,
        args.output_filename,
        args.allowed_modulations,
        args.ham_only,
        args.add_callsign
    )
    