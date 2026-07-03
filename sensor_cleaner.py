"""
Piezoelectric Smart Material Sensor Log Clean-up

Loads, validates, cleans, plots, and saves voltage sensor data.
"""
#Updated documentation
import argparse
import pandas as pd
import matplotlib.pyplot as plt


def load_sensor_data(filename):
    """Load sensor data from a CSV file."""
    return pd.read_csv(filename)


def clean_sensor_data(data, voltage_min=-1.0, voltage_max=1.0):
    """Clean sensor data and return cleaned data plus a report."""

    report = {}

    data["Time"] = pd.to_numeric(data["Time"], errors="coerce")
    data["Voltage"] = pd.to_numeric(data["Voltage"], errors="coerce")

    report["missing_before"] = data.isna().sum().to_dict()

    data["Voltage"] = data["Voltage"].interpolate()
    data = data.dropna(subset=["Time", "Voltage"])

    report["missing_after"] = data.isna().sum().to_dict()

    report["duplicated_timestamps"] = data.duplicated(subset=["Time"]).sum()
    data = data.drop_duplicates(subset=["Time"])

    impossible = (data["Voltage"] < voltage_min) | (data["Voltage"] > voltage_max)
    report["impossible_voltage_count"] = impossible.sum()
    data = data[~impossible]

    mean_voltage = data["Voltage"].mean()
    std_voltage = data["Voltage"].std()

    if std_voltage == 0:
        spikes = data.iloc[0:0]
    else:
        spikes = data[abs(data["Voltage"] - mean_voltage) > 3 * std_voltage]

    report["spike_count"] = len(spikes)

    return data, report, spikes


def plot_signal(raw_data, cleaned_data):
    """Plot raw and cleaned voltage signals."""

    plt.figure()
    plt.plot(raw_data["Time"], raw_data["Voltage"], label="Raw signal")
    plt.plot(cleaned_data["Time"], cleaned_data["Voltage"], label="Cleaned signal")
    plt.xlabel("Time")
    plt.ylabel("Voltage")
    plt.title("Piezoelectric Sensor Voltage Signal")
    plt.legend()
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Clean piezoelectric sensor voltage data.")
    parser.add_argument("input_file", nargs="?", default="example_sensor_data.csv")
    parser.add_argument("--output", default="cleaned_sensor_data.csv")
    parser.add_argument("--min-voltage", type=float, default=-1.0)
    parser.add_argument("--max-voltage", type=float, default=1.0)
    
    args = parser.parse_args()
    
    raw_data = load_sensor_data(args.input_file)

    raw_data["Time"] = pd.to_numeric(raw_data["Time"], errors="coerce")
    raw_data["Voltage"] = pd.to_numeric(raw_data["Voltage"], errors="coerce")

    cleaned_data, report, spikes = clean_sensor_data(
        raw_data.copy(),
        voltage_min=args.min_voltage,
        voltage_max=args.max_voltage,
        )

    cleaned_data.to_csv(args.output, index=False)

    print("Cleaning report")
    print("---------------")
    print(f"Input file: {args.input_file}")
    print(f"Output file: {args.output}")
    print()
    print(f"Missing values before cleaning: {report['missing_before']}")
    print(f"Missing values after cleaning: {report['missing_after']}")
    print(f"Duplicated timestamps removed: {report['duplicated_timestamps']}")
    print(f"Impossible voltage readings removed: {report['impossible_voltage_count']}")
    print(f"Possible voltage spikes detected: {report['spike_count']}")
    print()
    print("Possible voltage spikes:")
    print(spikes)
    print()
    print(f"Cleaned data saved to {args.output}")
    
   
    plot_signal(raw_data, cleaned_data)


if __name__ == "__main__":
    main()