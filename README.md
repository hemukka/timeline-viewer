# Timeline viewer

Convert Google Maps Timeline location history data to a more usable format and display the data on a map.

# Usage

These commands are for WSL/Ubuntu and may be different on other systems.

0. Install Python if not already. The code has been tested on version 3.12.3.

1. Download this repo.

2. Recommended but optional to create a virtual environment. One option for this is `venv`.

Create virtual environment:

```bash
python -m venv venv
```

Active the virtual environment:

```bash
source venv/bin/activate
```

3. Install the required packages listed in `requirements.txt`.

```bash
pip install -r requirements
```

4. In terminal or command promt, navigate to the project folder and run the script:

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

2. Save the most relevant data as CSV file.

3. Display the data on a map.

4. Ability to limit the time window that will be extracted.