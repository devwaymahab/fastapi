import time

def get_user_from_db(user_id: int):
    print("Fetching from DB...")

    time.sleep(2)  # Simulate DB latency

    return {
        "id": user_id,
        "name": "Mahab",
        "role": "Developer"
    }