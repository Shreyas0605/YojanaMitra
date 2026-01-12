#!/usr/bin/env python3
import re

# Read the HTML file
with open('static/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Apply Login page background - using proper quote escaping
login_pattern = r'(<div id="login-page" class="page-section" style="display:none;">)'
login_replacement = r'''<div id="login-page" class="page-section" style="display:none; position:relative; background-image: url('static/img/login.png'); background-size: cover; background-position: center; background-attachment: fixed; min-height: 100vh;">
                        <div style="position:absolute; top:0; left:0; right:0; bottom:0; background: rgba(255,255,255,0.85); backdrop-filter: blur(5px);"></div>'''

content = re.sub(login_pattern, login_replacement, content)

# Update Login card styling
login_section = re.search(r'<!-- LOGIN PAGE -->[\s\S]*?</div>\s*</div>\s*</div>\s*<!-- REGISTER PAGE -->', content)
if login_section:
    login_content = login_section.group(0)
    login_content_updated = re.sub(
        r'<div class="row justify-content-center">',
        '<div class="row justify-content-center align-items-center min-vh-100 py-5" style="position:relative; z-index: 1;">',
        login_content,
        count=1
    )
    login_content_updated = re.sub(
        r'<div class="card mt-5">',
        '<div class="card shadow-lg border-0" style="background: rgba(255,255,255,0.95); backdrop-filter: blur(10px);">',
        login_content_updated,
        count=1
    )
    content = content.replace(login_section.group(0), login_content_updated)

# Apply Register page background
register_pattern = r'(<div id="register-page" class="page-section" style="display:none;">)'
register_replacement = r'''<div id="register-page" class="page-section" style="display:none; position:relative; background-image: url('static/img/register.png'); background-size: cover; background-position: center; background-attachment: fixed; min-height: 100vh;">
                        <div style="position:absolute; top:0; left:0; right:0; bottom:0; background: rgba(255,255,255,0.85); backdrop-filter: blur(5px);"></div>'''

content = re.sub(register_pattern, register_replacement, content)

# Update Register card styling
register_section = re.search(r'<!-- REGISTER PAGE -->[\s\S]*?</div>\s*</div>\s*</div>\s*<!-- ADMIN LOGIN PAGE -->', content)
if register_section:
    register_content = register_section.group(0)
    register_content_updated = re.sub(
        r'<div class="card mt-5">',
        '<div class="card shadow-lg border-0" style="background: rgba(255,255,255,0.95); backdrop-filter: blur(10px);">',
        register_content,
        count=1
    )
    content = content.replace(register_section.group(0), register_content_updated)

# Apply Eligibility page background
eligibility_pattern = r'(<div id="eligibility-page" class="page-section" style="display:none;">)'
eligibility_replacement = r'''<div id="eligibility-page" class="page-section auth-bg-eligibility" style="display:none; position:relative; background-image: url('static/img/eligibility.png'); background-size: cover; background-position: center; background-attachment: fixed; min-height: 100vh;">
    <div style="position:absolute; top:0; left:0; right:0; bottom:0; background: rgba(255,255,255,0.85); backdrop-filter: blur(5px);"></div>'''
content = re.sub(eligibility_pattern, eligibility_replacement, content)

# Write back
with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Background styles applied successfully!")
