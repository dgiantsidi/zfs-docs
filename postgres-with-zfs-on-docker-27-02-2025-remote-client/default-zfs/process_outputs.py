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
                    "tps": float(parts[1]),
                    "kB_reads/s": float(parts[2]),
                    "kB_wrtn/s": float(parts[3]),
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
    time_intervals = list(range(1, len(cpu_user) + 1))
    time_intervals_text = list(range(0, len(cpu_user)*10, 10))
    

    # Extract TPS data for sda, sdb, and sdc
    tps_sda = [entry["tps"] for entry in device_data if entry["Device"] == "sda"]
    tps_sdb = [entry["tps"] for entry in device_data if entry["Device"] == "sdb"]
    tps_sdc = [entry["tps"] for entry in device_data if entry["Device"] == "sdc"]

    # Extract kB_read/s  kB_wrtn/s data for sda, sdb, and sdc
    readspers_sda = [entry["kB_reads/s"] for entry in device_data if entry["Device"] == "sda"]
    readspers_sdb = [entry["kB_reads/s"] for entry in device_data if entry["Device"] == "sdb"]
    readspers_sdc = [entry["kB_reads/s"] for entry in device_data if entry["Device"] == "sdc"]
    writespers_sda = [entry["kB_wrtn/s"] for entry in device_data if entry["Device"] == "sda"]
    writespers_sdb = [entry["kB_wrtn/s"] for entry in device_data if entry["Device"] == "sdb"]
    writespers_sdc = [entry["kB_wrtn/s"] for entry in device_data if entry["Device"] == "sdc"]

    # Plot CPU utilization
    plt.figure(figsize=(12, 12))
    plt.subplot(3, 1, 1)
    plt.plot(time_intervals_text, cpu_user, label="%user")
    plt.plot(time_intervals_text, cpu_system, label="%system")
    plt.plot(time_intervals_text, cpu_idle, label="%idle")
    plt.xlabel("Time Interval")
    plt.ylabel("CPU Utilization (%)")
    plt.title("CPU Utilization Over Time")
    plt.legend()

    # Plot TPS for sda, sdb, and sdc
    plt.subplot(3, 1, 2)
    plt.plot(time_intervals_text, tps_sda, label="sda")
    plt.plot(time_intervals_text, tps_sdb, label="sdb")
    plt.plot(time_intervals_text, tps_sdc, label="sdc")
    plt.xlabel("Time Interval")
    plt.ylabel("TPS")
    plt.title("TPS for sda/sdb/sdc Over Time")
    plt.legend()
    #plt.xticks(time_intervals, time_intervals_text)  # Set custom x-axis labels

    
    # Plot TPS for sda, sdb, and sdc
    plt.subplot(3, 1, 3)
    plt.plot(time_intervals_text, readspers_sda, label="sda (kB_reads/s)")
    plt.plot(time_intervals_text, readspers_sdb, label="sdb (kB_reads/s)")
    plt.plot(time_intervals_text, readspers_sdc, label="sdc (kB_reads/s)")
    plt.plot(time_intervals_text, writespers_sda, label="sda (kB_wrtn/s)")
    plt.plot(time_intervals_text, writespers_sdb, label="sdb (kB_wrtn/s)")
    plt.plot(time_intervals_text, writespers_sdc, label="sdc (kB_wrtn/s)")
    plt.xlabel("Time Interval")
    #plt.ylabel("Reads (KB) and writes (KB)")
    plt.title("Reads/Writes (KBs/s) sda/sdb/sdc Over Time")
    plt.legend()

    # Show the plots
    plt.tight_layout()
    plt.show()
    plt.grid(True)
    plt.savefig(file_path + ".png")

     #Run the main function
if __name__ == "__main__":
    main()
