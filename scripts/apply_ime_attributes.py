#!/usr/bin/env python3
import os
import re

method_xml_path = "app/src/main/res/xml/method.xml"

if os.path.exists(method_xml_path):
    with open(method_xml_path, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False
    # Check if isAuxiliary is missing
    if 'android:isAuxiliary="true"' not in content:
        # We find the <subtype ... /> tag and add the attributes
        # Let's match <subtype and find its closing />
        pattern = re.compile(r'(<subtype\b[^>]*?)(/?>)')
        match = pattern.search(content)
        if match:
            tag_body = match.group(1)
            # Ensure android:imeSubtypeLocale="en_US" is present
            if 'android:imeSubtypeLocale' not in tag_body:
                tag_body += '\n        android:imeSubtypeLocale="en_US"'
            # Ensure android:isAuxiliary="true" is present
            tag_body += '\n        android:isAuxiliary="true"'
            
            content = content[:match.start()] + tag_body + match.group(2) + content[match.end():]
            modified = True

    if modified:
        with open(method_xml_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Successfully updated method.xml with voice keyboard attributes.")
    else:
        print("method.xml is already up to date.")
else:
    print(f"Error: {method_xml_path} not found.")
