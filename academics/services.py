from decimal import Decimal

from django.db.models import DecimalField, ExpressionWrapper, F, Sum
from collections import OrderedDict


def get_module_average(module_choisi):
    total_categories = module_choisi.module.categories.count()
    total_notes = module_choisi.notes.count()

    if total_categories == 0 or total_notes < total_categories:
        return None

    weighted_note = ExpressionWrapper(
        F("valeur") * F("categorie__poids") / Decimal("100.0"),
        output_field=DecimalField(max_digits=6, decimal_places=2)
    )

    result = module_choisi.notes.annotate(
        weighted_note=weighted_note
    ).aggregate(
        average=Sum("weighted_note")
    )

    return result["average"]


def get_general_average(inscription):
    total = Decimal("0.00")

    for module_choisi in inscription.modules_choisis.select_related("module"):
        module_average = get_module_average(module_choisi)

        if module_average is not None:
            total += module_average * module_choisi.module.coefficient

    return round(total / Decimal("60.0"), 2)


def get_evolution_data(inscription):
    notes = (
        inscription.modules_choisis
        .prefetch_related("notes")
    )

    evolution = OrderedDict()

    for module_choisi in notes:
        for note in module_choisi.notes.all().order_by("date_saisie"):
            date_label = note.date_saisie.strftime("%d/%m/%Y %H:%M")

            current_average = get_general_average(inscription)

            evolution[date_label] = float(current_average)

    return {
        "labels": list(evolution.keys()),
        "values": list(evolution.values()),
    }