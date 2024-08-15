from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

load_dotenv() # this loads all the environment variables

# Function to load Google Gemini flash API And get response
def get_gemini_reponse(input_prompt,image,user_prompt):
    model=genai.GenerativeModel('gemini-1.5-pro-latest')
    response=model.generate_content([input_prompt,image[0],user_prompt])
    return response.text


# Function to process uploaded image to bytes
def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    

# Initializing the streamlit app
st.set_page_config(page_title="Gemini Calorie Counter App")
st.header("Gemini Calorie Counter App")
input=st.text_input("Ask any question related to your food: ",key="input")
uploaded_file = st.file_uploader("Upload an image of your food", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)    #show the image


submit=st.button("Submit & Process")

st.write("App created by: Ara")


# setting up the app's behavior
input_prompt="""
You are an expert nutritionist. 
You should answer the question entered by the user in the input based on the uploaded image you see.
You should also look at the food items found in the uploaded image and calculate the total calories. 
Also, provide the details of every food item with calories intake in the format below:

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----

"""


# Once submit button is clicked
if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_reponse(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)


