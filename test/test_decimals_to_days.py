from decimal import Decimal
ye=24.14842587507178
days = 365*(Decimal(str(ye))%1)
print(days)