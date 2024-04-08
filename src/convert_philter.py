import re
import sys

file_path = sys.argv[1]
file_prefix = file_path.removesuffix(".philter")
with open(file_path, 'r') as file:
    philter = file.read()

if not philter.endswith("\n"):
    philter = philter + "\n"

# Helper class for regex'n
class Regex:
    def __init__(self, prefix, suffix):
        self.prefix = prefix
        self.suffix = suffix
        self.value = None
    
    def inject_value(self, value):
        self.value = value
    
    def get_regex(self):
        if (self.value != None):
            return self.prefix + self.value + self.suffix
        else:
            return None

regex_entry = Regex("(?s)\$", "*? = (\{.*?\s\})(?=\s|$)")
regex_to_replace = Regex("(?s)\%", "\s")

# Get all key-values
regex_entry.inject_value("([^\n ]*)")
matches = re.finditer(regex_entry.get_regex(), philter, re.MULTILINE)
filter_entries = {}

# For each entry, find any %<var> to replace, then remove the entry
for matchNum, match in enumerate(matches, start=1):
    filter_key = match.group(1)
    # remove brackets, first newline, and first tab
    filter_val = match.group(2).replace('{', '').replace('}', '').replace('\n', '', 1).replace('    ', '', 1)

    filter_entries[filter_key] = filter_val
    # print(f"Found {filter_key} with \n{filter_val}")

    regex_entry.inject_value(filter_key)
    philter = re.sub(regex_entry.get_regex(), '', philter)
    regex_to_replace.inject_value(filter_key)
    philter = re.sub(regex_to_replace.get_regex(), filter_entries[filter_key], philter)

# cleanup and remove any leading newlines
philter = philter.strip()

# write out
with open(file_prefix + ".filter", "w") as out:
    out.write(philter)
