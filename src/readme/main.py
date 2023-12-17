# Libraries
import os
import requests

from datetime import datetime
from dataclasses import dataclass
from typing import Generator



def most_recent_advent_year(time: datetime = None) -> int:
    """
    Get the year of the most recent advent
    """
    time = time or datetime.now()

    if time.month < 12:
        return time.year - 1
    return time.year


with open('../../secrets.txt', 'r') as f:
    secrets = f.readlines()

# -------------------------------------------------------
# Constants
# -------------------------------------------------------
# Advent of Code user ID
USER_ID = os.environ.get("USERID", "3565819")

# Advent of Code session cookie
SESSION_COOKIE = os.environ.get("AOC_SESSION", secrets[0])

# Advent of Code private leaderboard ID
LEADERBOARD_ID = os.environ.get("LEADERBOARDID", "") or USER_ID

# Star symbol to insert in the table
STAR_SYMBOL = os.environ.get("STAR_SYMBOL", "⭐")

# Location of the README file
README_LOCATION = os.environ.get("README_LOCATION", "../../README.md")

# Advent of Code base URL, for testing
ADVENT_URL = os.environ.get("ADVENT_URL", "https://adventofcode.com")




@dataclass(frozen=True, eq=True)
class DayProgress:
    day: int
    part_1: bool
    part_2: bool


def get_progress(year=None) -> Generator[DayProgress, None, None]:
    """Get the progress for a specific year.

    Parameters
    ----------
    year: str or int
        The year.
    """
    if year is None:
        year = most_recent_advent_year()

    endpoint = f"{ADVENT_URL}/{year}/leaderboard/private/view/{LEADERBOARD_ID}.json"
    res = requests.get(endpoint, cookies={"session": SESSION_COOKIE})
    res.raise_for_status()

    leaderboard_info = res.json()

    stars = leaderboard_info["members"][USER_ID]["completion_day_level"]

    for day, parts in stars.items():
        completed = parts.keys()
        yield DayProgress(
            day=int(day),
            part_1="1" in completed,
            part_2="2" in completed,
        )


def get_problem(year, day):
    """Get problem information.

    Parameters
    ----------
    year: str or int
        The year
    day: str or int
        The day

    Returns
    -------
    Dictionary with information.
    """
    # Library
    from bs4 import BeautifulSoup

    # Get page content
    url = f"{ADVENT_URL}/{year}/day/{day}"
    page = requests.get(url)
    page.raise_for_status()

    # Extract title
    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find("article", class_="day-desc").find('h2')

    # Return
    return {
        'title': title.text.split(":")[1].strip()[:-3]
    }



def readme_table(year=None, dropdown=True):
    """Create readme table for specific year.

    Parameters
    ----------
    year: str or int
        The year to create the table for.

    Returns
    -------
    """
    if year is None:
        year = most_recent_advent_year()

    # Get information
    stars_info = sorted(list(get_progress(year)), key=lambda p: p.day)

    # Count all stars for each part
    part1_stars = sum([1 if s.part_1 else 0 for s in stars_info])
    part2_stars = sum([1 if s.part_2 else 0 for s in stars_info])

    # Create title
    title = '%s | %2s%s' % (year, part1_stars + part2_stars, STAR_SYMBOL)

    # Create array to insert
    to_insert = [
        title,
        " ",
        "| Day | Title | Part 1 | Part 2 |",
        "| :---: | :---: | :---: | :---: |",
    ]


    for star_info in stars_info:
        day_url = f"{ADVENT_URL}/{year}/day/{star_info.day}"
        day_text = f"[Day {star_info.day}]({day_url})"
        definition = get_problem(year, star_info.day)['title']
        part_1_text = STAR_SYMBOL if star_info.part_1 else " "
        part_2_text = STAR_SYMBOL if star_info.part_2 else " "
        to_insert.append(f"| {day_text} | {definition} | {part_1_text} | {part_2_text} |")

    if dropdown:
        to_insert[0] = "<summary> %s </summary>" % title
        to_insert = ['\n<details>'] + to_insert + ['</details>\n']

    return to_insert



def replace_in(path):
    """Replaces in an existing file.

    Parameters
    ----------
    path: str
        The path to include the markdown.
    """
    # Libraries
    import re

    # The template
    TEMPLATE = '<!--- advent_table_stars (%s) --->'

    # Load file content
    with open(path, "r") as f:
        content = f.read()

    # Find placeholders to replace with information
    tables = re.findall(TEMPLATE % '\d+', content)

    for year in tables:
        lines = readme_table(year=year)
        placeholder = TEMPLATE % year
        content = content.replace(placeholder, '\n'.join(lines))

    # Save
    with open(path, "w") as f:
        f.write(content)


def create_readme(path, start, end):
    """Create a new readme.

    Parameters
    ----------
    path: str
        The path to include the markdown.
    start: int
        Start year
    end: int
        End year

    Returns
    -------
    """
    # Create content
    content = ""
    for year in range(start, end+1)[::-1]:
        lines = readme_table(year=year)
        content += '\n'.join(lines)

    # Save
    with open(path, "w") as f:
        f.write(content)





if __name__ == '__main__':

    # Replace in existing readme.
    #replace_in(README_LOCATION)

    # Create readme from scratch.
    create_readme(README_LOCATION, 2015, 2023)