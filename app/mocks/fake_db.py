from datetime import datetime, timezone


fake_users_db = {
    "1": {
        "user_id": 1,
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc",
        "is_verified": True,
        "disabled": False,
        "created_at": datetime.now(timezone.utc),
    }
}

fake_refresh_tokens = {"token123": 1}
