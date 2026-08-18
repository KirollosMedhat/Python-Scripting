import os
import shutil
import sys
import time
from pathlib import Path


def main(inputPath:str):
    sortingPath = Path(inputPath)
    for file in os.listdir(sortingPath):
        name, ext = os.path.splitext(file)
        
        if len(ext) == 0: continue
        destinationName = f"/{ext[1:]}_files/"

        os.makedirs(Path(f"{sortingPath}{destinationName}"), exist_ok=True)
        shutil.move(Path(f"{sortingPath}/{file}"), Path(f"{sortingPath}{destinationName}"))

if __name__ == "__main__":
    print(f"\n\nStarted Sorting Directory:  {sys.argv[1]}\n\n")

    start_time = time.perf_counter()
    main(sys.argv[1])
    end_time = time.perf_counter()

    execution_time = end_time - start_time

    print(f"Script took {execution_time:.4f} seconds to complete.\n\n")
