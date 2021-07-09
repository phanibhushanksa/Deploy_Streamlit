import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px

st.set_page_config(page_title='test',layout='wide')

st.write("""
## US population according to state and county
""")

# reading and editing our data frame.
pop_df = pd.read_excel('USA_County_Population.xlsx',skiprows=3)
pop_df.rename(columns = {'Unnamed: 0': 'Name'}, inplace = True)

# getting the population according to year
def popByYear(year):
    df = pop_df[['Name','Census',year]]
    df.dropna(inplace=True)
    df['County'] = [0]*len(df)
    df['State'] = [0]*len(df)

    i = 0
    for name in df['Name']:
        df.loc[i,'County'] = name.split(',')[0].replace('.','').replace('County','')
        i+=1

    i = 0
    for name in df['Name']:
        if len(name.split(',')) == 2:
            df.loc[i,'State'] = name.split(',')[1]
        i+=1

    df['Country'] = 'USA'
    df.drop([0],inplace=True)
    return df
    


st.write("""
## Select an year from the dropdown to view the population data
""")
year = st.selectbox(label = '',options=[2017,2018,2019])
pop_data = popByYear(year)
#st.dataframe(pop_data)
fig_tree = px.treemap(pop_data, path=[px.Constant('Country'), 'State', 'County'], values=year)                
st.plotly_chart(fig_tree,use_container_width=True)


st.write("""
### Visuals from Mock data
""")

# mental health by race
st.write("""
### Percentage of patients with positive mental health in each race
""")
mock_data = pd.read_csv('mock_data.csv')
races = mock_data['Race'].unique()
per_mental_by_race = {}

for race in races:
    total_race = mock_data[mock_data['Race'] == race]
    total_race_pos = total_race[total_race['Mental_Health']== True]
    per_mental_by_race[race] = total_race_pos.shape[0]/total_race.shape[0]*100

# st.write(per_mental_by_race)
bar_df = pd.DataFrame(per_mental_by_race.items(),
                columns=['Race','Percent of mental health patients'])

# bar chart
bar = px.bar(bar_df,x='Race',y = 'Percent of mental health patients')

st.plotly_chart(bar)
# all patients with a positive mental health condition.
mental_pos = mock_data[mock_data['Mental_Health']== True]

# mental health by gender
st.write("""
Number of mental health paitents by race and gender
""")
mH_data = mock_data[['Gender','Race','Mental_Health']]
gDf = mH_data.groupby(['Race','Gender']).sum().reset_index()
fig = px.bar(gDf,x='Race',y='Mental_Health',color='Gender')
st.plotly_chart(fig)

#making a pie chart for the above data.
# also changing the colors used in the chart.
st.write("""
Proportion of mental health patients by race 
""")
fig = px.pie(gDf,values='Mental_Health',names='Race',
        color_discrete_sequence=px.colors.qualitative.Vivid)
st.plotly_chart(fig)

# make a tree map using zipcode, and race in each zipcode.

df_zip_race = mock_data[['Zipcode','Race','Mental_Health']]\
              .groupby(['Zipcode','Race'])\
              .sum().reset_index()
fig_tree = px.treemap(df_zip_race, 
            path=['Zipcode','Race'], values='Mental_Health')
#st.plotly_chart(fig_tree)

# percentage of mental health patients who received treatment by race. 
st.write("""
## percentage of mental health patients who received treatment
""")
df_mental_treatment = pd.DataFrame(columns=['Race','Percent'])

for race in races:
    total_race = mock_data[mock_data['Race'] == race]
    total_race_pos = total_race[(total_race['Mental_Health']==True)]
    pos_treatment = total_race_pos[total_race_pos['Any_Treatment'] != "['None']"]
    percentage = pos_treatment.shape[0]/total_race_pos.shape[0]*100
    df_mental_treatment = df_mental_treatment.append({'Race':race,'Percent':percentage},
                ignore_index = True)

df_mental_treatment.columns = ['Race','Percentage of mental health patients who recieved some kind of care']
fig = px.bar(df_mental_treatment, x = 'Race',y = 'Percentage of mental health patients who recieved some kind of care')
st.plotly_chart(fig)

# displaying total number of mental health patients by zipcode
# on a map.


# distribution of age. 
st.write("""
Number of mental health patients in each age group. 
""")
mock_data['Age_Group'] = ''
for ind in mock_data.index:
    if mock_data['Age'][ind] in range(10,19):
        mock_data['Age_Group'][ind] = '10-18'
    elif mock_data['Age'][ind] in range(19,26):
        mock_data['Age_Group'][ind] = '19-25'
    elif mock_data['Age'][ind] in range(26,41):
        mock_data['Age_Group'][ind] = '26-40'
    elif mock_data['Age'][ind] in range(41,61):
        mock_data['Age_Group'][ind] = '41-60'
    else:
        mock_data['Age_Group'][ind] = 'Above 60'

df_age = mock_data[['Age_Group','Mental_Health']].\
            groupby('Age_Group').sum().reset_index()
df_age.columns = ['Age_Group','Number of Mental Health Patients']
fig = px.bar(df_age,x='Age_Group',y='Number of Mental Health Patients')
st.plotly_chart(fig)

fig = px.pie(df_age,)

# cooccurance of other diseases with mental illness.
# make a bar chart for that. 
