import streamlit as st
import pandas as pd
import numpy as np
import time

st.title("Simple Streamlit Demo")

name = st.text_input("Enter your name: ")

num = st.selectbox("Select a number: ", list(range(1, 6)))

if st.button("Submit"):
    st.success(f"Hello, {name}! You selected number {num}.")

st.subheader("Random Data Chart")
data = pd.DataFrame(np.random.randn(10, 2), columns=["A", "B"])
st.line_chart(data)

st.subheader("Progress Bar Simulation")
progress_bar = st.progress(0)
for i in range(100):
    time.sleep(0.02)
    progress_bar.progress(i+1)

st.success("Progress Completed!")
