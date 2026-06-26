from datetime import datetime, timedelta
from collections import Counter

def generate_date_heat_map(dates, window_days=5):
    """
    Detects clusters of dates in a timeline.
    
    Args:
        dates (list): List of datetime objects or strings in YYYY-MM-DD format.
        window_days (int): The range of days to consider for a cluster.
        
    Returns:
        list: A sorted list of tuples (date, intensity) representing the heat map.
    """
    if not dates:
        return []

    # Convert strings to datetime objects if necessary
    parsed_dates = []
    for d in dates:
        d = str(d).split(" ")[0]
        if isinstance(d, str):
            parsed_dates.append(datetime.strptime(d, "%Y/%m/%d").date())
        elif isinstance(d, datetime):
            parsed_dates.append(d.date())
        else:
            parsed_dates.append(d)

    parsed_dates.sort()
    
    heat_map = Counter()
    
    # For every date in the timeline, we check how many other dates 
    # fall within the window of influence.
    for target_date in parsed_dates:
        count = 0
        for other_date in parsed_dates:
            diff = abs((target_date - other_date).days)
            if diff <= window_days:
                count += 1
        heat_map[target_date] = count

    # Return sorted by date
    return sorted(heat_map.items())

if __name__ == "__main__":
    # Example usage:
    sample_dates = [
        "1976/12/26", "1976/12/27", "1976/12/25", # Cluster 1
        "1980/01/10",                             # Isolated
        "1985/05/05", "2025/11/12", "1985/05/06", # Cluster 2
        "1985/05/10", "2023/1/11", "2020/3/24",
        "1999/4/19", "1998/5/25", "2025/11/14",
        "2023/4/12", "1998/5/27", "2021/7/2",
        "1998/5/30"
    ]
    
    results = generate_date_heat_map(sample_dates, window_days=3)
    
    print("Fecha      | Intensidad (Heat)")
    print("-" * 28)
    for date, intensity in results:
        print(f"{date} | {'*' * intensity} ({intensity})")
