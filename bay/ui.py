"""Shared presentation with responsive styles and accessible native controls."""

import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Literata:wght@500;600&family=Source+Sans+3:wght@400;500;600;700&display=swap');
        html, body, [data-testid="stApp"] {
            font-family: 'Source Sans 3', sans-serif;
        }
        h1, h2, h3 {
            color: #183B3D;
        }
        h1 {
            font-family: 'Literata', serif !important;
            font-size: 2.65rem !important;
            font-weight: 500 !important;
            letter-spacing: -0.035em;
            padding-top: 0 !important;
        }
        h2 {
            font-size: 1.65rem !important;
        }
        h3 {
            font-size: 1.25rem !important;
        }
        .stMainBlockContainer {
            max-width: 1140px;
            padding-top: 2.75rem;
            padding-bottom: 3rem;
        }
        [data-testid="stSidebar"] {
            border-right: 1px solid #CEDDD8;
        }
        [data-testid="stSidebar"] button {
            min-height: 44px;
        }
        [data-baseweb="select"] > div {
            min-height: 44px;
        }
        [data-testid="stMarkdownContainer"] p {
            max-width: 74ch;
        }
        [data-baseweb="tab"] {
            min-height: 48px;
            font-size: 1rem;
        }
        .survey-eyebrow {
            color: #456763;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            margin-bottom: 0.4rem;
        }
        .survey-context {
            color: #456763;
            border-top: 1px solid #CEDDD8;
            border-bottom: 1px solid #CEDDD8;
            padding: 0.8rem 0;
            margin: 0.6rem 0 1rem;
            font-size: 0.95rem;
        }
        @media (max-width: 640px) {
            h1 { font-size: 2rem !important; }
            .stMainBlockContainer {
                padding: 3.6rem 1rem 2rem;
            }
            [data-baseweb="tab-list"] { gap: 1rem; }
            [data-testid="stSidebar"] { max-width: 88vw; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def reset_controls(start, end) -> None:
    st.session_state["measurement"] = "Dissolved oxygen"
    st.session_state["comparison"] = "Temperature"
    st.session_state["time_window"] = (start, end)
    st.session_state["show_points"] = False
