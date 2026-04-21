# Import required libraries
import pandas as pd
import numpy as np

# -------------------------------
# Task 1: Create DataFrames
# -------------------------------

# Project DataFrame
project_data = pd.DataFrame([
    ["A001","Project 1",1002000,"Finished"],
    ["A002","Project 2",2000000,"Ongoing"],
    ["A003","Project 3",4500000,"Finished"],
    ["A004","Project 4",5500000,"Ongoing"],
    ["A005","Project 5",np.nan,"Finished"],
    ["A002","Project 6",680000,"Failed"],
    ["A005","Project 7",400000,"Finished"],
    ["A003","Project 8",350000,"Failed"],
    ["A001","Project 9",np.nan,"Ongoing"],
    ["A003","Project 10",300000,"Finished"],
    ["A001","Project 11",2000000,"Failed"],
    ["A004","Project 12",1000000,"Ongoing"],
    ["A004","Project 13",3000000,"Finished"],
    ["A005","Project 14",200000,"Finished"]
], columns=["ID","Project","Cost","Status"])

project_data.to_csv("project_data.csv", index=False)

# Employee DataFrame
employee_data = pd.DataFrame([
    ["A001","John Alter","M","Paris",25],
    ["A002","Alice Luxumberg","F","London",27],
    ["A003","Tom Sabestine","M","Berlin",29],
    ["A004","Nina Adgra","F","Newyork",31],
    ["A005","Amy Johny","F","Madrid",30]
], columns=["ID","Name","Gender","City","Age"])

employee_data.to_csv("employee_data.csv", index=False)

# Seniority DataFrame
seniority_level = pd.DataFrame([
    ["A001",2],
    ["A002",2],
    ["A003",3],
    ["A004",2],
    ["A005",3]
], columns=["ID","Designation Level"])

seniority_level.to_csv("seniority_level.csv", index=False)

# -------------------------------
# Task 2: Fill missing Cost using running average
# -------------------------------
cost_sum = 0
count = 0

for i in range(len(project_data)):
    if pd.isna(project_data.loc[i, "Cost"]):
        running_avg = cost_sum / count
        project_data.loc[i, "Cost"] = running_avg
        cost_sum += running_avg
    else:
        cost_sum += project_data.loc[i, "Cost"]
    count += 1

# -------------------------------
# Task 3: Split Name column
# -------------------------------
employee_data[["First Name","Last Name"]] = employee_data["Name"].str.split(" ", expand=True)
employee_data = employee_data.drop(columns=["Name"])

# -------------------------------
# Task 4: Merge DataFrames
# -------------------------------
final = pd.merge(project_data, employee_data, on="ID")
final = pd.merge(final, seniority_level, on="ID")

# -------------------------------
# Task 5: Add Bonus column
# -------------------------------
final["Bonus"] = 0

for i in range(len(final)):
    if final.loc[i, "Status"] == "Finished":
        final.loc[i, "Bonus"] = final.loc[i, "Cost"] * 0.05

# -------------------------------
# Task 6: Demote on failure & remove invalid levels
# -------------------------------
for i in range(len(final)):
    if final.loc[i, "Status"] == "Failed":
        final.loc[i, "Designation Level"] -= 1

final = final[final["Designation Level"] <= 4]

# -------------------------------
# Task 7: Add Mr./Mrs. and drop Gender
# -------------------------------
for i in range(len(final)):
    if final.loc[i, "Gender"] == "M":
        final.loc[i, "First Name"] = "Mr. " + final.loc[i, "First Name"]
    else:
        final.loc[i, "First Name"] = "Mrs. " + final.loc[i, "First Name"]

final = final.drop(columns=["Gender"])

# -------------------------------
# Task 8: Promote based on age
# -------------------------------
for i in range(len(final)):
    if final.loc[i, "Age"] > 29:
        final.loc[i, "Designation Level"] += 1

# -------------------------------
# Task 9: Total Project Cost
# -------------------------------
total_proj_cost = final.groupby(["ID","First Name"])["Cost"].sum().reset_index()
total_proj_cost = total_proj_cost.rename(columns={"Cost": "Total Cost"})

# -------------------------------
# Task 10: Filter city containing 'o'
# -------------------------------
employees_with_o = final[final["City"].str.contains("o")]

# -------------------------------
# Output Results
# -------------------------------
print("\nFinal DataFrame:\n", final)
print("\nTotal Project Cost:\n", total_proj_cost)
print("\nEmployees with 'o' in city:\n", employees_with_o)
