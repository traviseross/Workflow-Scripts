#!/usr/bin/python3
# libraries for system interfacing
import os, subprocess, time

"""
Customization:
replace "ZOTERO_FOLDER" with the folder where ZotFile stores files; after this, it will find links to those files
replace "USERNAME" below with your Mac user name, but you might need to adjust paths depending where you keep your DT3 databases.
replace "MOBILE_SYNC_FOLDER" with the path to whatever folder syncs annotated files back from your other devide
"""


def run_find(cmd_find):
    # parser to run command using subprocess (which will obtain output as bytestream)
    parser = subprocess.Popen(
        cmd_find,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    # get stdout/stderror from running command
    stdout, stderr = parser.communicate()

    # convert bytestream to utf-8
    stdout_utf8 = stdout.decode("utf-8")
    # get files (separation by newline)
    ln_files = stdout_utf8.split("\n")
    # remove "blank" files
    ln_files.remove("")
    cmd_files = [link for link in ln_files]
    return cmd_files


# command to check pdfs
zot_find = (
    'find /Users/USERNAME/MOBILE_SYNC_FOLDER -type f -maxdepth 1 ! -name "*.DS_Store" '
)
dt_find = "find /Users/USERNAME/DEVONthink /Users/USERNAME/Library/Application\ Support/DEVONthink\ 3/ -type f"
zot_files = run_find(zot_find)
dt_files = run_find(dt_find)
dt_files_names = [link.split("/")[-1] for link in dt_files]
# print(dt_files_names[:10])
# for each broken link found, iterate:
for link in zot_files:
    link_file = link.split("/")[-1]
    # 	print(link,link_file)
    if link_file in dt_files_names:
        dt_home = dt_files[dt_files_names.index(link_file)]
        os.system(f'mv "{link}" "{dt_home}"')
