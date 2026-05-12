from django.contrib import admin

from .models import (
    CatalogueModule,
    CategorieEvaluation,
    Inscription,
    ModuleChoisi,
    Note,
)


class CategorieEvaluationInline(admin.TabularInline):
    model = CategorieEvaluation
    extra = 1


@admin.register(CatalogueModule)
class CatalogueModuleAdmin(admin.ModelAdmin):
    list_display = ("intitule", "coefficient", "est_actif")
    list_filter = ("est_actif",)
    search_fields = ("intitule",)
    inlines = [CategorieEvaluationInline]


@admin.register(CategorieEvaluation)
class CategorieEvaluationAdmin(admin.ModelAdmin):
    list_display = ("nom", "module", "poids")
    list_filter = ("module",)
    search_fields = ("nom", "module__intitule")


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ("etudiant", "annee_academique", "statut", "date_creation")
    list_filter = ("statut", "annee_academique")
    search_fields = ("etudiant__username",)


@admin.register(ModuleChoisi)
class ModuleChoisiAdmin(admin.ModelAdmin):
    list_display = ("inscription", "module", "date_choix")
    list_filter = ("module",)
    search_fields = ("inscription__etudiant__username", "module__intitule")


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("module_choisi", "categorie", "valeur", "date_saisie")
    list_filter = ("categorie",)
    search_fields = (
        "module_choisi__inscription__etudiant__username",
        "module_choisi__module__intitule",
    )
    
