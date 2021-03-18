import os, subprocess, time, regex, re

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

dupe_find = 'find /Users/travisross/DEVONthink /Users/travisross/Library/Application\ Support/DEVONthink\ 3/ -type f -name "* - *[A-z][2-9].*"'
dupes = run_find(dupe_find)
dt_find = 'find /Users/travisross/DEVONthink /Users/travisross/Library/Application\ Support/DEVONthink\ 3/ -type f'
dt_files = run_find(dt_find)
dupe_names = [link.split("/")[-1] for link in dupes]
dt_files_names = [link.split("/")[-1] for link in dt_files]
for dupe in dupes:
    dupe_name = dupe.split("/")[-1]
    pattern = re.compile(r'[0-9].pdf')
    fixed_name = pattern.sub('.pdf', dupe_name)
    if fixed_name in dt_files_names:
        os.system(f"rm \"{dupe}\"")
        os.system(f'rm ~/ZotFile\ Import/\"{dupe_name}\"')
    else:
        pattern = re.compile(r'[0-9].pdf')
        fixed_full_path = pattern.sub('.pdf', dupe)
        os.system(f"mv \"{dupe}\" \"{fixed_full_path}\"")
        os.system(f'rm ~/ZotFile\ Import/\"{dupe_name}\"')
        os.system(f'ln -snf \"{fixed_full_path}\" ~/ZotFile\ Import/\"{fixed_name}\"')
        with open('/Users/travisross/changed_links.txt', 'a') as output_file:
            output_file.write(fixed_name + '\n')
