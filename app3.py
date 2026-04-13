import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Data Analysis Application")
st.subheader("A simple application")

dataset_options = ['iris','titanic','tips','diamonds']
selected_dataset = st.selectbox('Select a dataset',dataset_options)

if selected_dataset == 'iris':
    df = sns.load_dataset('iris')
elif selected_dataset == 'titanic':
    df = sns.load_dataset('titanic')
elif selected_dataset == 'tips':
    df = sns.load_dataset('tips')
elif selected_dataset == 'diamonds':
    df = sns.load_dataset('diamonds')

custom_dataset = st.file_uploader("Upload custom dataset",type = ['csv','xlsx'])
if custom_dataset is not None:
    df = pd.read_csv(custom_dataset)

#st.write(df.head())
st.write(df)

# Displaying number of rows and columns
st.write("Number of rows: ",df.shape[0])
st.write("Number of columns: ",df.shape[1])

# Displaying the column names
st.write("Column Names and Data types: ",df.dtypes)

# Printing the null values
if df.isnull().sum().sum() > 0:
    st.write("Null Values: ",df.isnull().sum().sort_values(ascending = False))
else:
    st.write("No null values")

# Displaying the summary statistics
st.write("Summary Statistics: ",df.describe())

# Select the specific columns for X or Y axis from the dataset and also select the plot type to plot the data
#x_axis = st.selectbox('Select X-axis',df.columns)
#y_axis = st.selectbox('Select Y-axis',df.columns)
#plot_type = st.selectbox('Select Plot Type',['line','scatter','bar','hist','box','kde'])


# plotting the data
#if plot_type == 'line':
#    st.line_chart(df[[x_axis, y_axis]])
#elif plot_type == 'scatter':
#    st.scatter_chart(df[[x_axis, y_axis]])
#elif plot_type == 'bar':
#   st.bar_chart(df[[x_axis, y_axis]])
#elif plot_type == 'hist':
#    df[x_axis].plot(kind = 'hist')
#    st.pyplot()
#elif plot_type == 'box':
#    df[[x_axis, y_axis]].plot(kind = 'box')
#    st.pyplot()
#elif plot_type == 'kde':
#    df[[x_axis, y_axis]].plot(kind = 'kde')
#    st.pyplot()


# Creating the pairplot
st.subheader('Pairplot')
# Select the column to be used as hue
hue_column = st.selectbox('Select a column to be used as hue',df.columns)
st.pyplot(sns.pairplot(df, hue = hue_column))

# Create a heatmap
st.subheader('Heatmap')
# Select the columns which are numeric and then create a correlation matrix
numeric_columns = df.select_dtypes(include = np.number).columns
corr_matrix = df[numeric_columns].corr()

from plotly import graph_objects as go

heatmap_fig = go.Figure(data = go.Heatmap(z = corr_matrix.values,
                                          x = corr_matrix.columns,
                                          y = corr_matrix.columns,
                                          colorscale = 'Viridis'))
st.plotly_chart(heatmap_fig)