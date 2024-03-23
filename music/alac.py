import os
import subprocess
import tempfile
import shutil
from multiprocessing import Pool
from tqdm import tqdm
import argparse

def convert_file(file, input_dir, output_dir, error_log_path):
    relative_path = os.path.relpath(file, input_dir)
    output_file = os.path.join(output_dir, os.path.splitext(relative_path)[0] + ".m4a")
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Check if the output file already exists
    if not os.path.exists(output_file):
        try:
            # Convert FLAC to ALAC using ffmpeg
            subprocess.run(["ffmpeg", "-i", file, "-acodec", "alac", output_file], check=True)
        except subprocess.CalledProcessError:
            # Log the file path to the error log file
            with open(error_log_path, "a") as error_log:
                error_log.write(file + "\n")

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Convert FLAC files to ALAC")
    parser.add_argument("input_dir", help="Input directory containing FLAC files")
    parser.add_argument("output_dir", help="Output directory for converted ALAC files")
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if file.endswith(".flac"):
                    temp_file.write(os.path.join(root, file) + "\n")
        temp_file_path = temp_file.name

    # Read the list of FLAC files from the temporary file
    with open(temp_file_path, "r") as file:
        flac_files = file.read().splitlines()

    # Get the total number of FLAC files
    total_files = len(flac_files)

    with Pool() as pool:
        # Create a temporary directory to store error log files for each process
        with tempfile.TemporaryDirectory() as temp_dir:   
            list(tqdm(pool.starmap(convert_file, [(file, input_dir, output_dir, os.path.join(temp_dir, f"error_log_{i}.log")) for i, file in enumerate(flac_files)]), total=total_files))

            # Combine the error log files into a single file
            error_log_path = "conversion_errors.log"
            with open(error_log_path, "w") as error_log:
                for i in range(len(flac_files)):
                    process_error_log_path = os.path.join(temp_dir, f"error_log_{i}.log")
                    if os.path.exists(process_error_log_path):
                        with open(process_error_log_path, "r") as process_error_log:
                            error_log.write(process_error_log.read())

    print("Conversion completed.")
    print(f"Errors, if any, are logged in: {error_log_path}")

if __name__ == "__main__":
    main()
