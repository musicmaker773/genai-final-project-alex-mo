# 1
import json
from openai import OpenAI
import streamlit as st
import requests

client = OpenAI(
    api_key = st.secrets["OPENAI_API_KEY"]
)
st.title("Pokedex Project")

# 2
system_prompt = """
I want you to help the user get specific information about a Pokemon they search up. You are assuming the role of a Pokedex, like how they are portrayed in the games and TV shows. Get your information like Wikis and Bulbapedia. You should give the name of the Pokemon, as well as the number they are associated with (like Pikachu #025). You should also give a brief, one-sentence discription of the Pokemon, as well as the category, list of Abilities, Type, and Weakness of the Pokemon.

 Respond with a JSON in the following format:

{
    "Name": "NAME",
    "Number": "####"
    "Description": "DESCRIPTION"
    "Category": "CATEGORY"
    "Abilities": [
        "ABILITY_1",
        "ABILITY_2",
        ...
    ],
    "Type": "TYPE",
    "Weakness": "WEAKNESS"
}
"""

# 3
user_prompt = st.text_input("What Pokemon do you want to know about:")

button = st.button("Submit")

if button:
    url = "https://pokeapi.co/api/v2/pokemon/" + user_prompt.lower()

    data = ""
    try:
        response = requests.get(url, timeout=5) # 5-second timeout protection
        
        # Check if the request was successful (Status Code 200)
        if response.status_code == 200:
            data = response.json()  # Parse JSON data into a dictionary
            print("Success!")
        else:
            data = "Failed"
            print(f"Failed with status code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"A network error occurred: {e}")

    # 4
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    # 5
    #print(json.loads(response.choices[0].message.content))
    st.session_state["temp"] = json.loads(response.choices[0].message.content)
    if "Failed" not in data:
        st.image(data['sprites']['front_default'])
    else:
        st.write("No image found!")

    st.write("Name: ", st.session_state["temp"]["Name"], st.session_state["temp"]["Number"])
    st.write()
    st.write("Description ", st.session_state["temp"]["Description"])
    st.write("Category:", st.session_state["temp"]["Category"])
    st.write("Abilities:")
    for i in st.session_state["temp"]["Abilities"]:
        st.write(i)

    st.write("Type:", st.session_state["temp"]["Type"])
    st.write()
    st.write("Weakness:", st.session_state["temp"]["Weakness"])
