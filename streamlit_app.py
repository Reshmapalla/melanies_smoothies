import streamlit as st

from snowflake.snowpark.functions import col

# Title for the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Orders that need to be filled")

# Active Snowflake session
cnx=st.connection("snowflake")
session=cnx.session()

# Section for customizing smoothies
st.header("Customize Your Smoothie")
st.write("Choose the fruits you want in your custom Smoothie!")

# Name on order input
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Retrieve fruit options for customization
try:
    fruit_options_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).collect()
    fruit_names = [row['FRUIT_NAME'] for row in fruit_options_df]  # Extract fruit names
except Exception as e:
    st.error(f"Error fetching fruit options: {e}")
    fruit_names = []

# Multi-select for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , fruit_names
    , max_selections=5
)

if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)  # Create a comma-separated string of ingredients

    # Insert order into the database
    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')
    """
    if st.button('Submit Order'):
        try:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
        except Exception as e:
            st.error(f"Error submitting your order: {e}")
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
sf_df=st.dataframe(data=smoothiefroot_response.json().use_container-width=true)

