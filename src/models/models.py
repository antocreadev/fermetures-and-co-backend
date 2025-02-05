import enum
from datetime import datetime
from typing import List, Optional

from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, Integer,
                        String, Table, event)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy_file import FileField

from src.database import Base
from src.tasks import get_password_hash


class Gender(str, enum.Enum):
    HOMME = "HOMME"
    FEMME = "FEMME"
    AUTRE = "AUTRE"

class Categorie(str, enum.Enum):
  PORTAIL_COULISSANT = "portail-coulissant"
  PORTAIL_BATTANT = "portail-battant"
  PORTILLON = "portillon"
  ACCESSOIRE_PORTAIL = "accessoire-portail"
  PERGOLA = "pergola"
  MOTORISATION = "motorisation-portail"

class StatutCommande(str, enum.Enum):
  EN_ATTENTE = "en-attente"
  EN_COURS = "en-cours"
  EN_LIVRAISON = "en-livraison"
  LIVRE = "livre"
  ANNULE = "annule"


# Table d'association pour la relation many-to-many entre Commande et Produit
commande_produit = Table(
    "commande_produit",
    Base.metadata,
    Column("commande_id", Integer, ForeignKey("commandes.id"), primary_key=True),
    Column("produit_id", Integer, ForeignKey("produits.id"), primary_key=True),
)

# Table d'association pour la relation many-to-many entre Produit et Image
produit_image = Table(
    "produit_image",
    Base.metadata,
    Column("produit_id", Integer, ForeignKey("produits.id"), primary_key=True),
    Column("image_id", Integer, ForeignKey("images.id"), primary_key=True),
)

class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    id: Mapped[int] = mapped_column(primary_key=True)
    sexe: Mapped[Gender] = mapped_column(Enum(Gender, values_callable=lambda obj: [e.value for e in obj]))
    nom: Mapped[str] = mapped_column(String(100))
    prenom: Mapped[str] = mapped_column(String(100))
    telephone: Mapped[str] = mapped_column(String(100))
    recevoirMails: Mapped[bool] = mapped_column(Boolean, default=True)
    rgpd: Mapped[bool] = mapped_column(Boolean, default=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    mot_de_passe: Mapped[str] = mapped_column(String(255))
    date_creation: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relations
    adresses: Mapped[List["Adresse"]] = relationship(back_populates="utilisateur", cascade="all, delete-orphan")
    commandes: Mapped[List["Commande"]] = relationship(back_populates="utilisateur", cascade="all, delete-orphan")

# Événement qui s'exécute avant l'insertion d'un nouvel utilisateur
@event.listens_for(Utilisateur, 'before_insert')
def hash_password_before_insert(mapper, connection, target):
    if target.mot_de_passe:  # Vérifie si un mot de passe est défini
        target.mot_de_passe = get_password_hash(target.mot_de_passe)

# Événement qui s'exécute avant la mise à jour d'un utilisateur
@event.listens_for(Utilisateur, 'before_update')
def hash_password_before_update(mapper, connection, target):
    # Vérifie si le mot de passe a été modifié
    if target.mot_de_passe and not target.mot_de_passe.startswith('$2b$'):  # Vérifie si le mot de passe n'est pas déjà haché
        target.mot_de_passe = get_password_hash(target.mot_de_passe)

class Adresse(Base):
    __tablename__ = "adresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    prenom: Mapped[str] = mapped_column(String(100))
    adresse: Mapped[str] = mapped_column(String(255))
    complement: Mapped[str] = mapped_column(String(255))
    ville: Mapped[str] = mapped_column(String(100))
    code_postal: Mapped[str] = mapped_column(String(10))
    pays: Mapped[str] = mapped_column(String(100))
    utilisateur_id: Mapped[int] = mapped_column(ForeignKey("utilisateurs.id"))

    # Relations
    utilisateur: Mapped["Utilisateur"] = relationship(back_populates="adresses")

class Commande(Base):
    __tablename__ = "commandes"

    id: Mapped[int] = mapped_column(primary_key=True)
    date_commande: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    statut: Mapped[StatutCommande] = mapped_column(Enum(StatutCommande))
    
    utilisateur_id: Mapped[int] = mapped_column(ForeignKey("utilisateurs.id"))

    # Relations
    utilisateur: Mapped["Utilisateur"] = relationship(back_populates="commandes")
    produits: Mapped[List["Produit"]] = relationship(secondary=commande_produit, back_populates="commandes")

class Produit(Base):
    __tablename__ = "produits"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String(500))
    prix: Mapped[float]
    bois_id: Mapped[Optional[int]] = mapped_column(ForeignKey("bois.id"))
    ral_id: Mapped[Optional[int]] = mapped_column(ForeignKey("rals.id"))
    categorie: Mapped[Categorie] = mapped_column(Enum(Categorie))
    hauteur: Mapped[float]
    largeur: Mapped[float]
    mitEnAvant: Mapped[bool]
    meilleurVente: Mapped[bool]


    # Relations
    bois: Mapped[Optional["Bois"]] = relationship()
    ral: Mapped[Optional["RAL"]] = relationship()
    images: Mapped[List["Image"]] = relationship(secondary=produit_image, back_populates="produits")
    commandes: Mapped[List["Commande"]] = relationship(secondary=commande_produit, back_populates="produits")
    options: Mapped[List["Produit"]] = relationship(
        "Produit",
        secondary="produit_options",
        primaryjoin="Produit.id==produit_options.c.produit_id",
        secondaryjoin="Produit.id==produit_options.c.option_id",
        back_populates="produits_parents"
    )
    produits_parents: Mapped[List["Produit"]] = relationship(
        "Produit",
        secondary="produit_options",
        primaryjoin="Produit.id==produit_options.c.option_id",
        secondaryjoin="Produit.id==produit_options.c.produit_id",
        back_populates="options"
    )

# Table d'association pour les options de produits
produit_options = Table(
    "produit_options",
    Base.metadata,
    Column("produit_id", Integer, ForeignKey("produits.id"), primary_key=True),
    Column("option_id", Integer, ForeignKey("produits.id"), primary_key=True),
)

class Bois(Base):
    __tablename__ = "bois"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    image_id: Mapped[Optional[int]] = mapped_column(ForeignKey("images.id"))

    # Relations
    image: Mapped[Optional["Image"]] = relationship()

class RAL(Base):
    __tablename__ = "rals"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    image_id: Mapped[Optional[int]] = mapped_column(ForeignKey("images.id"))

    # Relations
    image: Mapped[Optional["Image"]] = relationship()

class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(255))
    file: Mapped[str] = mapped_column(FileField)
    
    # Relations
    produits: Mapped[List["Produit"]] = relationship(secondary=produit_image, back_populates="images") 