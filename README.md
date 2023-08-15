# NFZ Data Extractor

This project aims to extract and analyze healthcare-related data from the Polish National Health Fund (NFZ) API. The data extracted includes various statistics and information related to medical services, hospitalizations, patient demographics, and more.

## Project Overview

The NFZ Data Extractor utilizes Python and the `requests` library to query the [NFZ API](https://api.nfz.gov.pl/app-stat-api-jgp/#swagger) and retrieve relevant data. The extracted data is then processed and saved in CSV format for further analysis.

The primary objectives of this project are:
- Retrieve medical statistics and information for the year 2020.
- Extract data types such as hospitalizations by age, general medical data, and other relevant categories.
- Store the extracted data in CSV files for further analysis.

## Features

- Data Extraction: Utilize API queries to fetch healthcare-related data from the NFZ API.
- Data Processing: Process the retrieved data and store it in CSV files for analysis.
- Multiple Categories: Extract various data categories such as hospitalizations by age, general medical data, etc.

## Usage

1. Clone this repository to your local machine.
2. Install the required Python packages using `pip install -r requirements.txt`.
3. Modify the parameters in the code to customize your data extraction.
4. Run the Python scripts to extract and save the data.

## Contributing

Contributions to this project are welcome! If you have any ideas, suggestions, or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- Data source: [NFZ API](https://api.nfz.gov.pl/app-stat-api-jgp/#swagger)
- Python libraries used: `requests`, `csv`, `datetime`, `time`, `math`
