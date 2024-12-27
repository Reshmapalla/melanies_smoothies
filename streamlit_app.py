# import streamlit as st
# from snowflake.snowpark.functions import col
# import requests

# # Title for the app
# st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
# st.write("Orders that need to be filled")

# # Active Snowflake session
# cnx = st.connection("snowflake")
# session = cnx.session()

# # Section for customizing smoothies
# st.header("Customize Your Smoothie")
# st.write("Choose the fruits you want in your custom Smoothie!")

# # Name on order input
# name_on_order = st.text_input("Name on Smoothie:")
# st.write("The name on your Smoothie will be:", name_on_order)

# # Retrieve fruit options for customization
# try:
#     # Fetching both FRUIT_NAME and SEARCH_ON columns from Snowflake
#     fruit_options_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON')).collect()
    
#     # Extracting fruit names into a list
#     fruit_names = [row['FRUIT_NAME'] for row in fruit_options_df]
    
# except Exception as e:
#     st.error(f"Error fetching fruit options: {e}")
#     fruit_names = []

# # Multi-select for ingredients
# ingredients_list = st.multiselect(
#     'Choose up to 5 ingredients:',
#     fruit_names,
#     max_selections=5
# )

# if ingredients_list:
#     ingredients_string = ', '.join(ingredients_list)  # Create a comma-separated string of ingredients
#     for fruit_chosen in ingredients_list:
#         # Fetch the corresponding SEARCH_ON value for the chosen fruit
#         search_on = next((row['SEARCH_ON'] for row in fruit_options_df if row['FRUIT_NAME'] == fruit_chosen), None)
        
#         if search_on:
#             st.write(f'The search value for {fruit_chosen} is {search_on}.')
            
#             st.subheader(f'{fruit_chosen} Nutrition Information')
            
#             # Make the API call using the SEARCH_ON value
#             try:
#                 smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
#                 smoothiefroot_response.raise_for_status()  # Check if the request was successful
#                 st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
#             except requests.HTTPError as http_err:
#                 if http_err.response.status_code == 404:
#                     st.warning(f"Nutrition information for {fruit_chosen} is not available.")
#     #             else:
#     #                 st.error(f"Error fetching nutrition information for {fruit_chosen}: {http_err}")
#     #         except Exception as api_error:
#     #             st.error(f"Error fetching nutrition information for {fruit_chosen}: {api_error}")
#     #     else:
#     #         st.error(f"No search value found for {fruit_chosen}.")

#     # # Insert order into the database
#     # my_insert_stmt = f"""
#     # INSERT INTO smoothies.public.orders (ingredients, name_on_order)
#     # VALUES ('{ingredients_string}', '{name_on_order}')
#     # """
#     # if st.button('Submit Order'):
#     #     try:
#     #         session.sql(my_insert_stmt).collect()
#     #         st.success('Your Smoothie is ordered!', icon="✅")
#     #     except Exception as e:
#     #         st.error(f"Error submitting your order: {e}")



import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Title for the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Orders that need to be filled")

# Active Snowflake session
cnx = st.connection("snowflake")
session = cnx.session()

# Section for customizing smoothies
st.header("Customize Your Smoothie")
st.write("Choose the fruits you want in your custom Smoothie!")

# Name on order input
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Retrieve fruit options for customization
try:
    # Fetching both FRUIT_NAME and SEARCH_ON columns from Snowflake
    fruit_options_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON')).collect()
    
    # Extracting fruit names into a list
    fruit_names = [row['FRUIT_NAME'] for row in fruit_options_df]
    
except Exception as e:
    st.error(f"Error fetching fruit options: {e}")
    fruit_names = []

# Multi-select for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_names,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)  # Create a comma-separated string of ingredients
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
        # search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
       
        st.subheader(fruit_chosen + ' Nutrition Information')
        
        # Make the API call using the SEARCH_ON value (for better API handling)
        # Assuming that `SEARCH_ON` can be used directly as the search term for the API call.
        search_term = next(row['SEARCH_ON'] for row in fruit_options_df if row['FRUIT_NAME'] == fruit_chosen)
        
        # API call to retrieve fruit information
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_term}")
        st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

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

