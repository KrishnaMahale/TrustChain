"""
Firebase Admin / Firestore client.

Uses environment variables:
- FIREBASE_PROJECT_ID
- FIREBASE_CLIENT_EMAIL
- FIREBASE_PRIVATE_KEY
"""
from functools import lru_cache

import firebase_admin
from firebase_admin import credentials, firestore

from config import get_settings


@lru_cache()
def get_firestore_client() -> firestore.Client:
    """
    Initialize and return a Firestore client.

    Uses service account fields from environment variables so we don't
    rely on a JSON key file on disk.
    """
    settings = get_settings()

    if not firebase_admin._apps:
        if not (
            settings.FIREBASE_PROJECT_ID
            and settings.FIREBASE_CLIENT_EMAIL
            and settings.FIREBASE_PRIVATE_KEY
        ):
            raise RuntimeError(
                "Firebase is not configured. Set FIREBASE_PROJECT_ID, "
                "FIREBASE_CLIENT_EMAIL and FIREBASE_PRIVATE_KEY in the environment."
            )

        private_key = settings.FIREBASE_PRIVATE_KEY.replace("\\n", "\n")

        cred = credentials.Certificate(
            {
                "type": "service_account",
                "project_id": settings.FIREBASE_PROJECT_ID,
                "client_email": settings.FIREBASE_CLIENT_EMAIL,
                "private_key": private_key,
            }
        )
        firebase_admin.initialize_app(cred, {"projectId": settings.FIREBASE_PROJECT_ID})

    return firestore.client()

