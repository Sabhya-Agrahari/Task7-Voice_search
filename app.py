import tkinter as tk
from tkinter import messagebox, filedialog
import speech_recognition as sr
from products import products
from tkinter import ttk

def record_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        try:
            audio = r.listen(source, timeout=10)
        except sr.WaitTimeoutError:
            messagebox.showerror("Error", "Listening timed out while waiting for phrase to start")
            return None
    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        messagebox.showerror("Error", "Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        messagebox.showerror("Error", f"Could not request results from Google Speech Recognition service; {e}")
        return None

        
def upload_voice():
    # Open file dialog to select an audio file
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.flac *.mp3")])
    if not file_path:
        # If no file is selected, return None
        return None

    r = sr.Recognizer()
    try:
        # Attempt to open and process the audio file
        with sr.AudioFile(file_path) as source:
            audio = r.record(source)
        # Attempt to recognize the audio
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        # Handle case where the audio is not understandable
        messagebox.showerror("Error", "Google Speech Recognition could not understand the audio")
        print("Error: Could not understand the audio.")
        return None
    except sr.RequestError as e:
        # Handle request errors to the recognition service
        messagebox.showerror("Error", f"Could not request results from Google Speech Recognition service; {e}")
        print(f"Request error: {e}")
        return None
    except ValueError as e:
        # Handle case where the file format is not supported
        messagebox.showerror("Error", f"Audio file could not be read; check if the file is corrupted or in another format: {e}")
        print(f"Value error: {e}")
        return None
    except Exception as e:
        # Handle unexpected errors
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        print(f"Unexpected error: {e}")
        return None

def search_products(query, products):
    if query is None or query.strip() == "":
        return ["Error: Could not understand the input."]

    query = query.lower()
    matching_products = {letter: [] for letter in 'abcde'}
    all_matching_products = {letter: [] for letter in 'abcde'}

    for product in products:
        first_letter = product[0].lower()
        if query in product.lower():
            if first_letter in matching_products:
                matching_products[first_letter].append(product)
        if first_letter in all_matching_products:
            all_matching_products[first_letter].append(product)

    if any(matching_products.values()):
        result = ["Product found:"]
        for letter in 'abcde':
            result.extend(matching_products[letter])
    else:
        result = ["No product found. Showing all products starting with A, B, C, D, E:"]
        for letter in 'abcde':
            result.extend(all_matching_products[letter])

    return result

def retrieve_all_products(products):
    result = ["All products in the list:"]
    for product in products:
        result.append(product)
    return result

def start_search_from_recording():
    voice_input = record_voice()
    display_results(voice_input)

def start_search_from_upload():
    voice_input = upload_voice()
    display_results(voice_input)

def display_results(voice_input):
    for widget in result_frame.winfo_children():
        widget.destroy()

    if voice_input:
        results = search_products(voice_input, products)
        
        if results[0] == "Product found":
            messagebox.showinfo("Success", "Product found")
        else:
            status_label = tk.Label(result_frame, text=results[0])
            status_label.pack(pady=5)

            # Create a Treeview to display all products starting with A, B, C, D, E
            columns = [letter.upper() for letter in 'abcde']
            tree = ttk.Treeview(result_frame, columns=columns, show='headings')
            for col in columns:
                tree.heading(col, text=col)
            tree.pack(pady=10, fill=tk.BOTH, expand=True)

            column_data = {letter: [] for letter in 'abcde'}
            for product in results[1:]:
                first_letter = product[0].lower()
                if first_letter in column_data:
                    column_data[first_letter].append(product)

            # Find the maximum number of items in any column
            max_items = max(len(column_data[letter]) for letter in 'abcde')

            for i in range(max_items):
                row = []
                for letter in 'abcde':
                    if i < len(column_data[letter]):
                        row.append(column_data[letter][i])
                    else:
                        row.append("")
                tree.insert("", tk.END, values=row)


def search_products_by_text():
    text_input = search_entry.get().strip().lower()
    if text_input in [product.lower() for product in products]:
        messagebox.showinfo("Success", "Product found")
    else:
        messagebox.showinfo("Unsuccessfull","Product are the found in product list")


def display_all_products():
    all_products = retrieve_all_products(products)
    display_all_results(all_products)

def display_all_results(all_products):
    for widget in result_frame.winfo_children():
        widget.destroy()

    status_label = tk.Label(result_frame, text=all_products[0])
    status_label.pack(pady=5)

    columns = [letter.upper() for letter in 'abcdefghijklmnopqrstuvwxyz']
    tree = ttk.Treeview(result_frame, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(pady=10, fill=tk.BOTH, expand=True)

    column_data = {letter: [] for letter in 'abcdefghijklmnopqrstuvwxyz'}
    for product in all_products[1:]:
        first_letter = product[0].lower()
        if first_letter in column_data:
            column_data[first_letter].append(product)

    max_items = max(len(column_data[letter]) for letter in 'abcdefghijklmnopqrstuvwxyz')

    for i in range(max_items):
        row = []
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            if i < len(column_data[letter]):
                row.append(column_data[letter][i])
            else:
                row.append("")
        tree.insert("", tk.END, values=row)

# Set up the GUI
root = tk.Tk()
root.title("Voice Product Search")

frame = tk.Frame(root)
frame.pack(pady=20)

heading_label = tk.Label(frame, text="My Product List", font=("Arial", 24, "bold"))
heading_label.pack(pady=10)

search_label = tk.Label(frame, text="Type the product name and press Search:")
search_label.pack(pady=10)

search_entry = tk.Entry(frame)
search_entry.pack(pady=5)

search_button = tk.Button(frame, text="Search", command=search_products_by_text)
search_button.pack(pady=10)


instructions_label = tk.Label(frame, text="Press the button and say product names or upload a voice file.")
instructions_label.pack(pady=10)

record_button = tk.Button(frame, text="Record Voice", command=start_search_from_recording)
record_button.pack(pady=10)

upload_button = tk.Button(frame, text="Upload Voice File", command=start_search_from_upload)
upload_button.pack(pady=10)



result_frame = tk.Frame(frame)
result_frame.pack(pady=10, fill=tk.BOTH, expand=True)

root.mainloop()
