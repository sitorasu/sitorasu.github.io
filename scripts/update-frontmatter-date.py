import sys
import re
import logging
from datetime import datetime, timezone, timedelta

def find_first_nonempty_line_index(lines: list[str]) -> int:
    for i in range(0, len(lines)):
        if lines[i].strip() != "":
            return i
    
    # All lines are empty: returns the length of the lines.
    return i
 
def find_pat_next(pat: re.Pattern[str], lines: list[str], start: int, end: int | None = None) -> int:
    if not end:
        end = len(lines)

    for i in range(start, end):
        if re.match(pat, lines[i]):
            return i
        
    # The pattern was not found: returns the end of the range.
    return i

def generate_date_line() -> str:
    jst = timezone(timedelta(hours=9))
    now = datetime.now(jst)
    return 'date: ' + now.isoformat()

def update(mdfile: str) -> None:
    with open(mdfile, 'w', encoding='utf-8') as f:
        lines = f.readlines()

        frontmat_open = find_first_nonempty_line_index(lines)
        if frontmat_open == len(lines):
            logging.warning(f"File '{mdfile}': Empty file: Skipped.")
            return
        
        sep_pat = re.compile(r'---\s*')
        if not re.match(sep_pat, lines[frontmat_open]):
            logging.warning(f"File '{mdfile}': No frontmatter: Skipped.")
            return
        
        frontmat_close = find_pat_next(sep_pat, lines, frontmat_open + 1)
        if frontmat_close == len(lines):
            logging.warning(f"File '{mdfile}': Frontmatter not closed: Skipped.")
            return
        
        date_pat = re.compile(r'date:\s*\w+')
        date_pos = find_pat_next(date_pat, lines, frontmat_open + 1, frontmat_close)
        date = generate_date_line()

        if date_pos == frontmat_close:
            lines.insert(date_pos, date)
            logging.info(f"File '{mdfile}': No 'date' field: Set '{date}'.")
        else:
            lines[date_pos] = date
            logging.info(f"File '{mdfile}': Set '{date}'.")
        
        f.writelines(lines)

def main():
    mdfiles = sys.argv[1:]
    for mdfile in mdfiles:
        update(mdfile)

if __name__ == '__main__':
    main()
