from datetime import datetime
from typing import Dict


class UserModel:

    @staticmethod
    def create_user_document(name: str, email: str, password: str, role: str) -> Dict:
        return {
            "name": name,
            "email": email,
            "password": password,
            "role": role,
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

    @staticmethod
    def sanitize_user_output(user_doc: Dict) -> Dict:
        """Remove sensitive fields before sending to API"""
        return {
            "name": user_doc.get("name"),
            "email": user_doc.get("email"),
            "role": user_doc.get("role"),
            "is_active": user_doc.get("is_active"),
            "created_at": user_doc.get("created_at")
        }