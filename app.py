import streamlit as st
import pandas as pd

# Functions
def get_unique_types(df):
    only_type = set([item.title() for row in list(df['type']) for item in row.split(", ")])
    
    return list(only_type)

def filter_by_type(df_types, types):
    df_set = set([word.lower() for word in df_types.split(", ")])
    types_set = set(map(str.lower, types))
    return types_set.issubset(df_set)

def format_types(df_types):
    types_lst = [single_type.title() for single_type in df_types.split(", ")]
    return " | ".join(types_lst)


CAPES_YELLOW_COLOR = "#FBBC04"

# Styles
initial_styles = f"""
<style>
    h1 {{
        text-align: center;
    }}

    .name {{
        text-decoration: underline;
        text-underline-offset: 5px;
        font-size: 1.5rem;
        font-weight: bold;
    }}

    p {{
        margin-bottom: 0.25rem;
    }}

    .container {{
        border: 1px solid gray;
        border-radius: 10px;
        margin: 10px auto;
        padding: 15px;
    }}

    .bolded {{
        font-weight: bold;
    }}

    .italicized {{
        font-style: italic;
    }}

    .colored {{
        color: {CAPES_YELLOW_COLOR};
    }}

    .centered {{
        text-align: center;
    }}

    .loc {{
        font-size: 1.15rem;
    }}
</style>
"""

# Page setup
st.set_page_config(page_title='CAPES Database Search', layout='wide')
st.markdown(initial_styles, unsafe_allow_html=True)
st.title("CAPES Database")
st.markdown("<br>", unsafe_allow_html=True)

# Connect to Google Sheet
sheet_id = "1iXVKk1C84ACGgWqBSssAxpIyJM3eHKDrxeVVusv2nME"
sheet_name = "things"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(url, dtype=str).fillna("0")
df['rating'] = df['rating'].astype(float)

print(df['pricing'])

# Constants
ALL_TYPES = get_unique_types(df)
N_CARDS_PER_ROW = 3

# Create the sidebar for filtering
st.sidebar.subheader("Filtering Options")
name = st.sidebar.text_input("Search", value="", placeholder="Enter Name")
search = st.sidebar.button("Search!", use_container_width=True)
types = st.sidebar.multiselect("Filter by Type", options=ALL_TYPES)
rating = st.sidebar.slider("Filter by Rating", 0.0, 5.0, value=0.0, step=0.25)
filter_btn = st.sidebar.button("Filter", use_container_width=True)
reset_btn = st.sidebar.button("Reset", type='primary', use_container_width=True)

# Filter dataframe
filter_one = df['supplier name'].str.contains(name)
filter_two = df['type'].apply(lambda x: filter_by_type(x, types))
filter_three = df['rating'] >= rating

filtered_df = df

if search:
    filtered_df = df[filter_one]

if filter_btn:
    filtered_df = df[filter_two & filter_three]

if reset_btn:
    filtered_df = df

# Show filtered results
filtered_df.sort_values('rating', ascending=False, inplace=True)

for n_row, row in filtered_df.reset_index().iterrows():
    i = n_row % N_CARDS_PER_ROW
    if i==0:
        cols = st.columns(N_CARDS_PER_ROW, gap='large')
    
    with cols[n_row%N_CARDS_PER_ROW]:
        st.markdown(f"""
        <div class='container'>
            <p class='colored name centered'>{row['supplier name']}</p>
            <p class='colored loc centered italicized'><span class='bolded'>Location:</span> {row['location']}</p>
            <p><span class='bolded'>Types:</span> {format_types(row['type'])}</p>
            <p><span class='bolded'>Pricing:</span> {row['pricing']}</p>
            <p><span class='bolded'>Lead Time:</span> {row['lead time']}</p>
            <p><span class='bolded'>Payment Method:</span> {row['payment method']}</p>
            <p><span class='bolded'>Phone Number:</span> {row['phone']}</p>
            <p><span class='bolded'>Telephone Number:</span> {row['telephone']}</p>
            <p><span class='bolded'>Email:</span> {row['email']}</p>
            <p><span class='bolded'>Facebook Link:</span> {row['fb']}</p>
            <p><span class='bolded'>Rating:</span> {row['rating']}/5.0</p>
            <p><span class='bolded'>Specific Review:</span> {row['specifics']}</p>
        </div>
        """, unsafe_allow_html=True)
    