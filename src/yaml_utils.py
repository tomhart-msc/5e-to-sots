import re
import yaml

def quote_colon_strings(yaml_text):
    # Match lines like: key: value with colon(s) in value
    pattern = re.compile(r'^( *[^:\n]+:\s*)([^"\n:]+:[^"\n]+)$', re.MULTILINE)
    return pattern.sub(r'\1"\2"', yaml_text)
