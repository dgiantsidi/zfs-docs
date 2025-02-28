import matplotlib.pyplot as plt
import re
import sys

# Function to parse the input file and extract TPS values
def parse_file(file_path):
    time_intervals = []
    tps_values = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            match = re.search(r'\[\s*(\d+)s\s*\].*tps:\s*([\d.]+)', line)
            if match:
                time_intervals.append(int(match.group(1)))
                tps_values.append(float(match.group(2)))

    return time_intervals, tps_values

# Main function to plot the TPS values
def main():
    file_path = sys.argv[1]  # Replace with your file path
    time_intervals, tps_values = parse_file(file_path)

    # Plot TPS values
    plt.figure(figsize=(12, 6))
    plt.plot(time_intervals, tps_values, label="TPS")
    plt.xlabel("Time Interval (seconds)")
    plt.ylabel("TPS")
    plt.title("TPS Over Time")
    plt.ylim(0, 2500)  # Set y-axis range from 0 to 2500

    plt.legend()
    plt.grid(True)
    plt.show()
    plt.savefig(file_path + ".png")

# Run the main function
if __name__ == "__main__":
    main()