import os
import sys
import logging
from app import app, db, SchemeSource, PendingScheme
from scheme_scraper import get_scraper

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BulkScrape")

def run_bulk_import():
    with app.app_context():
        # Get myScheme source
        source = SchemeSource.query.filter_by(scraper_type='myscheme').first()
        if not source:
            logger.error("myScheme source not found in database!")
            return

        logger.info(f"Starting bulk import from {source.name}...")
        
        # Instantiate scraper
        scraper = get_scraper(source.scraper_type, source.url)
        
        # Extract schemes (this will use the new pagination logic)
        schemes = scraper.extract_schemes()
        logger.info(f"Extracted {len(schemes)} schemes from API.")
        
        # Save to PendingScheme
        new_count = 0
        skip_count = 0
        
        for s_data in schemes:
            # Simple deduplication check by name
            existing = PendingScheme.query.filter_by(name=s_data['name']).first()
            if not existing:
                ps = PendingScheme(
                    name=s_data['name'],
                    description=s_data['description'],
                    category=s_data.get('category'),
                    application_link=s_data.get('application_link'),
                    benefits=s_data.get('benefits'),
                    eligibility=s_data.get('eligibility'),
                    source_id=source.id,
                    status='pending',
                    confidence_score=s_data.get('confidence_score', 0.8)
                )
                db.session.add(ps)
                new_count += 1
            else:
                skip_count += 1
        
        db.session.commit()
        logger.info(f"Import Complete! New: {new_count}, Skipped: {skip_count}")
        print(f"TOTAL_NEW={new_count}")

if __name__ == "__main__":
    run_bulk_import()
