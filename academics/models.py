from django.db import models
from decimal import Decimal
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
class CatalogueModule(models.Model):
    intitule = models.CharField(max_length=150, unique=True)
    coefficient = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    description = models.TextField(blank=True, null=True)
    est_actif = models.BooleanField(default=True)
    
    class Meta:
        ordering = ["intitule"]
        
    def __str__(self):
        return f"{self.intitule} ({self.coefficient})"


class CategorieEvaluation(models.Model):
   module = models.ForeignKey(CatalogueModule, on_delete=models.CASCADE, related_name="categories")
   nom = models.CharField(max_length=100)
   poids = models.PositiveBigIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
   
   class Meta:
       unique_together = ["module", "nom"]
       ordering = ["module__intitule", "nom"]
       
   def __str__(self):
        return f"{self.module.intitule} - {self.nom} ({self.poids}%)"
    
class Inscription(models.Model):
    STATUT_CHOICES = [
        ("ouverte", "Ouverte"),
        ("verrouillee", "Verrouillée"),
    ]
    
    etudiant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="inscriptions")
    annee_academique = models.CharField(max_length=20, default="2025-2026")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="ouverte")
    data_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ["etudiant", "annee_academique"]
        ordering = ["-data_creation"]
        
    def __str__(self):
        return f"{self.etudiant.username} - {self.annee_academique} - {self.statut}"
    
    
class ModuleChoisi(models.Model):
    inscription = models.ForeignKey(Inscription, on_delete=models.CASCADE, related_name="modules_choisis")
    module = models.ForeignKey(CatalogueModule, on_delete=models.CASCADE, related_name="choix")
    date_choix = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ["inscription", "module"]
        ordering = ["module__intitule"]
        
    def __str__(self):
        return f"{self.inscription.etudiant.username} - {self.module.intitule}"
    
    
class Note(models.Model):
    module_choisi = models.ForeignKey(ModuleChoisi, on_delete=models.CASCADE, related_name="notes")
    categorie = models.ForeignKey(CategorieEvaluation, on_delete=models.PROTECT, related_name="notes")
    valeur = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('20.00'))])
    date_saisie = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ["module_choisi", "categorie"]
        ordering = ["-date_saisie"]
        
    def __str__(self):
        return f"{self.module_choisi.module.intitule} - {self.categorie.nom}: {self.valeur}"
    

