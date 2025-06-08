import argparse
import re
import logging
from datetime import datetime, timezone, timedelta

def find_first_nonempty_line_index(lines: list[str]) -> int:
    for i in range(0, len(lines)):
        if lines[i].strip() != "":
            return i
    
    # All lines are empty: returns the length of the lines.
    return len(lines)
 
def find_pat_next(pat: re.Pattern[str], lines: list[str], start: int, end: int | None = None) -> int:
    if not end:
        end = len(lines)

    for i in range(start, end):
        if re.match(pat, lines[i]):
            return i
        
    # The pattern was not found: returns the end of the range.
    return end

def get_now_jst_isoformat() -> str:
    jst = timezone(timedelta(hours=9))
    now = datetime.now(jst)
    return now.isoformat(timespec='seconds')

def update(mdfile: str, target: str) -> None:
    with open(mdfile, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    frontmat_open = find_first_nonempty_line_index(lines)
    if frontmat_open == len(lines):
        logging.warning(f"Skipped '{mdfile}': Empty file.")
        return
    
    sep_pat = re.compile(r'---\s*')
    if not re.match(sep_pat, lines[frontmat_open]):
        logging.warning(f"Skipped '{mdfile}': No frontmatter.")
        return
    
    frontmat_close = find_pat_next(sep_pat, lines, frontmat_open + 1)
    if frontmat_close == len(lines):
        logging.warning(f"Skipped '{mdfile}': Frontmatter not closed.")
        return
    
    if target == 'date':
        date_pat = re.compile(r'date:')
        date_pos = find_pat_next(date_pat, lines, frontmat_open + 1, frontmat_close)

        if date_pos < frontmat_close:
            logging.info(f"Skipped '{mdfile}': 'date' field exists.")
            return

        date = get_now_jst_isoformat()
        lines.insert(frontmat_open + 1, f'date: {date}\n')
        logging.info(f"Modified '{mdfile}': Set 'date: {date}'.")

    else: # target == 'lastmod'
        lastmod_pat = re.compile(r'lastmod:')
        lastmod_pos = find_pat_next(lastmod_pat, lines, frontmat_open + 1, frontmat_close)

        date = get_now_jst_isoformat()

        if lastmod_pos < frontmat_close:
            lines[lastmod_pos] = f'lastmod: {date}\n'
            logging.info(f"Modified '{mdfile}': Update 'lastmod: {date}'.")
        else:
            lines.insert(frontmat_open + 1, f'lastmod: {date}\n')
            logging.info(f"Modified '{mdfile}': Insert 'lastmod: {date}'.")
        
    with open(mdfile, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def main():
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
    parser = argparse.ArgumentParser(description='Update date/lastmod in frontmatter')
    parser.add_argument('--target', required=True, choices=['date', 'lastmod'], help='Target of modification')
    parser.add_argument('files', nargs='*', help='Markdown files.')
    args = parser.parse_args()

    for mdfile in args.files:
        update(mdfile, args.target)

if __name__ == '__main__':
    main()
