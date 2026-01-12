"""
Quick script to check schemes and their detailed fields
"""

import os
import sys

# Add the parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db, Scheme, PendingScheme

with app.app_context():
    print("=== Checking Recent Schemes ===\n")
    
    # Get the 5 most recent schemes
    recent_schemes = Scheme.query.order_by(Scheme.created_at.desc()).limit(5).all()
    
    for scheme in recent_schemes:
        print(f"\n--- Scheme: {scheme.name} ---")
        print(f"Category: {scheme.category}")
        print(f"Benefits: {scheme.benefits[:100] if scheme.benefits else 'None'}...")
        print(f"Eligibility: {scheme.eligibility[:100] if scheme.eligibility else 'None'}...")
        print(f"Documents Required: {scheme.documents_required[:100] if scheme.documents_required else 'None'}...")
        print(f"Application Process: {scheme.application_process[:100] if scheme.application_process else 'None'}...")
        print(f"Exclusions: {scheme.exclusions[:100] if scheme.exclusions else 'None'}...")
        print("-" * 80)
    
    print("\n\n=== Checking Pending Schemes ===\n")
    
    # Get pending schemes
    pending = PendingScheme.query.filter_by(status='pending').limit(3).all()
    
    for scheme in pending:
        print(f"\n--- Pending Scheme: {scheme.name} ---")
        print(f"Category: {scheme.category}")
        print(f"Benefits: {scheme.benefits[:100] if scheme.benefits else 'None'}...")
        print(f"Eligibility: {scheme.eligibility[:100] if scheme.eligibility else 'None'}...")
        print(f"Documents Required: {scheme.documents_required[:100] if scheme.documents_required else 'None'}...")
        print(f"Application Process: {scheme.application_process[:100] if scheme.application_process else 'None'}...")
        print(f"Exclusions: {scheme.exclusions[:100] if scheme.exclusions else 'None'}...")
        print("-" * 80)
