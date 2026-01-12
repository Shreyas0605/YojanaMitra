"""
Background Job Scheduler for Automated Scheme Scraping
Runs weekly to check government websites for new schemes
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class SchemeScraperScheduler:
    """Manages background scraping jobs"""
    
    def __init__(self, app, db, models):
        self.app = app
        self.db = db
        self.models = models
        self.scheduler = BackgroundScheduler()
        self._stop_flag = False
        self._is_running = False
        self.setup_jobs()

    def is_scraping_running(self):
        """Check if scraping job is currently active"""
        return self._is_running
    
    def setup_jobs(self):
        """Configure scheduled jobs"""
        # Weekly scraping job - Runs every Sunday at 2:00 AM
        self.scheduler.add_job(
            func=self.run_scraping_job,
            trigger=CronTrigger(day_of_week='sun', hour=2, minute=0),
            id='weekly_scheme_scrape',
            name='Weekly Scheme Scraping',
            replace_existing=True
        )
        
        logger.info("Scheduler configured: Weekly scraping on Sundays at 2:00 AM")

    def stop_scraping(self):
        """Signal the running scraping job to stop"""
        print("Stop signal received. Stopping scraping job...")
        self._stop_flag = True
    
    def safe_print(self, msg):
        """Print message safely handling potential encoding issues in Windows terminals"""
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)
            logger.info(msg) # Mirror to python logger
        except Exception:
            try:
                # Try encoding as utf-8 and decoding with errors replaced
                sanitized = str(msg).encode('ascii', errors='replace').decode('ascii')
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {sanitized}", flush=True)
                logger.info(sanitized)
            except:
                pass # Last resort: silent fail to prevent thread crash

    def run_scraping_job(self, limit=None):
        """Main scraping job - executed by scheduler"""
        self.safe_print(f"DEBUG: run_scraping_job thread entered. Limit: {limit}")
        self._is_running = True
        self._stop_flag = False
        
        try:
            from scheme_scraper import get_scraper
            
            # Use stored models
            SchemeSource = self.models.get('SchemeSource')
            PendingScheme = self.models.get('PendingScheme')
            ScrapeLog = self.models.get('ScrapeLog')
            AdminNotification = self.models.get('AdminNotification')
            Admin = self.models.get('Admin')
            Scheme = self.models.get('Scheme')

            with self.app.app_context():
                self.safe_print("\n" + "="*60)
                self.safe_print(f"SCRAPING JOB INITIATED (Limit: {limit})")
                self.safe_print("="*60)
                
                # Get all active scrape sources
                sources = SchemeSource.query.filter_by(is_active=True).all()
                sources.sort(key=lambda s: 0 if s.scraper_type == 'myscheme' else 1)
                self.safe_print(f"Found {len(sources)} active scrape sources.")
                
                if not sources:
                    self.safe_print("WARNING: No active scrape sources found.")
                    return

                total_schemes_found = 0
                
                for source in sources:
                    if self._stop_flag:
                        self.safe_print("Job stopped by user.")
                        break

                    try:
                        self.safe_print(f"\n[SCAN] Starting Source: {source.name}")
                        self.safe_print(f"      URL: {source.url}")
                        
                        # Create an initial 'running' log entry
                        initial_log = ScrapeLog(
                            source_id=source.id,
                            status='running',
                            schemes_found=0,
                            error_message=f"Job started at {datetime.now()}"
                        )
                        self.db.session.add(initial_log)
                        self.db.session.commit()
                        
                        # Get appropriate scraper
                        scraper = get_scraper(source.scraper_type, source.url)
                        self.safe_print(f"      Scraper: {scraper.__class__.__name__}")
                        
                        # Extract schemes
                        self.safe_print("      Extracting schemes... (This may take a moment)")
                        schemes = scraper.extract_schemes(limit=limit)
                        self.safe_print(f"      Extraction finished. Found {len(schemes)} total schemes.")
                        
                        if self._stop_flag:
                            self.safe_print("      Stopping mid-batch...")
                            break

                        # Get existing scheme names
                        existing_schemes = [s.name for s in Scheme.query.all()]
                        existing_pending = [s.name for s in PendingScheme.query.filter_by(status='pending').all()]
                        all_existing = existing_schemes + existing_pending
                        self.safe_print(f"      [DB] Cross-referencing {len(all_existing)} known schemes...")
                        
                        new_schemes_count = 0
                        
                        for scheme_data in schemes:
                            if self._stop_flag: break
                            
                            if not scraper.is_duplicate(scheme_data['name'], all_existing):
                                self.safe_print(f"      ✨ NEW SCHEME: {scheme_data['name']}")
                                
                                pending_scheme = PendingScheme(
                                    name=scheme_data['name'],
                                    description=scheme_data['description'],
                                    category=scheme_data.get('category'),
                                    target_audience=scheme_data.get('target_audience'),
                                    benefits=scheme_data.get('benefits'),
                                    eligibility=scheme_data.get('eligibility'),
                                    application_link=scheme_data.get('application_link'),
                                    min_age=scheme_data.get('min_age'),
                                    max_age=scheme_data.get('max_age'),
                                    allowed_genders=scheme_data.get('allowed_genders'),
                                    min_income=scheme_data.get('min_income'),
                                    max_income=scheme_data.get('max_income'),
                                    allowed_occupations=scheme_data.get('allowed_occupations'),
                                    allowed_castes=scheme_data.get('allowed_castes'),
                                    allowed_states=scheme_data.get('allowed_states'),
                                    allowed_marital_status=scheme_data.get('allowed_marital_status'),
                                    disability_requirement=scheme_data.get('disability_requirement', 'Any'),
                                    residence_requirement=scheme_data.get('residence_requirement', 'Any'),
                                    minority_requirement=scheme_data.get('minority_requirement', 'Any'),
                                    senior_citizen_requirement=scheme_data.get('senior_citizen_requirement', 'Any'),
                                    widow_requirement=scheme_data.get('widow_requirement', 'Any'),
                                    disability_percentage_min=scheme_data.get('disability_percentage_min'),
                                    bank_account_required=scheme_data.get('bank_account_required', 'No'),
                                    aadhaar_required=scheme_data.get('aadhaar_required', 'No'),
                                    allowed_ration_card_types=scheme_data.get('allowed_ration_card_types'),
                                    min_education_level=scheme_data.get('min_education_level', 'None'),
                                    exclusions=scheme_data.get('exclusions'),
                                    application_process=scheme_data.get('application_process'),
                                    documents_required=scheme_data.get('documents_required'),
                                    allowed_father_occupations=scheme_data.get('allowed_father_occupations'),
                                    allowed_mother_occupations=scheme_data.get('allowed_mother_occupations'),
                                    allowed_religions=scheme_data.get('allowed_religions'),
                                    land_type_requirement=scheme_data.get('land_type_requirement', 'Any'),
                                    orphan_requirement=scheme_data.get('orphan_requirement', 'Any'),
                                    tribal_requirement=scheme_data.get('tribal_requirement', 'Any'),
                                    source_id=source.id,
                                    status='pending',
                                    confidence_score=scheme_data.get('confidence_score', 0.5)
                                )
                                
                                self.db.session.add(pending_scheme)
                                self.db.session.flush()
                                
                                admins = Admin.query.all()
                                for admin in admins:
                                    notification = AdminNotification(
                                        admin_id=admin.id,
                                        pending_scheme_id=pending_scheme.id,
                                        message=f"New scheme detected: {pending_scheme.name}"
                                    )
                                    self.db.session.add(notification)
                                
                                new_schemes_count += 1
                                all_existing.append(scheme_data['name'])
                        
                        source.last_scraped = datetime.utcnow()
                        
                        # Update the initial log to 'success'
                        initial_log.status = 'success'
                        initial_log.schemes_found = new_schemes_count
                        initial_log.error_message = f"Completed at {datetime.now()}"
                        
                        total_schemes_found += new_schemes_count
                        self.safe_print(f"      COMPLETED {source.name}: Found {new_schemes_count} new schemes.")
                        self.db.session.commit()
                        
                    except Exception as e:
                        self.db.session.rollback()
                        error_msg = str(e)
                        self.safe_print(f"      ERROR scraping {source.name}: {error_msg}")
                        
                        try:
                            # Update initial log with error
                            initial_log.status = 'error'
                            initial_log.error_message = error_msg
                            self.db.session.commit()
                        except:
                            pass 
                
                status_msg = "INTERRUPTED" if self._stop_flag else "COMPLETE"
                self.safe_print("\n" + "="*60)
                self.safe_print(f"SCRAPING JOB {status_msg}")
                self.safe_print(f"TOTAL NEW SCHEMES FOUND: {total_schemes_found}")
                self.safe_print("="*60 + "\n")
                
        except Exception as e:
            self.safe_print(f"CRITICAL ERROR in Scheduler: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            self._is_running = False
            self.safe_print("Scheduler state reset to IDLE.")

    def start(self):
        """Start the scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Scheduler started")
    
    def shutdown(self):
        """Gracefully shutdown the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler shut down")
    
    def trigger_manual_scrape(self):
        """Manually trigger scraping (for admin use)"""
        if self._is_running:
            print("WARNING: Already running, ignoring trigger")
            return
        logger.info("Manual scrape triggered by admin")
        self.run_scraping_job()


# Global scheduler instance (initialized in app.py)
scheduler_instance = None

def init_scheduler(app, db, models):
    """Initialize and start the scheduler"""
    global scheduler_instance
    scheduler_instance = SchemeScraperScheduler(app, db, models)
    scheduler_instance.start()
    return scheduler_instance
