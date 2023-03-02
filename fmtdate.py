from datetime import datetime

def formatDate(date: str) -> str:
    if date:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        return date_obj.strftime("%d %b %Y")
    return "no date was provided"