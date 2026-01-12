from app import app, db, Scheme, SchemeSource
import json

def analyze_db():
    with app.app_context():
        # Get counts per source
        results = db.session.query(SchemeSource.name, db.func.count(Scheme.id))\
            .outerjoin(Scheme)\
            .group_by(SchemeSource.name).all()
        
        print("--- Scheme Distribution ---")
        for source_name, count in results:
            print(f"{source_name}: {count}")
            
        print("\n--- Sample Names (First 10 per source) ---")
        sources = SchemeSource.query.all()
        for source in sources:
            print(f"\nSource: {source.name}")
            schemes = Scheme.query.filter_by(source_id=source.id).limit(10).all()
            for s in schemes:
                print(f" - {s.name}")

if __name__ == "__main__":
    analyze_db()
