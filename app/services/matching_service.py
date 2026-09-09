import math


# --------------------------------------------------
# RED CELL DONOR COMPATIBILITY
# --------------------------------------------------

COMPATIBLE_DONORS = {
    "O-": ["O-"],

    "O+": ["O-", "O+"],

    "B-": ["B-", "O-"],

    "B+": ["B+", "B-", "O+", "O-"],

    "A-": ["A-", "O-"],

    "A+": ["A+", "A-", "O+", "O-"],

    "AB-": ["AB-", "A-", "B-", "O-"],

    "AB+": [
        "AB+",
        "AB-",
        "A+",
        "A-",
        "B+",
        "B-",
        "O+",
        "O-"
    ]
}


def get_compatible_donor_groups(recipient_blood_group: str):

    recipient_blood_group = recipient_blood_group.upper()

    return COMPATIBLE_DONORS.get(
        recipient_blood_group,
        []
    )


# --------------------------------------------------
# DISTANCE CALCULATION
# --------------------------------------------------

def calculate_distance_km(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float
):

    if None in [lat1, lon1, lat2, lon2]:
        return None

    earth_radius_km = 6371.0

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_lat / 2) ** 2
        +
        math.cos(lat1)
        *
        math.cos(lat2)
        *
        math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return earth_radius_km * c


# --------------------------------------------------
# DISTANCE SCORE
# --------------------------------------------------

def calculate_distance_score(
    distance_km: float | None
):

    if distance_km is None:
        return 0

    if distance_km <= 2:
        return 100

    if distance_km <= 5:
        return 90

    if distance_km <= 10:
        return 75

    if distance_km <= 20:
        return 60

    if distance_km <= 50:
        return 40

    return 20


# --------------------------------------------------
# MATCH SCORE
# --------------------------------------------------

def calculate_match_score(
    distance_km: float | None,
    urgency: str
):

    distance_score = calculate_distance_score(
        distance_km
    )

    urgency = urgency.upper()

    if urgency == "CRITICAL":
        score = (
            distance_score * 0.7
            + 30
        )

    elif urgency == "HIGH":
        score = (
            distance_score * 0.8
            + 20
        )

    else:
        score = distance_score

    return round(
        min(score, 100),
        2
    )