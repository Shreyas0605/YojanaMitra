import sys
import io
from app import app, db, Scheme, PendingScheme, SchemeSource, ScrapeLog
from sqlalchemy import desc

# Force UTF-8 for output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with app.app_context():
    print(f"--- Database Status ---")
    print(f"Actual Schemes: {Scheme.query.count()}")
    print(f"Pending Schemes: {PendingScheme.query.count()}")
    
    print(f"\n--- Sources Status ---")
    sources = SchemeSource.query.all()
    for s in sources:
        print(f"Source: {s.name} ({s.scraper_type})")
        print(f"  URL: {s.url}")
        print(f"  Active: {s.is_active}")
        print(f"  Last Scraped: {s.last_scraped}")
    
    print(f"\n--- Recent Scrape Logs ---")
    logs = ScrapeLog.query.order_by(desc(ScrapeLog.scraped_at)).limit(15).all()
    for l in logs:
        source_name = l.source.name if l.source else "Unknown"
        print(f"[{l.scraped_at}] {source_name}: {l.status} - {l.schemes_found} found")
        if l.error_message:
            print(f"  Error: {l.error_message}")

    print(f"\n--- Sample Pending Schemes ---")
    pending = PendingScheme.query.limit(10).all()
    for p in pending:
        try:
            source_name = p.source.name if p.source else '?'
            print(f"- {p.name} (Source: {source_name})")
        except:
            print(f"- [Encoding Error In Name]")
