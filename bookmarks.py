import json
import os
from datetime import datetime

# List of possible file names
possible_filenames = ["Bookmarks", "bookmarks.json", "Bookmarks.json"]

def convert_to_html(json_data):
    html_content = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>\n"""

    def process_bookmark(bookmark):
        url = bookmark.get("url", "")
        name = bookmark.get("name", "Untitled")
        add_date = bookmark.get("date_added", "")
        add_date_str = datetime.utcfromtimestamp(int(add_date) / 1e6).strftime("%Y-%m-%d %H:%M:%S") if add_date else ""
        return f'        <DT><A HREF="{url}" ADD_DATE="{add_date_str}">{name}</A>\n'

    def process_folder(folder, level=1):
        folder_name = folder.get("name", "Untitled Folder")
        html_str = f'{"    " * level}<DT><H3>{folder_name}</H3>\n'
        html_str += f'{"    " * level}<DL><p>\n'
        
        for item in folder.get("children", []):
            if item.get("type") == "folder":
                html_str += process_folder(item, level + 1)
            elif item.get("type") == "url":
                html_str += process_bookmark(item)
        
        html_str += f'{"    " * level}</DL><p>\n'
        return html_str

    for root_name, root_content in json_data["roots"].items():
        if "children" in root_content:
            html_content += process_folder(root_content)

    html_content += "</DL><p>\n"
    return html_content

# Process each found file in possible_filenames
for filename in possible_filenames:
    if os.path.exists(filename):
        with open(filename, "r") as file:
            bookmarks_json = json.load(file)
        
        html_output = convert_to_html(bookmarks_json)

        # Output filename will be based on the input filename
        output_html_filename = f"{os.path.splitext(filename)[0]}.html"

        with open(output_html_filename, "w") as html_file:
            html_file.write(html_output)

        print(f"Converted {filename} to {output_html_filename}")