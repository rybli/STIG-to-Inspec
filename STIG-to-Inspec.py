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

tag_re = re.compile(r'<[^>]+>')
re_tag = re.compile(r'Satisfies.+')

for vid in root.findall('{http://checklists.nist.gov/xccdf/1.1}Group'):
    VID = vid.get('id').encode('utf-8')
    # pass
    for child in vid:
        for title in child.findall('{http://checklists.nist.gov/xccdf/1.1}title'):
            TITLE = title.text.encode('utf-8')
            # pass
        for description in child.findall('{http://checklists.nist.gov/xccdf/1.1}description'):
            desc = tag_re.sub('', description.text)
            DESCRIPTION = re_tag.sub('', desc).encode('utf-8')  # Regex to remove broken html/xml tags and not useful data.
            # pass
        for fixtext in child.findall('{http://checklists.nist.gov/xccdf/1.1}fixtext'):
            FIXTEXT = fixtext.text.encode('utf-8')
            # pass
        for morechild in child:
            for checktext in morechild.findall('{http://checklists.nist.gov/xccdf/1.1}check-content'):
                CHECKTEXT = checktext.text.encode('utf-8')
                # pass
    # print(template.format(VID, TITLE, DESCRIPTION, CHECKTEXT, FIXTEXT))
    inspecfile = open(VID + '.rb', "w")
    inspecfile.write(template.format(VID, TITLE, DESCRIPTION, CHECKTEXT, FIXTEXT))
    inspecfile.close()

