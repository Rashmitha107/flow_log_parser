from collections import defaultdict

# Mapping of protocol numbers to protocol names
PROTOCOL_MAPPING = {
    '1': 'icmp',
    '2': 'igmp',
    '6': 'tcp',
    '17': 'udp',
    # Add more mappings if needed.
}

# Parse the lookup table CSV to map dstport/protocol to tags.
def parse_lookup_table(file_path):
    lookup = {}
    with open(file_path, 'r') as file:
        # Skip the header line if exists
        header = file.readline()
        for line in file:
            parts = line.strip().split(',')
            dstport = parts[0]    # destination port
            protocol = parts[1].lower()  # protocol in lookup table
            tag = parts[2]
            # Store tags in a list to handle multiple tags for same port/protocol
            if (dstport, protocol) in lookup:
                lookup[(dstport, protocol)].append(tag)
            else:
                lookup[(dstport, protocol)] = [tag]
    return lookup

# Parse the flow log file and map each entry to tags using the lookup table.
def parse_flow_logs(file_path, lookup_table, flow_log_type="default", dstport_index=6, protocol_index=7):
    tag_counts = defaultdict(int)  # Stores count for each tag
    port_protocol_counts = defaultdict(int)  # Stores count for each port/protocol combination

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) <= max(dstport_index, protocol_index):
                continue  # Skip malformed lines

            # Extract relevant fields from flow log
            dstport = parts[dstport_index]
            protocol_number = parts[protocol_index]

            # Convert protocol number to protocol name
            protocol = PROTOCOL_MAPPING.get(protocol_number, None)
            if not protocol:
                protocol = 'unknown'  # If protocol is not found in the mapping

            # Retrieve tags from the lookup table
            tags = lookup_table.get((dstport, protocol), ['Untagged'])

            # Update counts for each tag
            for tag in tags:
                tag_counts[tag] += 1
            
            # Update port/protocol combination counts
            port_protocol_counts[(dstport, protocol)] += 1

    return tag_counts, port_protocol_counts
    
# Write the tag counts and port/protocol combination counts to an output file.
def write_output(tag_counts, port_protocol_counts, output_file):
    with open(output_file, 'w') as file:
        file.write("Tag Counts:\n")
        file.write("Tag,Count\n")
        for tag, count in tag_counts.items():
            file.write(f"{tag},{count}\n")
        
        file.write("\nPort/Protocol Combination Counts:\n")
        file.write("Port,Protocol,Count\n")
        for (port, protocol), count in port_protocol_counts.items():
            file.write(f"{port},{protocol},{count}\n")

def main():
    
    use_default = input("Do you want to use the default files (flow_logs.txt, lookup_table.csv, output.csv)? (y/n): ").strip().lower()

    if use_default == 'y':
        flow_log_file = 'flow_logs.txt'  # Default flow log file path
        lookup_file = 'lookup_table.csv'  # Default lookup table CSV file path
        output_file = 'output.csv'  # Default output file path
        flow_log_type = "default"  # Automatically set to default for default files
        dstport_index = 6  # Default: destination port is column 7 (index 6)
        protocol_index = 7  # Default: protocol is column 8 (index 7)
    else:
        flow_log_file = input("Enter the path to the flow log file: ").strip()
        lookup_file = input("Enter the path to the lookup table CSV file: ").strip()
        output_file = input("Enter the path to the output file: ").strip()
        flow_log_type = input("Is the flow log format default or custom? (default/custom): ").strip().lower()

        if flow_log_type == "custom":
            dstport_index = int(input("Enter the column number for destination port: ").strip()) - 1
            protocol_index = int(input("Enter the column number for protocol: ").strip()) - 1
        else:
            dstport_index = 6  # Default: destination port is column 7
            protocol_index = 7  # Default: protocol is column 8 

    # Parse the lookup table
    lookup_table = parse_lookup_table(lookup_file)
    
    # Parse flow logs and generate the counts
    tag_counts, port_protocol_counts = parse_flow_logs(flow_log_file, lookup_table, flow_log_type, dstport_index, protocol_index)
    
    # Write the output to a file
    write_output(tag_counts, port_protocol_counts, output_file)
    
    print(f"Results saved in {output_file}")

if __name__ == "__main__":
    main()
