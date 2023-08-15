import requests
import csv
import time
import math
import datetime


class NFZDataProcessor:
    """Class for processing NFZ data and saving to CSV."""

    def __init__(self):
        """Initialize the NFZDataProcessor class."""
        self.desired_type = "general-data"
        self.file_path = "index_of_tables_data.csv"
        self.wait_time = 0.2

    def load_id_data(self):
        """
        Load and filter ID data from a CSV file.

        Returns:
            list: List of filtered IDs.
        """
        id_data = []
        with open(self.file_path, mode="r", newline="", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if len(row) >= 2 and row[1] == self.desired_type:
                    id_data.append(row[0])
        return id_data

    def fetch_general_data(self, table_id, parameters):
        """
        Fetch general data from NFZ API.

        Args:
            table_id (str): Table ID.
            parameters (dict): Query parameters.

        Returns:
            list: List of dictionaries containing general data.
        """
        url = f'https://api.nfz.gov.pl/app-stat-api-jgp/basic-data/{table_id}'
        response = requests.get(url, params=parameters, timeout=5)
        raw_data = response.json()
        general_data = []
        number_of_pages = math.ceil(raw_data["meta"]['count'] / parameters["limit"] + 1)

        for page in range(1, number_of_pages):
            parameters["page"] = page
            response = requests.get(url, params=parameters, timeout=5)
            raw_data = response.json()
            general_data.extend(raw_data["data"]['attributes']["data"])
            time.sleep(self.wait_time)

        return general_data

    def save_to_csv(self, csv_data, file_path):
        """
        Save data to a CSV file.

        Args:
            csv_data (list): List of dictionaries containing data.
            file_path (str): Path to the CSV file.
        """
        with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
            fieldnames = [
                "year", "branch", "name", "number-of-patients", "number-of-hospitalizations",
                "ratio-of-rehospitalizations", "percentage", "percentage-of-sections",
                "duration-of-hospitalization-mediana", "duration-of-hospitalization-mode",
                "average-value-of-hospitalization", "average-value-of-hospitalization-points",
                "average-value-of-drg", "average-value-of-drg-points"
            ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_data)


def main():
    """Main function to process NFZ data and save to CSV."""
    nfz_processor = NFZDataProcessor()

    id_data = nfz_processor.load_id_data()
    total_elements = len(id_data)
    print(f"Start {datetime.datetime.now()}")

    csv_data = []
    for idx, table_id in enumerate(id_data, 1):
        print(f"Remaining: {total_elements - idx} out of {total_elements}")

        parameters = {
            "branch": "true",
            "hospitalType": "false",
            "limit": 25,
            "format": "json",
            "page": 1,
        }
        general_data = nfz_processor.fetch_general_data(table_id, parameters)

        for item in general_data:
            row = {
                "year": item["year"],
                "branch": item["branch"],
                "name": item["name"],
                "number-of-patients": item["number-of-patients"],
                "number-of-hospitalizations": item["number-of-hospitalizations"],
                "ratio-of-rehospitalizations": item["ratio-of-rehospitalizations"],
                "percentage": item["percentage"],
                "percentage-of-sections": item["percentage-of-sections"],
                "duration-of-hospitalization-mediana": item["duration-of-hospitalization-mediana"],
                "duration-of-hospitalization-mode": item["duration-of-hospitalization-mode"],
                "average-value-of-hospitalization": item["average-value-of-hospitalization"],
                "average-value-of-hospitalization-points": item["average-value-of-hospitalization-points"],
                "average-value-of-drg": item["average-value-of-drg"],
                "average-value-of-drg-points": item["average-value-of-drg-points"]
            }
            csv_data.append(row)

    nfz_processor.save_to_csv(csv_data, "general-data.csv")
    print("CSV data has been successfully saved.")


if __name__ == "__main__":
    main()
