import json
import os
import logging
from pathlib import Path
from tqdm import tqdm
from sys import argv
from contextlib import suppress

HELP_DOC = f"""Usage: {argv[0]} <hash_dir> <obj_dir> -o <out_dir> [<options>]
Extract game assets files of Minecraft Java Edition.

Arguments:
    <hash_dir>   JSON map directory
    <obj_dir>    Resource files directory (.minecraft/assets/objects/)
    -o <out_dir> Specify the output directory
Options:
    -h, --help      Show this help message and exit
    -v, --version   Show version information and exit
"""

def extract_assets(hash_dir: str, obj_dir: str, out_dir: str):
    """
    Extract assets from Minecraft resource files and save them with the original directory structure.

    :param hash_dir: JSON map directory
    :param obj_dir: Resource files directory (.minecraft/assets/objects/)
    :param out_dir: Output directory
    """
    # read JSON map
    logging.info(f"Reading map file: {hash_dir}")
    with open(hash_dir, 'r', encoding='utf-8') as f:
        data = json.load(f)

    objects = data.get('objects', {})
    total_files = len(objects)
    logging.info(f"Found {total_files} resource files to process")

    success_count = 0
    fail_count = 0

    # create progress bar via tqdm
    with tqdm(objects.items(), total=total_files, desc="Extracting resource files") as pbar:
        for relative_path, file_info in pbar:
            file_hash = file_info['hash']
            file_size = file_info['size']

            # construct source file path (first two characters as subdirectory)
            hash_prefix = file_hash[:2]
            source_path = Path(obj_dir) / hash_prefix / file_hash

            # construct destination file path
            dest_path = Path(out_dir) / relative_path
            dest_dir = dest_path.parent

            # create destination directory
            try:
                dest_dir.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                logging.error(f"create directory failed: {dest_dir} - {str(e)}")
                fail_count += 1
                continue

            # copy file
            try:
                if not source_path.exists():
                    logging.warning(f"source file doesn't exist: {source_path}")
                    fail_count += 1
                    continue

                # check file size
                actual_size = os.path.getsize(source_path)
                if actual_size != file_size:
                    logging.warning(f"file size doesn't match: {relative_path} (expected: {file_size}, actual: {actual_size})")
                    fail_count += 1
                    continue
                
                # shutil.copy2(source_path, dest_path)
                success_count += 1

                # time.sleep(0.01)

                # update progress bar description
                pbar.set_postfix({"success": success_count, "fail": fail_count})

            except Exception as e:
                logging.error(f"copy file failed: {relative_path} - {str(e)}")
                fail_count += 1

        # summary
        logging.info(f"Successfully done! Success: {success_count}, Fail: {fail_count}, Total: {total_files}")

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(funcName)s/%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    args = argv[1:]
    if not args:
        logging.error(f"no arguments provided (\"{Path(argv[0]).name} -h\" for help)")
        exit(1)
    if '-h' in args or '--help' in args:
        print(HELP_DOC)
        exit(0)
    if '-v' in args or '--version' in args:
        print("Minecraft Assets Extractor v1.0")
        exit(0)
    if "-o" not in args:
        logging.error(f"output directory not specified (\"{Path(argv[0]).name} -h\" for help)")
        exit(1)
    
    try:
        hash_dir = args[0]
        obj_dir = args[1]
        out_dir = args[3]
    except IndexError:
        logging.error(f"missing arguments (\"{Path(argv[0]).name} -h\" for help)")
        exit(1)
        
    if not all([hash_dir, obj_dir, out_dir]):
        logging.error(f"invalid arguments (\"{Path(argv[0]).name} -h\" for help)")
        exit(1)

    if Path(hash_dir).exists() and Path(obj_dir).exists():
        if Path(hash_dir).suffix.lower() != '.json':
            logging.error("map file must be a .json file")
            exit(1)
        else:
            try:
                extract_assets(hash_dir, obj_dir, out_dir)
            except Exception as e:
                logging.critical(f"critical error: {str(e)}")
    else:
        logging.error("directory doesn't exist")
        exit(1)
        
if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        main()