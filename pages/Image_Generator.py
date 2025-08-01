import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file
gemini_api_key = os.getenv('GEMINI_API_KEY')

# Instantiate Gemini client
client = genai.Client(api_key=gemini_api_key)

st.set_page_config(page_title="Gemini Image Generator", page_icon="🎨")
st.title("Gemini AI Image Generator")

# Prompt input
prompt = st.text_area(
    "Enter a prompt to generate an image:"
)

if st.button("Generate Image"):
    with st.spinner("Generating image with Gemini..."):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-preview-image-generation",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT", "IMAGE"]
                )
            )

            image_data = None
            text_response = None

            # Extract parts
            for part in response.candidates[0].content.parts:
                if hasattr(part, "text") and part.text:
                    text_response = part.text
                elif hasattr(part, "inline_data") and part.inline_data:
                    image_data = part.inline_data.data

            # Show results
            if text_response:
                st.write(text_response)

            if image_data:
                image = Image.open(BytesIO(image_data))
                st.subheader("🖼️ Generated Image")
                st.image(image, caption="Generated by Gemini", width=300)
            else:
                st.error("No image was generated.")

        except Exception as e:
            st.error(f"❌ Error: {e}")
