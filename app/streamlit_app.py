"""Streamlit workspace for house-price estimation and model analysis."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_preprocessing import load_dataset
from src.model_inference import load_latest_model, predict_property


st.set_page_config(page_title="Home Value Studio", page_icon="H", layout="wide")

st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700;800&display=swap');
      :root { --ink:#17231f; --muted:#63736b; --paper:#f2f4ed; --white:#fff; --line:#d8ded5; --acid:#d9f16d; --green:#23654d; }
      html, body, [class*="css"] { font-family:'DM Sans',sans-serif; letter-spacing:0 !important; }
      .stApp { background:var(--paper); color:var(--ink); }
      [data-testid="stHeader"] { background:rgba(242,244,237,.88); }
      [data-testid="stAppViewContainer"] > .main .block-container { max-width:1440px; padding:2.2rem 3.2rem 4rem; }
      h1,h2,h3,h4,p,span,label { letter-spacing:0 !important; }
      h1 { font-size:2.65rem !important; line-height:1.05 !important; font-weight:700 !important; color:var(--ink) !important; }
      h2 { font-size:1.3rem !important; font-weight:700 !important; color:var(--ink) !important; }
      h3 { font-size:1.05rem !important; font-weight:700 !important; color:var(--ink) !important; }
      [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p,
      [data-testid="stMarkdownContainer"] label, .stSelectbox label, .stNumberInput label,
      .stSlider label { color:#26362f !important; font-weight:600 !important; }
      [data-baseweb="select"] > div, [data-testid="stNumberInput"] input { background:#fff !important; color:#17231f !important; border-color:#c6d0c5 !important; }
      [data-testid="stNumberInput"] button { color:#26362f !important; }
      [data-testid="stForm"] { background:#fff; border:1px solid var(--line); border-radius:8px; padding:1.15rem 1.3rem .4rem; }
      [data-testid="stFormSubmitButton"] button { background:#17231f !important; color:#e1f47e !important; border:1px solid #17231f !important; border-radius:4px !important; min-height:48px; font-weight:700 !important; }
      [data-testid="stFormSubmitButton"] button:hover { background:#294237 !important; border-color:#294237 !important; }
      .stButton button { border-radius:4px; }
      [data-testid="stMetric"] { background:#fff; border:1px solid var(--line); border-radius:6px; padding:16px 18px; }
      [data-testid="stMetricLabel"] p { color:#63736b !important; font-size:.8rem !important; font-weight:600 !important; }
      [data-testid="stMetricValue"] { color:#17231f !important; font-weight:700 !important; }
      [data-testid="stTabs"] [role="tablist"] { gap:8px; border-bottom:1px solid var(--line); }
      [data-testid="stTabs"] button[role="tab"] { color:#52635a !important; font-weight:600; padding:12px 16px; }
      [data-testid="stTabs"] button[role="tab"][aria-selected="true"] { color:#17231f !important; border-bottom:3px solid #23654d; }
      [data-testid="stSidebar"] { background:#e6ebe2; }
      .masthead { display:flex; justify-content:space-between; align-items:center; gap:1rem; border-bottom:1px solid var(--line); padding-bottom:1rem; margin-bottom:2rem; }
      .brand { display:flex; align-items:center; gap:12px; color:var(--ink); font-weight:800; font-size:1.05rem; }
      .brand-mark { display:grid; place-items:center; width:38px; height:38px; background:var(--ink); color:var(--acid); border-radius:5px; font-weight:800; }
      .brand-meta { color:var(--muted); font:500 11px 'DM Mono',monospace; text-transform:uppercase; }
      .status-pill { display:inline-flex; align-items:center; gap:8px; border:1px solid #c5d2c5; border-radius:20px; padding:8px 12px; color:#365344; background:#edf2e8; font-size:12px; font-weight:600; }
      .status-dot { width:7px; height:7px; border-radius:50%; background:#47815e; }
      .kicker { color:#63736b; font:500 11px 'DM Mono',monospace; text-transform:uppercase; margin-bottom:8px; }
      .intro { color:#58685f; font-size:1.02rem; margin-top:-8px; margin-bottom:1.4rem; }
      .price-panel { min-height:220px; background:#17231f; color:#eff3e9; padding:28px; border-radius:7px; position:relative; overflow:hidden; }
      .price-panel:after { content:''; position:absolute; right:-36px; top:-56px; width:180px; height:180px; border:1px solid #536a52; border-radius:50%; box-shadow:0 0 0 22px #17231f,0 0 0 23px #536a52,0 0 0 50px #17231f,0 0 0 51px #536a52; opacity:.45; }
      .price-panel .label { color:#c0ccc0; font-size:13px; }
      .price-panel strong { display:block; position:relative; z-index:1; color:#e1f47e; font-size:clamp(2rem,4vw,3.4rem); line-height:1.15; margin:12px 0; }
      .price-panel .range { color:#d3ddd0; font-size:14px; }
      .price-panel .model-note { margin-top:22px; color:#aab9aa; font:400 11px 'DM Mono',monospace; }
      .empty-panel { display:grid; place-items:center; min-height:220px; padding:28px; background:#e7ebe3; border:1px dashed #b8c3b7; border-radius:7px; text-align:center; color:#596b60; }
      .empty-panel b { color:#26382f; font-size:1.05rem; }
      .section-label { color:#607168; font:500 11px 'DM Mono',monospace; text-transform:uppercase; }
      .insight-row { border-bottom:1px solid var(--line); padding:12px 0; }
      .fineprint { color:#68766e; font-size:12px; line-height:1.6; }
      div[data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:6px; overflow:hidden; }
      @media (max-width:800px) {
        [data-testid="stAppViewContainer"] > .main .block-container { padding:1.2rem 1rem 3rem; }
        h1 { font-size:2rem !important; }
        .masthead { align-items:flex-start; }
        .status-pill { font-size:10px; padding:6px 8px; }
        .price-panel { padding:22px; min-height:195px; }
      }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def get_market_data() -> tuple[pd.DataFrame, pd.Series]:
    return load_dataset(PROJECT_ROOT / "house_prices.csv")


try:
    _, model_report = load_latest_model()
    market_features, market_prices = get_market_data()
except (FileNotFoundError, ValueError) as error:
    st.error(str(error))
    st.stop()

market = market_features.copy()
market["Price"] = market_prices
location_options = sorted(market["Location"].astype(str).unique())
type_options = sorted(market["Property_Type"].astype(str).unique())

st.markdown(
    "<div class='masthead'><div class='brand'><span class='brand-mark'>H</span>"
    "<span>Home Value Studio<br><span class='brand-meta'>Property intelligence / India</span></span></div>"
    f"<span class='status-pill'><span class='status-dot'></span>Model online · {model_report['selected_algorithm']}</span></div>",
    unsafe_allow_html=True,
)
st.markdown('<p class="kicker">Residential valuation workspace</p>', unsafe_allow_html=True)
st.title("Know the value behind every address.")
st.markdown(
    "<p class='intro'>Explore a data-backed asking-price estimate, grounded in the property's features and local market.</p>",
    unsafe_allow_html=True,
)

median_price = float(market["Price"].median())
average_area = float(market["Area"].median())
metric_columns = st.columns(4)
for column, label, value, detail in zip(
    metric_columns,
    ("LISTINGS ANALYZED", "MEDIAN ASKING PRICE", "MEDIAN HOME SIZE", "MODEL TEST R²"),
    (f"{len(market):,}", f"₹{median_price / 1_000_000:.1f}M", f"{average_area:,.0f} sq ft", f"{model_report['selected_metrics']['r2']:.3f}"),
    ("Source dataset", "Across all locations", "Across all listings", "60 holdout properties"),
):
    column.metric(label, value)
    column.caption(detail)

st.write("")
estimate_tab, market_tab, model_tab = st.tabs(["Estimate a property", "Market overview", "Model lab"])

with estimate_tab:
    form_column, result_column = st.columns([1, 1.1], gap="large")
    with form_column:
        st.subheader("Property profile")
        st.caption("Enter the key details. Your estimate updates when you run the valuation.")
        with st.form("property_form", border=False):
            area_column, age_column = st.columns(2)
            area = area_column.number_input("Built-up area · sq ft", min_value=100, max_value=10_000, value=1_500, step=50)
            age = age_column.number_input("Property age · years", min_value=0, max_value=150, value=5, step=1)
            bed_column, bath_column = st.columns(2)
            bedrooms = bed_column.number_input("Bedrooms", min_value=1, max_value=10, value=3, step=1)
            bathrooms = bath_column.number_input("Bathrooms", min_value=1, max_value=10, value=2, step=1)
            location = st.selectbox("Location", location_options, index=location_options.index("City Center") if "City Center" in location_options else 0)
            property_type = st.selectbox("Property type", type_options)
            submitted = st.form_submit_button("Run property valuation  →", use_container_width=True)

    if submitted:
        try:
            prediction = predict_property(
                {"Area": area, "Bedrooms": bedrooms, "Bathrooms": bathrooms, "Age": age,
                 "Location": location, "Property_Type": property_type}
            )
            st.session_state["active_prediction"] = prediction
            st.session_state["active_property"] = {
                "Area": area, "Bedrooms": bedrooms, "Bathrooms": bathrooms, "Age": age,
                "Location": location, "Property_Type": property_type,
            }
            history = st.session_state.setdefault("prediction_history", [])
            history.insert(0, {**st.session_state["active_property"], **prediction})
            st.session_state["prediction_history"] = history[:20]
        except ValueError as error:
            st.error(str(error))

    with result_column:
        st.subheader("Valuation result")
        active = st.session_state.get("active_prediction")
        if active:
            st.markdown(
                f"<div class='price-panel'><span class='label'>Estimated asking price</span>"
                f"<strong>₹{active['estimated_price']:,.0f}</strong>"
                f"<span class='range'>Indicative range&nbsp;&nbsp; ₹{active['estimated_range_low']:,.0f} – ₹{active['estimated_range_high']:,.0f}</span>"
                f"<div class='model-note'>{active['algorithm'].upper()} &nbsp; / &nbsp; MODEL {active['model_version']}</div></div>",
                unsafe_allow_html=True,
            )
            property_record = st.session_state["active_property"]
            matched_market = market[
                (market["Location"] == property_record["Location"])
                & (market["Property_Type"] == property_record["Property_Type"])
            ]
            if not matched_market.empty:
                typical_price = float(matched_market["Price"].median())
                price_delta = active["estimated_price"] - typical_price
                st.write("")
                st.metric(
                    f"Compared with {property_record['Location']} {property_record['Property_Type'].lower()} median",
                    f"₹{typical_price:,.0f}",
                    f"Estimate is ₹{abs(price_delta):,.0f} {'above' if price_delta >= 0 else 'below'} this group median",
                    delta_color="off",
                )
            st.caption("The range is an empirical error band, not a guarantee or formal appraisal.")
        else:
            st.markdown(
                "<div class='empty-panel'><div><span class='section-label'>READY WHEN YOU ARE</span>"
                "<br><br><b>Your valuation will appear here.</b><br><br>"
                "Complete the property profile to see its estimate, indicative range, and local comparison.</div></div>",
                unsafe_allow_html=True,
            )

    st.divider()
    history_column, impact_column = st.columns([1.05, .95], gap="large")
    with history_column:
        history_title, clear_column = st.columns([1, .3], vertical_alignment="center")
        history_title.subheader("Recent valuations")
        history = st.session_state.get("prediction_history", [])
        if history and clear_column.button("Clear", key="clear_history"):
            st.session_state["prediction_history"] = []
            st.rerun()
        if history:
            history_frame = pd.DataFrame(history)
            st.dataframe(
                history_frame[["Location", "Property_Type", "Area", "Bedrooms", "estimated_price"]].rename(
                    columns={"Property_Type": "Type", "Area": "Sq ft", "Bedrooms": "Beds", "estimated_price": "Estimate (₹)"}
                ).style.format({"Estimate (₹)": "₹{:,.0f}", "Sq ft": "{:,.0f}"}),
                use_container_width=True,
                hide_index=True,
            )
            export = history_frame.to_csv(index=False).encode("utf-8")
            st.download_button("Download estimate history", export, "home_value_estimates.csv", "text/csv")
        else:
            st.markdown("<p class='fineprint'>Your completed valuations will be saved in this browser session.</p>", unsafe_allow_html=True)
    with impact_column:
        st.subheader("What the model pays attention to")
        importance = pd.DataFrame(model_report["feature_importance"])
        for row in importance.head(4).itertuples():
            st.markdown(
                f"<div class='insight-row'><span>{row.feature.replace('_', ' ')}</span>"
                f"<span style='float:right;color:#23654d;font-weight:700'>{row.importance_mean:.2f}</span></div>",
                unsafe_allow_html=True,
            )
        st.markdown("<p class='fineprint'>Permutation importance measures how much held-out model performance changes when a feature is shuffled. It is not a causal effect.</p>", unsafe_allow_html=True)

with market_tab:
    st.subheader("A clearer read on the local market")
    st.caption("Explore how listing prices vary across the supplied sample. Use the filters to focus the view.")
    filter_location, filter_type = st.columns(2)
    selected_location = filter_location.selectbox("Filter location", ["All locations", *location_options], key="market_location")
    selected_type = filter_type.selectbox("Filter property type", ["All types", *type_options], key="market_type")
    filtered = market.copy()
    if selected_location != "All locations":
        filtered = filtered[filtered["Location"] == selected_location]
    if selected_type != "All types":
        filtered = filtered[filtered["Property_Type"] == selected_type]
    if filtered.empty:
        st.warning("No records match these filters.")
    else:
        market_metrics = st.columns(3)
        market_metrics[0].metric("Properties in view", f"{len(filtered):,}")
        market_metrics[1].metric("Median asking price", f"₹{filtered['Price'].median():,.0f}")
        market_metrics[2].metric("Typical floor area", f"{filtered['Area'].median():,.0f} sq ft")
        chart_column, distribution_column = st.columns([1.2, .8], gap="large")
        with chart_column:
            st.markdown("#### Price and floor area")
            st.scatter_chart(filtered, x="Area", y="Price", color="Location", size="Bedrooms", height=360)
        with distribution_column:
            st.markdown("#### Median by location")
            by_location = filtered.groupby("Location")["Price"].median().sort_values(ascending=True)
            st.bar_chart(by_location, horizontal=True, height=360)
        st.markdown("#### Sample listings")
        st.dataframe(
            filtered[["Area", "Bedrooms", "Bathrooms", "Age", "Location", "Property_Type", "Price"]]
            .rename(columns={"Area": "Sq ft", "Property_Type": "Type", "Price": "Asking price (₹)"})
            .sort_values("Asking price (₹)", ascending=False)
            .head(12)
            .style.format({"Asking price (₹)": "₹{:,.0f}", "Sq ft": "{:,.0f}"}),
            use_container_width=True,
            hide_index=True,
        )

with model_tab:
    st.subheader("Model performance and interpretation")
    st.caption("Three regression approaches are compared. Cross-validation selects the final estimator; the test partition remains held out.")
    comparison = pd.DataFrame(model_report["algorithms"]).T
    st.dataframe(
        comparison[["cv_r2_mean", "cv_r2_std", "mae", "rmse", "r2", "mape"]].rename(
            columns={"cv_r2_mean": "CV R² mean", "cv_r2_std": "CV R² std", "mae": "MAE (₹)",
                     "rmse": "RMSE (₹)", "r2": "Test R²", "mape": "MAPE (%)"}
        ).style.format({"CV R² mean": "{:.3f}", "CV R² std": "{:.3f}", "MAE (₹)": "₹{:,.0f}",
                        "RMSE (₹)": "₹{:,.0f}", "Test R²": "{:.3f}", "MAPE (%)": "{:.1f}%"}),
        use_container_width=True,
    )
    interpretation_column, metrics_column = st.columns([1.15, .85], gap="large")
    with interpretation_column:
        st.markdown("#### Feature importance")
        st.bar_chart(importance.set_index("feature")["importance_mean"], horizontal=True, height=320)
        st.markdown(f"<p class='fineprint'>{model_report['interpretation_method']}. Importance can be shared across correlated inputs and is not evidence of causality.</p>", unsafe_allow_html=True)
    with metrics_column:
        st.markdown("#### Validation record")
        st.metric("Selected estimator", model_report["selected_algorithm"])
        st.metric("Training / test rows", f"{model_report['training_rows']} / {model_report['test_rows']}")
        st.metric("5-fold CV R²", f"{model_report['selected_metrics']['cv_r2_mean']:.3f} ± {model_report['selected_metrics']['cv_r2_std']:.3f}")
        st.markdown(f"<p class='fineprint'>Model version {model_report['model_version']}<br>Random seed {model_report['random_state']}<br>Split and preprocessing settings are documented in the project config.</p>", unsafe_allow_html=True)

st.divider()
st.markdown(
    "<p class='fineprint'>For learning and market exploration only. Estimates reflect the supplied sample and are not professional valuations, lending decisions, or investment advice.</p>",
    unsafe_allow_html=True,
)