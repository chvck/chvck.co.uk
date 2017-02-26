import os
import re
from urlparse import urlparse
import requests

def download_image(target_file, url):
    with open(target_file, 'wb') as handle:
        response = requests.get(url, stream=True)

        if not response.ok:
            print response

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)


for filename in os.listdir('content'):
    new_lines = []
    print(filename)
    with open('content/' + filename, 'r') as open_file:
        for line in open_file.readlines():
            match = re.search('(?:!\[.*?\]\((.*?)\))', line)
            if match is not None:
                url = match.group(1)
                if not "googleusercontent" in url:
                    try:
                        parsed = urlparse(url)
                        target_file = 'images/' + os.path.basename(parsed.path)
                        download_image(target_file, url)
                        target_file = '{filename}' + target_file
                        line = line.replace(url, target_file)
                    except IOError:
                        print "error in " + filename
            new_lines.append(line)

    with open('content/' + filename, 'w') as open_file:
        for new_line in new_lines:
            open_file.write(new_line)
