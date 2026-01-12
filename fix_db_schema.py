import sqlite3
import os

db_path = os.path.join('instance', 'yojanamitra.db')

def add_column_if_not_exists(cursor, table, col_name, col_type):
    try:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {col_name} {col_type}")
        print(f"Added column {col_name} to {table}")
    except sqlite3.OperationalError as e:
        if 'duplicate column' in str(e).lower():
            print(f"Column {col_name} already exists in {table}")
        else:
            print(f"Error adding {col_name}: {e}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables found:", tables)

# List of columns to add to 'user' table
columns = [
    ('father_occupation', 'TEXT'),
    ('mother_occupation', 'TEXT'),
    ('religion', 'TEXT'),
    ('land_type', 'TEXT'),
    ('is_orphan', 'TEXT'),
    ('is_tribal', 'TEXT'),
    ('caste', 'TEXT'),
    ('sub_caste', 'TEXT'),
    ('dob', 'TEXT'),
    ('aadhaar_available', 'TEXT'),
    ('district', 'TEXT'),
    ('block_taluk', 'TEXT'),
    ('domicile_status', 'TEXT'),
    ('family_type', 'TEXT'),
    ('total_family_members', 'INTEGER'),
    ('is_head_of_family', 'TEXT'),
    ('annual_family_income', 'INTEGER'),
    ('income_slab', 'TEXT'),
    ('income_certificate_available', 'TEXT'),
    ('ration_card_available', 'TEXT'),
    ('ration_card_type', 'TEXT'),
    ('education_status', 'TEXT'),
    ('highest_education_level', 'TEXT'),
    ('current_course', 'TEXT'),
    ('institution_type', 'TEXT'),
    ('employment_status', 'TEXT'),
    ('govt_employee_in_family', 'TEXT'),
    ('is_farmer', 'TEXT'),
    ('own_agricultural_land', 'TEXT'),
    ('land_size_acres', 'REAL'),
    ('is_tenant_farmer', 'TEXT'),
    ('disability_percentage', 'INTEGER'),
    ('is_widow_single_woman', 'TEXT'),
    ('is_senior_citizen', 'TEXT'),
    ('bank_account_available', 'TEXT'),
    ('aadhaar_linked_bank', 'TEXT'),
    ('mobile_linked_bank', 'TEXT'),
    ('income_cert_last_1_year', 'TEXT'),
    ('scheme_previously_availed', 'TEXT'),
    ('willing_to_submit_docs', 'TEXT'),
    ('child_age', 'INTEGER'),
    ('education_milestones', 'TEXT'),
    ('career_goal', 'TEXT')
]

print("Starting migration...")
for col_name, col_type in columns:
    add_column_if_not_exists(cursor, 'user', col_name, col_type)

conn.commit()
conn.close()
print("Migration complete.")
