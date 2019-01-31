AREAS = ["code", "description", "price_unit", "price_pack"]


def validate_create(product):
    for area in AREAS:
        if area not in product:
            return False, "missing {} in request".format(area)
    return True, "ok"