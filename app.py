import os


def rename_files_in_directory(directory, max_length=50):
    # List all files in the directory
    for filename in os.listdir(directory):
        # Full path of the file
        file_path = os.path.join(directory, filename)

        # Skip directories
        if os.path.isdir(file_path):
            continue

        # Extract the file extension
        file_extension = os.path.splitext(filename)[1]

        # If the filename is longer than max_length, rename it
        if len(filename) > max_length:
            # Create a new shorter name
            new_filename = filename[:max_length] + file_extension
            new_file_path = os.path.join(directory, new_filename)

            # Rename the file
            os.rename(file_path, new_file_path)
            print(f"Renamed: {filename} -> {new_filename}")


directory = (
    "/workspaces/dashboard-visualization-bps/PDRB Pengeluaran Publikasi Softfile"
)
rename_files_in_directory(directory)
