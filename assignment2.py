import argparse
import urllib.request
import logging
import datetime
import csv


def downloadData(url):
    """Opens data"""
    try:
        response = urllib.request.urlopen(url)
        lines = [li.decode('utf-8') for li in response.readlines()]
        """Decode data"""
        csvData = csv.reader(lines)
        return csvData
    except urllib.error.URLError as e:
        print(e)
    else:
        pass


logging.basicConfig(filename='error.log', level=logging.ERROR,
                    format='%(message)s'
                    )


def processData(csvData):
    """
    Extracts data and create dictionaries:
        Key = name, Value = Birthday
    """
    next(csvData)
    personData = {}
    for row in csvData:
        try:
            dates = datetime.datetime.strptime(row[2], '%d/%m/%Y').date()
        except ValueError:
            logging.error("Error processing line #{} for ID #{}"
                          .format((int(row[0])+1), row[0])
                          )
        finally:
            personData[row[0]] = [row[1], dates]
    return personData


def displayPerson(id, personData):
    """
    Uses input to display requested data
    """
    while True:
        idin = int(input("Enter ID#: "))
        if idin <= 0:
            print("No user found with that ID")
            break
        else:
            for id, value in personData.items():
                if int(id) == idin:
                    print("Person # {} is {} with a birthday of {}."
                          .format(id, value[0], value[1]))


def main(url):
    print(f"Running main with URL = {url}...")


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str,
                        required=True)
    args = parser.parse_args()
    main(args.url)

file = processData(downloadData(args.url))
displayPerson(id, file)
