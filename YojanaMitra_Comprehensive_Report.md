# YojanaMitra - Comprehensive Project Report
**Version:** 1.0 (Development) | **Date:** 2026-01-12

## 1. Executive Summary
**YojanaMitra** is an intelligent, AI-driven welfare portal designed to bridge the gap between Indian citizens and government schemes. Unlike traditional static portals, it actively discovers new schemes (via scraping), intelligently matches users based on holistic criteria (caste, income, occupation), and provides proactive guidance through AI chatbots and lifecycle forecasting.

## 2. Architecture Details
The project follows a **Monolithic Client-Server Architecture** utilizing a robust Python backend and a lightweight, responsive frontend.

### 2.1 Backend Architecture
-   **Framework:** Flask (Python Microframework).
-   **Pattern:** MVC (Model-View-Controller) structure consolidated within `app.py`.
-   **Concurrency:** Threaded execution for background tasks (Scraping, Email/SMS dispatch).
-   **Scheduler:** `APScheduler` manages periodic scraping jobs (Weekly/Daily).

### 2.2 Frontend Architecture
-   **Pattern:** Single Page Application (SPA) hybrid behavior using Vanilla JavaScript `showPage()` routing.
-   **Framework:** **Bootstrap 5.3.2** for responsive, modern UI components.
-   **Dynamic Content:** DOM manipulation via JavaScript to render schemes, modals, and user profiles without page reloads.

### 2.3 Data Flow
1.  **Ingestion:** Automated Scraper -> `PendingScheme` Table.
2.  **Curation:** Admin Admin Panel -> Approval/Rejection (`Scheme` Table) -> Notification Trigger.
3.  **Discovery:** User Profile Data -> Matching Engine -> `Scheme` Table (Filtered).
4.  **Interaction:** Chatbot <-> Gemini API <-> User Context.

## 3. Technology Stack

### Backend
-   **Language:** Python 3.x
-   **Web Server:** Flask 3.0.0
-   **ORM:** Flask-SQLAlchemy (abstraction over SQLite).
-   **Utilities:** `python-dotenv` (Config), `APScheduler` (Jobs).

### Frontend
-   **Language:** HTML5, CSS3, JavaScript (ES6+).
-   **Styling:** Bootstrap 5, FontAwesome 6 (Icons), Custom CSS (`style.css`).
-   **Auth:** Google One Tap (GSI) library integration (prepared).

### Database
-   **Engine:** SQLite (`yojanamitra.db`).
-   **Reasoning:** Lightweight, serverless, zero-config for rapid deployment.

### AI & Automation
-   **LLM:** Google Gemini Pro (`google-generativeai`) for Chatbot and text analysis.
-   **Vision AI:** Google Gemini Vision for Document Validation (e.g., Aadhaar/Income Cert analysis).
-   **Scraping:** BeautifulSoup4, Selenium (headless), LXML.

### Communication
-   **SMS:** Twilio API.
-   **Email:** Flask-Mail (SMTP via Gmail).

## 4. Core Features Catalogue

### 4.1 Intelligent Scheme Discovery
-   **Automated Scraping:** System autonomously visits configured "Source URLs" (e.g., MyScheme, SevaSindhu) to extract new scheme data.
-   **Pending Queue:** Scraped schemes enter a "Pending" state for Admin review, ensuring data quality.
-   **Batch Approval:** Admins can approve multiple schemes at once.

### 4.2 Precision Matching Engine
-   **Holistic Criteria:** Matches based on granular attributes:
    -   Basic: Age, Gender, Income, Caste, State.
    -   Advanced: Father/Mother Occupation, Disability %, Land Holding, Ration Card Type.
-   **Conflict Resolution:** actively detects "Mutually Exclusive" schemes (e.g., if User applies for "Scheme A", warn them about conflict with "Scheme B").
-   **Lifecycle Forecast:** Predicts eligibility for schemes in **1, 3, and 5 years** based on user's trajectory (e.g., "In 2 years, when you turn 18...").

### 4.3 User Experience (UX)
-   **Smart Redirection:** "Apply Now" checks if a direct link exists; if not, performs a "Beneficial Search" on MyScheme portal.
-   **Multi-language Support:** Full toggling between **English** and **Kannada**.
-   **dashboard:** Persistent user profile with edit capabilities.

### 4.4 AI Powers
-   **YojanaMitra Bot:** A context-aware chatbot that answers questions about schemes.
-   **Document Validator:** Users can upload documents (e.g., Income Cert), and the AI verifies them against scheme requirements.

### 4.5 Dual Channel Notifications
-   **Real-time Alerts:** Automatically sends **SMS** and **Emails** to all registered users when a new scheme is Approved.
-   **Tech:** Integrated `Twilio` (SMS) and `Flask-Mail` (Email) loops.

### 4.6 Administrator Panel
-   **Secured Access:** Separate Admin login.
-   **Scheme Management:** CRUD operations, Batch Processing.
-   **System Health:** Monitoring of Scraper logs.

## 5. Database Schema (Key Tables)
-   `User`: Stores profile demographics, income, occupation details.
-   `Admin`: Credentials for backend access.
-   `Scheme`: The core catalog of verified schemes.
-   `PendingScheme`: Holding area for scraped data.
-   `SchemeSource`: Configurable list of target URLs for the scraper.
-   `ScrapeLog`: Audit trail of scraping jobs (Success/Failure stats).
-   `AdminNotification`: Alerts for admins when scraper finds new items.

## 6. External Integrations
| Service | Purpose | status |
| :--- | :--- | :--- |
| **Google Gemini** | Chatbot & OCR Logic | Active |
| **Twilio** | SMS Notifications | Active |
| **Gmail SMTP** | Email Notifications | Active |
| **MyScheme Portal** | Data Source | Connected |

---
*End of Report*
