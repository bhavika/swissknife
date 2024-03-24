import os
import argparse
from collections import defaultdict
from heapq import nlargest

ALAC_DIR = "files/apple_music"
OUTPUT_DIR = "ipod"

def process_directory(directory):
   audio_formats = {'.mp3', '.wav', '.flac', '.aac', '.m4a', '.ogg', '.wma', '.alac'}
   audio_counts = defaultdict(int)
   other_counts = defaultdict(int)
   directory_sizes = defaultdict(int)
   missing_flacs = []
   format_files = defaultdict(list)

   for root, dirs, files in os.walk(directory):
       for file in files:
           file_path = os.path.join(root, file)
           file_extension = os.path.splitext(file)[1].lower()

           if file_extension in audio_formats:
               audio_counts[file_extension] += 1
               format_files[file_extension].append(file_path)

               if file_extension == '.flac':
                   alac_path = os.path.join(ALAC_DIR, os.path.relpath(file_path, directory))
                   alac_path = os.path.splitext(alac_path)[0] + '.m4a'
                   if not os.path.exists(alac_path):
                       missing_flacs.append(file_path)
           else:
               other_counts[file_extension] += 1
           directory_sizes[root] += os.path.getsize(file_path)

   # Write missing FLACs to file
   with open(f"{OUTPUT_DIR}/missing_flac.txt", 'w') as f:
       f.write('\n'.join(missing_flacs))

   # Write file paths per audio format to separate files
   for fmt, files in format_files.items():
       with open(f'{OUTPUT_DIR}/{fmt[1:]}_files.txt', 'w') as f:
           f.write('\n'.join(files))

   top_directories = nlargest(10, directory_sizes.items(), key=lambda x: x[1])

   print("Audio file counts:")
   for fmt, count in audio_counts.items():
       print(f"{format}: {count}")

   print("\nOther file counts:")
   for fmt, count in other_counts.items():
       print(f"{format}: {count}")

   print("\nTop 10 largest directories:")
   for directory, size in top_directories:
       print(f"{directory}: {size} bytes")

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Process directory and generate file statistics.')
parser.add_argument('input_directory', type=str, help='Path to the input directory')
args = parser.parse_args()

process_directory(args.input_directory)