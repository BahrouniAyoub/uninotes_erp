from django.urls import path

from . import views

urlpatterns = [
    path("", views.student_dashboard_view, name="student_dashboard"),
    path( "evolution/",views.evolution_view,name="evolution"),
    
    path("tutor/students/", views.tutor_students_view, name="tutor_students"),
    path("tutor/students/<int:student_id>/", views.tutor_student_dashboard_view, name="tutor_student_dashboard"),
]