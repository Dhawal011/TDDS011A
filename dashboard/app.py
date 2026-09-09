import streamlit as st
import pandas as pd
import plotly.express as px

from api_client import (
    get_donors,
    get_requests,
    get_inventory,
    get_demand_history,
    get_model_info,
    predict_demand,
    predict_shortage_risk,
    find_matching_donors
)


# ---------------------------------------
# Page configuration
# ---------------------------------------

st.set_page_config(
    page_title="Blood Donor Intelligence System",
    page_icon="🩸",
    layout="wide"
)


# ---------------------------------------
# Header
# ---------------------------------------

st.title("🩸 Blood Donor Intelligence System")

st.caption(
    "ML-powered blood demand forecasting, "
    "inventory analysis and donor matching"
)


# ---------------------------------------
# Load API data
# ---------------------------------------

try:

    donors = get_donors()
    requests_data = get_requests()
    inventory = get_inventory()
    demand_history = get_demand_history()
    model_info = get_model_info()

except Exception as e:

    st.error(
        "Unable to connect to the FastAPI backend."
    )

    st.code(str(e))

    st.stop()


# ---------------------------------------
# Sidebar
# ---------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Dashboard",
        "Demand Forecast",
        "Shortage Risk",
        "Donor Matching"
    ]
)


# =======================================
# DASHBOARD
# =======================================

if page == "Dashboard":

    st.header("System Overview")

    total_donors = len(donors)

    available_donors = sum(
        1
        for donor in donors
        if donor["is_available"]
    )

    total_requests = len(requests_data)

    pending_requests = sum(
        1
        for request in requests_data
        if request["request_status"] == "PENDING"
    )

    total_inventory = sum(
        item["units_available"]
        for item in inventory
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Donors",
        total_donors
    )

    col2.metric(
        "Available Donors",
        available_donors
    )

    col3.metric(
        "Pending Requests",
        pending_requests
    )

    col4.metric(
        "Inventory Units",
        total_inventory
    )

    st.divider()

    # -----------------------------------
    # Demand trend
    # -----------------------------------

    st.subheader("Historical Blood Demand")

    demand_df = pd.DataFrame(
        demand_history
    )

    if not demand_df.empty:

        demand_df["date"] = pd.to_datetime(
            demand_df["date"]
        )

        fig = px.line(
            demand_df,
            x="date",
            y="quantity_demanded",
            markers=True,
            title="Monthly Blood Demand"
        )

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Units Demanded"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # -----------------------------------
    # Supply vs demand
    # -----------------------------------

    st.subheader("Supply vs Demand")

    if not demand_df.empty:

        supply_demand_df = demand_df[
            [
                "date",
                "quantity_demanded",
                "quantity_supplied"
            ]
        ].copy()

        supply_demand_long = supply_demand_df.melt(
            id_vars="date",
            value_vars=[
                "quantity_demanded",
                "quantity_supplied"
            ],
            var_name="Metric",
            value_name="Units"
        )

        fig2 = px.line(
            supply_demand_long,
            x="date",
            y="Units",
            color="Metric",
            markers=True,
            title="Historical Supply vs Demand"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )


# =======================================
# DEMAND FORECAST
# =======================================

elif page == "Demand Forecast":

    st.header("🤖 Blood Demand Forecast")

    st.write(
        "Predict future blood demand using "
        "the trained machine learning model."
    )

    month_names = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]

    selected_month = st.selectbox(
        "Select forecast month",
        range(1, 13),
        format_func=lambda x: month_names[x - 1]
    )

    if st.button(
        "Predict Blood Demand",
        type="primary"
    ):

        try:

            result = predict_demand(
                selected_month
            )

            st.success(
                "Demand prediction generated."
            )

            col1, col2 = st.columns(2)

            col1.metric(
                "Predicted Demand",
                f'{result["predicted_demand"]:.0f} units'
            )

            col2.metric(
                "Forecast Month",
                month_names[
                    selected_month - 1
                ]
            )

        except Exception as e:

            st.error(
                f"Prediction failed: {e}"
            )

    st.divider()

    st.subheader("Model Information")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Model",
        model_info["model_name"]
    )

    col2.metric(
        "RMSE",
        model_info["rmse"]
    )

    col3.metric(
        "MAPE",
        f'{model_info["mape"]}%'
    )

    st.write(
        f'**Training samples:** '
        f'{model_info["final_training_samples"]}'
    )

    st.write(
        f'**Evaluation samples:** '
        f'{model_info["evaluation_test_samples"]}'
    )


# =======================================
# SHORTAGE RISK
# =======================================

elif page == "Shortage Risk":

    st.header("🚨 Blood Shortage Risk")

    st.write(
        "Estimate shortage risk using predicted "
        "demand and current blood inventory."
    )

    month_names = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]

    selected_month = st.selectbox(
        "Select month",
        range(1, 13),
        format_func=lambda x: month_names[x - 1],
        key="risk_month"
    )

    if st.button(
        "Analyze Shortage Risk",
        type="primary"
    ):

        try:

            result = predict_shortage_risk(
                selected_month
            )

            st.subheader("Risk Analysis")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Predicted Demand",
                f'{result["predicted_demand"]:.0f}'
            )

            col2.metric(
                "Current Inventory",
                f'{result["current_inventory"]:.0f}'
            )

            col3.metric(
                "Supply Gap",
                f'{result["supply_gap"]:.0f}'
            )

            risk = result["risk_level"]

            if risk == "HIGH":

                st.error(
                    f"🔴 HIGH SHORTAGE RISK"
                )

            elif risk == "MEDIUM":

                st.warning(
                    f"🟠 MEDIUM SHORTAGE RISK"
                )

            else:

                st.success(
                    f"🟢 LOW SHORTAGE RISK"
                )

            st.metric(
                "Shortage Probability",
                f'{result["shortage_probability"] * 100:.1f}%'
            )

        except Exception as e:

            st.error(
                f"Risk analysis failed: {e}"
            )


# =======================================
# DONOR MATCHING
# =======================================

elif page == "Donor Matching":

    st.header("🩸 Donor Matching")

    st.write(
        "Find compatible available donors "
        "for an existing blood request."
    )

    if not requests_data:

        st.info(
            "No blood requests are currently available."
        )

    else:

        request_options = {
            (
                f'{item["id"]} — '
                f'{item["hospital_name"]} — '
                f'{item["blood_group"]}'
            ): item["id"]
            for item in requests_data
        }

        selected_request = st.selectbox(
            "Select blood request",
            list(request_options.keys())
        )

        if st.button(
            "Find Matching Donors",
            type="primary"
        ):

            request_id = request_options[
                selected_request
            ]

            try:

                result = find_matching_donors(
                    request_id
                )

                st.metric(
                    "Compatible Donors",
                    result["total_matches"]
                )

                if result["matches"]:

                    matches_df = pd.DataFrame(
                        result["matches"]
                    )

                    display_columns = [
                        "donor_id",
                        "donor_name",
                        "blood_group",
                        "city",
                        "distance_km",
                        "match_score"
                    ]

                    st.dataframe(
                        matches_df[
                            display_columns
                        ],
                        use_container_width=True,
                        hide_index=True
                    )

                else:

                    st.warning(
                        "No compatible donors found."
                    )

            except Exception as e:

                st.error(
                    f"Matching failed: {e}"
                )