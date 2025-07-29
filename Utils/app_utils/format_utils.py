"""Utility formatting helpers."""

def human_readable_size(value: str | int, *, kilobytes: bool = True) -> str:
    """Convert a size value to a human-friendly string.

    Args:
        value: Numeric size or string representing the size.
        kilobytes: If True, treat the number as kilobytes; otherwise bytes.

    Returns:
        str: Formatted size (e.g., ``10.5 MB``).
    """
    try:
        num = float(str(value).strip())
    except (ValueError, TypeError):
        return str(value)

    if kilobytes:
        num *= 1024  # convert to bytes

    step = 1024.0
    units = ["B", "KB", "MB", "GB", "TB"]
    unit = 0
    while num >= step and unit < len(units) - 1:
        num /= step
        unit += 1
    return f"{num:.1f} {units[unit]}"

