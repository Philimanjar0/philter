import re
import sys

# Read in the file
file_path = sys.argv[1]
file_prefix = file_path.removesuffix(".philter")
with open(file_path, 'r') as file:
    philter = file.read()

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
regex_to_replace = Regex("(?s)\%(", ")(\s*?)$")

# Get all key-values
regex_entry.inject_value("([^\n ]*)")
matches = re.finditer(regex_entry.get_regex(), philter, re.MULTILINE)
filter_entries = {}

# For each entry, find any %<var> to replace, then remove the entry
for matchNum, match in enumerate(matches, start=1):
    filter_key = match.group(1)
    # remove brackets, strip all leading and trailing whitespace
    filter_val = match.group(2).strip('\{\}').strip()
    # print(f"Found {filter_key} with value \n    {filter_val}")
    regex_to_replace.inject_value(".*?")
    nested_matches = re.finditer(regex_to_replace.get_regex(), filter_val, re.MULTILINE)

    # Resolve nested references
    filter_val = re.sub(regex_to_replace.get_regex(), lambda m : filter_entries[m.group(1).strip()], filter_val, flags=re.MULTILINE)

    filter_entries[filter_key] = filter_val

    regex_entry.inject_value(filter_key)
    philter = re.sub(regex_entry.get_regex(), '', philter)
    regex_to_replace.inject_value(filter_key)
    philter = re.sub(regex_to_replace.get_regex(), filter_entries[filter_key], philter, flags=re.MULTILINE)

# cleanup and remove any leading newlines
philter = philter.strip()

# write out to the .filter
with open(file_prefix + ".filter", "w") as out:
    out.write(philter)
