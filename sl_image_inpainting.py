import streamlit as st
from openai import OpenAI
import os
from PIL import Image
import requests
from io import BytesIO
import numpy as np
from streamlit_drawable_canvas import st_canvas

# Initialize OpenAI client
client = OpenAI()

def save_image(image, filename):
    image.save(filename)
    return filename

def main():
    st.title("OpenAI Image Editor with DALL-E 2")

    # File uploader for the image
    image_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if image_file:
        # Display the uploaded image
        image = Image.open(image_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Create a canvas for mask drawing
        st.subheader("Draw Mask")
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",  # Transparent orange
            stroke_width=30,
            stroke_color="#000000",
            background_color="#ffffff",
            background_image=image,
            update_streamlit=True,
            height=image.height,
            width=image.width,
            drawing_mode="freedraw",
            key="canvas",
        )

        # Prompt input
        prompt = st.text_input("Enter your prompt for image editing")

        # Generate button
        if st.button("Generate Edited Image"):
            if canvas_result.image_data is not None and prompt:
                with st.spinner("Generating edited image..."):
                    # Save the original image
                    image_path = save_image(image, "original_image.png")

                    # Create and save the mask
                    mask = Image.fromarray((canvas_result.image_data[:, :, 3] > 0).astype(np.uint8) * 255)
                    mask_path = save_image(mask, "mask.png")

                    # Call OpenAI API
                    try:
                        response = client.images.edit(
                            model="dall-e-2",
                            image=open(image_path, "rb"),
                            mask=open(mask_path, "rb"),
                            prompt=prompt,
                            n=1,
                            size="1024x1024"
                        )
                        image_url = response.data[0].url

                        # Display the generated image
                        st.image(image_url, caption="Generated Image")

                        # Provide download link
                        st.markdown(f"[Download Generated Image]({image_url})")

                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")

                    finally:
                        # Clean up temporary files
                        os.remove(image_path)
                        os.remove(mask_path)
            else:
                st.warning("Please draw a mask and provide a prompt.")

if __name__ == "__main__":
    main()
