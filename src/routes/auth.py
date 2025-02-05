from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.schemas.auth import (LoginRequest, RegisterRequest,
                              ResetPasswordRequest)
from src.schemas.token import Token
from src.services.auth import AuthService

router = APIRouter(tags=["Authentification"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register", response_model=Token)
def register(user_data: RegisterRequest, db: Session = Depends(get_db)):
    """Inscription d'un nouvel utilisateur"""
    user = AuthService.register_user(db, user_data)
    return AuthService.create_user_token(user)

@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Connexion d'un utilisateur"""
    user = AuthService.authenticate_user(db, login_data.email, login_data.mot_de_passe)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return AuthService.create_user_token(user)

@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Obtention du token d'accès"""
    user = AuthService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return AuthService.create_user_token(user)

@router.post("/reset-password", response_model=dict)
def reset_password(reset_data: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Réinitialiser le mot de passe d'un utilisateur"""
    try:
        AuthService.reset_password(db, reset_data)
        return {
            "message": "Mot de passe modifié avec succès",
            "status": "success"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Une erreur est survenue lors de la réinitialisation du mot de passe"
        ) 