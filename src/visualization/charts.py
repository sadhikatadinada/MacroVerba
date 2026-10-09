import plotly.express as px
import pandas as pd

def plot_boe_2021_2023_trajectory(stance_df: pd.DataFrame):
    """
    Generates an interactive chronological time-series of the BoE's 
    communication stance during the 2021-2023 inflation shock.
    """
    boe_df = stance_df[stance_df['Institution'] == 'BoE'].copy()
    
    if boe_df.empty:
        return None

    boe_df['Date_Str'] = boe_df['Title'].str.replace("BoE Monetary Policy Summary - ", "", regex=False)
    boe_df['Date'] = pd.to_datetime(boe_df['Date_Str'], format="%B %Y", errors='coerce')
    boe_df = boe_df.dropna(subset=['Date']).sort_values('Date')

    fig = px.bar(
        boe_df, 
        x='Date', 
        y='Net_Stance_Score',
        title='Bank of England: Communication Stance During 2021-23 Inflation Shock',
        labels={'Net_Stance_Score': 'Net Hawkish Score (per 1,000 words)', 'Date': 'MPC Meeting Date'},
        color='Net_Stance_Score',
        color_continuous_scale=['#2166ac', '#d1e5f0', '#fddbc7', '#b2182b'],
        color_continuous_midpoint=0,
        hover_data=['Title']
    )
    
    fig.update_layout(xaxis_tickformat="%b %Y", showlegend=False, title_font=dict(size=14))
    return fig

def plot_cross_institution_comparison(stance_df: pd.DataFrame):
    """
    Generates an interactive cross-institutional box plot to compare 
    the variance and baseline tone of central bank communications.
    """
    clean_df = stance_df[stance_df['Net_Stance_Score'].between(-20, 20)].copy()
    
    fig = px.box(
        clean_df, 
        x='Institution', 
        y='Net_Stance_Score',
        color='Institution',
        title='Comparative Rhetorical Stance Distribution (Filtered Corpus)',
        labels={'Net_Stance_Score': 'Net Hawkish Score', 'Institution': 'Central Bank'},
        points="all",
        hover_data=['Title']
    )
    
    fig.add_hline(y=0, line_dash="dash", line_color="black", annotation_text="Neutral Stance")
    fig.update_layout(title_font=dict(size=14))
    return fig

def get_communication_narrative_table() -> pd.DataFrame:
    """
    Returns a standardized comparative table of central bank communication,
    primary policy concerns, and policy decisions during the 2021-2023 shock.
    """
    data = [
        {
            "Central Bank": "Bank of England (BoE)",
            "Key Shock Phase": "December 2021 (Early Liftoff)",
            "Primary Rhetorical Concern": "Labor market tightness, emerging services inflation, and prospective energy price pass-through.",
            "Policy Decision": "+15 bps (Bank Rate to 0.25%)",
            "Key Excerpt / Stance": "MPC judged that monetary policy should tighten modestly to return CPI to target.",
            "MacroVerba Stance": "+1.38"
        },
        {
            "Central Bank": "Bank of England (BoE)",
            "Key Shock Phase": "November 2023 (Persistent Squeeze)",
            "Primary Rhetorical Concern": "Persistence in domestic wage settlements and services inflation; rejecting early rate cut speculation.",
            "Policy Decision": "Hold at 5.25% (Restrictive plateau)",
            "Key Excerpt / Stance": "Policy is likely to need to be restrictive for an extended period of time to squeeze out inflation.",
            "MacroVerba Stance": "+11.97"
        },
        {
            "Central Bank": "US Federal Reserve",
            "Key Shock Phase": "March–June 2022 (The Transitory Pivot)",
            "Primary Rhetorical Concern": "Demand-supply imbalances, unanchoring risks in market expectations, and broadening price pressures across goods and services.",
            "Policy Decision": "+25 bps in March, accelerated to +75 bps in June",
            "Key Excerpt / Stance": "The Committee is strongly committed to returning inflation to its 2 percent objective.",
            "MacroVerba Stance": "Aggressive Hawkish Pivot"
        },
        {
            "Central Bank": "US Federal Reserve",
            "Key Shock Phase": "May 2023 (Terminal Rate Convergence)",
            "Primary Rhetorical Concern": "Cumulative policy lag, tighter credit conditions from banking stress vs. stubborn core services inflation.",
            "Policy Decision": "+25 bps (Target range 5.00%–5.25%)",
            "Key Excerpt / Stance": "Tighter credit conditions are likely to weigh on economic activity; inflation remains elevated.",
            "MacroVerba Stance": "Restrictive Vigilance"
        },
        {
            "Central Bank": "Reserve Bank of India (RBI)",
            "Key Shock Phase": "May 2022 (Off-Cycle Action)",
            "Primary Rhetorical Concern": "War-induced global commodity spillovers, edible oil and fertilizer supply shocks, second-round manufacturing input pass-through.",
            "Policy Decision": "+40 bps (Off-cycle Repo Rate hike to 4.40%)",
            "Key Excerpt / Stance": "Sustained high inflation inevitably unhinges inflation expectations... requiring calibrated withdrawal of accommodation.",
            "MacroVerba Stance": "Decisive Hawkish Shift"
        },
        {
            "Central Bank": "Reserve Bank of India (RBI)",
            "Key Shock Phase": "February 2023 (Target Anchoring)",
            "Primary Rhetorical Concern": "Core CPI persistence (excluding food and fuel) and the need to firmly break inflation inertia toward 4.0%.",
            "Policy Decision": "+25 bps (Repo Rate to 6.50%)",
            "Key Excerpt / Stance": "Monetary policy must remain relentlessly focused on aligning inflation with the target while supporting growth.",
            "MacroVerba Stance": "Target-Anchored Neutral"
        }
    ]
    return pd.DataFrame(data)

def plot_inflation_shock(macro_df: pd.DataFrame):
    """Generates a line chart of headline CPI across the three economies."""
    fig = px.line(
        macro_df, 
        x='Date', 
        y='Inflation_YoY', 
        color='Country',
        title='1. The Common Shock: Headline CPI Inflation (2020–2024)',
        labels={'Inflation_YoY': 'Headline CPI (YoY %)', 'Country': 'Economy'}
    )

    fig.add_hline(y=2, line_dash="dash", line_color="gray", annotation_text="Fed/BoE 2% Target")
    fig.add_hline(y=4, line_dash="dash", line_color="gray", annotation_text="RBI 4% Target")
    fig.update_layout(title_font=dict(size=14))
    return fig

def plot_nominal_rates(macro_df: pd.DataFrame):
    """Generates a line chart of nominal policy rates."""
    fig = px.line(
        macro_df, 
        x='Date', 
        y='Policy_Rate', 
        color='Institution',
        title='2. Divergent Responses: Nominal Policy Rates',
        labels={'Policy_Rate': 'Nominal Policy Rate (%)', 'Institution': 'Central Bank'}
    )
    fig.update_layout(title_font=dict(size=14))
    return fig

def plot_real_rates(macro_df: pd.DataFrame):
    """Generates a line chart of ex-post real policy rates."""
    fig = px.line(
        macro_df, 
        x='Date', 
        y='Real_Rate', 
        color='Institution',
        title='3. The Real Policy Stance: Ex-Post Real Rates',
        labels={'Real_Rate': 'Real Rate (Nominal - Inflation %)', 'Institution': 'Central Bank'}
    )
    fig.add_hline(y=0, line_dash="solid", line_color="black", annotation_text="Zero Real Rate")
    fig.update_layout(title_font=dict(size=14))
    return fig