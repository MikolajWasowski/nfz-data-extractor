import requests
import csv
import time
import datetime


class NFZDataExtractor:
    """Class for extracting NFZ data from API and saving to CSV."""

    def __init__(self):
        """Initialize the NFZDataExtractor class."""
        self.url = 'https://api.nfz.gov.pl/app-stat-api-jgp/index-of-tables'
        self.file_path = "benefits_data.csv"
        self.wait_time = 0.2

    def load_benefits_list(self):
        """
        Load and clean the benefits list from a CSV file.

        Returns:
            list: List of cleaned benefits.
        """
        with open(self.file_path, mode='r', encoding='utf-8-sig') as file:
            data_file = file.readlines()

        benefits_list = [item.strip() for item in data_file]
        return list(set(benefits_list))

    def fetch_tables_data(self, benefit, year, catalog):
        """
        Fetch tables data from NFZ API.

        Args:
            benefit (str): Benefit name.
            year (int): Year.
            catalog (str): Catalog.

        Returns:
            list: List of dictionaries containing table data.
        """
        try:
            parameters = {
                "catalog": catalog,
                "name": benefit,
                "year": year
            }
            response = requests.get(self.url, params=parameters, timeout=5)
            index_tables_data = response.json()
            tables = index_tables_data["data"]["attributes"]['years'][0]["tables"]
            table_data = []
            for i in tables:
                if i["type"] in ["general-data", "hospitalization-by-age"]:
                    row = {
                        "table_id": i["id"],
                        "table_type": i["type"]
                    }
                    table_data.append(row)
            return table_data
        except TypeError as e:
            return []
        except requests.exceptions.ConnectTimeout:
            return []

    def save_to_csv(self, csv_data, file_path):
        """
        Save data to a CSV file.

        Args:
            csv_data (list): List of dictionaries containing data.
            file_path (str): Path to the CSV file.
        """
        with open(file_path, mode='a', newline='', encoding='utf-8-sig') as file:
            fieldnames = ["table_id", "table_type"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerows(csv_data)


def main():
    """Main function to extract NFZ data and save to CSV."""
    nfz_extractor = NFZDataExtractor()
    print(f"Start {datetime.datetime.now()}")
    benefits_list = nfz_extractor.load_benefits_list()
    for idx, benefit in enumerate(benefits_list, 1):
        for year in [2019, 2020]:
            for catalog in ["1a", "1b", "1c", "1d", "1w"]:
                table_data = nfz_extractor.fetch_tables_data(benefit, year, catalog)
                nfz_extractor.save_to_csv(table_data, nfz_extractor.file_path)

                # Display remaining elements and add delay
                remaining_elements = len(benefits_list) - idx
                total_elements = len(benefits_list)
                print(f"Remaining: {remaining_elements} out of {total_elements}")
                time.sleep(nfz_extractor.wait_time)

    print("CSV data has been successfully saved.")
    print(f"End {datetime.datetime.now()}")


if __name__ == "__main__":
    main()
