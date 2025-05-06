import json
import csv
import argparse

def load_location_data(file_path):
    """Load and return the data from a Google Timeline JSON file."""
    with open(file_path) as file:
        # deserialize json file to a python object
        data = json.load(file)

    print(f"Top-level keys: {data.keys()}")
    print(f"Number of 'semantic segments': {len(data['semanticSegments'])}")
    # print(f"First location point: {data['semanticSegments'][0]['timelinePath']}")

    count = 0
    locations = []

    for item in data['semanticSegments']:
        # skip other segments (activity, visit, timelineMemory) 
        if "timelinePath" not in item:
            continue
        
        for location in item["timelinePath"]:
            coordinate = location["point"].replace("°", "").split(", ")
            locations.append({
                "time": location["time"],
                "lat": coordinate[0],
                "lng": coordinate[1]
            })
        count += 1 

    print(f"Number of 'timelinePath' segments: {count}")
    print(f"Number of location data points: {len(locations)}")
    print(f"First data point:\n{locations[0]}")

    return locations


def write_to_csv(locations, file_path):
    """Write location data to CSV."""
    if not file_path.endswith(".csv"):
        file_path += ".csv"
    with open(file_path, 'w', newline='') as csvfile:
        csvwriter = csv.DictWriter(csvfile, locations[0].keys())
        csvwriter.writeheader()
        csvwriter.writerows(locations)
    print(f"Wrote location data to: {file_path}")


def main():
    
    parser = argparse.ArgumentParser(description="Convert Google Timeline data to a simple CSV file.")
    parser.add_argument("input_json",
                        nargs="?",
                        default="Timeline.json",
                        help="Path to Google Timeline JSON file. Default: Timeline.json")
    parser.add_argument("-o", "--output_csv",
                        default="timeline.csv",
                        help="Path to output CSV file. Overwrites existing file. Default: timeline.csv"
                        )
    args = parser.parse_args()

    locations = load_location_data(args.input_json)
    write_to_csv(locations, args.output_csv)


if __name__ == "__main__":
    main()
