"""
This module is for formatting date
"""
from datetime import datetime

def format_date(date: str) -> str:
    """format date to render like this: 03 Nov 2023"""
    if date:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        return date_obj.strftime("%d %b %Y")
    return "no date was provided"
