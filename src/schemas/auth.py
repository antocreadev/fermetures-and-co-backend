from pydantic import BaseModel, EmailStr

from src.models.models import Gender


class LoginRequest(BaseModel):
    email: EmailStr
    mot_de_passe: str

class RegisterRequest(BaseModel):
    email: EmailStr
    mot_de_passe: str
    sexe: Gender
    nom: str
    prenom: str
    telephone: str
    recevoirMails: bool = True
    rgpd: bool = True

    class Config:
        use_enum_values = True
        json_encoders = {
            Gender: lambda v: v.value
        }

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    ancien_mot_de_passe: str
    nouveau_mot_de_passe: str 