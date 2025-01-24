# ReadMe for Flow Logs Parser

## 1. Running the Program

### Using Default Files:
1. Ensure the following files are in the same directory as the script:
   - `flow_logs.txt`: Contains the flow log entries.
   - `lookup_table.csv`: Contains the mapping of destination ports and protocols to tags.
   - `output.csv`: The file where the results will be saved.
2. Run the script and choose the default option (`y`) when prompted:
   ```bash
   python flow_logs_parser.py
   ```
3. The program will parse the flow logs, apply the lookup table, and save the results to `output.csv`.

### Using Custom Files:
1. Provide the paths to your custom files when prompted.
2. Specify whether your flow log format is default(version 2) or custom.
3. For custom formats, input the column numbers for the destination port and protocol when prompted.
4. Run the program, and it will generate the output at the specified location.

---

## 2. Assumptions
- The `flow_logs.txt` file contains space-separated entries.
- The `lookup_table.csv` is a comma-separated file with three columns: destination port, protocol, and tag.
- Default column indices for destination port and protocol in flow logs are 6 and 7, respectively.
- Protocol numbers in the flow logs are mapped to names using the `PROTOCOL_MAPPING` dictionary.
- Entries with unknown protocols are tagged as `unknown`.
- Entries without a matching tag in the lookup table are tagged as `Untagged`.

---

## 3. Potential Improvements
- **Dynamic Protocol Mapping:** Extend `PROTOCOL_MAPPING` to include all protocol numbers as per the IANA registry.
- **Error Handling:** Improve robustness by handling file I/O errors, malformed lines, and invalid inputs more gracefully.
- **Output Format:** Allow users to choose between CSV, JSON, or other formats for the output.

---

## 4. Scaling for Large Data Volumes
- **Streaming Processing:** Instead of loading entire files into memory, process the flow logs line by line to reduce memory usage.
- **Parallel Processing:** Use Python's multiprocessing library or frameworks like Apache Spark to handle large-scale log data efficiently.
- **Database Integration:** Load the flow logs and lookup table into a database for efficient querying and scalability.
- **Cloud Solutions:** Utilize cloud services like AWS Lambda, S3, and Athena for serverless and distributed processing.

---

## 5. Additional Metrics
- **Top Tags:** Identify the most frequently occurring tags.
- **Protocol Distribution:** Calculate the percentage of each protocol type.
- **Port Utilization:** List the most commonly used destination ports.
- **Time-Based Analysis:** Add a timestamp column to the logs for temporal analysis of traffic patterns.

---
