from utils import arc_to_date
from utils import convert_angle_decimal
from datetime import datetime, timezone, date, timedelta
arc = convert_angle_decimal(23,39,12)
naibod_key = 0.9856472
init_date = datetime(1976, 12, 26, 17, 40, 00, tzinfo=timezone.utc)
mature_dt,days_arc=arc_to_date(arc, naibod_key, init_date)
print(mature_dt,days_arc)