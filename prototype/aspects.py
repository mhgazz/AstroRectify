def calculate_aspects(ra: float) -> dict[str,float]:
    """
    Calcula los aspectos astrológicos para una ascensión recta dada.

    Args:
        ra (float): La ascensión recta del cuerpo celeste en grados (0-360).

    Returns:
        list[float]: Una lista de valores de ascensión recta para los aspectos calculados.
                     Todos los valores están normalizados entre 0 y 360 grados.
    """
    aspects = {}

    # Función auxiliar para normalizar el ángulo entre 0 y 360 grados
    def normalize_angle(angle):
        #return angle % 360
        return angle

    # Aspectos principales
    aspect_degrees = {
        "conjuncion" : 0,
        "cuadratura": 90,
        "trigono": 120,
        "sextil": 60,
        "semicuadratura": 45,
        "semisextil": 30,
        "quincuncio": 150,
        "sesquicuadratura": 135,
        # Conjunción (0 grados) no se calcula explícitamente como un "aspecto" adicional
        # ya que es el propio punto de partida, pero se podría añadir si fuera necesario.
    }

    for name, degrees in aspect_degrees.items():
        if degrees != 180 and degrees != 0:  # Para aspectos que tienen +/-
            aspects[name+"+"] = round(normalize_angle(ra + degrees),2)
            aspects[name+"-"] = round(normalize_angle(ra - degrees),2)
        else:  # Oposición solo tiene un valor (RA + 180)
            aspects[name] = round(normalize_angle(ra + degrees),2)

    # Si quieres incluir la conjunción (el propio RA), puedes añadirla:
    # aspects.append(normalize_angle(ra))

    return aspects