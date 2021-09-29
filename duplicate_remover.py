import os, subprocess, time, regex, re
ZOTERO_FOLDER = 'ZotFile\ Import'
USERNAME = 'travisross'

def run_find(cmd_find):
	#parser to run command using subprocess (which will obtain output as bytestream)
	parser = 	subprocess.Popen(cmd_find,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	#get stdout/stderror from running command
	stdout,stderr = parser.communicate()

	#convert bytestream to utf-8
	stdout_utf8=stdout.decode('utf-8')
	#get files (separation by newline)
	ln_files = stdout_utf8.split("\n")
	#remove "blank" files 
	ln_files.remove('')
	cmd_files = [link for link in ln_files]
	return(cmd_files)
broken_links = f'find -L /Users/{USERNAME}/{ZOTERO_FOLDER} -type l -name "* - * - [0-9]*" ! -name "*.DS_Store" '
zot_find = f'find /Users/{USERNAME}/{ZOTERO_FOLDER} -type l ! -name "*.DS_Store" '
dupe_find = f'find /Users/{USERNAME}/DEVONthink /Users/{USERNAME}/Library/Application\ Support/DEVONthink\ 3/ -type f -name "* - *[A-z][1-9].*"'
dupes = run_find(dupe_find)
dupe_names = [link.split("/")[-1] for link in dupes]
dt_find = f'find /Users/{USERNAME}/DEVONthink /Users/{USERNAME}/Library/Application\ Support/DEVONthink\ 3/ -type f -name "* - * [0-9]*" \( -iname \*.pdf -o -iname \*.docx -o -iname \*.doc -o -iname \*.xlsx -o -iname \*.xls -o -iname \*.md -o -iname \*.ppt -o -iname \*.pptx \)'
broken_links = run_find(broken_links)
zot_files = run_find(zot_find)
dt_files = run_find(dt_find)
zot_files_names = [link.split("/")[-1] for link in zot_files]
broken_links_name = [link.split("/")[-1] for link in broken_links]
dt_files_names = [link.split("/")[-1] for link in dt_files]

for dupe in dupes:
    i=0
    doctest=dupe.split(".")[-1]
    dupe_name = dupe.split("/")[-1]
    pattern = re.compile(r'[0-9].pdf')
    fixed_name = pattern.sub('.pdf', dupe_name)
    if doctest=="doc":
        i=1
    elif doctest=="docx":
        i=1
    else:
        i=0
    if i>0:
        pass
    else:
        if fixed_name in dt_files_names:
            confirm = input(f"replace {dupe_name} with {fixed_name}? y/n ")
            if confirm == "y":
                    os.system(f"rm \"{dupe}\"")
        else:
            pattern = re.compile(r'[0-9].pdf')
            fixed_full_path = pattern.sub('.pdf', dupe)
            confirm = input(f"move {dupe_name} to {fixed_full_path}? y/n ")
            if confirm == "y":
                os.system(f"mv \"{dupe}\" \"{fixed_full_path}\"")
                os.system(f'rm /Users/{USERNAME}/{ZOTERO_FOLDER}/\"{dupe_name}\"')
                os.system(f'ln -snf \"{fixed_full_path}\" ~/{ZOTERO_FOLDER}/\"{fixed_name}\"')
