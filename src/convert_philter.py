import re
import sys

# Read in the file
file_path = sys.argv[1]
file_prefix = file_path.removesuffix(".philter")
with open(file_path, 'r') as file:
    philter = file.read()

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
