import os
import shutil
import time
import logging

# Set up logging
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up logging to write messages to the console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
# Function to replicate source folder to replica folder
def replicate_folder(source_folder, replica_folder):
    for root, dirs, files in os.walk(source_folder):
        for directory in dirs:
            source_path = os.path.join(root, directory)
            replica_path = os.path.join(replica_folder, os.path.relpath(source_path, source_folder))
            if not os.path.exists(replica_path):
                os.mkdir(replica_path)
                logging.info('Folder created: %s', replica_path)
                print('Folder created:', replica_path)

        for file in files:
            source_path = os.path.join(root, file)
            replica_path = os.path.join(replica_folder, os.path.relpath(source_path, source_folder))
            if not os.path.exists(replica_path):
                shutil.copy2(source_path, replica_path)
                logging.info('File copied: %s -> %s', source_path, replica_path)
                print('File copied:', source_path, '->', replica_path)
            elif os.stat(source_path).st_mtime - os.stat(replica_path).st_mtime > 1:
                shutil.copy2(source_path, replica_path)
                logging.info('File copied: %s -> %s', source_path, replica_path)
                print('File copied:', source_path, '->', replica_path)
                
    # Remove files in replica folder that do not exist in source folder
    for root, dirs, files in os.walk(replica_folder):
        for file in files:
            replica_path = os.path.join(root, file)
            source_path = os.path.join(source_folder, os.path.relpath(replica_path, replica_folder))
            if not os.path.exists(source_path):
                os.remove(replica_path)
                logging.info('File removed: %s', replica_path)
                print('File removed:', replica_path)

        for directory in dirs:
            replica_path = os.path.join(root, directory)
            source_path = os.path.join(source_folder, os.path.relpath(replica_path, replica_folder))
            if not os.path.exists(source_path):
                shutil.rmtree(replica_path)
                logging.info('Folder removed: %s', replica_path)
                print('Folder removed:', replica_path)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("interval", type=int, help="Interval in seconds")
    parser.add_argument("folder1", help="Path to folder 1.")
    parser.add_argument("folder2", help="Path to folder 2.")
    args = parser.parse_args()

    folder1_path = args.folder1
    folder2_path = args.folder2
    interval=args.interval
    #source_folder = 'D:\ANJU\solo'
    #replica_folder = 'D:\ANJU\solo1'

    while True:
        replicate_folder(folder1_path, folder2_path)
        time.sleep(interval)