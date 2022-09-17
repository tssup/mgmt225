import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt




st.set_page_config(page_title = "First App",
                    layout = "wide")

#read data
df = pd.read_csv("train.csv")




st.title("Second App in Streamlit")
bldg_type_input = st.selectbox("Choose the building type", options = df.BldgType.unique()) 

filtered_df = df[df["BldgType"] == bldg_type_input]


st.markdown("###")

colA, colB, colC = st.columns(3)
fig = plt.figure()
ax = fig.add_subplot()
sns.scatterplot(data = filtered_df, y = filtered_df.SalePrice, x = filtered_df.LotArea)
colA.pyplot(fig)

fig = plt.figure()
ax = fig.add_subplot()
sns.scatterplot(data = filtered_df, y = filtered_df.SalePrice, x = filtered_df.LotArea)
colB.pyplot(fig)

fig = plt.figure()
ax = fig.add_subplot()
sns.scatterplot(data = filtered_df, y = filtered_df.SalePrice, x = filtered_df.LotArea)
colC.pyplot(fig)

st.markdown("----")

st.sidebar.header("Enter the details")