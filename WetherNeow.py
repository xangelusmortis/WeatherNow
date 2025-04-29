import tkinter as tk
import requests

window = tk.Tk()
window.title("Weather Now")
window.configure(background="Light Blue")

# --- API Frame ---
api_frame = tk.LabelFrame(window, text="Live Weather - (Weather Now Map)", padx=10, pady=10)
api_frame.pack(padx=10, pady=10, fill="x")

city_label = tk.Label(api_frame, text="Enter the city, state, or zip to get weather from your area.")
city_label.pack(pady=5)

city_entry = tk.Entry(api_frame, width=30)
city_entry.pack()

city_button = tk.Button(api_frame, text="Get Weather", command=lambda: get_weather())
city_button.pack()

weather_result = tk.Label(api_frame, text="", justify="left")
weather_result.pack(pady=10)

def get_weather():
    city = city_entry.get()
    if not city:
        weather_result.config(text="Please enter a city.")
        return

    api_key = "4ce30896f4e17f46551f11fab859c03a"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            weather_result.config(text=f"Error: {data['message']}")
            return

        description = data["weather"][0]["description"].title()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        wind = data["wind"]["speed"]

        weather_result.config(
            text=f"{city.title()}:\nTemperature: {temp}°F - {description}\nFeels like {feels_like}°F\nWind: {wind} mph"
        )

        with open("weather_log.txt", "a") as file:
            file.write(f"{city.title()}: {description}, {temp}°F (feels like {feels_like}°F), Wind: {wind} mph\n")

    except Exception as e:
        weather_result.config(text=f"Error: {e}")

# --- Manual Input Frame ---
manual_frame = tk.LabelFrame(window, text="Manual Weather Input", pady=10, padx=10)
manual_frame.pack(padx=10, pady=10, fill="x")

text_label = tk.Label(manual_frame, text="Select the current weather in your area.")
text_label.pack(pady=5)

weather_frame = tk.Frame(manual_frame)
weather_frame.pack(pady=10)

weather_types = ["Sunny", "Raining", "Cloudy", "Storming", "Snowing"]
for i, weather in enumerate(weather_types):
    buttonC = tk.Button(
        weather_frame,
        text=weather,
        relief=tk.RAISED,
        borderwidth=1,
        width=15
    )
    buttonC.grid(row=0, column=i, padx=5, pady=5)

# --- Big Textbox ---
text_box = tk.Text(manual_frame, height=5, width=50)
text_box.pack(pady=10)
text_box.insert(tk.END, "Enter your weather comments here:")

# --- Run ---
window.mainloop()

