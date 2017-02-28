import os
import re
from urlparse import urlparse
import requests

for filename in os.listdir('content'):
    new_lines = []
    print(filename)
    if not os.path.isdir('content/' + filename):
        with open('content/' + filename, 'r') as open_file:
            i = 0
            slug_index = 0
            found = False
            for line in open_file.readlines():
                if line.startswith('Slug:'):
                    slug_index = i
                match = re.search('(?:!\[.*?\]\((.*?)\))', line)
                if match is not None and not found:
                    url = match.group(1)
                    if not "googleusercontent" in url:
                        parsed = urlparse(url)
                        target_file = '/thumbnails/thumbnail_wide/' + os.path.basename(parsed.path)
                        new_line = 'Thumbnail: ' + target_file + '\n'
                        new_lines.insert(i - (i - slug_index), new_line)
                        found = True
                i += 1
                new_lines.append(line)

        with open('content/' + filename, 'w') as open_file:
            for new_line in new_lines:
                open_file.write(new_line)
