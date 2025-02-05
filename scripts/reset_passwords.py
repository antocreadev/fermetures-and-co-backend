from src.database import SessionLocal
from src.models.models import Utilisateur
from src.tasks import get_password_hash


def reset_passwords():
    db = SessionLocal()
    try:
        # Définir un mot de passe temporaire pour tous les utilisateurs
        temp_password = "ChangeMe123!"
        hashed_password = get_password_hash(temp_password)
        
        users = db.query(Utilisateur).all()
        for user in users:
            user.mot_de_passe = hashed_password
        
        db.commit()
        print(f"Mots de passe réinitialisés pour {len(users)} utilisateurs")
    finally:
        db.close()

if __name__ == "__main__":
    reset_passwords() 