'''
This Python file uses functions created inside main.py file
to create complete analysis of all sample images.
'''

from main import analyzeParticles, savePlots, getSummary
import pandas as pd
import os

# Reading mean length (in pixels) from scale calibration table
scale = 0.3

# Empty variable data which will contain measurements of all images
data = []

# Function from main.py: creates sample{i}.csv file
analyzeParticles("sample1.png", scale=scale, knownDistance=0.01, distinguishJuveniles=True)

# Read created csv file and transfer data to data variable
df = pd.read_csv("results/sample1.csv")
df = df.reset_index()

for index, row in df.iterrows():
    row["Sample Image Index"] = int(1)
    row["Feret\'s Diameter [μm]"] = round(row["Feret\'s diameter"] * 1000, 3)
    data.append(row)

# Remove used csv file
os.remove("results/sample1.csv")

# Sorting of data ascending by particle size
df = pd.DataFrame(data)
df_sorted = df.sort_values("Feret\'s diameter", ascending=True)
df_sorted = df_sorted.drop(df.columns[0], axis=1)

# Getting statistics summary of particle size variable
feret = df_sorted["Feret\'s Diameter [μm]"]
summary = getSummary(variable = feret)

'''
Create Excel file containing 2 sheets:
    1) all measurements from all images
    2) summary statistics
'''
writer = pd.ExcelWriter("results/collembolan_size_analysis.xlsx", engine = 'xlsxwriter')
df_sorted.to_excel(writer, sheet_name='measurements')
summary.to_excel(writer, sheet_name='summary')
writer.save()
writer.close()

# Create and save boxplot and histogram of particle size parameter
savePlots(variable = feret)