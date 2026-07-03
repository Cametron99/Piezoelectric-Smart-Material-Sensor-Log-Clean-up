"""
Piezoelectric Smart Material Sensor Log Clean-up

Author: Cameron Spalding

This script loads voltage measurements from a CSV file and displays
basic information about the dataset.
"""

import pandas as pd


def load_sensor_data(filename):
"""Load sensor data from a CSV file."""
data = pd.read_csv(filename)
return data


def main():
filename = "example_sensor_data.csv"

try:
data = load_sensor_data(filename)

print("Dataset loaded successfully!")
print()

print(data.head())

print()
print(f"Number of rows: {len(data)}")
print(f"Number of columns: {len(data.columns)}")

except FileNotFoundError:
print(f"Error: '{filename}' was not found.")


if __name__ == "__main__":
main()
