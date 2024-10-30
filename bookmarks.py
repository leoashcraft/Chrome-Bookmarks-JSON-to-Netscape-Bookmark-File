import json
import os
from datetime import datetime
import glob

def convert_to_html(json_data, folder_name=None):
    html_content = ""
    if folder_name:
        html_content += f'<DT><H3>{folder_name}</H3>\n<DL><p>\n'

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

    if folder_name:
        html_content += "</DL><p>\n"

    return html_content

# Find all .json files in the current directory
json_files = glob.glob("*.json")

# Generate .html file from .json file
if len(json_files) == 1:
    json_file = json_files[0]
    with open(json_file, "r") as file:
        bookmarks_json = json.load(file)

    html_output = "<!DOCTYPE NETSCAPE-Bookmark-file-1>\n"
    html_output += "<!-- This is an automatically generated file. -->\n"
    html_output += '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n'
    html_output += "<TITLE>Bookmarks</TITLE>\n"
    html_output += "<H1>Bookmarks</H1>\n"
    html_output += "<DL><p>\n"
    html_output += convert_to_html(bookmarks_json)
    html_output += "</DL><p>\n"

    base_name = os.path.splitext(json_file)[0]
    unique_filename = f"{base_name}.html"
    with open(unique_filename, "w") as file:
        file.write(html_output)

    print(f"Converted '{json_file}' to '{unique_filename}'")

# Generate merged .html file if there's more than one .json file.
elif len(json_files) > 1:
    merged_html_content = "<!DOCTYPE NETSCAPE-Bookmark-file-1>\n"
    merged_html_content += "<!-- This is an automatically generated file. -->\n"
    merged_html_content += '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n'
    merged_html_content += "<TITLE>Bookmarks</TITLE>\n"
    merged_html_content += "<H1>Bookmarks</H1>\n"
    merged_html_content += "<DL><p>\n"

    for index, json_file in enumerate(json_files):
        with open(json_file, "r") as file:
            bookmarks_json = json.load(file)

        folder_name = os.path.splitext(json_file)[0]
        merged_html_content += convert_to_html(bookmarks_json, folder_name=folder_name)

    merged_html_content += "</DL><p>\n"

    with open("bookmarks.html", "w") as merged_file:
        merged_file.write(merged_html_content)

    print("Merged all JSON bookmarks into 'bookmarks.html'")
else:
    print("No JSON bookmarks files found.")
