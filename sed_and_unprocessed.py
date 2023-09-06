import os
import shutil
import zipfile
import csv

def remove_includes(file_path):
    temp_file = file_path + ".tmp"
    with open(file_path, 'r') as input_file, open(temp_file, 'w') as output_file:
        for line in input_file:
            if not line.strip().startswith("#include"):
                output_file.write(line)
    shutil.move(temp_file, file_path)


def process_unprocessed_files(source_path, destination_path):
    output_file_path = os.path.join(destination_path, "processed_output.csv")

    with open(output_file_path, 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(['File Name', 'Processed Data'])  # Write header

        for root, dirs, files in os.walk(source_path):
            for file_name in files:
                if file_name.lower().endswith(".unprocessed"):
                    file_path = os.path.join(root, file_name)
                    processed_data = []
                    current_data = []

                    with open(file_path, 'r') as input_file:
                        for line in input_file:
                            stripped_line = line.strip()
                            if stripped_line:
                                if stripped_line != "-" * 80:  # Skip lines containing only hyphens
                                    current_data.append(stripped_line.split()[0])
                            elif current_data:
                                processed_data.append('\n'.join(current_data))
                                current_data = []

                    if current_data:  # Handle the last section if there is any
                        processed_data.append('\n'.join(current_data))

                    if processed_data:
                        for data_section in processed_data:
                            csv_writer.writerow([file_name, data_section])

                    # Move the processed file to another location if needed
                    processed_file_path = os.path.join(destination_path, file_name)
                    shutil.move(file_path, processed_file_path)

    print("Processing completed and CSV file generated.")


def main():
    action = input("Enter 'sed' to remove #include lines or 'extract' to perform extraction and moving or 'process' for processing unprocessed files: ")


    if action == "sed":
        source_path = input("Enter the source folder path: ")
        for root, dirs, files in os.walk(source_path):
            for file_name in files:
                if file_name.lower().endswith((".cpp", ".h")):
                    file_path = os.path.join(root, file_name)
                    remove_includes(file_path)
        print("Lines starting with '#include' removed.")

    elif action == "extract":
        source_path = input("Enter the source folder path: ")
        destination_path = input("Enter the destination folder path: ")

        for root, dirs, files in os.walk(source_path):
            for file_name in files:
                if file_name.lower().endswith(".zip"):
                    zip_file_path = os.path.join(root, file_name)
                    extract_folder = os.path.join(destination_path, file_name.replace(".zip", ""))
                    os.makedirs(extract_folder, exist_ok=True)

                    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                        zip_ref.extractall(extract_folder)

                    for extracted_root, extracted_dirs, extracted_files in os.walk(extract_folder):
                        for extracted_file in extracted_files:
                            if extracted_file.lower().endswith(".unprocessed"):
                                src_file = os.path.join(extracted_root, extracted_file)
                                dest_file = os.path.join(destination_path, extracted_file)
                                shutil.move(src_file, dest_file)

                    shutil.rmtree(extract_folder)

        print("Extraction and moving completed.")

    elif action == "process":
        source_path = input("Enter the source folder path: ")
        destination_path = input("Enter the destination folder path: ")

        process_unprocessed_files(source_path, destination_path)
        print("Processing completed.")

    else:
        print("Invalid action.")

if __name__ == "__main__":
    main()
