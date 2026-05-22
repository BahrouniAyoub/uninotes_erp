from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Profile
from academics.models import Inscription
from django.contrib.auth.models import User
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
    
@login_required
def tutor_students_view(request):
    if request.user.profile.role != Profile.ROLE_TUTOR:
        messages.error(request, "Accès réservé aux tuteurs.")
        return redirect("home")

    students = request.user.profile.students.all()

    return render(request, "dashboard/tutor_students.html", {
        "students": students,
    })


@login_required
def tutor_student_dashboard_view(request, student_id):
    if request.user.profile.role != Profile.ROLE_TUTOR:
        messages.error(request, "Accès réservé aux tuteurs.")
        return redirect("home")

    student = get_object_or_404(
        User,
        id=student_id,
        tutors=request.user.profile
    )

    inscription = Inscription.objects.filter(
        etudiant=student,
        annee_academique="2025-2026"
    ).prefetch_related(
        "modules_choisis__module__categories",
        "modules_choisis__notes__categorie"
    ).first()

    if not inscription:
        messages.info(request, "Cet étudiant n’a pas encore d’inscription.")
        return redirect("tutor_students")

    modules_data = []

    for module_choisi in inscription.modules_choisis.all():
        modules_data.append({
            "choix": module_choisi,
            "average": get_module_average(module_choisi),
        })

    general_average = get_general_average(inscription)

    return render(request, "dashboard/tutor_student_dashboard.html", {
        "student": student,
        "inscription": inscription,
        "modules_data": modules_data,
        "general_average": general_average,
    })