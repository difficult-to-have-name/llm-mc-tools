import re
from sys import argv
import logging
import os
from pathlib import Path

HELP_DOC = f"""Usage: {argv[0]} <log_dir> -o <out_dir> [<options>]
Extract chat messages from Minecraft log files.

Arguments:
    <log_dir>    Directory to the input Minecraft log file
    -o <out_dir> Specify the output directory
Options:
    -h, --help      Show this help message and exit
    -v, --version   Show version information and exit
"""

def clean_minecraft_formatting(text):
    """
    Sanitize Minecraft formatting codes from the text
    
    :param text: The input text with Minecraft formatting codes
    """
    return re.sub(r'§[0-9a-fk-or]', '', text).strip()

def parse_minecraft_log(input_file, output_file):
    """
    Extract real content chat messages from a Minecraft log file and save them to an output file.
    
    :param input_file: Directory to the input Minecraft log file
    :param output_file: Directory to the output text file
    
    :return: Number of lines written to the output file
    """
    
    if os.path.abspath(input_file) == os.path.abspath(output_file):
        logging.error("Input and output files must be different.")
        return 1

    if not os.path.exists(input_file):
        logging.error(f"Input file does not exist: {input_file}")
        return 1

    try:
        with open(input_file, 'r', encoding='gbk', errors='replace') as f_in, \
            open(output_file, 'w', encoding='utf-8') as f_out:
            line_count = 0
            
            for line in f_in:
                # only process lines containing chat messages
                if '[CHAT]' in line and ('<' in line or '加入' in line or '退出' in line or '欢迎' in line):
                    # extract timestamp and message content
                    time_match = re.search(r'\[(\d{2}:\d{2}:\d{2})\]', line)
                    if time_match:
                        time_str = time_match.group(1)
                        # extract message content (from [CHAT] onwards)
                        message_start = line.find('[CHAT]') + 6
                        message = line[message_start:].strip()

                        # sanitize formatting and write to output
                        clean_msg = clean_minecraft_formatting(message)
                        if clean_msg:
                            f_out.write(f"[{time_str}] {clean_msg}\n")
                            line_count += 1
            return line_count
    except OSError as e:
        logging.error(f"File operation error: {str(e)}")
        return 1
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return 1

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(funcName)s/%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    args = argv[1:]
    if not args:
        logging.critical(f"no arguments provided (\"{Path(argv[0]).name} -h\" for help)")
        exit(1)
    if '-h' in args or '--help' in args:
        print(HELP_DOC)
        exit(0)
    if '-v' in args or '--version' in args:
        print("Minecraft Assets Extractor v1.0")
        exit(0)
    if "-o" not in args:
        logging.critical(f"output directory not specified (\"{Path(argv[0]).name} -h\" for help)")
        exit(1)
    
    try:
        log_dir = args[0]
        out_dir = args[2]
    except IndexError:
        logging.error(f"missing arguments (\"{Path(argv[0]).name} -h\" for help)")
        exit(1)

    if not all([log_dir, out_dir]):
        logging.error(f"invalid arguments (\"{Path(argv[0]).name} -h\" for help)")
        exit(1)
        
    if Path(log_dir).exists():
        try:
            line = parse_minecraft_log(log_dir, out_dir)
            logging.info(f"Log parsed to {out_dir} with {line} lines.")
        except Exception as e:
            logging.critical(f"critical error: {str(e)}")
    else:
        logging.error("directory doesn't exist")
        exit(1)

if __name__ == '__main__':
    main()