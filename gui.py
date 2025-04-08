import tkinter as tk
import requests

# API endpoint
API_URL = "http://127.0.0.1:8000/upload-images/"

def upload_images():
    try:
        response = requests.post(API_URL)
        if response.status_code == 200:
            result = response.json().get("message", "Success!")
        else:
            result = f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        result = f"Exception: {str(e)}"

    result_label.config(text=result)

# GUI layout
window = tk.Tk()
window.title("Image Uploader")
window.geometry("400x200")

upload_button = tk.Button(window, text="📤 Upload Images to PostgreSQL", command=upload_images, font=("Arial", 14))
upload_button.pack(pady=40)

result_label = tk.Label(window, text="", font=("Arial", 12))
result_label.pack()

window.mainloop()