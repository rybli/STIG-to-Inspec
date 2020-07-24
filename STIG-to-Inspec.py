import xml.etree.ElementTree as ET
import re
import argparse

parser = argparse.ArgumentParser(description='Python script to parse STIG XML to Chef Inspec Ruby files.')
parser.add_argument('-f', '--file', metavar='FILE_PATH', help='Path to STIG XML file to be parsed.')
args = parser.parse_args()

print(args.file)
tree = ET.parse(args.file)
root = tree.getroot()

# Namespaces needed
# Group = {http://checklists.nist.gov/xccdf/1.1}Group
# title = {http://checklists.nist.gov/xccdf/1.1}title
# description = {http://checklists.nist.gov/xccdf/1.1}description
# fixtext = {http://checklists.nist.gov/xccdf/1.1}fixtext
# check-content = {http://checklists.nist.gov/xccdf/1.1}check-content

# Skeleton File for Inspec Ruby Checks

template = '# encoding: utf-8\n' \
           '\n' \
           'control "{0}" do\n' \
           '\ttitle "{1}"\n' \
           '\tdesc "{2}"\n' \
           '\timpact 0.5\n' \
           '\ttag "check": "{3}"\n' \
           '\ttag "fix": "{4}"\n' \
           '\n' \
           '\t# Write Check Logic Here\n' \
           '\n' \
           'end'

# TODO Get category and set the severity
# CATI = High (0.7 Impact)
# CATII = Medium (0.5 Impact)
# CATIII = Low (0.3 Impact)

tag_re = re.compile(r'<[^>]+>')
re_tag = re.compile(r'Satisfies.+')

for vid in root.findall('{http://checklists.nist.gov/xccdf/1.1}Group'):
    VID = vid.get('id')
    for child in vid:
        for title in child.findall('{http://checklists.nist.gov/xccdf/1.1}title'):
            TITLE = title.text
            # pass
        for description in child.findall('{http://checklists.nist.gov/xccdf/1.1}description'):
            desc = tag_re.sub('', description.text)
            DESCRIPTION = re_tag.sub('', desc)  # Regex removes broken style tags and not useful data.
            # pass
        for fixtext in child.findall('{http://checklists.nist.gov/xccdf/1.1}fixtext'):
            FIXTEXT = fixtext.text
            # pass
        for morechild in child:
            for checktext in morechild.findall('{http://checklists.nist.gov/xccdf/1.1}check-content'):
                CHECKTEXT = checktext.text
                # pass
    inspecfile = open(VID + '.rb', "w")
    inspecfile.write(template.format(VID, TITLE, DESCRIPTION, CHECKTEXT.replace('"', "'"), FIXTEXT.replace('"', "'")))
    inspecfile.close()
    # print(template.format(VID, TITLE, DESCRIPTION, CHECKTEXT.replace('"', "'"), FIXTEXT.replace('"', "'")))
