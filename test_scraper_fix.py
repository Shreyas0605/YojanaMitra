"""
Test the improved scraper to verify data extraction works
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from scheme_scraper import MySchemeScraper

# Set console encoding
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Test the scraper on a small sample
scraper = MySchemeScraper('https://www.myscheme.gov.in/search')

print("Testing MySchemeScraper with fixed extraction logic...")
print("Extracting 3 schemes for verification...\n")

schemes = scraper.extract_schemes(limit=3)

if schemes:
    print(f"[OK] Successfully extracted {len(schemes)} schemes\n")
    print("=" * 80)
    
    for i, scheme in enumerate(schemes, 1):
        print(f"\n--- Scheme {i}: {scheme['name']} ---")
        print(f"Category: {scheme['category']}")
        
        benefits = scheme.get('benefits', '')
        eligibility = scheme.get('eligibility', '')
        docs = scheme.get('documents_required', '')
        app_process = scheme.get('application_process', '')
        
        print(f"\nBenefits: {benefits[:150]}..." if len(benefits) > 150 else f"\nBenefits: {benefits}")
        print(f"Eligibility: {eligibility[:150]}..." if len(eligibility) > 150 else f"\nEligibility: {eligibility}")
        print(f"Documents: {docs[:150]}..." if len(docs) > 150 else f"\nDocuments: {docs}")
        print(f"Process: {app_process[:150]}..." if len(app_process) > 150 else f"\nProcess: {app_process}")
        
        # Check if we got real data
        has_benefits = benefits and benefits != 'Refer to portal' and len(benefits) > 5
        has_eligibility = eligibility and eligibility != 'Refer to portal' and len(eligibility) > 5
        
        print(f"\n[STATUS] Benefits extracted: {'YES' if has_benefits else 'NO (empty or fallback)'}")
        print(f"[STATUS] Eligibility extracted: {'YES' if has_eligibility else 'NO (empty or fallback)'}")
        print("=" * 80)
        
    # Summary
    total_with_benefits = sum(1 for s in schemes if s.get('benefits') and s['benefits'] != 'Refer to portal' and len(s['benefits']) > 5)
    total_with_eligibility = sum(1 for s in schemes if s.get('eligibility') and s['eligibility'] != 'Refer to portal' and len(s['eligibility']) > 5)
    
    print(f"\n\n=== SUMMARY ===")
    print(f"Schemes with real benefits data: {total_with_benefits}/{len(schemes)}")
    print(f"Schemes with real eligibility data: {total_with_eligibility}/{len(schemes)}")
    
    if total_with_benefits > 0 and total_with_eligibility > 0:
        print("\n[SUCCESS] Fixed scraper is extracting real data!")
    else:
        print("\n[WARNING] Scraper still returning empty or fallback data - may need additional fixes")
else:
    print("[ERROR] No schemes extracted")
