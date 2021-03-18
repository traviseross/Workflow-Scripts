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

time.sleep(1)


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
broken_links = f'find -L /Users/{USERNAME}/{ZOTERO_FOLDER} -type l -name "* - * - [0-9]*" ! -name "*.DS_Store" '
zot_find = f'find /Users/{USERNAME}/{ZOTERO_FOLDER} -type l ! -name "*.DS_Store" '
dt_find = f'find /{DT3_PATH} /Users/{USERNAME}/Library/Application\ Support/DEVONthink\ 3 -type f -name "* - * [0-9]*" \( -iname \*.pdf -o -iname \*.docx -o -iname \*.doc -o -iname \*.xlsx -o -iname \*.xls -o -iname \*.md -o -iname \*.ppt -o -iname \*.pptx \)'
broken_links = run_find(broken_links)
zot_files = run_find(zot_find)
dt_files = run_find(dt_find)
zot_files_names = [link.split("/")[-1] for link in zot_files]
broken_links_name = [link.split("/")[-1] for link in broken_links]
dt_files_names = [link.split("/")[-1] for link in dt_files]
# print(dt_files_names[:10])
# for each broken link found, iterate:
for link in broken_links:
	link_file = link.split("/")[-1]
	#   print(link,link_file)
	if link_file in dt_files_names:
		dt_home = dt_files[dt_files_names.index(link_file)]
		os.system(f"ln -snf \"{dt_home}\" ~/ZotFile\ Import/")
	else:
		with open(f"/Users/{USERNAME}/missing_links.txt", "a") as output_file:
			output_file.write(link_file + "\n")
n = 0
for file in dt_files_names:
	n = n + 1
	if file in zot_files_names:
		pass
	else:
		dt_home = dt_files[dt_files_names.index(file)]
		os.system(f"ln -snf \"{dt_home}\" ~/ZotFile\ Import/")
