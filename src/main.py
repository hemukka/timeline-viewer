import os
import json
import csv
import argparse
from datetime import date
import folium
from folium.plugins import HeatMap, HeatMapWithTime, FastMarkerCluster, Draw
from statistics import median

def load_location_data(file_path, start_date, end_date):
    """Load and return the data from a Google Timeline JSON file."""
    try:
        with open(file_path, encoding="utf-8") as file:
            # deserialize json file to a python object
            data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"JSON decoding failed:\n{e}")
        raise SystemExit # same as sys.exit()

    if "semanticSegments" not in data:
        raise Exception("Timeline file doesn't contain any semantic segments.")

    print(f"Top-level keys: {data.keys()}")
    print(f"Number of 'semantic segments': {len(data['semanticSegments'])}")
    # print(f"First location point: {data['semanticSegments'][0]['timelinePath']}")

    start = date.fromordinal(1)
    end = date.today()
    if start_date:
        start = date.fromisoformat(start_date)
    if end_date:
        end = date.fromisoformat(end_date)
    print(f"Extracting data from {start} to {end}")

    count = 0
    locations = []

    for item in data['semanticSegments']:
        # skip other segments (activity, visit, timelineMemory) 
        if "timelinePath" not in item:
            continue
        # from timelinePath segment, grab time, lat, and lon from all points
        for location in item["timelinePath"]:
            if not (start <= date.fromisoformat(location["time"].split("T")[0]) <= end):
                continue
            coordinate = location["point"].replace("°", "").split(", ")
            locations.append({
                "time": location["time"],
                "lat": coordinate[0],
                "lng": coordinate[1]
            })
        count += 1 

    print("Extracted data:")
    print(f"- Number of 'timelinePath' segments: {count}")
    print(f"- Number of location data points: {len(locations)}")
    print(f"- First data point:\n{locations[0]}")

    return locations


def write_to_csv(locations:list[dict], file_path:str):
    """Write location data to CSV."""
    if not file_path.endswith((".csv", ".CSV")):
        file_path += ".csv"
    with open(file_path, 'w', newline='') as csvfile:
        csvwriter = csv.DictWriter(csvfile, locations[0].keys())
        csvwriter.writeheader()
        csvwriter.writerows(locations)
    print(f"Wrote location data to: {file_path}")


def create_interactive_map(locations, raw_points=False):
    """Create html file with interactive map displaying the location data."""

    avg_lat = median(float(point["lat"]) for point in locations)
    avg_lon = median(float(point["lng"]) for point in locations)

    map = folium.Map(
        location=[avg_lat, avg_lon],
        zoom_start=5,
        prefer_canvas=True, #use canvas rather than DOM for better performance with many points
    )

    # create circle markers for all data points
    if raw_points:
        fg_points = folium.FeatureGroup("all points")
        for point in locations:
            fg_points.add_child(folium.CircleMarker(
                (float(point["lat"]), float(point["lng"])),
                radius=1,
                popup=point["time"]
            ))
        map.add_child(fg_points)


    points = [(float(point["lat"]), float(point["lng"])) for point in locations]

    # create line through all data points
    # fg_lines = folium.FeatureGroup(name="location line").add_child(
    #     folium.PolyLine(points)
    # )
    # map.add_child(fg_lines)

    # create clustered cicrle markers, that are fast to genereate
    # callback = ('function (row) {' 
    #             'var circle = L.circleMarker(new L.LatLng(row[0], row[1]), {color: "red",  radius: 2});'
    #             'return circle};')
    # FastMarkerCluster(points, name="clusters", callback=callback).add_to(map)

    # create heatmap from all data points
    HeatMap(
        points,
        name="heatmap",
        min_opacity=0.6,
        radius=4,
        blur=4,
        gradient=({"0.4": "blue", "0.6": "cyan", "0.7": "lime", "0.8": "yellow", "1.0": "red"}),
    ).add_to(map)

    # create scrolling "heatmap" from all data points
    # points needs to be a list of list of points
    points = []
    for point in locations:
        points.append([[float(point["lat"]), float(point["lng"])]])
    HeatMapWithTime(
        points,
        index=[point["time"] for point in locations],
        name="heatmap with time",
        radius=15,
        min_speed=10,
        max_speed=200,
        speed_step=10,
        min_opacity=0.9, # type: ignore
    ).add_to(map)

    Draw().add_to(map)

    folium.LayerControl().add_to(map)

    if not os.path.exists("map"):
        os.makedirs("map")
    map.save("map/index.html")
    print(f"Map created in: map/index.html")


def main():
    
    # setup command-line parsing
    parser = argparse.ArgumentParser(description="Convert Google Timeline data to a simple CSV file.")
    parser.add_argument("input_json",
                        nargs="?",
                        default="Timeline.json",
                        help="Path to Google Timeline JSON file. Default: Timeline.json")
    parser.add_argument("-o", "--output_csv",
                        default="timeline.csv",
                        help="Path to output CSV file. Overwrites existing file. Default: timeline.csv"
                        )
    parser.add_argument("-s", "--start_date",
                        help="Filter extracted data to this date and after. Must be YYYY-MM-DD.")
    parser.add_argument("-e", "--end_date",
                        help="Filter extracted data to this date and before. Must be YYYY-MM-DD.")                    
    parser.add_argument("-r", "--raw_points",
                        action="store_true",
                        help="Draw all locations as points on the map. Can be slow to generate with many locations.")
    args = parser.parse_args()

    if not os.path.isfile(args.input_json):
        print(f"'{os.path.abspath(args.input_json)}' file not found.")
        return
    if os.path.splitext(args.input_json)[1].lower() != ".json":
        print(f"Input file is not a JSON file: '{args.input_json}'")
        return

    locations = load_location_data(args.input_json, args.start_date, args.end_date)
    write_to_csv(locations, args.output_csv)

    create_interactive_map(locations, args.raw_points)


if __name__ == "__main__":
    main()
