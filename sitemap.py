#!/usr/bin/env python3

# Copyright (c) 2022 Wessex Lift Co. Ltd. <marketing@wessexlifts.co.uk>

## Description:

# Generate an XML sitemap in the site root "/". Change the
# base_url to modify this for another website.

# Site specific things, for Wessex, are mainly in the function
# handling the setting of the priority. You might have to
# manually change this if you want to use it for another website.

## License:

# See /LICENSE file in the root of the repository.

## Code:

from textwrap import dedent
import glob
import os
import platform
import time

base_url      = ""
base_dir      = os.getcwd() + "/"
xml_preamble  = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<!-- Generated with `bin/sitemap.py` -->
"""
xml_postamble = "</urlset>"
xml_file_path = "sitemap.xml"


def loc_line(loc_str):
    """
    Returns a formatted <loc> XML line.
    """
    loc_str = loc_str.replace(".php","").replace("index","")
    return(f"<loc>{base_url}{loc_str}</loc>")


def priority_line(priority_string, file_depth):
    """
    Returns a formatted <priority> line.

    This is quite simply implemented. It makes index
    slightly higher than other vlaues and it changes
    other values depending on if they contain 'blog'
    or if they are located in a subfolder.
    """
    # Increase how important the file depth is
    d = ( file_depth * 1.5 ) / 10

    # Start at 0.9 as a baseline for variations
    p = 0.9 - d

    # Main "/" index file, for 1 priority
    if "/index.php" in priority_string \
        and file_depth == 1:
        p = priority_number(1)

    # Increase all other index files slightly
    elif "/index.php" in priority_string:
        p = priority_number(p + 0.1)

    # Increate all other /lift subdir pages
    elif "/lifts" in priority_string:
        p = priority_number(p + 0.2)

    # Decrease /blog pages if not current year
    elif "/blog" in priority_string \
        and not time.strftime("/%Y") in priority_string:
        p = priority_number(p - 0.15)

    else:
        p = priority_number(p)

    return f"<priority>{p}</priority>"


def priority_number(p):
    """
    For use with priority numbers. Simply returns a 2
    decimal place float for the number that we give it.
    """
    return "{:.2f}".format(p)


def lastmod_line(file_path):
    """
    Returns the <lastmod> line.
    """
    if platform.system() == 'Windows':
        lastmod_since_epoch = os.path.getmtime(file_path)
    else:
        lastmod_since_epoch = os.stat(file_path).st_mtime
    # Epoch to Time Format
    lastmod_time = time.strftime('%Y-%m-%dT%H:%M:%S+00:00',
                   time.localtime(lastmod_since_epoch))
    return f"<lastmod>{lastmod_time}</lastmod>"


def match_robots_txt(filename):
    """
    Check the current file against the robots.txt file in
    the site root.
    """
    with open(base_dir + "robots.txt") as f:
        # There is no .php in the robots.txt file, so
        # we need to remove it before we try the matching
        filename = filename.replace(".php","")
        if not filename in f.read():
            return True


def scan_check(filename, filepath):
    """
    Check if this is a file we should be scanning/adding
    to the XML sitemap, or if it should be skipped.
    """
    if ".php" in filename and \
        os.path.isfile(filepath) and \
        match_robots_txt(filename) and \
        not "elms" in filename:
        return True


def main():
    out_file = open(xml_file_path, "w")
    out_file.write(xml_preamble)

    for file in glob.iglob(base_dir + '**/**', recursive=True):

        # Get the filename and convert "\" -> "/"
        filename = file.replace(base_dir[:-1], "").replace("\\", "/")
        filepath = file

        # Get the depth of the file by seeing how many
        # forward slashes are present. This is for the
        # priority, mainly.
        file_depth = filename.count("/")

        if scan_check(filename, filepath):
            out_file.write(dedent(f"""\
                <url>
                    {loc_line(filename)}
                    {lastmod_line(filepath)}
                    {priority_line(filename, file_depth)}
                </url>
                """))

    out_file.write(xml_postamble)
    out_file.close


if __name__ == '__main__':
    main()
