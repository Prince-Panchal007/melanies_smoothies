# Import python packages.
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app.
st.title(":cup_with_straw: Customise Your Smoothie!:cup_with_straw:")
st.write(
  """Choose the fruits you want in your custome Smoothie!
  """
)

name=st.text_input('Name on Smoothie')
st.write(f'the name on the Smoothie will be: {name}')
cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('search_on'))
# st.dataframe(data=my_dataframe, use_container_width=True)
pd_df=my_dataframe.to_pandas()
ing=st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)
s=''
if ing:
    # st.write(ing)
    # st.text(ing)
    for i in ing:
        s+=i+' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == i, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', i,' is ', search_on, '.')
        st.subheader(i+' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+search_on)  
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + s + f"""','{name}')"""
    # st.write(my_insert_stmt)
    tti=st.button('Submit')
    if tti:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name}!', icon="✅")
