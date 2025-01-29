from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.models import (RAL, Adresse, Bois, Commande, Image, Produit,
                               Utilisateur)


class ImageService:
    @staticmethod
    def get_all(db: Session) -> List[Image]:
        return db.query(Image).all()

    @staticmethod
    def get_by_id(db: Session, image_id: int) -> Optional[Image]:
        return db.query(Image).filter(Image.id == image_id).first()

class BoisService:
    @staticmethod
    def get_all(db: Session) -> List[Bois]:
        return db.query(Bois).all()

    @staticmethod
    def get_by_id(db: Session, bois_id: int) -> Optional[Bois]:
        return db.query(Bois).filter(Bois.id == bois_id).first()

class RALService:
    @staticmethod
    def get_all(db: Session) -> List[RAL]:
        return db.query(RAL).all()

    @staticmethod
    def get_by_id(db: Session, ral_id: int) -> Optional[RAL]:
        return db.query(RAL).filter(RAL.id == ral_id).first()

class AdresseService:
    @staticmethod
    def get_all(db: Session) -> List[Adresse]:
        return db.query(Adresse).all()

    @staticmethod
    def get_by_id(db: Session, adresse_id: int) -> Optional[Adresse]:
        return db.query(Adresse).filter(Adresse.id == adresse_id).first()

    @staticmethod
    def get_by_utilisateur(db: Session, utilisateur_id: int) -> List[Adresse]:
        return db.query(Adresse).filter(Adresse.utilisateur_id == utilisateur_id).all()

class ProduitService:
    @staticmethod
    def get_all(db: Session) -> List[Produit]:
        return db.query(Produit).all()

    @staticmethod
    def get_by_id(db: Session, produit_id: int) -> Optional[Produit]:
        return db.query(Produit).filter(Produit.id == produit_id).first()

    @staticmethod
    def get_by_categorie(db: Session, categorie: str) -> List[Produit]:
        return db.query(Produit).filter(Produit.categorie == categorie).all()

    @staticmethod
    def get_meilleurs_ventes(db: Session) -> List[Produit]:
        return db.query(Produit).filter(Produit.meilleurVente == True).all()

    @staticmethod
    def get_mis_en_avant(db: Session) -> List[Produit]:
        return db.query(Produit).filter(Produit.mitEnAvant == True).all()

class CommandeService:
    @staticmethod
    def get_all(db: Session) -> List[Commande]:
        return db.query(Commande).all()

    @staticmethod
    def get_by_id(db: Session, commande_id: int) -> Optional[Commande]:
        return db.query(Commande).filter(Commande.id == commande_id).first()

    @staticmethod
    def get_by_utilisateur(db: Session, utilisateur_id: int) -> List[Commande]:
        return db.query(Commande).filter(Commande.utilisateur_id == utilisateur_id).all()

class UtilisateurService:
    @staticmethod
    def get_all(db: Session) -> List[Utilisateur]:
        return db.query(Utilisateur).all()

    @staticmethod
    def get_by_id(db: Session, utilisateur_id: int) -> Optional[Utilisateur]:
        return db.query(Utilisateur).filter(Utilisateur.id == utilisateur_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[Utilisateur]:
        return db.query(Utilisateur).filter(Utilisateur.email == email).first() 