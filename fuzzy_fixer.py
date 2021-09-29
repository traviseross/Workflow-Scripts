#!/usr/bin/python3
# libraries for system interfacing
import os
import subprocess
import time
import errno

"""
Customization:
"""
ZOTERO_FOLDER = "ZotFile\ Import"
USERNAME = "travisross"
DT3_PATH = "Volumes/WD/DEVONthink"
os_system_cmd = (
        "find /Users/"
        + USERNAME
        + "/"
        + ZOTERO_FOLDER
        + " -type f -exec mv {} /Users/"
        + USERNAME
        + "/Library/Application\ Support/DEVONthink\ 3/Inbox \;"
)
os.system(os_system_cmd)
broken_links = f'find -L /Users/{USERNAME}/{ZOTERO_FOLDER} -type l -name "* - * - [0-9]*" ! -name "*.DS_Store" '

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

broken_links = run_find(broken_links)

for link in broken_links:
        file_ext = link.split('.')[-1]
        auth_title = link.split('/')[-1]
        author = auth_title.split(' ')[0]
        short_title_1 = auth_title.split(' - ')[1]
        short_title = author+"* *"+short_title_1+"*"
        cmd = '''find /'''+DT3_PATH+''' /Users/'''+USERNAME+'''/Library/Application\ Support/DEVONthink\ 3 -type f -name "*'''+short_title+'''" -iname "*'''+file_ext+'''" -exec ln -snf {} ~/ZotFile\ Import \; -exec ln -snf {} "'''+link+'''" \;'''
        print(cmd)
        proceed=input('Proceed? y/n')
        if proceed == 'y':
            os.system(cmd)
        else:
            pass



