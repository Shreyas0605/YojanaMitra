"""
Update SchemeSource URLs to point to the specific scraping targets
"""
from app import app, db, SchemeSource

def update_sources():
    with app.app_context():
        # Update Karnataka SevaSethe
        sevasethe_url = "https://sevasindhu.karnataka.gov.in/Sevasindhu/DepartmentServices"
        source = SchemeSource.query.filter(SchemeSource.name.like('%SevaSethe%')).first()
        if source:
            source.url = sevasethe_url
            print(f"Updated SevaSethe URL to: {sevasethe_url}")
        
        # Update Karnataka One
        k_one_url = "https://karnatakaone.gov.in/Public/Services"
        source = SchemeSource.query.filter(SchemeSource.name.like('%Karnataka One%')).first()
        if source:
            source.url = k_one_url
            print(f"Updated Karnataka One URL to: {k_one_url}")
        # Update myScheme to use specialized scraper
        source = SchemeSource.query.filter(SchemeSource.name.like('%myScheme%')).first()
        if source:
            source.scraper_type = 'myscheme'
            print(f"Updated myScheme scraper type to: myscheme")
            
        db.session.commit()
        print("Database updated successfully!")

if __name__ == "__main__":
    update_sources()
