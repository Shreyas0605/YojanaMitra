from app import app

def list_routes():
    print("Listing all registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.rule} {rule.methods}")

if __name__ == "__main__":
    list_routes()
