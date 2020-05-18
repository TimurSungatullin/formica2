from datetime import timedelta


EVERYDAY = 1
EVERY_WEEK = 2
EVERY_MONTH = 3
EVERY_YEAR = 4
REGULARITY = (
    (EVERYDAY, 'Каждый день'),
    (EVERY_WEEK, 'Каждую неделю'),
    (EVERY_MONTH, 'Каждый месяц'),
    (EVERY_YEAR, 'Каждый год'),
)


def get_next_period(date, regularity):
    # TODO Пересмотреть этот метод
    if regularity == EVERYDAY:
        date = date + timedelta(days=1)
    elif regularity == EVERY_WEEK:
        date = date + timedelta(days=7)
    elif regularity == EVERY_MONTH:
        date = date + timedelta(days=30)
    elif regularity == EVERY_YEAR:
        date = date + timedelta(days=365)

    return date


def set_values_to_model(model, values):
    for key, value in values.items():
        if getattr(model, key, None) != value and value is not None:
            setattr(model, key, value)
    model.save()
