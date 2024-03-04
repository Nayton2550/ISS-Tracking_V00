import requests
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

def get_iss_and_craft_location():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    craft_latitude = 40.7128
    craft_longitude = -74.0060

    return iss_latitude, iss_longitude, craft_latitude, craft_longitude

def update_location():
    iss_latitude, iss_longitude, craft_latitude, craft_longitude = get_iss_and_craft_location()
    iss_latitude_label.config(text=f"ISS Latitude: {iss_latitude}")
    iss_longitude_label.config(text=f"ISS Longitude: {iss_longitude}")
    craft_latitude_label.config(text=f"Craft Latitude: {craft_latitude}")
    craft_longitude_label.config(text=f"Craft Longitude: {craft_longitude}")

    iss_latitudes.append(iss_latitude)
    iss_longitudes.append(iss_longitude)
    craft_latitudes.append(craft_latitude)
    craft_longitudes.append(craft_longitude)

    
    # Get current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Append latitude, longitude, and time to DataFrame
    df.loc[len(df)] = [current_time,iss_latitude, iss_longitude]
    df.to_excel("iss_locations2.xlsx", index=False)

   

    ax.clear()
    ax.plot(iss_latitudes, iss_longitudes, label='ISS')
    ax.plot(craft_latitudes, craft_longitudes, label='Craft')
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.legend()
    canvas.draw()
    root.after(1000, update_location)  # Update location every 5 seconds


root = tk.Tk()
root.title("ISS and Craft Tracker")

iss_latitude_label = tk.Label(root, text="ISS Latitude: ", font=("Helvetica", 12))
iss_latitude_label.pack()

iss_longitude_label = tk.Label(root, text="ISS Longitude: ", font=("Helvetica", 12))
iss_longitude_label.pack()

craft_latitude_label = tk.Label(root, text="Craft Latitude: ", font=("Helvetica", 12))
craft_latitude_label.pack()

craft_longitude_label = tk.Label(root, text="Craft Longitude: ", font=("Helvetica", 12))
craft_longitude_label.pack()

# Create Matplotlib figure and canvas
fig = plt.Figure()
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

iss_latitudes = []
iss_longitudes = []
craft_latitudes = []
craft_longitudes = []
df = pd.DataFrame(columns=["Time", "Latitude", "Longitude"])

update_location()  # Initial update

root.mainloop()
