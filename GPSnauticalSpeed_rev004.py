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