import json
import csv

file_path = "../Timeline.json"

def main():
    
    with open(file_path) as file:
        # deserialize json file to a python object
        data = json.load(file)

    print(f"Top-level keys: {data.keys()}")
    print(f"Number of 'semantic segments': {len(data['semanticSegments'])}")
    # print(f"First location point: {data['semanticSegments'][0]['timelinePath']}")

    count = 0
    locations = []

    for item in data['semanticSegments']:
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

    with open('../timeline.csv', 'w', newline='') as csvfile:
        csvwriter = csv.DictWriter(csvfile, locations[0].keys())
        csvwriter.writeheader()
        csvwriter.writerows(locations)

if __name__ == "__main__":
    main()
