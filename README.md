<h1>My Zotero to DEVONthink 3 workflow</h1>
<p>I wrote the following interrelated scripts to automate file management between my reference manager <a href="https://www.zotero.org" target="_blank">Zotero</a> and <a href="https://www.devontechnologies.com" target="_blank">DEVONthink 3</a>, the database program in which I store all of my files. Many academics (and probably other professionals) use these two programs in tandem, but they have no obvious integration. Zotero makes it very simple to import a citation and a PDF attachment of a scholarly article and it makes it very easy to find the document you know you want by title or author (or both). DEVONthink, however, is a powerful database that builds connections between your documents and lets you search within them with stunning power and precision. It is a much more powerful research management database, and so I keep all of my materials in it, including many that are not in Zotero.</p><p><h3>Goals:</h3></p><ul><li>I wanted to take advantage of Zotero's ability (assisted by ZotFile) to download and rename files from scholarly datases automatically.<li>I wanted each new file to move immediately into DEVONthink 3.<li>I wanted to maintain exactly one copy of each of my documents that I could access either directly from Zotero or DEVONthink 3.</li></ul><p>With the help of <a href="https://github.com/dchartash">@dchartash</a>, I succeeded. He deserves credit for much of what is good here; the blame for the kludgy parts rests entirely with me.</p>
<H1>How it works:</H1><ol><li>The python script "fix_broken_symlinks.py" watches the folder into which ZotFile puts renamed attachments after Zotero downloads them.</li><li>It then moves any file in that folder&mdash;otherwise filled with symlinks to moved files&mdash;to the inbox of DEVONthink 3...</li><li>...and then waits 10 seconds while DEVONthink moves that file around internally to its satisfaction. Don't question the magic.</li><li>Rather than search for just the new file, the script identifies all the broken symlinks in Zotero's directory and searches all of the possible locations within DT3's proprietary folder structure for each file by name.</li><li>Once found, it (over)writes a new symbolic link in the ZotFile folder that points to the copy it found in DT3.</li><li>"com.USERNAME.filewatcher.plist" watches each folder within DT3's file structure and runs the script every time something moves, which seamlessly keeps Zotero linked to attachments in DT3.</li></ol><p><B>Note:</b> DT3 silently moves files internally within its folder structure, which breaks links even after the initial importation. While a folder action script (like "MobileSyncer.scpt") could watch one folder, it made more sense to write "com.USERNAME.filewatcher.plist" and put it in /Library/LaunchDaemons/ to watch all of these folders at once. To implement this, you would need to update the paths depending on the number and names of your DEVONthink databases, but this template should provide a sufficient place to start.</p><H1>But what if I need to save an externally edited file back into DT3?</H1><p>If you open, annotate, and save a file on your Mac, Zotero's linked file will continue to point to the updated file. But what if you want to read and annotate a file on your iPhone or iPad? (NB: This uses the iOS-only app <a href="https://apps.apple.com/us/app/devonthink-to-go/id395722470">DEVONthink to Go</a>, so this solution unfortunately requires an iOS device as currently written.) I wanted a way to send files directly to my mobile device, annotate them, and then seamlessly save the annotated file over the top of the original file that will be buried somewhere in DEVONthink's folder structure. The workflows work like this:<ol><li>I highlight a document in DT3 on my Mac, then run the little script "push_it.scpt" with a keyboard shortcut.</li><li>That script uses <a href="https://www.prowlapp.com">Prowl</a> sends an antiquated but effective push notifcation to my iOS device that contains a URL that, when clicked, opens that document in DEVONthink To Go. I can then open it in another application like Word or GoodReader.</li><li>When I'm done, I save it to a dedicated folder in iCloud that syncs to my Mac, making sure to save it with <i>precisely the same filename</i>.</li><li>"MobileSyncer.scpt" is a Folder Action Script that watches that particular iCloud folder on my Mac and, when it sees a new file, it runs the python script "replace_DT3_files.py".</li><li>As its name implies, that python script searches the underlying folder structure of DT3's databases on my Mac for a file with the same name and replaces the older DT3 copy with the newer, annotated version.</li></ol></p><h1>Implementation instructions:</h1><ol><li>Fix the paths to match your file locations by:<ul><li>Replacing USERNAME with your actual Mac username, assuming that is the name of your home directory.</li><li>Replace "/DEVONthink" and "/ZOTERO_FOLDER" throughout with the appropriate directories for your DT3 databases and whatever folder you tell ZotFile to move renamed files into.</li><li>In filewatcher.plist, you'll have to modify the list of folders to watch according to the number and names of your databases.</ul><li>You'll need an account and API key if you want to use <a href="https://www.prowlapp.com" target="_blank">Prowl</a> to pass documents from DT3 on your Mac to DEVONthink To Go on iOS (and you'll need to sync your databases through a cloud service, this only sends the URL, not the file itself, which DTTG needs to get on its own.</li>Update MobileSyncer and replace_DT3_files.py with the appropriate synced directory (iCloud in my case) to watch for updated files coming back from another device.</li></ol><H1>Warnings and disclaimers:</H1><p>These scripts are given for information purposes only. As they are custom solutions for my particular workflow, I cannot offer support for how they might be implemented into your workflow nor am I responsible for what happens if you choose to use them either in full or in part. They watch folders that DEVONthink hid for a reason; they silently dig through your entire database, moving and overwriting data without user interaction at terrifying speeds and scale. As such, they are not for the feint of heart. You should know what they do and how before you try to modify them to do what you need for them to do on your machine. Good luck!</p>
<h1>DEVONthink and Zotero workflows</h1><p>I scripted a workflow (I had significant assistance from <a href="https://github.com/dchartash" target="_blank">@dchartash</a>, at least for the good parts) to do the following: