"""
Web Scraper Module for Government Scheme Websites
Automatically detects and extracts scheme information from Karnataka and national education portals
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime
from typing import List, Dict, Optional
import logging
import google.generativeai as genai
import os

logger = logging.getLogger(__name__)

# Configure Gemini for structured extraction
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        ai_model = genai.GenerativeModel('gemini-flash-latest')
        logger.info("Gemini AI initialized for scheme extraction")
    except Exception as e:
        print(f"Error initializing Gemini: {e}")
        ai_model = None
else:
    ai_model = None


class BaseScraper:
    """Base class for all government website scrapers"""
    
    def __init__(self, source_url: str, rate_limit_seconds: float = 3.0):
        self.source_url = source_url
        self.rate_limit = rate_limit_seconds
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def safe_print(self, msg):
        """Standardized safe terminal printing for all scrapers"""
        try:
            print(f"      [SCRAPER] {msg}", flush=True)
            logger.info(f"[SCRAPER] {msg}")
        except:
            try:
                # Sanitize for traditional Windows terminal
                sanitized = str(msg).encode('ascii', errors='replace').decode('ascii')
                print(f"      [SCRAPER] {sanitized}", flush=True)
                logger.info(f"[SCRAPER] {sanitized}")
            except:
                pass # Silent failure for terminal stability
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a web page with rate limiting"""
        try:
            time.sleep(self.rate_limit)  # Respect rate limiting
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None
    
    def extract_schemes(self, limit: Optional[int] = None) -> List[Dict]:
        """Override in subclass to implement specific extraction logic
        
        Args:
            limit (int, optional): Maximum number of schemes to extract.
        """
        raise NotImplementedError("Subclass must implement extract_schemes()")
    
    def normalize_scheme_data(self, raw_data: Dict) -> Dict:
        """
        Convert raw scraped data into database-compatible format
        Returns scheme data with confidence score
        """
        if not self.is_valid_scheme_name(raw_data.get('name', '')):
            return None
            
        scheme = {
            'name': raw_data.get('name', '').strip(),
            'description': raw_data.get('description', '').strip(),
            'category': self.infer_category(raw_data),
            'target_audience': raw_data.get('target_audience', ''),
            'benefits': raw_data.get('benefits', ''),
            'eligibility': raw_data.get('eligibility', ''),
            'application_link': raw_data.get('application_link', ''),
            'exclusions': raw_data.get('exclusions', ''),
            'application_process': raw_data.get('application_process', ''),
            'documents_required': raw_data.get('documents_required', ''),
            'confidence_score': 0.5 # Default
        }
        
        # Extract structured criteria
        # Try AI extraction first for high precision
        criteria = self.extract_criteria_with_ai(raw_data)
        
        # If AI identifies this as NOT a scheme, skip it
        if criteria and criteria.get('is_not_a_scheme'):
            logger.info(f"AI filtered out non-scheme item: {raw_data.get('name')}")
            return None

        if not criteria:
            # Fallback to rule-based
            criteria = self.extract_criteria_rules(raw_data)
            scheme['confidence_score'] = self.calculate_confidence(raw_data)
        else:
            # AI found criteria, boost confidence
            scheme['confidence_score'] = max(0.8, self.calculate_confidence(raw_data))
            
        scheme.update(criteria)
        return scheme
    
    def infer_category(self, data: Dict) -> str:
        """Infer scheme category from text content"""
        text = f"{data.get('name', '')} {data.get('description', '')}".lower()
        
        categories = {
            'Education': ['scholarship', 'education', 'student', 'school', 'college', 'university', 'study', 'vidya'],
            'Agriculture': ['farmer', 'agriculture', 'crop', 'kisan', 'krishi', 'farm', 'raitha'],
            'Healthcare': ['health', 'medical', 'hospital', 'treatment', 'doctor', 'arogya'],
            'Housing': ['house', 'housing', 'shelter', 'awas', 'home', 'gruha'],
            'Social Welfare': ['welfare', 'pension', 'widow', 'disability', 'senior citizen', 'social'],
            'Employment': ['employment', 'job', 'skill', 'training', 'rojgar', 'yuva'],
            'Women Empowerment': ['woman', 'women', 'girl', 'mahila', 'maternity', 'lakshmi'],
            'Energy': ['solar', 'electricity', 'power', 'energy', 'jyothi'],
            'Water': ['water', 'jal', 'drinking water'],
            'Pension': ['pension', 'retirement', 'old age']
        }
        
        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        return 'Other'
    
    def calculate_confidence(self, data: Dict) -> float:
        """Calculate confidence score (0.0-1.0) based on data completeness"""
        score = 0.0
        # Name is crucial
        if data.get('name') and len(data['name'].strip()) > 5:
            score += 0.4
        
        # Description or benefits
        if (data.get('description') and len(data['description'].strip()) > 10) or \
           (data.get('benefits') and len(data['benefits'].strip()) > 10):
            score += 0.3
            
        # Link
        if data.get('application_link'):
            score += 0.2
            
        # Category inferred
        if self.infer_category(data) != 'Other':
            score += 0.1
            
        return min(1.0, score)
    
    def is_valid_scheme_name(self, text: str) -> bool:
        """Filter out navigational text, notifications, and generic labels"""
        text = text.lower().strip()
        
        # 1. Basic length checks
        if len(text) < 8 or len(text) > 200: return False
        
        # 2. Junk Keywords (Substrings)
        exclude_keywords = [
            'login', 'register', 'signin', 'sign in', 'sign up', 'contact', 'about us', 
            'faq', 'help', 'click here', 'read more', 'view all', 'download', 'pdf',
            'nodal officer', 'institute', 'verification', 'dashboard', 'home', 'back',
            'sitemap', 'accessibility', 'screen reader', 'skip to main', 'content',
            'apply for', 'application for', 'status', 'track', 'eligibility',
            'guidelines', 'announcement', 'notification', 'circular', 'required to',
            'processed for', 'applicants', 'services', 'get services', 'portal', 
            'official website', 'welcome to', 'click below', 'ಇಲ್ಲಿ ಕ್ಲಿಕ್ ಮಾಡಿ', 
            'ಹೆಚ್ಚಿನ ಮಾಹಿತಿಗಾಗಿ', 'ಸೇವೆಗಳನ್ನು ಪಡೆಯಲು', 'ನಾಗರಿಕ ಸೇವೆ',
            'current year', 'last updated', 'privacy policy', 'copyright', 'disclaimer',
            'term of use', 'search result', 'page 1', 'show results', 'previous', 'next',
            'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
            'september', 'october', 'november', 'december',
            'excel', 'word file', 'audio file', 'powerpoint', 'ppt', 'video', 'multimedia',
            'document', 'powered by', 'required field', 'instruction', 'search for',
            'filter by', 'sort by', 'all categories', 'quick links', 'important links',
            'presentation', 'presentations',
            'sign out', 'signout', 'cancel', 'ok', 'something went wrong', 'try again',
            'are you sure', 'want to sign out', 'logged in as', 'my profile', 'my account',
            'session expired', 'loading...', 'please wait', 'no results found',
            'error 404', 'page not found', 'server error', 'invalid request',
            'click to close', 'close window', 'print this page', 'share on facebook',
            'share on twitter', 'follow us', 'subscribe to', 'mailing list',
            'cookie policy', 'we use cookies', 'accept and close', 'manage preferences',
            'navigation menu', 'toggle navigation', 'search schemes', 'find schemes',
            'back to top', 'return to top', 'go to top', 'scroll to top',
            'loading schemes', 'fetching data', 'please check your internet',
            'retry connection', 'form validation error', 'field is required',
            'select an option', 'choose from list', 'drop down menu',
            'unsupported browser', 'best viewed in', 'optimized for',
            'official mobile app', 'get it on google play', 'available on app store'
        ]
        
        for keyword in exclude_keywords:
            if keyword in text:
                return False
        
        # 3. Regex patterns for dates and numeric junk
        junk_patterns = [
            r'^[0-9\s\-]+$', # Only numbers and symbols
            r'\b20[2-3][0-9]\b', # Any year from 2020-2039
            r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+[0-9]{1,2}\b', # Month + Day
            r'\b[0-9]{1,2}:[0-9]{2}(\s+)?(am|pm)?\b', # Time
            r'(january|february|march|april|may|june|july|august|september|october|november|december)',
            r'version\s+[0-9\.]+', # Version numbers
            r'step\s+[0-9]', # Step 1, 6 Steps
            r'showing\s+[0-9]+\s+to\s+[0-9]+', # Showing 1 to 10
            r'[0-9]+\s+results?\s+found', # 150 results found
            r'page\s+[0-9]+', # Page 1
            r'last\s+updated\s+on',
            r'powered\s+by',
            r'required\s+fields?',
            r'find\s+the\s+best\s+schemes',
            r'this\s+section\s+provides',
            r'sign\s+out', r'log\s+out',
            r'something\s+went\s+wrong',
            r'try\s+again\s+later',
            r'\.xlsx?$', r'\.docx?$', r'\.pptx?$', r'\.mp3$', r'\.mp4$', r'\.zip$', # File extensions
            r'^click here$', r'^read more$', r'^view all$', r'^download$',
            r'^apply now$', r'^apply online$', r'^register now$',
            r'^close$', r'^cancel$', r'^ok$', r'^submit$', r'^reset$',
            r'^\d+\s*min\s*read$', # 5 min read
            r'facebook|twitter|instagram|linkedin|youtube|whatsapp', # Social media noise
            r'^(audio|video|word|excel|powerpoint|ppt|pdf|document)\s*files?$', # Block pure file-type names
            r'^presented\s*by$', r'^presentations?$',
            r'^current\s+year\s+text/heading'
        ]
        
        for pattern in junk_patterns:
            if re.search(pattern, text, re.I):
                return False

        # 4. Filter if it doesn't contain at least one letter (handles purely symbolic text)
        if not re.search(r'[a-zA-Z]', text):
            return False
            
        return True

    def extract_criteria_with_ai(self, data: Dict) -> Optional[Dict]:
        """Use Gemini to extract granular criteria from unstructured text with retry logic"""
        # GLOBAL DISABLE: Bypassing AI to prevent rate limits during scraped testing
        # Can be re-enabled by removing this return
        return None 
        
        if not ai_model: return None
        
        text_to_analyze = f"""
        Scheme Name: {data.get('name')}
        Description: {data.get('description')}
        Eligibility Text: {data.get('eligibility')}
        Benefits: {data.get('benefits')}
        """
        
        prompt = f"""
        Extract structured eligibility criteria from this Indian Government Scheme.
        
        CRITICAL: If the input text is NOT for a specific government scheme (e.g. it is a navigation link, a promotional banner, a login button, generic instructional text, file download list, list of documents, or general portal help text), return EXACTLY: {{"is_not_a_scheme": true}}
        
        DO NOT extract:
        - Lists of file types (Excel, Word, PDF, Audio, Video, PPT)
        - Instructional steps (Step 1, Step 2, etc.)
        - Generic descriptions of a portal (e.g. "This section provides info...")
        - Footer or header navigation links
        - "Powered by" or "Copyright" text
        - Generic headings like "Government Schemes" or "Services"
        
        Return ONLY a JSON object with these fields. Use null if not mentioned.
        
        {{
            "min_age": int,
            "max_age": int,
            "min_income": int,
            "max_income": int,
            "allowed_genders": ["Male", "Female", "Transgender", "All"],
            "allowed_occupations": ["Farmer", "Student", "Unemployed", "Self-Employed", "Worker", "All"],
            "allowed_castes": ["General", "SC", "ST", "OBC", "Minority", "All"],
            "allowed_states": ["Karnataka", "All"],
            "disability_requirement": "Yes" or "No" or "Any",
            "residence_requirement": "Rural" or "Urban" or "Any",
            "minority_requirement": "Yes" or "No" or "Any",
            "senior_citizen_requirement": "Yes" or "No" or "Any",
            "widow_requirement": "Yes" or "No" or "Any",
            "disability_percentage_min": int,
            "bank_account_required": "Yes" or "No",
            "aadhaar_required": "Yes" or "No",
            "allowed_ration_card_types": ["BPL", "APL", "AAY", "PHH", "All"],
            "min_education_level": "None" or "Primary" or "Secondary" or "Graduate" or "Post-Graduate",
            "exclusions": "string description of exclusions or null",
            "application_process": "detailed step-by-step application instructions or null",
            "documents_required": "list or description of required documents or null"
        }}
        
        Scheme Data:
        {text_to_analyze}
        """
        
        max_retries = 3
        retry_delay = 5  # Start with 5 seconds
        
        for attempt in range(max_retries):
            try:
                # Add a small delay between AI requests to avoid immediate rate limit
                time.sleep(2) 
                
                response = ai_model.generate_content(prompt)
                # Find JSON in response
                match = re.search(r'\{.*\}', response.text, re.DOTALL)
                if match:
                    extracted = json.loads(match.group())
                    # Normalize JSON arrays to strings for DB
                    for field in ['allowed_genders', 'allowed_occupations', 'allowed_castes', 'allowed_states', 'allowed_ration_card_types']:
                        if field in extracted:
                            extracted[field] = json.dumps(extracted[field] if extracted[field] else [])
                    return extracted
                break # Success or no match
            except Exception as e:
                if "429" in str(e) or "Quota exceeded" in str(e):
                    logger.warning(f"AI Rate Limit hit (Attempt {attempt+1}/{max_retries}). Retrying in {retry_delay}s...")
                    time.sleep(retry_delay)
                    retry_delay *= 2 # Exponential backoff
                else:
                    logger.error(f"AI Extraction failed: {e}")
                    break
        return None

    def extract_criteria_rules(self, data: Dict) -> Dict:
        """Fallback rule-based extraction for structured eligibility criteria"""
        criteria = {
            'min_age': None, 'max_age': None, 'min_income': None, 'max_income': None,
            'allowed_genders': json.dumps(['All']),
            'allowed_states': json.dumps(['Karnataka']),
            'allowed_occupations': json.dumps([]),
            'allowed_castes': json.dumps([]),
            'allowed_education': json.dumps([]),
            'allowed_marital_status': json.dumps([]),
            'disability_requirement': 'Any', 'residence_requirement': 'Any',
            'minority_requirement': 'Any', 'senior_citizen_requirement': 'Any',
            'widow_requirement': 'Any', 'disability_percentage_min': None,
            'bank_account_required': 'No', 'aadhaar_required': 'No',
            'allowed_ration_card_types': json.dumps(['All']),
            'min_education_level': 'None'
        }
        
        text = (data.get('name', '') + ' ' + data.get('description', '') + ' ' + data.get('eligibility', '')).lower()
        
        # Simple keywords
        if any(w in text for w in ['women', 'female', 'girl', 'mahila']):
            criteria['allowed_genders'] = json.dumps(['Female'])
        if any(w in text for w in ['farmer', 'kisan', 'raitha']):
            criteria['allowed_occupations'] = json.dumps(['Farmer'])
        if any(w in text for w in ['student', 'vidya', 'scholarship']):
            criteria['allowed_occupations'] = json.dumps(['Student'])
            
        # Caste
        castes = []
        if 'sc' in text or 'scheduled caste' in text: castes.append('SC')
        if 'st' in text or 'scheduled tribe' in text: castes.append('ST')
        if 'obc' in text: castes.append('OBC')
        if 'minority' in text: castes.append('Minority'); criteria['minority_requirement'] = 'Yes'
        if castes: criteria['allowed_castes'] = json.dumps(castes)
        
        return criteria
    
    def is_duplicate(self, scheme_name: str, existing_schemes: List[str]) -> bool:
        """Check if scheme already exists using precise matching"""
        name = scheme_name.lower().strip()
        for existing in existing_schemes:
            existing_lower = existing.lower().strip()
            if name == existing_lower: return True
            
            # Substring match only if they are very similar in length (80%+)
            # This avoids "Audio Files" matching "Scheme for Audio Files" etc.
            if len(name) > 15 and len(existing_lower) > 15:
                ratio = min(len(name), len(existing_lower)) / max(len(name), len(existing_lower))
                if ratio > 0.8 and (name in existing_lower or existing_lower in name):
                    return True
        return False


class KarnatakaSevaSetheScraper(BaseScraper):
    """Scraper for SevaSethe Karnataka portal services using internal API"""
    
    def extract_schemes(self, limit: Optional[int] = None) -> List[Dict]:
        # API Endpoints discovered via analysis
        dept_api_url = "https://sevasindhu.karnataka.gov.in/api/dept"
        base_url = "https://sevasindhu.karnataka.gov.in"
        
        logger.info(f"Scraping Karnataka SevaSethe API: {dept_api_url}")
        schemes = []
        
        try:
            # 1. Fetch Departments
            # Add specific headers to mimic browser Ajax
            headers = {
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://sevasindhu.karnataka.gov.in/Sevasindhu/DepartmentServices'
            }
            self.session.headers.update(headers)
            
            resp = self.session.get(dept_api_url, timeout=30, verify=False)
            if resp.status_code != 200:
                logger.error(f"Failed to fetch departments API: {resp.status_code}")
                return schemes
                
            departments = resp.json()
            logger.info(f"Found {len(departments)} departments")
            
            # 2. Iterate Departments and fetch services
            for dept in departments:
                dept_id = dept.get('Id')
                dept_name = dept.get('Name', 'Unknown Dept')
                
                if not dept_id: continue
                
                # Fetch services for this dept
                service_api_url = f"{base_url}/api/dept/{dept_id}"
                
                # Small delay to be polite to the API
                time.sleep(0.5) 
                
                try:
                    s_resp = self.session.get(service_api_url, timeout=10, verify=False)
                    if s_resp.status_code == 200:
                        services = s_resp.json()
                        for svc in services:
                            svc_name = svc.get('Name', '').strip()
                            if not self.is_valid_scheme_name(svc_name): continue
                            
                            # Construct Scheme Object
                            scheme = {
                                'name': svc_name,
                                'description': f"Service provided by {dept_name} via Seva Sindhu",
                                'category': self.infer_category({'name': svc_name, 'description': dept_name}),
                                'application_link': f"https://sevasindhu.karnataka.gov.in/Sevasindhu/Serviceplus?serviceId={svc.get('Id')}", # Construct valid link if possible, else generic
                                'benefits': 'Online Application',
                                'eligibility': 'Karnataka Resident'
                            }
                            normalized = self.normalize_scheme_data(scheme)
                            if normalized:
                                schemes.append(normalized)
                except Exception as e:
                    logger.warning(f"Failed to fetch services for dept {dept_id}: {e}")
                    continue
            
            logger.info(f"Found {len(schemes)} schemes/services from SevaSethe API")
            
        except Exception as e:
            logger.error(f"Error scraping SevaSethe API: {e}")
        
        return schemes

    def normalize_scheme_data(self, raw_data: Dict) -> Dict:
        # Override to bypass AI and use rule-based only for speed
        if not self.is_valid_scheme_name(raw_data.get('name', '')): return None
        
        scheme = {
            'name': raw_data.get('name', '').strip(),
            'description': raw_data.get('description', '').strip(),
            'category': self.infer_category(raw_data),
            'target_audience': raw_data.get('target_audience', ''),
            'benefits': raw_data.get('benefits', ''),
            'eligibility': raw_data.get('eligibility', ''),
            'application_link': raw_data.get('application_link', ''),
            'exclusions': raw_data.get('exclusions', ''),
            'application_process': raw_data.get('application_process', ''),
            'documents_required': raw_data.get('documents_required', ''),
            'confidence_score': 0.6 
        }
        # Rule-based only
        criteria = self.extract_criteria_rules(raw_data)
        scheme.update(criteria)
        return scheme



class KarnatakaGuaranteeScraper(BaseScraper):
    """Scraper for Karnataka Guarantee Schemes (Gruha Jyothi, etc.)"""
    
    def extract_schemes(self, limit: Optional[int] = None) -> List[Dict]:
        target_url = "https://sevasindhugs.karnataka.gov.in/"
        logger.info(f"Scraping Karnataka Guarantee Schemes: {target_url}")
        schemes = []
        
        try:
            soup = self.fetch_page(target_url)
            if not soup: return schemes
            
            # These layouts often change, but currently they are prominent buttons/links
            # Look for specific known guarantee scheme names
            guarantees = [
                {'name': 'Gruha Jyothi', 'kn': 'ಗೃಹ ಜ್ಯೋತಿ', 'desc': 'Free electricity up to 200 units for Karnataka households'},
                {'name': 'Gruha Lakshmi', 'kn': 'ಗೃಹ ಲಕ್ಷ್ಮಿ', 'desc': '₹2000 monthly assistance for woman head of family'},
                {'name': 'Shakti Scheme', 'kn': 'ಶಕ್ತಿ', 'desc': 'Free bus travel for women in Karnataka'},
                {'name': 'Yuva Nidhi', 'kn': 'ಯುವನಿಧಿ', 'desc': 'Unemployment assistance for graduates and diploma holders'},
                {'name': 'Anna Bhagya', 'kn': 'ಅನ್ನ ಭಾಗ್ಯ', 'desc': 'Free rice/food grains for BPL card holders'}
            ]
            
            # Scan page text to see if these exist
            page_text = soup.get_text().lower()
            
            for g in guarantees:
                # Check for either English or Kannada name
                if g['name'].lower() in page_text or g['kn'] in page_text:
                    link = target_url # Default to landing page
                    
                    # Try to find specific link
                    # Look for links containing the name
                    link_el = soup.find('a', href=True, string=re.compile(f"{g['name']}|{g['kn']}", re.I))
                    if link_el:
                         href = link_el['href']
                         if href.startswith('http'): link = href
                         else: link = target_url + href
                    
                    normalized = self.normalize_scheme_data({
                        'name': g['name'],
                        'description': g['desc'],
                        'category': 'Social Welfare',
                        'application_link': link,
                        'eligibility': 'Karnataka Resident',
                        'confidence_score': 1.0 # High confidence as we matched specific list
                    })
                    if normalized:
                        schemes.append(normalized)
                    
            logger.info(f"Found {len(schemes)} guarantee schemes")
            
        except Exception as e:
            logger.error(f"Error scraping Guarantee Schemes: {e}")
        return schemes

    def normalize_scheme_data(self, raw_data: Dict) -> Dict:
        # Override to bypass AI and use rule-based only for speed
        if not self.is_valid_scheme_name(raw_data.get('name', '')): return None
        
        scheme = {
            'name': raw_data.get('name', '').strip(),
            'description': raw_data.get('description', '').strip(),
            'category': self.infer_category(raw_data),
            'target_audience': raw_data.get('target_audience', ''),
            'benefits': raw_data.get('benefits', ''),
            'eligibility': raw_data.get('eligibility', ''),
            'application_link': raw_data.get('application_link', ''),
            'exclusions': raw_data.get('exclusions', ''),
            'application_process': raw_data.get('application_process', ''),
            'documents_required': raw_data.get('documents_required', ''),
            'confidence_score': 0.6 
        }
        # Rule-based only
        criteria = self.extract_criteria_rules(raw_data)
        scheme.update(criteria)
        return scheme

class KarnatakaOneScraper(BaseScraper):

    """Scraper for Karnataka One portal"""
    
    def extract_schemes(self, limit: Optional[int] = None) -> List[Dict]:
        target_url = "https://karnatakaone.gov.in/Public/Services"
        logger.info(f"Scraping Karnataka One: {target_url}")
        schemes = []
        
        try:
            # Force verify=False for gov sites often having cert issues
            resp = self.session.get(target_url, timeout=30, verify=False)
            resp.encoding = 'utf-8' # Force UTF-8 to handle Kannada characters
            
            if resp.status_code != 200: return schemes
            soup = BeautifulSoup(resp.content, 'html.parser')
            
            # Karnataka One usually lists services in accordion or table
            # Look for service items in lists or divs with 'service' class
            items = soup.find_all(['div', 'li', 'a'], class_=lambda x: x and 'service' in x.lower())
            
            # Fallback: Look for any list items inside a "Services" container if class fails
            if len(items) < 5:
                container = soup.find(string=re.compile("Services", re.I))
                if container:
                    parent = container.find_parent('div') or container.find_parent('section')
                    if parent:
                        items.extend(parent.find_all('li'))
            
            for item in items:
                text = item.get_text(strip=True)
                if self.is_valid_scheme_name(text):
                     # Often these are links
                    link = target_url
                    if item.name == 'a': 
                        href = item.get('href')
                        if href: link = href if href.startswith('http') else "https://karnatakaone.gov.in" + href
                    elif item.find('a'):
                         href = item.find('a').get('href')
                         if href: link = href if href.startswith('http') else "https://karnatakaone.gov.in" + href

                    normalized = self.normalize_scheme_data({
                        'name': text,
                        'description': f"Service available on Karnataka One: {text}",
                        'application_link': link
                    })
                    if normalized:
                        schemes.append(normalized)

            # Also try tables as fallback
            if len(schemes) < 2:
                tables = soup.find_all('table')
                for table in tables:
                    for row in table.find_all('tr')[1:]:
                        cols = row.find_all('td')
                        if len(cols) >= 1:
                            text = cols[0].get_text(strip=True)
                            if self.is_valid_scheme_name(text):
                                normalized = self.normalize_scheme_data({
                                    'name': text,
                                    'description': f"Service available on Karnataka One: {text}",
                                    'application_link': target_url
                                })
                                if normalized:
                                    schemes.append(normalized)
            
            logger.info(f"Found {len(schemes)} schemes from Karnataka One")
            
        except Exception as e:
            logger.error(f"Error scraping Karnataka One: {e}")
        return schemes

    def normalize_scheme_data(self, raw_data: Dict) -> Dict:
        # Override to bypass AI and use rule-based only for speed
        if not self.is_valid_scheme_name(raw_data.get('name', '')): return None
        
        scheme = {
            'name': raw_data.get('name', '').strip(),
            'description': raw_data.get('description', '').strip(),
            'category': self.infer_category(raw_data),
            'target_audience': raw_data.get('target_audience', ''),
            'benefits': raw_data.get('benefits', ''),
            'eligibility': raw_data.get('eligibility', ''),
            'application_link': raw_data.get('application_link', ''),
            'exclusions': raw_data.get('exclusions', ''),
            'application_process': raw_data.get('application_process', ''),
            'documents_required': raw_data.get('documents_required', ''),
            'confidence_score': 0.6 
        }
        # Rule-based only
        criteria = self.extract_criteria_rules(raw_data)
        scheme.update(criteria)
        return scheme


class EducationGovInScraper(BaseScraper):
    """Scraper for National Scholarship Portal"""
    
    def extract_schemes(self, limit: Optional[int] = None) -> List[Dict]:
        target_url = "https://scholarships.gov.in/"
        logger.info(f"Scraping NSP: {target_url}")
        schemes = []
        
        try:
            soup = self.fetch_page(target_url)
            if not soup: return schemes
            
            # Look for specific scheme identifiers
            # Use regex to find text that looks like a scheme name
            # Often inside specific containers like 'scheme-list' or 'accordion'
            
            # Generic approach for NSP:
            # Look for links or headers containing "Scheme" but filter heavily
            elements = soup.find_all(['a', 'h3', 'h4', 'div'], string=re.compile(r"Scheme|Scholarship", re.I))
            
            for el in elements:
                text = el.get_text(strip=True)
                
                # HEAVY filtering for NSP because it has lots of noise
                if not self.is_valid_scheme_name(text): continue
                if "scheme" not in text.lower() and "scholarship" not in text.lower(): continue 
                
                # Check parents to ensure it's not a menu item
                if el.find_parent(class_=re.compile(r'menu|nav|footer|header', re.I)): continue

                link = target_url
                if el.name == 'a':
                    href = el.get('href')
                    if href: link = href if href.startswith('http') else target_url + href
                
                normalized = self.normalize_scheme_data({
                    'name': text,
                    'description': "National Scholarship Scheme",
                    'category': "Education",
                    'application_link': link
                })
                if normalized:
                    schemes.append(normalized)
            
            # Unique filter
            unique_schemes = []
            seen = set()
            for s in schemes:
                if s['name'] not in seen:
                    seen.add(s['name'])
                    unique_schemes.append(s)
            
            logger.info(f"Found {len(unique_schemes)} schemes from NSP")
            return unique_schemes
            
        except Exception as e:
            logger.error(f"Error scraping NSP: {e}")
            return []


class MySchemeScraper(BaseScraper):
    """Specialized scraper for myScheme.gov.in using their public API"""
    
    def normalize_scheme_data(self, raw_data: Dict) -> Dict:
        """Override to SKIP AI extraction and use only rule-based parsing"""
        if not self.is_valid_scheme_name(raw_data.get('name', '')):
            return None
            
        # Helper to safely serialize lists
        def safe_serialize(val):
            if isinstance(val, list):
                return json.dumps(val)
            return str(val) if val is not None else ''

        scheme = {
            'name': raw_data.get('name', '').strip(),
            'description': raw_data.get('description', '').strip(),
            'category': self.infer_category(raw_data),
            'target_audience': safe_serialize(raw_data.get('target_audience', '')),
            'benefits': raw_data.get('benefits', ''),
            'eligibility': raw_data.get('eligibility', ''),
            'application_link': raw_data.get('application_link', ''),
            'exclusions': raw_data.get('exclusions', ''),
            'application_process': raw_data.get('application_process', ''),
            'documents_required': raw_data.get('documents_required', ''),
            'confidence_score': 0.9 # High confidence from official API
        }
        
        # FORCE RULE-BASED ONLY (No AI)
        criteria = self.extract_criteria_rules(raw_data)
        scheme.update(criteria)
        return scheme

    def extract_schemes(self, limit: Optional[int] = None) -> List[Dict]:
        logger.info(f"MyScheme API Scrape (Detailed): {self.source_url} (Limit: {limit})")
        schemes = []
        
        # Pagination settings
        batch_size = 50 # Reduced batch size to manage detail fetching
        max_schemes = limit if limit else 6000 # Use limit if provided, else safety cap
        current_offset = 0
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://www.myscheme.gov.in',
            'Referer': 'https://www.myscheme.gov.in/',
            'x-api-key': 'tYTy5eEhlu9rFjyxuCr7ra7ACp4dv1RH8gWuHTDc'
        }

        while current_offset < max_schemes:
            # 1. Search API to get list of slugs
            api_url = f"https://api.myscheme.gov.in/search/v6/schemes?lang=en&q=[]&keyword=&sort=&from={current_offset}&size={batch_size}"
            
            try:
                self.safe_print(f"Fetching search batch: offset={current_offset}, size={batch_size}")
                response = requests.get(api_url, headers=headers, timeout=20)
                
                if response.status_code != 200:
                    self.safe_print(f"API Error at offset {current_offset}: {response.status_code}")
                    break
                    
                data = response.json()
                items = data.get('data', {}).get('hits', {}).get('items', [])
                
                if not items:
                    logger.info(f"No more items found at offset {current_offset}. Finishing.")
                    break
                    
                for idx, item in enumerate(items):
                    fields = item.get('fields', {})
                    slug = fields.get('slug')
                    if not slug: continue
                    
                    if (idx + 1) % 10 == 0:
                        self.safe_print(f"Processing item {idx + 1}/{len(items)} in current batch...")

                    # 2. Fetch Full Details for this slug
                    detail_url = f"https://api.myscheme.gov.in/schemes/v6/public/schemes?slug={slug}&lang=en"
                    try:
                        # Polite delay
                        time.sleep(0.2) 
                        d_resp = requests.get(detail_url, headers=headers, timeout=10)
                        
                        if d_resp.status_code == 200:
                            details_json = d_resp.json()
                            
                            # Handle different response structures:
                            # 1. Direct list: [ { "en": { ... } } ]
                            # 2. Nested data: { "data": { "en": { ... } } }
                            # 3. Direct dict: { "en": { ... } }
                            
                            root = {}
                            if isinstance(details_json, list) and details_json:
                                root = details_json[0].get('en', {})
                            elif isinstance(details_json, dict):
                                if 'data' in details_json and isinstance(details_json['data'], dict):
                                    root = details_json['data'].get('en', {})
                                else:
                                    root = details_json.get('en', {})
                            
                            if not root:
                                self.safe_print(f"Warning: Could not find 'en' content for {slug}")
                                continue
                                
                            basic = root.get('basicDetails', {})
                            content = root.get('schemeContent', {})
                            
                            # TOP-LEVEL FIELDS (in root 'en')
                            eligibility_criteria = root.get('eligibilityCriteria', [])
                            application_process = root.get('applicationProcess', [])
                            
                            name = basic.get('schemeName')
                            if not name: name = fields.get('schemeName') # Fallback
                            
                            if self.is_valid_scheme_name(name):
                                link = f"https://www.myscheme.gov.in/schemes/{slug}"
                                
                                # Helper function to convert list/dict/slate to readable string
                                def extract_text(data):
                                    """Recursively extract readable text from various API response formats"""
                                    if data is None: return ''
                                    
                                    if isinstance(data, str):
                                        return data.strip()
                                    
                                    if isinstance(data, dict):
                                        # 1. Prefer markdown versions if this is a container dict
                                        for md_key in ['eligibilityDescription_md', 'benefitsDescription_md', 'description_md', 'content_md', 'text_md', 'markdown']:
                                            if data.get(md_key):
                                                return data.get(md_key).strip()
                                        
                                        # 2. Try common direct text keys (expanded list)
                                        for text_key in ['description', 'text', 'content', 'label', 'value', 'title', 'criteriaDescription', 'benefitDescription']:
                                            val = data.get(text_key)
                                            if val and isinstance(val, str) and val.strip():
                                                return val.strip()
                                        
                                        # 3. Check for children/nodes array (common in slate editors)
                                        if 'children' in data and isinstance(data['children'], list):
                                            return extract_text(data['children'])
                                        
                                        if 'nodes' in data and isinstance(data['nodes'], list):
                                            return extract_text(data['nodes'])
                                        
                                        # 4. If it's a slate-like object, recurse through values
                                        parts = []
                                        for k, v in data.items():
                                            if k not in ['type', 'mode', 'url', 'align', 'id', '__typename']: # Skip metadata
                                                text = extract_text(v)
                                                if text: parts.append(text)
                                        return '\n'.join(parts) if parts else ''
                                    
                                    if isinstance(data, list):
                                        if len(data) == 0: return ''
                                        parts = []
                                        for item in data:
                                            text = extract_text(item)
                                            if text: parts.append(text)
                                        return '\n'.join(parts) if parts else ''
                                        
                                    # Handle numbers and other types
                                    if isinstance(data, (int, float)):
                                        return str(data)
                                        
                                    return ''
                                
                                # EXTRACT FROM MULTIPLE POSSIBLE LOCATIONS
                                # Benefits - try multiple sources
                                benefits_raw = (
                                    content.get('benefits_md') or 
                                    extract_text(content.get('benefits')) or 
                                    extract_text(root.get('benefits')) or
                                    extract_text(basic.get('benefits')) or
                                    ''
                                )
                                
                                # Eligibility - try multiple sources
                                eligibility_raw = (
                                    content.get('eligibility_md') or
                                    extract_text(eligibility_criteria) or 
                                    extract_text(content.get('eligibility')) or
                                    extract_text(root.get('eligibility')) or
                                    ''
                                )
                                
                                # Application Process - try multiple sources
                                app_process_raw = (
                                    content.get('applicationProcess_md') or
                                    extract_text(application_process) or
                                    extract_text(content.get('applicationProcess')) or
                                    extract_text(root.get('applicationProcess')) or
                                    ''
                                )
                                
                                # Documents Required - try multiple sources  
                                docs_required = ''
                                scheme_definitions = root.get('schemeDefinitions', {})
                                if isinstance(scheme_definitions, dict):
                                    docs_list = (
                                        scheme_definitions.get('documents') or 
                                        scheme_definitions.get('requiredDocuments') or 
                                        scheme_definitions.get('documentsRequired') or
                                        []
                                    )
                                    docs_required = extract_text(docs_list)
                                
                                # Also try from content
                                if not docs_required:
                                    docs_required = (
                                        content.get('documents_md') or
                                        content.get('documentsRequired_md') or
                                        extract_text(content.get('documents')) or
                                        extract_text(content.get('documentsRequired')) or
                                        extract_text(root.get('documentsRequired')) or
                                        ''
                                    )
                                
                                # Exclusions
                                exclusions_raw = (
                                    content.get('exclusions_md') or 
                                    extract_text(content.get('exclusions')) or 
                                    extract_text(root.get('exclusions')) or
                                    ''
                                )
                                
                                # Description
                                description = (
                                    content.get('detailedDescription_md') or 
                                    content.get('description_md') or
                                    basic.get('briefDescription', fields.get('briefDescription', ''))
                                )
                                
                                normalized = self.normalize_scheme_data({
                                    'name': name,
                                    'description': description,
                                    'application_link': link,
                                    'category': fields.get('schemeCategory', ['Other'])[0] if fields.get('schemeCategory') else 'Other',
                                    'benefits': str(benefits_raw),
                                    'eligibility': str(eligibility_raw),
                                    'exclusions': str(exclusions_raw),
                                    'application_process': str(app_process_raw),
                                    'documents_required': str(docs_required),
                                    'target_audience': basic.get('targetBeneficiaries', fields.get('targetAudience', []))
                                })
                                
                                if normalized:
                                    schemes.append(normalized)
                                    # Check strict limit if provided (stop EXACTLY at limit)
                                    if limit and len(schemes) >= limit:
                                        logger.info(f"Reached user limit of {limit} schemes.")
                                        return schemes
                        else:
                            logger.warning(f"Failed to fetch details for {slug}: {d_resp.status_code}")
                            
                    except Exception as e:
                        logger.error(f"Error fetching details for {slug}: {e}")
                            
                logger.info(f"Batch processed. Total found so far: {len(schemes)}")
                
                if len(items) < batch_size:
                    break
                    
                current_offset += batch_size
                
            except Exception as e:
                logger.error(f"MyScheme API failed at offset {current_offset}: {e}")
                break
                
        logger.info(f"MyScheme Scrape Complete: Total {len(schemes)} schemes extracted")
        return schemes


class GenericGovernmentScraper(BaseScraper):
    """Generic scraper parsing tables and lists"""
    
    def extract_schemes(self, limit: Optional[int] = None) -> List[Dict]:
        logger.info(f"Generic scrape: {self.source_url}")
        schemes = []
        
        try:
            soup = self.fetch_page(self.source_url)
            if not soup: return schemes
            
            # --- SPA HARDENING: Pre-process soup to remove junk ---
            # Remove scripts, styles, and hidden elements typical of SPA noise
            for trash in soup.find_all(['script', 'style', 'nav', 'footer', 'header']):
                trash.decompose()
            
            # Remove elements with aria-hidden="true" or hidden attribute
            for hidden in soup.find_all(attrs={"aria-hidden": "true"}):
                hidden.decompose()
            for hidden in soup.find_all(attrs={"hidden": True}):
                hidden.decompose()
            
            # Remove elements with common SPA "hidden" or "loading" classes
            for junk_el in soup.find_all(class_=re.compile(r'ng-hide|v-hide|hidden|loading|spinner|modal|overlay|popup', re.I)):
                junk_el.decompose()

            # 1. Look for tables
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                if len(rows) > 1:
                    for row in rows[1:]: # Skip header
                        cols = row.find_all('td')
                        if len(cols) >= 1:
                            # Heuristic: Find the cell with the most text
                            texts = [c.get_text(strip=True) for c in cols]
                            text = " ".join(texts)
                            if len(text) > 15:
                                link = row.find('a')['href'] if row.find('a', href=True) else self.source_url
                                if not link.startswith('http'): link = self.source_url.rstrip('/') + '/' + link.lstrip('/')
                                
                                normalized = self.normalize_scheme_data({
                                    'name': texts[0][:150] if texts else "Unknown Scheme",
                                    'description': text,
                                    'application_link': link
                                })
                                if normalized:
                                    schemes.append(normalized)

            # 2. Look for common card/list patterns if tables yield nothing
            if not schemes:
                # Look for divs that might be cards (common in gov sites)
                cards = soup.find_all(['div', 'li', 'article'], class_=re.compile(r'card|item|service|scheme|box', re.I))
                for card in cards:
                    text = card.get_text(strip=True)
                    if len(text) > 30 and self.is_valid_scheme_name(text[:100]):
                        link_el = card.find('a', href=True)
                        link = link_el['href'] if link_el else self.source_url
                        if not link.startswith('http'): link = self.source_url.rstrip('/') + '/' + link.lstrip('/')
                        
                        normalized = self.normalize_scheme_data({
                            'name': text[:100],
                            'description': text,
                            'application_link': link
                        })
                        if normalized:
                            schemes.append(normalized)

            # 3. Last resort: AI Page Chunking (if Gemini is available)
            if not schemes and ai_model:
                logger.info("No patterns found, attempting AI-assisted page parsing...")
                # Extract clean text chunks from page
                text_content = soup.get_text(separator='\n', strip=True)
                # Take first 4000 chars as it usually contains the main list
                snippet = text_content[:4000]
                
                prompt = f"""
                Examine this web page content from an Indian Government portal. 
                Identify and extract a list of ACTUAL specific government schemes or benefits (e.g. "PM-KISAN", "Scholarship for Girls").
                
                CRITICAL EXCLUSIONS:
                - Do NOT include dates, months, or years (e.g. "2026", "January").
                - Do NOT include navigational text (e.g. "Home", "Sitemap", "Login").
                - Do NOT include generic portal titles or search results headings.
                - Do NOT include file download lists (e.g. "Excel file", "Audio file").
                - Do NOT include instructional steps (e.g. "Step 1 of 6").
                - Only include items that are clearly individual schemes or services.
                
                Return a JSON array of objects:
                [{{"name": "string", "description": "string", "link": "string"}}]
                
                If no specific schemes are found, return [].
                
                Content:
                {snippet}
                """
                
                try:
                    max_retries = 2
                    retry_delay = 5
                    
                    for attempt in range(max_retries):
                        try:
                            time.sleep(2) # Throttle to avoid immediate rate limit
                            response = ai_model.generate_content(prompt)
                            match = re.search(r'\[.*\]', response.text, re.DOTALL)
                            if match:
                                ai_schemes = json.loads(match.group())
                                for s in ai_schemes:
                                    norm = self.normalize_scheme_data({
                                        'name': s.get('name'),
                                        'description': s.get('description'),
                                        'application_link': s.get('link') or self.source_url
                                    })
                                    if norm: schemes.append(norm)
                                break # Successful extraction
                        except Exception as e:
                            if "429" in str(e) or "Quota exceeded" in str(e):
                                logger.warning(f"AI Page Parsing Rate Limit (Attempt {attempt+1}/{max_retries}). Retrying in {retry_delay}s...")
                                time.sleep(retry_delay)
                                retry_delay *= 2
                            else:
                                raise e # Re-raise other errors to be caught by outer block
                except Exception as e:
                    logger.error(f"AI Page parsing failed: {e}")
                                
            logger.info(f"Generic scraper found {len(schemes)} items")
        except Exception as e:
            logger.error(f"Generic scraper error: {e}")
            
        return schemes

def get_scraper(source_type: str, url: str) -> BaseScraper:
    scrapers = {
        'karnataka_sevasethe': KarnatakaSevaSetheScraper,
        'karnataka_guarantee': KarnatakaGuaranteeScraper,
        'karnataka_one': KarnatakaOneScraper,
        'education_gov_in': EducationGovInScraper,
        'myscheme': MySchemeScraper,
        'generic': GenericGovernmentScraper
    }
    return scrapers.get(source_type, GenericGovernmentScraper)(url)
