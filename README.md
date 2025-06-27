# RadioReference to SDRUno Converter

This script converts CSV files downloaded from radioreference.com into the `.s1b` bank file format used by SDRUno software. It allows for filtering by modulation type and amateur radio frequencies, and can automatically append call signs to the frequency descriptions.

## Features

- Converts radioreference.com CSV files to SDRUno `.s1b` format.
- Command-line interface for specifying input and output files.
- Filter frequencies by modulation type (AM, FM, NFM).
- Option to include only amateur radio frequencies.
- Option to append the FCC callsign to the description of each frequency.

## Prerequisites

- Python 3.x

## Usage

You can run the script from your terminal. Use the `-h` or `--help` flag to see all available options.

```bash
python radio_ref_to_sdruno.py -h
```

### Basic Conversion

To convert a file, you must specify the input and output file paths.

```bash
python radio_ref_to_sdruno.py -i ctid_1855_1751041884.csv -o my_sdr_bank.s1b
```

### Filtering by Modulation

To include only specific modulation types (e.g., `AM` and `NFM`), use the `-m` flag.

```bash
python radio_ref_to_sdruno.py -i ctid_1855_1751041884.csv -o am_nfm_only.s1b -m AM NFM
```

### Filtering for Ham Radio Frequencies

Use the `--ham-only` flag to create a bank file containing only amateur radio frequencies. This filter works by checking if the "Tag" column in the input CSV contains the word "Ham".

```bash
python radio_ref_to_sdruno.py -i ctid_1855_1751041884.csv -o ham_frequencies.s1b --ham-only
```

### Adding the Callsign

Use the `--add-callsign` flag to append the `FCC Callsign` from the input file to the end of the frequency description.

```bash
python radio_ref_to_sdruno.py -i ctid_1855_1751041884.csv -o with_callsigns.s1b --add-callsign
```

### Combined Example

You can combine these options. The following example creates a file with only AM amateur radio frequencies and appends their call signs.

```bash
python radio_ref_to_sdruno.py -i ctid_1855_1751041884.csv -o ham_am_with_callsigns.s1b -m AM --ham-only --add-callsign
```

## Input and Output File Formats

### Input File (radioreference.com CSV)

The script expects a CSV file with headers, containing at least the following columns:

- `Frequency Output`
- `Description`
- `Mode`
- `FCC Callsign` (optional, used with `--add-callsign`)
- `Tag` (optional, used with `--ham-only`)

### Output File (.s1b)

The script generates a CSV file that is compatible with the SDRUno bank import feature. Although it has a `.s1b` extension, it is a plain text CSV file with the following columns:

1. **Frequency (Hz):** The frequency in Hertz.
2. **Store Flag:** Defaults to 'Y'.
3. **Mode:** The demodulation mode (e.g., 'AM', 'FM').
4. **Name/Description:** A description of the frequency.
5. **Empty Column:** An empty field.
6. **Filter:** The filter bandwidth (e.g., 'AM', 'NFM').
7. **Bandwidth:** Defaults to '12K'.
8. **Antenna:** Defaults to 'AntA'.
9. **Empty Column:** An empty field.

