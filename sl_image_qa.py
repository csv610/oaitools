import tkinter as tk
from tkinter import filedialog
from openai import OpenAI
import base64

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def ask_question_about_image(client, image_path, question):
    try:
        # Encode the image
        base64_image = encode_image(image_path)

        # Create the message for the API
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ]

        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=messages,
            max_tokens=300
        )

        # Return the model's answer
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

def select_image():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])
    return file_path

def main():
    # Get the OpenAI API key from the user
    api_key = input("Please enter your OpenAI API key: ")
    
    # Initialize the OpenAI client with the API key
    client = OpenAI(api_key=api_key)

    # Get the image file from the user
    print("Please select an image file.")
    image_path = select_image()
    
    if not image_path:
        print("No image selected. Exiting.")
        return

    # Get the question from the user
    question = input("What would you like to ask about the image? ")

    # Ask the question about the image
    answer = ask_question_about_image(client, image_path, question)

    # Print the answer
    print("\nAnswer:")
    print(answer)

if __name__ == "__main__":
    main()
