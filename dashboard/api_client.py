import requests


API_BASE_URL = "http://127.0.0.1:8000"


def get_data(endpoint):

    response = requests.get(
        f"{API_BASE_URL}{endpoint}",
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def post_data(endpoint, payload):

    response = requests.post(
        f"{API_BASE_URL}{endpoint}",
        json=payload,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def get_donors():

    return get_data("/donors/")


def get_requests():

    return get_data("/requests/")


def get_inventory():

    return get_data("/inventory/")


def get_demand_history():

    return get_data("/demand-history/")


def get_model_info():

    return get_data("/prediction/model-info")


def predict_demand(target_month):

    return post_data(
        "/prediction/demand",
        {
            "target_month": target_month
        }
    )


def predict_shortage_risk(target_month):

    return post_data(
        "/prediction/shortage-risk",
        {
            "target_month": target_month
        }
    )


def find_matching_donors(request_id):

    return get_data(
        f"/matching/find/{request_id}"
    )