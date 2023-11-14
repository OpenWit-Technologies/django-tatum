def validate_required_fields(fields: dict) -> bool:
    """
    Validates that all required fields are present in the fields dictionary.
    """
    return {
        'detail': f'Field {field} is required.'
        for field in fields if fields.get(field) is None
        or fields.get(field).strip() == ''
        or fields.get(field) == []
    }
    