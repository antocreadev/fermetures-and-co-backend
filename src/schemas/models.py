from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from src.models.models import Categorie, Gender, StatutCommande


class FileField(BaseModel):
    filename: str
    content_type: Optional[str] = None
    size: Optional[int] = None
    url: Optional[str] = None
    path: Optional[str] = None

class ImageBase(BaseModel):
    filename: str
    file: Dict[str, Any]

class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

# Schémas pour Bois
class BoisBase(BaseModel):
    nom: str
    image_id: Optional[int] = None

class BoisCreate(BoisBase):
    pass

class Bois(BoisBase):
    id: int
    image: Optional[Image] = None

    class Config:
        from_attributes = True

# Schémas pour RAL
class RALBase(BaseModel):
    nom: str
    image_id: Optional[int] = None

class RALCreate(RALBase):
    pass

class RAL(RALBase):
    id: int
    image: Optional[Image] = None

    class Config:
        from_attributes = True

# Schémas pour Adresse
class AdresseBase(BaseModel):
    nom: str
    prenom: str
    adresse: str
    complement: str
    ville: str
    code_postal: str
    pays: str

class AdresseCreate(AdresseBase):
    pass

class Adresse(AdresseBase):
    id: int
    utilisateur_id: int

    class Config:
        from_attributes = True

# Schémas pour Produit
class ProduitBase(BaseModel):
    nom: str
    description: Optional[str] = None
    prix: float
    categorie: Categorie
    hauteur: float
    largeur: float
    mitEnAvant: bool
    meilleurVente: bool
    bois_id: Optional[int] = None
    ral_id: Optional[int] = None

class ProduitCreate(ProduitBase):
    pass

class Produit(ProduitBase):
    id: int
    bois: Optional[Bois] = None
    ral: Optional[RAL] = None
    images: List[Image] = []

    class Config:
        from_attributes = True

# Schémas pour Commande
class CommandeBase(BaseModel):
    statut: StatutCommande

class CommandeCreate(CommandeBase):
    pass

class Commande(CommandeBase):
    id: int
    date_commande: datetime
    utilisateur_id: int
    produits: List[Produit] = []

    class Config:
        from_attributes = True

# Schémas pour Utilisateur
class UtilisateurBase(BaseModel):
    sexe: Gender
    nom: str
    prenom: str
    telephone: str
    recevoirMails: bool = True
    rgpd: bool = True
    email: str

class UtilisateurCreate(UtilisateurBase):
    mot_de_passe: str

class Utilisateur(UtilisateurBase):
    id: int
    date_creation: datetime
    adresses: List[Adresse] = []
    commandes: List[Commande] = []

    class Config:
        from_attributes = True

