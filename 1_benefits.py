import requests
import csv


class NFZAPI:
    """Class for managing NFZ API requests and data processing."""

    def __init__(self):
        """Initialize the NFZAPI class."""
        self.url = f'https://api.nfz.gov.pl/app-stat-api-jgp/benefits/'
        self.parameters = {
            "benefit": "",
            "catalog": "1a",
            "limit": 25,
            "format": "json",
            "page": 1
        }

    def get_benefits_data(self):
        """
        Get benefits data from NFZ API.

        Returns:
            dict: JSON response containing benefits data.
        """
        response = requests.get(self.url, params=self.parameters)
        return response.json()

    def get_number_of_pages(self):
        """
        Calculate the number of pages for pagination.

        Returns:
            int: Number of pages.
        """
        benefits_data = self.get_benefits_data()
        return benefits_data["meta"]['count'] // self.parameters["limit"] + 1

    def get_cleaned_name(self, name):
        """
        Clean and format the benefit name.

        Args:
            name (str): Raw benefit name.

        Returns:
            str: Cleaned benefit name.
        """
        return name.replace("*", "").strip()

    def save_to_csv(self, csv_data, file_path):
        """
        Save data to a CSV file.

        Args:
            csv_data (list): List of dictionaries containing data.
            file_path (str): Path to the CSV file.
        """
        with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
            fieldnames = ["name"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_data)


def main():
    """Main function to fetch NFZ API data and save to CSV."""
    nfz_api = NFZAPI()

    csv_data = []
    number_of_pages = nfz_api.get_number_of_pages()
    for page in range(1, number_of_pages):
        nfz_api.parameters["page"] = page
        benefits_data = nfz_api.get_benefits_data()
        for item in benefits_data["data"]:
            row = {
                "name": nfz_api.get_cleaned_name(item['name']),
            }
            csv_data.append(row)

    file_path = "benefits_data.csv"
    nfz_api.save_to_csv(csv_data, file_path)
    print("CSV data has been successfully saved to", file_path)


if __name__ == "__main__":
    main()
