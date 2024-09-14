

def humanise_seconds(seconds: float) -> str:
    """Humanise the format of seconds into digestable time format"""
    if seconds < 0:
        return "negative time"
    
    seconds = round(seconds)
    if seconds == 0:
        return "0s"

    minutes = seconds // 60
    seconds = seconds % 60

    humanised_format = []
    if minutes:
        humanised_format.append(f"{minutes}m")
    if seconds:
        humanised_format.append(f"{seconds}s")
    
    return ' '.join(humanised_format)
