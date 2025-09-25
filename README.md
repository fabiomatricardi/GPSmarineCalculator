# GPS Distance Calculator (Advanced) Documentation

---

## Packages Requirements

This application uses several Python packages to provide its functionality. To run the app successfully, ensure the following packages are installed:

```bash
pip install tkinter geopy folium
```

> **Note:** `tkinter` is usually included with Python, but for some environments (e.g., headless servers), you may need to install it separately. `geopy` is used for calculating distances between geographic coordinates, and `folium` is used to generate interactive maps.

---

## How to Run

1. Save the provided Python code into a file named, for example, `gps_distance_calculator.py`.
2. Open a terminal or command prompt and navigate to the directory containing the script.
3. Run the script using:

```bash
python gps_distance_calculator.py
```

The GUI window will open, and you can start adding GPS points, setting travel times, and calculating distances.

<img src='https://github.com/fabiomatricardi/GPSmarineCalculator/raw/main/GPSnauticalSpeed_rev003_006.png' width=900>

---

## Description of Classes and Functions

### Classes

- **No classes are defined** in this script. The entire application is implemented using functions and global variables.

### Functions

- **`open_map_in_browser(m)`**
  Saves the generated map to a temporary HTML file and opens it in the default web browser. This function avoids opening the map directly in the GUI window, which could interfere with the Tkinter interface.

- **`save_results_to_file(points, travel_hours, total_distance, avg_speed, start_time, end_time)`**
  Saves the GPS data, travel time, total distance, and average speed to a text file in the current working directory. The filename includes a timestamp to avoid overwriting previous results.

- **`create_gui()`**
  The main function that sets up the graphical user interface using `tkinter`. It includes input fields for GPS coordinates, date/time pickers for travel time, and buttons to add points, set travel time, calculate results, and save data.

- **`set_travel_hours_from_datetime()`**
  Prompts the user to input start and end times via `simpledialog`, validates the input, and updates the displayed travel time and time range.

- **`add_point()`**
  Prompts the user to input latitude and longitude for a new GPS point, validates the coordinates, and adds the point to the list.

- **`calculate_distance()`**
  Calculates the total distance between consecutive GPS points, computes average speed, and displays a summary in a popup. It also generates an interactive map using `folium`, placing markers at each point and drawing a polyline between them. The map is opened in a new browser tab via a separate thread to prevent freezing the GUI.

- **`save_results_to_file(...)`** and **`open_map_in_browser(m)`**
  These functions are called from `calculate_distance()` to handle file saving and map opening respectively.

---

## Description of the App Goal

The **GPS Distance Calculator (Advanced)** is a desktop application designed to help users calculate the total distance traveled between a series of GPS coordinates, along with the average speed and total travel time. It provides an interactive GUI for inputting GPS points and travel time ranges, and generates a visual map showing the route and distance traveled.

Key features include:
- Input of GPS coordinates (latitude and longitude) for multiple points.
- Selection of start and end times for travel duration.
- Calculation of total distance, travel time, and average speed.
- Interactive map generation using `folium` showing all points and the route.
- Saving of results to a text file with timestamps for record-keeping.

This tool is useful for outdoor navigation, tracking travel routes, and analyzing movement patterns.

---

## Additional Notes

- The application uses `threading` to open the map in a separate thread, ensuring the GUI remains responsive during map generation.
- Date/time inputs are expected in `YYYY-MM-DD HH:MM` format.
- The map is generated using `folium` and opened in the default web browser, so internet access is required for map display.
- The results are saved in the current working directory with a unique timestamp to prevent overwriting.

---

## Example Usage

1. Run the script.
2. Click **"Add Point"** and enter coordinates (e.g., `40.7128, -74.0060`).
3. Set travel time using **"Set Travel Time from Start/End"** (optional).
4. Click **"Calculate Distance & Show Map"** to see results and map.
5. Click **"Save Results to File"** to save the data locally.

---

> *Documentation READ.ME created with LFM2-2.6b by Liquid AI*

Prompt used:
```markdown
Given the following python app, please help me to write a proper Documentation text including:
- packages requirements
- how to run
- description of classes and functions
- description of the app goal

here the python app:
>```python
><INSERT HERE YOUR CODE>
>```
```
---


