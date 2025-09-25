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

1. Clone the repo`.
2. Open a terminal or command prompt and navigate to the directory containing the script.
3. Run the script using:

```bash
python GPSnauticalSpeed_rev004.py
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
## Additional feature - load from TXT existing routes with GPS points

> I want to be able to start with an existing list of points: can you add this feature and give me an example of how to prepare the data for this purpose?


Absolutely! I'll enhance your app to allow loading an **existing list of GPS points** from a file at startup. This will let users:

- Save point lists for reuse.
- Load predefined routes (e.g., sailing paths, flight plans).
- Avoid re-entering coordinates every time.

---

### ✅ New Feature: Load Points from File

We’ll support a simple **CSV or TXT file** format like this:

```csv
latitude,longitude
40.7128,-74.0060
34.0522,-118.2437
41.8781,-87.6298
```

> 💡 The first line is a header (optional), then one point per line: `lat,lon`

You can name the file anything, e.g., `route1.txt`, `hawaii_voyage.csv`, etc.

---

### 🔧 Changes Made to Your Code

I’ve updated your code with:
1. A **"Load Points" button** in the GUI.
2. A function `load_points_from_file()` that reads and validates coordinates.
3. Optional: Warns if any coordinate is invalid but skips or rejects it based on preference.

---

### ✅ Updated Code (with Load Feature)

Replace your entire code with this updated version:

```python
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk, filedialog
import geopy.distance
import folium
import webbrowser
import os
import threading
from datetime import datetime
import tempfile


# --- Safe function to create and open map in browser ---
def open_map_in_browser(m):
    temp_dir = tempfile.gettempdir()
    html_filename = os.path.join(temp_dir, "gps_distance_map.html")

    try:
        m.save(html_filename)
        webbrowser.open(f"file://{html_filename}")
        print(f"Map saved to {html_filename} and opened in browser.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save or open map: {str(e)}")


# --- Save results to file in current directory ---
def save_results_to_file(points, travel_hours, total_distance, avg_speed, start_time, end_time):
    current_dir = os.getcwd()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"gps_results_{timestamp}.txt"

    file_path = os.path.join(current_dir, filename)

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("=== GPS Distance Calculation Results ===\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M') if start_time else 'N/A'}\n")
            f.write(f"End Time: {end_time.strftime('%Y-%m-%d %H:%M') if end_time else 'N/A'}\n")
            f.write(f"Travel Time: {travel_hours:.1f} hours\n")
            f.write(f"Total Distance: {total_distance:.2f} nautical miles\n")
            f.write(f"Average Speed: {avg_speed:.2f} knots\n\n")
            f.write("List of Points (Latitude, Longitude):\n")
            for i, (lat, lon) in enumerate(points):
                f.write(f"  Point {i+1}: {lat:.6f}, {lon:.6f}\n")
        messagebox.showinfo("Save Success", f"Results saved to:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Save Error", f"Failed to save file: {str(e)}")


# --- Load GPS points from a CSV/TXT file ---
def load_points_from_file():
    file_path = filedialog.askopenfilename(
        title="Select GPS Points File",
        filetypes=[("Text/CSV Files", "*.txt *.csv"), ("All Files", "*.*")]
    )
    if not file_path:
        return []

    points = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line_num, line in enumerate(lines):
            line = line.strip()
            if not line or line.lower().startswith('latitude') or line.lower().startswith('lat'):
                continue  # Skip headers or empty lines

            parts = line.split(',')
            if len(parts) != 2:
                messagebox.showwarning("Format Warning", f"Skipping invalid line {line_num + 1}: '{line}'")
                continue

            try:
                lat = float(parts[0].strip())
                lon = float(parts[1].strip())
                if not (-90 <= lat <= 90):
                    raise ValueError(f"Latitude {lat} out of range [-90, 90]")
                if not (-180 <= lon <= 180):
                    raise ValueError(f"Longitude {lon} out of range [-180, 180]")

                points.append((lat, lon))
            except ValueError as ve:
                messagebox.showwarning("Invalid Data", f"Line {line_num + 1}: Invalid coordinate - {ve}")

        if points:
            messagebox.showinfo("Load Success", f"Loaded {len(points)} point(s) from:\n{os.path.basename(file_path)}")
        else:
            messagebox.showwarning("No Points Loaded", "No valid GPS points found in the file.")

    except Exception as e:
        messagebox.showerror("File Error", f"Could not read file: {str(e)}")

    return points


# --- GUI with full date/time picker and start/end times in summary ---
def create_gui():
    root = tk.Tk()
    root.title("GPS Distance Calculator (Advanced)")
    root.geometry("600x750")  # Slightly taller for new button

    points = []  # Store all points as [(lat, lon), ...]
    travel_hours = 0.0
    start_time = None
    end_time = None

    def set_travel_hours_from_datetime():
        nonlocal travel_hours, start_time, end_time
        try:
            start_str = simpledialog.askstring("Start Date & Time", "Enter start time (e.g. 2025-04-05 08:00):")
            if not start_str:
                return

            end_str = simpledialog.askstring("End Date & Time", "Enter end time (e.g. 2025-04-05 18:00):")
            if not end_str:
                return

            start_time = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
            end_time = datetime.strptime(end_str, "%Y-%m-%d %H:%M")

            if start_time >= end_time:
                messagebox.showerror("Error", "End time must be after start time.")
                return

            travel_hours = (end_time - start_time).total_seconds() / 3600

            # Update UI
            time_label.config(text=f"Travel Time: {travel_hours:.1f} hours")
            start_end_label.config(text=f"Start: {start_time.strftime('%Y-%m-%d %H:%M')} | End: {end_time.strftime('%Y-%m-%d %H:%M')}")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid date/time format. Use YYYY-MM-DD HH:MM. Error: {str(e)}")

    def add_point():
        nonlocal points
        try:
            point_str = simpledialog.askstring("Add Point", "Enter lat, lon (e.g. 40.7128, -74.0060):")
            if not point_str:
                return

            lat, lon = map(float, point_str.split(','))
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                messagebox.showerror("Error", "Invalid coordinates. Latitude: -90 to 90, Longitude: -180 to 180.")
                return

            points.append((lat, lon))
            messagebox.showinfo("Success", f"Point added: {lat}, {lon}")

            count_label.config(text=f"Points: {len(points)}")

        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")

    def load_points():
        nonlocal points
        loaded = load_points_from_file()
        if loaded:
            points.extend(loaded)
            count_label.config(text=f"Points: {len(points)}")
            messagebox.showinfo("Update", f"Current route now has {len(points)} total point(s).")

    def calculate_distance():
        nonlocal travel_hours
        if len(points) < 2:
            messagebox.showerror("Error", "Need at least 2 points to calculate distance.")
            return

        # Calculate distances between consecutive points
        total_distance = 0.0
        coords = [(lat, lon) for lat, lon in points]

        for i in range(len(coords) - 1):
            p1 = coords[i]
            p2 = coords[i + 1]
            dist = geopy.distance.distance(p1, p2).nm
            total_distance += dist

        # Calculate average speed in knots
        if travel_hours <= 0:
            avg_speed = 0
            speed_text = "N/A"
        else:
            avg_speed = total_distance / travel_hours
            speed_text = f"{avg_speed:.2f} knots"

        # Build summary
        summary = (
            f"Total Distance: {total_distance:.2f} nmi\n"
            f"Travel Time: {travel_hours:.1f} hours\n"
            f"Average Speed: {avg_speed:.2f} knots"
        )

        messagebox.showinfo("Summary", summary)

        # Create map
        m = folium.Map(
            location=[(coords[0][0] + coords[-1][0]) / 2, (coords[0][1] + coords[-1][1]) / 2],
            zoom_start=5
        )

        # Add markers
        for i, (lat, lon) in enumerate(coords):
            popup_text = f"Point {i+1}\nLat: {lat:.4f}\nLon: {lon:.4f}"
            folium.Marker(
                [lat, lon],
                popup=popup_text,
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)

        # Add polyline
        folium.PolyLine(coords, color="blue", weight=3, opacity=0.8, popup="Route").add_to(m)

        # Summary popup
        start_str = start_time.strftime('%Y-%m-%d %H:%M') if start_time else "N/A"
        end_str = end_time.strftime('%Y-%m-%d %H:%M') if end_time else "N/A"
        summary_html = f"""
        <div style="font-family: Arial; font-size: 14px; background: #f0f0f0; padding: 10px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); font-weight: bold;">
            <strong>Total Distance:</strong> {total_distance:.2f} nmi<br>
            <strong>Start Time:</strong> {start_str}<br>
            <strong>End Time:</strong> {end_str}<br>
            <strong>Travel Time:</strong> {travel_hours:.1f} h<br>
            <strong>Average Speed:</strong> {avg_speed:.2f} knots<br>
            <strong>Points:</strong> {len(points)} total
        </div>
        """

        folium.Marker(
            coords[0],
            popup=folium.Popup(summary_html, max_width=300),
            icon=folium.Icon(color="green", icon="info-sign")
        ).add_to(m)

        # Open map
        threading.Thread(target=open_map_in_browser, args=(m,), daemon=True).start()

        # Save results
        save_results_to_file(points, travel_hours, total_distance, avg_speed, start_time, end_time)

    # === UI Elements ===
    title_label = tk.Label(root, text="GPS Distance Calculator (Advanced)", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    left_frame = tk.Frame(root, width=500, bg="lightgray")
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(left_frame, text="Points:", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
    count_label = tk.Label(left_frame, text="Points: 0", font=("Arial", 12))
    count_label.pack(anchor="w", padx=10, pady=2)

    add_button = tk.Button(left_frame, text="Add Point", command=add_point, bg="lightblue", font=("Arial", 10))
    add_button.pack(pady=5)

    load_button = tk.Button(left_frame, text="Load Points from File", command=load_points, bg="lightgreen", font=("Arial", 10))
    load_button.pack(pady=5)

    # --- Travel Time Input Section ---
    tk.Label(left_frame, text="Travel Time (Start & End)", font=("Arial", 12)).pack(anchor="w", padx=10, pady=10)

    tk.Label(left_frame, text="Start Date & Time (YYYY-MM-DD HH:MM):", font=("Arial", 10)).pack(anchor="w", padx=10, pady=2)
    tk.Label(left_frame, text="End Date & Time (YYYY-MM-DD HH:MM):", font=("Arial", 10)).pack(anchor="w", padx=10, pady=2)

    time_button = tk.Button(left_frame, text="Set Travel Time from Start/End", command=set_travel_hours_from_datetime, bg="lightgreen", font=("Arial", 10))
    time_button.pack(pady=5)

    time_label = tk.Label(left_frame, text="Travel Time: 0.0 hours", font=("Arial", 12))
    time_label.pack(anchor="w", padx=10, pady=5)

    start_end_label = tk.Label(left_frame, text="Start: N/A | End: N/A", font=("Arial", 10), fg="gray")
    start_end_label.pack(anchor="w", padx=10, pady=2)

    calc_button = tk.Button(left_frame, text="Calculate Distance & Show Map", command=calculate_distance, bg="darkblue", fg="white", font=("Arial", 10))
    calc_button.pack(pady=20)

    save_button = tk.Button(left_frame, text="Save Results to File", command=lambda: save_results_to_file(points, travel_hours, 0, 0, start_time, end_time), bg="orange", fg="white", font=("Arial", 10))
    save_button.pack(pady=5)

    note_label = tk.Label(left_frame, text="Note: Travel time is required for speed calculation.", font=("Arial", 9), fg="gray")
    note_label.pack(anchor="w", padx=10, pady=5)

    root.mainloop()


# --- Run the app ---
if __name__ == "__main__":
    create_gui()
```

---

### 📝 How to Prepare Your Data File

Create a `.txt` or `.csv` file like this:

#### Example: `my_route.txt`
```csv
latitude,longitude
40.7128,-74.0060
34.0522,-118.2437
41.8781,-87.6298
29.7604,-95.3698
```

> You can skip the header if you want:
>
> ```
> 40.7128,-74.0060
> 34.0522,-118.2437
> ```

Save it anywhere on your computer — then use the **"Load Points from File"** button in the app.

---

### ✅ Tips

- Use consistent formatting: comma-separated, no extra spaces.
- Validate coordinates before saving the file.
- You can export routes from tools like Google Earth, MarineTraffic, or GPS loggers into this format.

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


