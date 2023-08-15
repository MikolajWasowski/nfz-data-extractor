import requests
import csv
import time
import math
import datetime


class NFZHospitalizationProcessor:
    """Class for processing hospitalization data and saving to CSV."""

    def __init__(self):
        """Initialize the NFZHospitalizationProcessor class."""
        self.desired_type = "hospitalization-by-age"
        self.file_path = "index_of_tables_data.csv"
        self.delay_time = 0.2

    def load_id_data(self):
        """
        Load and filter ID data from a CSV file.

        Returns:
            list: List of filtered IDs.
        """
        id_set = set()
        with open(self.file_path, mode="r", newline="", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if len(row) >= 2 and row[1] == self.desired_type:
                    id_set.add(row[0])
        return list(id_set)

    def fetch_hospitalization_data(self, table_id, parameters):
        """
        Fetch hospitalization data from NFZ API.

        Args:
            table_id (str): Table ID.
            parameters (dict): Query parameters.

        Returns:
            list: List of dictionaries containing hospitalization data.
        """
        url = f'https://api.nfz.gov.pl/app-stat-api-jgp/hospitalizations-by-patient-age/{table_id}'
        response = requests.get(url, params=parameters, timeout=4)
        raw_data = response.json()
        hospitalization_data = []
        number_of_pages = math.ceil(raw_data["meta"]['count'] / parameters["limit"] + 1)

        for page in range(1, number_of_pages):
            parameters["page"] = page
            response = requests.get(url, params=parameters, timeout=5)
            raw_data = response.json()
            hospitalization_data.extend(raw_data["data"]["attributes"]["data"])
            time.sleep(self.delay_time)

        return hospitalization_data

    def save_to_csv(self, csv_data, file_path):
        """
        Save data to a CSV file.

        Args:
            csv_data (list): List of dictionaries containing data.
            file_path (str): Path to the CSV file.
        """
        with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
            fieldnames = [
                "year", "branch", "name", "age-group-name",
                "number-of-hospitalizations", "percentage",
                "duration-of-hospitalization-mediana"
            ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_data)


def main():
    """Main function to process hospitalization data and save to CSV."""
    nfz_hospitalization_processor = NFZHospitalizationProcessor()

    id_data = nfz_hospitalization_processor.load_id_data()
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
        hospitalization_data = nfz_hospitalization_processor.fetch_hospitalization_data(table_id, parameters)

        for item in hospitalization_data:
            row = {
                "year": item["year"],
                "branch": item["branch"],
                "name": item["name"],
                "age-group-name": item["age-group-name"],
                "number-of-hospitalizations": item["number-of-hospitalizations"],
                "percentage": item["percentage"],
                "duration-of-hospitalization-mediana": item["duration-of-hospitalization-mediana"],
            }
            csv_data.append(row)

    nfz_hospitalization_processor.save_to_csv(csv_data, "hospitalization-by-age.csv")
    print("CSV data has been successfully saved.")
    print(f"End {datetime.datetime.now()}")


if __name__ == "__main__":
    main()
