import os
import subprocess
import tempfile
import shutil
from multiprocessing import Pool
from tqdm import tqdm
import argparse

def convert_file(file, input_dir, output_dir):
    relative_path = os.path.relpath(file, input_dir)
    output_file = os.path.join(output_dir, os.path.splitext(relative_path)[0] + ".m4a")

    # Create the output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Check if the output file already exists
    if not os.path.exists(output_file):
        # Convert FLAC to ALAC using ffmpeg
        subprocess.run(["ffmpeg", "-i", file, "-acodec", "alac", output_file], check=True)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Convert FLAC files to ALAC")
    parser.add_argument("input_dir", help="Input directory containing FLAC files")
    parser.add_argument("output_dir", help="Output directory for converted ALAC files")
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir

    # Create a temporary file to store the list of FLAC files
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        # Find all FLAC files in the input directory and its subdirectories
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

    # Create a pool of worker processes
    with Pool() as pool:
        # Process the FLAC files in parallel with a progress bar
        list(tqdm(pool.starmap(convert_file, [(file, input_dir, output_dir) for file in flac_files]), total=total_files))

    # Remove the temporary file
    os.remove(temp_file_path)

    print("Conversion completed.")

if __name__ == "__main__":
    main()
