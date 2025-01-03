import re
import sys

# Read in the file
file_path = sys.argv[1]
file_prefix = file_path.removesuffix(".philter")
with open(file_path, 'r') as file:
    philter = file.read()

included_files = set()
import_regex = "import (\w*.philter)"

# helper to recursively resolve imports. This ill only import each file once.
# Circular or duplicate dependencies are resolved by just skipping any subsequent imports
def resolve_include(base_contents):
    match = re.search(import_regex, base_contents, re.MULTILINE)
    if (match == None):
        # no imports found, return
        return base_contents
    file = match.group(1)
    if (file in included_files):
        # If this import has already been used, delete the import statement and continue
        print("warning: found circular or duplicate dependency.")
        base_contents = re.sub(match.re, "", base_contents)
    else:
        included_files.add(file)
        with open(file, 'r') as f:
            include_contents = f.read()
            base_contents = re.sub(match.re, include_contents, base_contents, count=1)
    # recursively resolve imports
    return resolve_include(base_contents)

philter = resolve_include(philter)

# Helper class for regex'n
# Helps create a regex string by concatenating a prefix, suffix, and value.
# Useful for finding many slight variations in of the same pattern (like variable decleration)
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

# this regex finds variable declarations.
#   Declarations start with 'var'.
#   First capture group is the entire block. This is used to delete the declaration.
#   Second capture group is the variable name.
#   Third capture group is the variables value.
decleration_regex = Regex("var (", ")\s*=\s*\{([\s\S]*?)\}\s*")
decleration_regex.inject_value("\w*") # Initially match any variable names.

# this regex finds variable usage.
#   Usage starts with '$'
#   First capture group what should be replaced. EG $variable_name
#   Second capture group is the variable name.
usage_regex = Regex("(\$(", ")(?=$|\W))")

# Get all key-values.
declarations = re.finditer(decleration_regex.get_regex(), philter, re.MULTILINE)

# dictionary representation of key-value pairs.
variables_dict = {}

# TODO remove inline comments in a preprocessing step.
# For each variable declaration, find any usage to replace.
for matchNum, match in enumerate(declarations, start=1):
    var_name = match.group(1)
    var_value = match.group(2).strip()

    # find any replace any nested usage
    usage_regex.inject_value("\w*")
    var_value = re.sub(usage_regex.get_regex(), lambda match : variables_dict[match.group(2)], var_value, flags=re.MULTILINE)

    # print("Replacing " + var_name + " with \n    " + var_value)

    # add the key-value
    variables_dict[var_name] = var_value

    # remove the declaration
    philter = re.sub(match.re, '', philter)

    # replace all of var_name usages with var_value
    usage_regex.inject_value(var_name)
    # print("Replacing using " + usage_regex.get_regex())
    philter = re.sub(usage_regex.get_regex(), variables_dict[var_name], philter, flags=re.MULTILINE)

# cleanup and remove any leading newlines
philter = philter.strip()

# write out to the .filter
with open(file_prefix + ".filter", "w") as out:
    out.write(philter)
