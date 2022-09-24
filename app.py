
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")


@st.cache
def get_data():
    df = pd.read_excel('100km Radius - AFN Dataset for Github.xlsx')
    return df


df = get_data()

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns(
    (.1, 2.3, .1, 1.3, .1))
with row0_1:
    st.title('Analyzer')


################
### ANALYSIS ###
################

@st.cache(ttl=24*60*60)
def chart1_data(band, year):
    df_filtered = df[df['Reference Year / Année de référence'] == year]
    df_filtered = df_filtered[df_filtered['Band Name'] == band]
    return df_filtered


def chart1(df_filtered):
    total_df_filtered = df_filtered.groupby(['Facility Name', 'Reporting Company Trade Name / Nom commercial de la société déclarante'])[
        'Total Emissions (tonnes CO2e) / Émissions totales (tonnes éq. CO2)'].sum().reset_index()

    fig = px.bar(total_df_filtered, x="Reporting Company Trade Name / Nom commercial de la société déclarante", y="Total Emissions (tonnes CO2e) / Émissions totales (tonnes éq. CO2)",
                 color='Facility Name')
    fig.update_layout(template='simple_white', xaxis_title='Reporting Company', xaxis={'categoryorder': 'total ascending'},
                      yaxis_title='Total Emissions (tonnes CO2e)', title='Total Emissions per Facility Name', height=600)  # barmode='stack'
    st.plotly_chart(fig, use_container_width=True)


@st.cache(ttl=24*60*60)
def chart2_data(band, year):
    df_filtered = df[df['Reference Year / Année de référence'] == year]
    df_filtered = df_filtered[df_filtered['Band Name'] == band]
    return df_filtered


def chart2(df_filtered):
    total_df_filtered = df_filtered.groupby(['Facility Name', "English Facility NAICS Code Description / Description du code SCIAN de l'installation en anglais"])[
        'Total Emissions (tonnes CO2e) / Émissions totales (tonnes éq. CO2)'].sum().reset_index()

    fig = px.bar(total_df_filtered, x="English Facility NAICS Code Description / Description du code SCIAN de l'installation en anglais", y="Total Emissions (tonnes CO2e) / Émissions totales (tonnes éq. CO2)",
                 color='Facility Name')
    fig.update_layout(template='simple_white', xaxis_title='English Facility NAICS Code Description', xaxis={'categoryorder': 'total ascending'},
                      yaxis_title='Total Emissions (tonnes CO2e)', title='Total Emissions per English Facility NAICS Code', height=600)  # barmode='stack'
    st.plotly_chart(fig, use_container_width=True)


@st.cache(ttl=24*60*60)
def chart3_data(band):
    df2 = df[df['Band Name'] == band]
    color = "English Facility NAICS Code Description / Description du code SCIAN de l'installation en anglais"
    top_cats = df2[color].value_counts().head(10).index.tolist()
    df2.loc[~df2[color].isin(top_cats), color] = 'Others'
    return df2


def chart3(df2):
    fig = px.bar(df2, y='Total Emissions (tonnes CO2e) / Émissions totales (tonnes éq. CO2)', x='Reference Year / Année de référence',
                 color="English Facility NAICS Code Description / Description du code SCIAN de l'installation en anglais")

    # fig.update_layout(template='simple_white',
    #                   title=' Total Emissions per Refrence Year', height=600)
    fig.update_layout(template='simple_white', yaxis_title='Total Emissions (tonnes CO2e)',
                      title=' Total Emissions per Refrence Year', height=600,
                      legend=dict(orientation="h", yanchor="top", y=-1.02, xanchor="right", x=1, title='NAICS Code'))

    st.plotly_chart(fig, use_container_width=True)


row4_spacer1, row4_1, row4_spacer2 = st.columns((.2, 7.1, .2))
with row4_1:
    st.subheader('Chart 1: Total Emissions per Facility Name')
row5_spacer1, row5_1, row5_spacer2, row5_2, row5_spacer3 = st.columns(
    (.2, 2.3, .4, 4.4, .2))
with row5_1:
    band_chart1 = st.selectbox("Please select Band Name", list(
        df['Band Name'].unique()), key='band_chart1', index=363)
    year_chart1 = st.selectbox("Please elect year", list(
        df['Reference Year / Année de référence'].unique()), key='year_chart1')

with row5_2:
    df_filtered = chart1_data(band_chart1, year_chart1)
    chart1(df_filtered)

row6_spacer1, row6_1, row6_spacer2 = st.columns((.2, 7.1, .2))
with row6_1:
    st.subheader('Chart 2: Total Emissions per English Facility NAICS Code')
row7_spacer1, row7_1, row7_spacer2, row7_2, row7_spacer3 = st.columns(
    (.2, 2.3, .4, 4.4, .2))
with row7_1:
    band_chart2 = st.selectbox("Please select Band Name", list(
        df['Band Name'].unique()), key='band_chart2', index=363)
    year_chart2 = st.selectbox("Please select year", list(
        df['Reference Year / Année de référence'].unique()), key='year_chart2')

with row7_2:
    df_filtered = chart2_data(band_chart2, year_chart2)
    chart2(df_filtered)

row8_spacer1, row8_1, row8_spacer2 = st.columns((.2, 7.1, .2))
with row8_1:
    st.subheader('Chart 3: Total Emissions per Refrence Year')
row9_spacer1, row9_1, row9_spacer2, row9_2, row9_spacer3 = st.columns(
    (.2, 2.3, .4, 4.4, .2))
with row9_1:
    band_chart3 = st.selectbox("Please select Band Number", list(
        df['Band Name'].unique()), key='band_chart3')
with row9_2:
    df2 = chart3_data(band_chart3)
    chart3(df2)
