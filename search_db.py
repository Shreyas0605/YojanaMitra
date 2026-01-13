import os

db_path = r'c:\ym\yojana-mitra-backend\instance\yojanamitra.db'
if os.path.exists(db_path):
    with open(db_path, 'rb') as f:
        data = f.read()
        if b'Spoorthi' in data:
            print("FOUND 'Spoorthi' in DB binary!")
            # Find the context
            idx = data.find(b'Spoorthi')
            print(f"Context: {data[max(0, idx-50):idx+100]}")
        else:
            print("NOT FOUND 'Spoorthi' in DB binary.")
else:
    print(f"DB not found at {db_path}")
