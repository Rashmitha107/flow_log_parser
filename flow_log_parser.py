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
def parse_flow_logs(file_path, lookup_table):
    tag_counts = defaultdict(int)  # Stores count for each tag
    port_protocol_counts = defaultdict(int)  # Stores count for each port/protocol combination

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) < 12:
                continue  # Skip malformed lines

            # Extract relevant fields from flow log
            dstport = parts[6]   # This is the destination port (Column 7 in the flow log)
            protocol_number = parts[7]  # This is the protocol number (Column 8 in the flow log)

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
    
    flow_log_file = 'flow_logs.txt' 
    lookup_file = 'lookup_table.csv' 
    output_file = 'output.csv' 

    # Parse the lookup table
    lookup_table = parse_lookup_table(lookup_file)
    
    # Parse flow logs and generate the counts
    tag_counts, port_protocol_counts = parse_flow_logs(flow_log_file, lookup_table)
    
    # Write the output to a file
    write_output(tag_counts, port_protocol_counts, output_file)
    
    print(f"Results saved in {output_file}")

if __name__ == "__main__":
    main()
