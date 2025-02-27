import matplotlib.pyplot as plt
import sys

# Function to parse the input file and extract CPU and device data
def parse_file(file_path):
    cpu_data = []
    device_data = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        cpu_section = False
        device_section = False

        for line in lines:
            line = line.strip()
            if line.startswith("avg-cpu:"):
                cpu_section = True
                device_section = False
                continue
            elif line.startswith("Device"):
                cpu_section = False
                device_section = True
                continue
            elif line == "":
                cpu_section = False
                device_section = False
                continue

            if cpu_section:
                parts = line.split()
#                print(parts)
                cpu_data.append({
                    "%user": float(parts[0]),
                    "%nice": float(parts[1]),
                    "%system": float(parts[2]),
                    "%iowait": float(parts[3]),
                    "%steal": float(parts[4]),
                    "%idle": float(parts[5])
                })
            elif device_section:
                parts = line.split()
                device_data.append({
                    "Device": parts[0],
                    "tps": float(parts[1])
                })

    return cpu_data, device_data

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)

    file_path = sys.argv[1]
    # Parse the input file
    cpu_data, device_data = parse_file(file_path)

    # Extract CPU utilization data
    cpu_user = [entry["%user"] for entry in cpu_data]
    cpu_system = [entry["%system"] for entry in cpu_data]
    cpu_idle = [entry["%idle"] for entry in cpu_data]

    # Extract TPS data for sda, sdb, and sdc
    tps_sda = [entry["tps"] for entry in device_data if entry["Device"] == "sda"]
    tps_sdb = [entry["tps"] for entry in device_data if entry["Device"] == "sdb"]
    tps_sdc = [entry["tps"] for entry in device_data if entry["Device"] == "sdc"]

    # Plot CPU utilization
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(cpu_user, label="%user")
    plt.plot(cpu_system, label="%system")
    plt.plot(cpu_idle, label="%idle")
    plt.xlabel("Time Interval")
    plt.ylabel("CPU Utilization (%)")
    plt.title("CPU Utilization Over Time")
    plt.legend()

    # Plot TPS for sda, sdb, and sdc
    plt.subplot(2, 1, 2)
    plt.plot(tps_sda, label="sda")
    plt.plot(tps_sdb, label="sdb")
    plt.plot(tps_sdc, label="sdc")
    plt.xlabel("Time Interval")
    plt.ylabel("TPS")
    plt.title("TPS for sda/sdb/sdc Over Time")
    plt.legend()

    # Show the plots
    plt.tight_layout()
    plt.show()
    plt.grid(True)
    plt.savefig(file_path + ".png")

     #Run the main function
if __name__ == "__main__":
    main()
