#!/usr/bin/env python3
import os
import re

# 1. Update method.xml with voice keyboard attributes
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


# 2. Redirect all upstream repository references to the fork repository
upstream_ref = "rustemar/voice-keyboard"
fork_ref = "cwhde/voice-keyboard"

print(f"Redirecting all upstream references ({upstream_ref}) to fork ({fork_ref})...")

exclude_dirs = {'.git', '.gradle', 'build', 'gradle'}

for root, dirs, files in os.walk('.'):
    # Exclude unwanted directories
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    
    for file in files:
        # We only process text source files and markdown files
        if file.endswith(('.kt', '.java', '.xml', '.md', '.yml', '.yaml', '.gradle', '.kts')):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                
                if upstream_ref in file_content:
                    updated_content = file_content.replace(upstream_ref, fork_ref)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    print(f"Redirected repository reference in: {filepath}")
            except Exception as e:
                # Silently ignore files we can't read/write easily
                pass


# 3. Ensure the Obtainium Badge is in README.md
readme_path = "README.md"
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()

    badge_markdown = '[![Get it on Obtainium](https://raw.githubusercontent.com/ImranR98/Obtainium/main/assets/badges/get-on-obtainium.svg)](https://obtainium.imranr.dev/app?url=https://github.com/cwhde/voice-keyboard)'
    
    # Check if badge is present (or if there is an Obtainium redirect link)
    if "https://obtainium.imranr.dev/app?url=" not in readme_content:
        # Find '# Voice Keyboard' to insert the badge under the main title
        pattern = re.compile(r'(# Voice Keyboard\n)')
        match = pattern.search(readme_content)
        if match:
            insert_pos = match.end()
            readme_content = (
                readme_content[:insert_pos]
                + "\n"
                + badge_markdown
                + "\n"
                + readme_content[insert_pos:]
            )
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(readme_content)
            print("Successfully prepended the Obtainium badge in README.md.")
        else:
            print("Warning: Could not find main title in README.md to insert Obtainium badge.")
    else:
        print("Obtainium badge is already present in README.md.")
