# general imports
import openai, os, json

# gui dependent imports
import tkinter as tk
from tkinter import filedialog
import pyperclip

# html parsing imports
from bs4 import BeautifulSoup

# Set the API key
openai.api_key = os.getenv("OPENAI_API_KEY")

import tkinter as tk
from tkinter import filedialog
import pyperclip

def open_file_dialog():
    global file_content
    file_path = filedialog.askopenfilename(title="Select Evernote HTML File", filetypes=[("HTML Files", "*.html")])

    if file_path:
        
        print(f"\033[32mINFO:\033[0m Selected file: {file_path}")
        
        with open(file_path, 'r') as file:
            file_name = os.path.basename(file_path)
            
            file_content = file.read()
            
            # parse the html file using beautiful soup
            soup = BeautifulSoup(file_content, 'html.parser')
            text = soup.get_text(strip=True)
            
            print(f"\033[32mINFO:\033[0m Extracted text from {file_name}")
            print(f"\033[32mINFO:\033[0m Extracted text: {text}")
            
        message_label.config(text=f"Here is the content from {file_name}")
        open_button.pack_forget()  # Remove the button after uploading
        display_text.config(state=tk.NORMAL)
        display_text.delete(1.0, tk.END)
        display_text.insert(tk.END, text)
        display_text.config(state=tk.DISABLED)  # Make the text widget read-only
        create_flashcards_button.pack()

def create_flashcards():
    
    # get the text from the text widget
    text = display_text.get(1.0, tk.END)
    
    generation_message = "Generating flashcards..."
    
    # replace the file text with the generation message
    display_text.config(state=tk.NORMAL)
    display_text.delete(1.0, tk.END)
    display_text.insert(tk.END, generation_message)
    display_text.config(state=tk.DISABLED)  # Make the text widget read-only
    
    num_flashcards = flashcard_entry.get()
    
    if num_flashcards == "" or num_flashcards.isnumeric() == False:
        num_flashcards = json.loads(open("config.json").read())["num_flashcards"]
    
    
    print(f"\033[32mINFO:\033[0m Generating {num_flashcards} flashcards")
    
    # load the prompt from config.json
    prompt = json.loads(open("config.json").read())["prompt"]
        
    # parse the file_name from the message_label
    file_name = message_label["text"].split()[-1]
    
    # format the prompt with the text and the number of flashcards
    prompt = prompt.format(text=str(text), num_flashcards=str(num_flashcards))
    print(f"\033[32mINFO:\033[0m Prompt: {prompt}")
    
    # make a request to openai library using the prompt to perform a CHAT completion
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt},
            ]
    )
    
    response_text = response.choices[0].message['content']

    # print the response text
    print(f"\033[32mINFO:\033[0m Generated text: {response_text}")
    
    generated_flashcards_label = f"Here are your generated flashcards for {file_name}"
    
    # replace the message label with the generated flashcards label
    message_label.config(text=generated_flashcards_label)
    
    # replace the text widget with the generated flashcards
    display_text.config(state=tk.NORMAL)
    display_text.delete(1.0, tk.END)
    display_text.insert(tk.END, response_text)
    display_text.config(state=tk.DISABLED)  # Make the text widget read-only
    
    # copy the generated flashcards to the clipboard
    pyperclip.copy(response_text)
    
    # print the generated flashcards to the clipboard
    print(f"\033[32mINFO:\033[0m Generated flashcards copied to clipboard")

# Create the main window
root = tk.Tk()
root.title("File Selector")

# Create a label for the message
message_label = tk.Label(root, text="Select Evernote HTML File")
message_label.pack()

# Create a button to open the file dialog
open_button = tk.Button(root, text="Open File", command=open_file_dialog)
open_button.pack()

# Create an entry widget for the number of flashcards
flashcard_label = tk.Label(root, text="Number of Flashcards:")
flashcard_label.pack()

flashcard_entry = tk.Entry(root)
flashcard_entry.pack()

# Create a text widget to display file contents
display_text = tk.Text(root, height=50, width=150, wrap=tk.WORD)
display_text.config(state=tk.DISABLED)  # Make the text widget read-only
display_text.pack()



# Create a button to create flashcards
create_flashcards_button = tk.Button(root, text="Create Flashcards", command=create_flashcards)

# Start the GUI event loop
root.mainloop()


