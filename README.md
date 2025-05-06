# Timeline viewer

Convert Google Maps Timeline location history data to a more usable format and display the data on a map.

# Usage

In terminal or command promt, navigate to the project folder and run the script:

```bash
python src/main.py /path/to/your/Timeline.json -o /path/to/your/output.csv
```

All arguments are optional. By default:
- input file is `Timeline.json`
- output file is `timeline.csv` 

Get full help message with `-h` or `--help` flag:

```bash
python src/main.py -h
```


# Roadmap

1. Reading the data. Code is able to read the Google Maps Timeline JSON data, and extract the most relevant data. To start with we want just the lat and long coordinates of all available times.