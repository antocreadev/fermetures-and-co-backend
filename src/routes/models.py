from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.schemas.models import (RAL, Adresse, Bois, Commande, Image, Produit,
                                Utilisateur)
from src.services.models import (AdresseService, BoisService, CommandeService,
                                 ImageService, ProduitService, RALService,
                                 UtilisateurService)

router = APIRouter()

# Routes pour les images
@router.get("/images/", response_model=List[Image], tags=["Images"])
def get_images(db: Session = Depends(get_db)):
    """Récupérer toutes les images"""
    return ImageService.get_all(db)

@router.get("/images/{image_id}", response_model=Image, tags=["Images"])
def get_image(image_id: int, db: Session = Depends(get_db)):
    """Récupérer une image par son ID"""
    image = ImageService.get_by_id(db, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image non trouvée")
    return image

# Routes pour les bois
@router.get("/bois/", response_model=List[Bois], tags=["Bois"])
def get_all_bois(db: Session = Depends(get_db)):
    """Récupérer tous les types de bois"""
    return BoisService.get_all(db)

@router.get("/bois/{bois_id}", response_model=Bois, tags=["Bois"])
def get_bois(bois_id: int, db: Session = Depends(get_db)):
    """Récupérer un type de bois par son ID"""
    bois = BoisService.get_by_id(db, bois_id)
    if not bois:
        raise HTTPException(status_code=404, detail="Type de bois non trouvé")
    return bois

# Routes pour les RAL
@router.get("/rals/", response_model=List[RAL], tags=["RAL"])
def get_all_rals(db: Session = Depends(get_db)):
    """Récupérer tous les RAL"""
    return RALService.get_all(db)

@router.get("/rals/{ral_id}", response_model=RAL, tags=["RAL"])
def get_ral(ral_id: int, db: Session = Depends(get_db)):
    """Récupérer un RAL par son ID"""
    ral = RALService.get_by_id(db, ral_id)
    if not ral:
        raise HTTPException(status_code=404, detail="RAL non trouvé")
    return ral

# Routes pour les adresses
@router.get("/adresses/", response_model=List[Adresse], tags=["Adresses"])
def get_all_adresses(db: Session = Depends(get_db)):
    """Récupérer toutes les adresses"""
    return AdresseService.get_all(db)

@router.get("/adresses/{adresse_id}", response_model=Adresse, tags=["Adresses"])
def get_adresse(adresse_id: int, db: Session = Depends(get_db)):
    """Récupérer une adresse par son ID"""
    adresse = AdresseService.get_by_id(db, adresse_id)
    if not adresse:
        raise HTTPException(status_code=404, detail="Adresse non trouvée")
    return adresse

@router.get("/utilisateurs/{utilisateur_id}/adresses", response_model=List[Adresse], tags=["Adresses"])
def get_adresses_utilisateur(utilisateur_id: int, db: Session = Depends(get_db)):
    """Récupérer toutes les adresses d'un utilisateur"""
    return AdresseService.get_by_utilisateur(db, utilisateur_id)

# Routes pour les produits
@router.get("/produits/", response_model=List[Produit], tags=["Produits"])
def get_all_produits(db: Session = Depends(get_db)):
    """Récupérer tous les produits"""
    return ProduitService.get_all(db)

@router.get("/produits/{produit_id}", response_model=Produit, tags=["Produits"])
def get_produit(produit_id: int, db: Session = Depends(get_db)):
    """Récupérer un produit par son ID"""
    produit = ProduitService.get_by_id(db, produit_id)
    if not produit:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return produit

@router.get("/produits/categorie/{categorie}", response_model=List[Produit], tags=["Produits"])
def get_produits_by_categorie(categorie: str, db: Session = Depends(get_db)):
    """Récupérer tous les produits d'une catégorie"""
    return ProduitService.get_by_categorie(db, categorie)

@router.get("/produits/meilleurs-ventes", response_model=List[Produit], tags=["Produits"])
def get_meilleurs_ventes(db: Session = Depends(get_db)):
    """Récupérer les produits marqués comme meilleures ventes"""
    return ProduitService.get_meilleurs_ventes(db)

@router.get("/produits/mis-en-avant", response_model=List[Produit], tags=["Produits"])
def get_produits_mis_en_avant(db: Session = Depends(get_db)):
    """Récupérer les produits mis en avant"""
    return ProduitService.get_mis_en_avant(db)

# Routes pour les commandes
@router.get("/commandes/", response_model=List[Commande], tags=["Commandes"])
def get_all_commandes(db: Session = Depends(get_db)):
    """Récupérer toutes les commandes"""
    return CommandeService.get_all(db)

@router.get("/commandes/{commande_id}", response_model=Commande, tags=["Commandes"])
def get_commande(commande_id: int, db: Session = Depends(get_db)):
    """Récupérer une commande par son ID"""
    commande = CommandeService.get_by_id(db, commande_id)
    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return commande

@router.get("/utilisateurs/{utilisateur_id}/commandes", response_model=List[Commande], tags=["Commandes"])
def get_commandes_utilisateur(utilisateur_id: int, db: Session = Depends(get_db)):
    """Récupérer toutes les commandes d'un utilisateur"""
    return CommandeService.get_by_utilisateur(db, utilisateur_id)

# Routes pour les utilisateurs
@router.get("/utilisateurs/", response_model=List[Utilisateur], tags=["Utilisateurs"])
def get_all_utilisateurs(db: Session = Depends(get_db)):
    """Récupérer tous les utilisateurs"""
    return UtilisateurService.get_all(db)

@router.get("/utilisateurs/{utilisateur_id}", response_model=Utilisateur, tags=["Utilisateurs"])
def get_utilisateur(utilisateur_id: int, db: Session = Depends(get_db)):
    """Récupérer un utilisateur par son ID"""
    utilisateur = UtilisateurService.get_by_id(db, utilisateur_id)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return utilisateur

@router.get("/utilisateurs/email/{email}", response_model=Utilisateur, tags=["Utilisateurs"])
def get_utilisateur_by_email(email: str, db: Session = Depends(get_db)):
    """Récupérer un utilisateur par son email"""
    utilisateur = UtilisateurService.get_by_email(db, email)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return utilisateur
