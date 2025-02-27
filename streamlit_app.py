
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
#         ingredients_string += fruit_chosen + ' '
        
#         # search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
#         # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
       
#         st.subheader(fruit_chosen + ' Nutrition Information')
        
#         # Make the API call using the SEARCH_ON value (for better API handling)
#         # Assuming that `SEARCH_ON` can be used directly as the search term for the API call.
#         search_term = next(row['SEARCH_ON'] for row in fruit_options_df if row['FRUIT_NAME'] == fruit_chosen)
        
#         # API call to retrieve fruit information
#         smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_term}")
#         st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

#     # Insert order into the database
#     my_insert_stmt = f"""
#     INSERT INTO smoothies.public.orders (ingredients, name_on_order)
#     VALUES ('{ingredients_string}', '{name_on_order}')
#     """
#     if st.button('Submit Order'):
#         try:
#             session.sql(my_insert_stmt).collect()
#             st.success('Your Smoothie is ordered!', icon="✅")
#         except Exception as e:
#             st.error(f"Error submitting your order: {e}")

import streamlit as st
from snowflake.snowpark.functions import col
import requests
 
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
 
st.write(""" Choose the fruits you want in your custom Smoothie! """)
 
# Take the name for the smoothie order
name_on_order = st.text_input('Name on Smoothie:')
st.write('The Name on your Smoothie will be:', name_on_order)
 
# Get active session from Snowflake
cnx=st.connection("snowflake")
session = cnx.session()
 
# Query the fruit options from Snowflake table
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe,use_container_width=True)
#st.stop()
 
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()
 
# Create a multiselect for users to choose up to 5 ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', my_dataframe,max_selections=5
)
 
# Initialize an empty string for ingredients
ingredients_string = ''
 
# If the user selects ingredients
if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+search_on)
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
 
    # Create the SQL insert statement
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """
 
    # Display the SQL statement (for debugging or review purposes)
    st.write(my_insert_stmt)
 
else:
    # Handle the case where no ingredients are selected
    my_insert_stmt = None
    st.write("Please choose some ingredients.")
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
# Add button to submit the order
if my_insert_stmt:  # Only show the button if the insert statement is valid
    time_to_insert = st.button('Submit Order')
 
    if time_to_insert:
        # Execute the SQL insert statement when the button is pressed
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
