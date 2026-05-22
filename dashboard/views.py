from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.models import Profile
from academics.models import Inscription
from academics.services import (
    get_evolution_data,
    get_general_average,
    get_module_average,
)
def home(request):
    return render(request, "core/home.html")
@login_required
def student_dashboard_view(request):
    if request.user.profile.role != Profile.ROLE_STUDENT:
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect("home")

    inscription = Inscription.objects.filter(
        etudiant=request.user,
        annee_academique="2025-2026"
    ).prefetch_related(
        "modules_choisis__module__categories",
        "modules_choisis__notes__categorie"
    ).first()

    if not inscription:
        messages.info(request, "Vous devez d’abord créer votre panier.")
        return redirect("basket")

    modules_choisis = inscription.modules_choisis.all()
    
    module_data = []

    for module_choisi in modules_choisis:
        module_data.append({
            "choix": module_choisi,
            "average": get_module_average(module_choisi),
        })

    general_average = get_general_average(inscription)

    return render(request, "dashboard/student_dashboard.html", {
        "inscription": inscription,
        "modules_data": module_data,
        "general_average": general_average,
    })
    
    
@login_required
def evolution_view(request):
    if request.user.profile.role != Profile.ROLE_STUDENT:
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect("home")

    inscription = Inscription.objects.filter(
        etudiant=request.user,
        annee_academique="2025-2026"
    ).first()

    if not inscription:
        messages.error(request, "Aucune inscription trouvée.")
        return redirect("basket")

    evolution_data = get_evolution_data(inscription)

    return render(request, "dashboard/evolution.html", {
        "labels": evolution_data["labels"],
        "values": evolution_data["values"],
    })