from datetime import timedelta
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.models import Utilisateur
from src.schemas.auth import (LoginRequest, RegisterRequest,
                              ResetPasswordRequest)
from src.tasks import create_access_token, get_password_hash, verify_password


class AuthService:
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[Utilisateur]:
        try:
            user = db.query(Utilisateur).filter(Utilisateur.email == email).first()
            if not user:
                return None
            
            if not verify_password(password, user.mot_de_passe):
                return None
            
            return user
        except Exception as e:
            print(f"Erreur d'authentification: {str(e)}")  # Pour le débogage
            return None

    @staticmethod
    def register_user(db: Session, user_data: RegisterRequest) -> Utilisateur:
        # Vérifier si l'email existe déjà
        existing_user = db.query(Utilisateur).filter(Utilisateur.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email déjà utilisé")

        # Créer le nouvel utilisateur
        db_user = Utilisateur(
            email=user_data.email,
            mot_de_passe=user_data.mot_de_passe,  # Le hachage sera fait automatiquement
            sexe=user_data.sexe,
            nom=user_data.nom,
            prenom=user_data.prenom,
            telephone=user_data.telephone,
            recevoirMails=user_data.recevoirMails,
            rgpd=user_data.rgpd
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def create_user_token(user: Utilisateur) -> dict:
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=timedelta(minutes=300)
        )
        return {"access_token": access_token, "token_type": "bearer"}

    @staticmethod
    def reset_password(db: Session, reset_data: ResetPasswordRequest) -> bool:
        user = db.query(Utilisateur).filter(Utilisateur.email == reset_data.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

        # Vérifier l'ancien mot de passe
        if not verify_password(reset_data.ancien_mot_de_passe, user.mot_de_passe):
            raise HTTPException(status_code=400, detail="Ancien mot de passe incorrect")

        # Mettre à jour avec le nouveau mot de passe
        user.mot_de_passe = get_password_hash(reset_data.nouveau_mot_de_passe)
        db.commit()
        return True 