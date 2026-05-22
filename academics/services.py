from decimal import Decimal

from django.db.models import DecimalField, ExpressionWrapper, F, Sum


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



def get_historical_module_average(module_choisi, date_limit):
    total_categories = module_choisi.module.categories.count()

    notes_qs = module_choisi.notes.filter(
        date_saisie__lte=date_limit
    )

    if total_categories == 0 or notes_qs.count() < total_categories:
        return None

    weighted_note = ExpressionWrapper(
        F("valeur") * F("categorie__poids") / Decimal("100.0"),
        output_field=DecimalField(max_digits=6, decimal_places=2)
    )

    result = notes_qs.annotate(
        weighted_note=weighted_note
    ).aggregate(
        average=Sum("weighted_note")
    )

    return result["average"]


def get_historical_general_average(inscription, date_limit):
    total = Decimal("0.00")

    for module_choisi in inscription.modules_choisis.select_related("module"):
        module_average = get_historical_module_average(module_choisi, date_limit)

        if module_average is not None:
            total += module_average * module_choisi.module.coefficient

    return round(total / Decimal("60.0"), 2)


def get_evolution_data(inscription):
    dates = (
        inscription.modules_choisis
        .values_list("notes__date_saisie", flat=True)
        .exclude(notes__date_saisie__isnull=True)
        .order_by("notes__date_saisie")
        .distinct()
    )

    labels = []
    values = []

    for date in dates:
        labels.append(date.strftime("%d/%m/%Y %H:%M"))
        values.append(float(get_historical_general_average(inscription, date)))

    return {
        "labels": labels,
        "values": values,
    }