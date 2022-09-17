import streamlit as st
import pandas as pd
import numpy as np


# import pandas dataset
@st.cache
def read_file():
    orders = pd.read_csv("orders.csv", encoding="ISO-8859-1")
    return orders


orders = read_file()

results = pd.pivot_table(orders, index='Salesperson',
                         aggfunc=np.sum,
                         values=["Revenue"],
                         margins=True)
