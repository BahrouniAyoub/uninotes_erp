from decimal import Decimal, InvalidOperation

# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from .models import Note

from accounts.models import Profile
from .models import CatalogueModule, Inscription, ModuleChoisi


def get_current_inscription(user):
    inscription, created = Inscription.objects.get_or_create(
        etudiant=user,
        annee_academique="2025-2026",
    )
    return inscription


def get_total_coefficients(inscription):
    result = inscription.modules_choisis.aggregate(
        total=Sum("module__coefficient")
    )
    return result["total"] or 0


@login_required
def basket_view(request):
    if request.user.profile.role != Profile.ROLE_STUDENT:
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect("home")

    inscription = get_current_inscription(request.user)
    total = get_total_coefficients(inscription)
    remaining = 60 - total

    selected_module_ids = inscription.modules_choisis.values_list(
        "module_id",
        flat=True
    )

    catalogue = CatalogueModule.objects.filter(
        est_actif=True
    ).exclude(
        id__in=selected_module_ids
    ).prefetch_related("categories")

    suggestions = catalogue.filter(coefficient__lte=remaining)

    return render(request, "academics/basket.html", {
        "inscription": inscription,
        "catalogue": catalogue,
        "modules_choisis": inscription.modules_choisis.select_related("module"),
        "total": total,
        "remaining": remaining,
        "suggestions": suggestions,
    })


@login_required
def add_module_view(request, module_id):
    if request.user.profile.role != Profile.ROLE_STUDENT:
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect("home")

    inscription = get_current_inscription(request.user)

    if inscription.statut == Inscription.STATUT_VERROUILLEE:
        messages.error(request, "Votre inscription est verrouillée. Aucune modification n’est possible.")
        return redirect("basket")

    module = get_object_or_404(CatalogueModule, id=module_id, est_actif=True)

    total = get_total_coefficients(inscription)
    new_total = total + module.coefficient

    if new_total > 60:
        messages.error(
            request,
            f"Impossible d’ajouter le module {module.intitule} "
            f"(coefficient : {module.coefficient}). "
            f"Votre total actuel est de {total}. "
            f"L’ajout porterait le total à {new_total}, ce qui dépasse la limite de 60."
        )
        return redirect("basket")

    ModuleChoisi.objects.create(
        inscription=inscription,
        module=module
    )

    if new_total == 60:
        inscription.statut = Inscription.STATUT_VERROUILLEE
        inscription.save()
        messages.success(
            request,
            "Module ajouté. Votre inscription est maintenant verrouillée à 60 points."
        )
    else:
        messages.success(request, "Module ajouté au panier.")

    return redirect("basket")


@login_required
def remove_module_view(request, module_choisi_id):
    if request.user.profile.role != Profile.ROLE_STUDENT:
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect("home")

    inscription = get_current_inscription(request.user)

    if inscription.statut == Inscription.STATUT_VERROUILLEE:
        messages.error(request, "Votre inscription est verrouillée. Aucune modification n’est possible.")
        return redirect("basket")

    module_choisi = get_object_or_404(
        ModuleChoisi,
        id=module_choisi_id,
        inscription=inscription
    )
    module_choisi.delete()

    messages.success(request, "Module retiré du panier.")
    return redirect("basket")



@login_required
def manage_notes_view(request, module_choisi_id):
    if request.user.profile.role != Profile.ROLE_TUTOR:
        messages.error(request, "Accès réservé aux tuteurs.")
        return redirect("home")

    module_choisi = get_object_or_404(
        ModuleChoisi,
        id=module_choisi_id,
        inscription__etudiant__in=request.user.profile.students.all()
    )

    inscription = module_choisi.inscription
    student = inscription.etudiant

    if inscription.statut != Inscription.STATUT_VERROUILLEE:
        messages.error(
            request,
            "Les notes ne peuvent être saisies qu’après verrouillage de l’inscription."
        )
        return redirect("tutor_student_dashboard", student_id=student.id)

    categories = module_choisi.module.categories.all()

    if request.method == "POST":
        submitted_notes = []

        for categorie in categories:
            valeur = request.POST.get(f"categorie_{categorie.id}")

            if valeur:
                try:
                    note_value = Decimal(valeur)
                except InvalidOperation:
                    messages.error(request, "Chaque note doit être une valeur numérique.")
                    return redirect("manage_notes", module_choisi_id=module_choisi.id)

                if note_value < Decimal("0") or note_value > Decimal("20"):
                    messages.error(request, "Chaque note doit être comprise entre 0 et 20.")
                    return redirect("manage_notes", module_choisi_id=module_choisi.id)

                submitted_notes.append((categorie, note_value))

        for categorie, note_value in submitted_notes:
            Note.objects.update_or_create(
                module_choisi=module_choisi,
                categorie=categorie,
                defaults={"valeur": note_value}
            )

        messages.success(request, "Notes enregistrées avec succès.")
        return redirect("tutor_student_dashboard", student_id=student.id)

    existing_notes = {
        note.categorie_id: note
        for note in module_choisi.notes.all()
    }

    return render(request, "academics/manage_notes.html", {
        "module_choisi": module_choisi,
        "categories": categories,
        "existing_notes": existing_notes,
    })
