import streamlit as st
from openai import OpenAI
import requests
from io import BytesIO
from PIL import Image

# Initialize OpenAI client
client = OpenAI()

def generate_image(prompt):
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def main():
    st.title("DALL-E 3 Image Generation")
    
    # User input for OpenAI API key
    api_key = st.text_input("Enter your OpenAI API key:", type="password")
    
    if api_key:
        client.api_key = api_key
        
        # User input for image prompt
        prompt = st.text_input("Enter a prompt for the image:")
        
        if st.button("Generate Image"):
            if prompt:
                with st.spinner("Generating image..."):
                    image_url = generate_image(prompt)
                    if image_url:
                        # Download and display the image
                        response = requests.get(image_url)
                        img = Image.open(BytesIO(response.content))
                        st.image(img, caption="Generated Image", use_column_width=True)
                        st.success("Image generated successfully!")
            else:
                st.warning("Please enter a prompt.")
    else:
        st.warning("Please enter your OpenAI API key to proceed.")

if __name__ == "__main__":
    main()
