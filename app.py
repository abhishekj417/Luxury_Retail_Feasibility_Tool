import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Luxury Retail Store Feasibility Study",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f1f1f;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #f0f0f0 0%, #ffffff 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        color: #2c3e50;
        border-bottom: 3px solid #3498db;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .subsection-header {
        font-size: 1.3rem;
        color: #34495e;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
        font-weight: 600;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #3498db;
        margin: 1rem 0;
    }
    .feasibility-green {
        background-color: #d4edda;
        color: #155724;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .feasibility-amber {
        background-color: #fff3cd;
        color: #856404;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .feasibility-red {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #dc3545;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">💎 Luxury Retail Store Feasibility Study Tool</div>', unsafe_allow_html=True)
st.markdown("### Comprehensive Financial Analysis for Watches & Jewelry Retail")

# Initialize session state
if 'calculated' not in st.session_state:
    st.session_state.calculated = False

# Create tabs for the 4 sections
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Store Setup Inputs", 
    "📊 Financial Assumptions", 
    "💰 Detailed P&L", 
    "🎯 Executive Summary"
])

# =============================================================================
# SECTION 1: STORE SETUP INPUTS
# =============================================================================
with tab1:
    st.markdown('<div class="section-header">Store Setup & Configuration</div>', unsafe_allow_html=True)

    # Location & Space Parameters
    st.markdown('<div class="subsection-header">📍 Location & Space Parameters</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        store_name = st.text_input("Store Name/Location", "Dubai Mall - Luxury Wing")
        city = st.selectbox("City", [
            "Dubai", "Abu Dhabi", "Sharjah", "Riyadh", "Jeddah", 
            "Doha", "Kuwait City", "Muscat", "Manama", "Other"
        ])

    with col2:
        location_type = st.selectbox("Location Type", [
            "Premium Mall", "Street Retail", "Hotel Arcade", 
            "Airport", "Standalone Boutique"
        ])
        zone_class = st.selectbox("Zone Classification", [
            "Super Prime (A+)", "Prime (A)", "Secondary (B)", "Tertiary (C)"
        ])

    with col3:
        retail_area_sqft = st.number_input("Retail Area (sq ft)", 
            min_value=100, value=1500, step=50)
        storage_area_sqft = st.number_input("Storage/Back Office Area (sq ft)", 
            min_value=50, value=300, step=50)

    total_area = retail_area_sqft + storage_area_sqft
    st.info(f"**Total Area: {total_area:,.0f} sq ft** ({total_area * 0.0929:.1f} sq m)")

    col1, col2, col3 = st.columns(3)

    with col1:
        base_rent_per_sqft = st.number_input("Base Rent per sq ft per Month (AED)", 
            min_value=10.0, value=150.0, step=10.0)
        monthly_base_rent = total_area * base_rent_per_sqft
        st.success(f"**Monthly Base Rent: AED {monthly_base_rent:,.0f}**")

    with col2:
        security_deposit_months = st.number_input("Security Deposit (Months of Rent)", 
            min_value=1, value=3, step=1)
        security_deposit = monthly_base_rent * security_deposit_months
        st.success(f"**Security Deposit: AED {security_deposit:,.0f}**")

    with col3:
        annual_rent_escalation = st.slider("Annual Rent Escalation (%)", 
            min_value=0.0, max_value=10.0, value=3.0, step=0.5)

    # Capital Expenditure
    st.markdown("---")
    st.markdown('<div class="subsection-header">🏗️ Capital Expenditure</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        fitout_cost_per_sqft = st.number_input("Fit-out Cost per sq ft (AED)", 
            min_value=100.0, value=800.0, step=50.0)
        total_fitout = retail_area_sqft * fitout_cost_per_sqft
        st.info(f"**Total: AED {total_fitout:,.0f}**")

    with col2:
        furniture_fixtures = st.number_input("Furniture & Fixtures (AED)", 
            min_value=0, value=300000, step=10000)

    with col3:
        pos_system = st.number_input("POS & IT Systems (AED)", 
            min_value=0, value=100000, step=5000)

    with col4:
        security_system = st.number_input("Security Systems (AED)", 
            min_value=0, value=150000, step=10000)

    col1, col2, col3 = st.columns(3)

    with col1:
        signage_branding = st.number_input("Signage & Branding (AED)", 
            min_value=0, value=80000, step=5000)

    with col2:
        initial_renovation = st.number_input("Initial Renovation Costs (AED)", 
            min_value=0, value=100000, step=10000)

    with col3:
        other_capex = st.number_input("Other Pre-Opening Costs (AED)", 
            min_value=0, value=50000, step=5000)

    total_capex = (total_fitout + furniture_fixtures + pos_system + 
                   security_system + signage_branding + initial_renovation + other_capex)

    st.metric("**Total Capital Expenditure**", f"AED {total_capex:,.0f}")

    # Product Mix & Inventory
    st.markdown("---")
    st.markdown('<div class="subsection-header">🛍️ Product Mix & Inventory Planning</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### ⌚ Watches")
        watch_mix_pct = st.slider("Watches % of Revenue", 0, 100, 60, 5)
        watch_avg_price = st.number_input("Avg. Watch Retail Price (AED)", 
            min_value=1000, value=25000, step=1000)
        watch_gross_margin = st.slider("Watch Gross Margin %", 0, 100, 35, 1)
        watch_initial_units = st.number_input("Initial Watch Inventory (Units)", 
            min_value=0, value=100, step=5)
        watch_turnover_days = st.number_input("Watch Inventory Turnover (Days)", 
            min_value=30, value=180, step=10)
        watch_shrinkage = st.slider("Watch Shrinkage/Loss %", 0.0, 5.0, 0.5, 0.1)

    with col2:
        st.markdown("#### 💍 Jewelry")
        jewelry_mix_pct = st.slider("Jewelry % of Revenue", 0, 100, 30, 5)
        jewelry_avg_price = st.number_input("Avg. Jewelry Retail Price (AED)", 
            min_value=1000, value=15000, step=1000)
        jewelry_gross_margin = st.slider("Jewelry Gross Margin %", 0, 100, 40, 1)
        jewelry_initial_units = st.number_input("Initial Jewelry Inventory (Units)", 
            min_value=0, value=150, step=5)
        jewelry_turnover_days = st.number_input("Jewelry Inventory Turnover (Days)", 
            min_value=30, value=120, step=10)
        jewelry_shrinkage = st.slider("Jewelry Shrinkage/Loss %", 0.0, 5.0, 0.3, 0.1)

    with col3:
        st.markdown("#### 👜 Accessories")
        accessories_mix_pct = 100 - watch_mix_pct - jewelry_mix_pct
        st.info(f"**Accessories: {accessories_mix_pct}%**")
        accessories_avg_price = st.number_input("Avg. Accessory Retail Price (AED)", 
            min_value=100, value=2500, step=100)
        accessories_gross_margin = st.slider("Accessories Gross Margin %", 0, 100, 50, 1)
        accessories_initial_units = st.number_input("Initial Accessories Inventory (Units)", 
            min_value=0, value=200, step=10)
        accessories_turnover_days = st.number_input("Accessories Inventory Turnover (Days)", 
            min_value=30, value=90, step=10)
        accessories_shrinkage = st.slider("Accessories Shrinkage/Loss %", 0.0, 5.0, 0.2, 0.1)

    # Calculate initial inventory investment
    watch_initial_cost = watch_initial_units * watch_avg_price * (1 - watch_gross_margin/100)
    jewelry_initial_cost = jewelry_initial_units * jewelry_avg_price * (1 - jewelry_gross_margin/100)
    accessories_initial_cost = accessories_initial_units * accessories_avg_price * (1 - accessories_gross_margin/100)
    total_initial_inventory = watch_initial_cost + jewelry_initial_cost + accessories_initial_cost

    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Watch Inventory", f"AED {watch_initial_cost:,.0f}")
    col2.metric("Jewelry Inventory", f"AED {jewelry_initial_cost:,.0f}")
    col3.metric("Accessories Inventory", f"AED {accessories_initial_cost:,.0f}")
    col4.metric("**Total Inventory**", f"AED {total_initial_inventory:,.0f}")

    # Supply Chain Parameters
    st.markdown("---")
    st.markdown('<div class="subsection-header">🚚 Supply Chain Parameters</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        supplier_payment_terms = st.number_input("Supplier Payment Terms (Days)", 
            min_value=0, value=30, step=5)

    with col2:
        landed_cost_pct = st.slider("Landed Cost % (Duties, Shipping, Insurance)", 
            0.0, 15.0, 3.0, 0.5)

    with col3:
        forex_hedging_cost = st.slider("Forex Hedging Cost (% of imports)", 
            0.0, 3.0, 0.5, 0.1)

    # Operational Timeline
    st.markdown("---")
    st.markdown('<div class="subsection-header">⏱️ Operational Timeline</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        lease_to_opening_months = st.number_input("Lease Signing to Opening (Months)", 
            min_value=1, value=4, step=1)

    with col2:
        preopening_expense_months = st.number_input("Pre-Opening Expense Period (Months)", 
            min_value=1, value=3, step=1)

    with col3:
        rampup_months = st.number_input("Ramp-up to Stabilization (Months)", 
            min_value=1, value=6, step=1)

    with col4:
        projection_years = st.number_input("Financial Projection Period (Years)", 
            min_value=3, value=5, step=1)

    # Summary box
    st.markdown("---")
    st.success(f"""
    **Initial Investment Summary:**
    - Capital Expenditure: AED {total_capex:,.0f}
    - Security Deposit: AED {security_deposit:,.0f}
    - Initial Inventory: AED {total_initial_inventory:,.0f}
    - **TOTAL INITIAL INVESTMENT: AED {total_capex + security_deposit + total_initial_inventory:,.0f}**
    """)

# =============================================================================
# SECTION 2: FINANCIAL ASSUMPTIONS
# =============================================================================
with tab2:
    st.markdown('<div class="section-header">Financial Assumptions</div>', unsafe_allow_html=True)

    # Revenue Assumptions
    st.markdown('<div class="subsection-header">💰 Revenue Assumptions</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Daily Footfall Projections**")
        year1_daily_footfall = st.number_input("Year 1 Daily Footfall (Stabilized)", 
            min_value=10, value=200, step=10)
        year2_footfall_growth = st.slider("Year 2 Footfall Growth %", 0, 50, 10, 1)
        year3_footfall_growth = st.slider("Year 3 Footfall Growth %", 0, 50, 8, 1)
        year4plus_footfall_growth = st.slider("Year 4+ Footfall Growth %", 0, 50, 5, 1)

    with col2:
        st.markdown("**Conversion & Transaction**")
        conversion_rate = st.slider("Conversion Rate (%)", 0.5, 20.0, 3.0, 0.5)

        st.markdown("**Average Transaction Value by Category:**")
        watch_avg_txn = st.number_input("Watch Avg Transaction (AED)", 
            min_value=1000, value=28000, step=1000)
        jewelry_avg_txn = st.number_input("Jewelry Avg Transaction (AED)", 
            min_value=1000, value=18000, step=1000)
        accessories_avg_txn = st.number_input("Accessories Avg Transaction (AED)", 
            min_value=100, value=3500, step=100)

    # Calculate blended average transaction value
    blended_avg_txn = (watch_avg_txn * watch_mix_pct/100 + 
                       jewelry_avg_txn * jewelry_mix_pct/100 + 
                       accessories_avg_txn * accessories_mix_pct/100)

    st.info(f"**Blended Average Transaction Value: AED {blended_avg_txn:,.0f}**")

    # Ramp-up Profile
    st.markdown("---")
    st.markdown("**📈 Ramp-up Profile (Revenue as % of Stabilized)**")
    st.caption("Define monthly ramp-up percentages during the stabilization period")

    rampup_profile = []
    cols = st.columns(6)
    for i in range(rampup_months):
        with cols[i % 6]:
            pct = st.slider(f"Month {i+1}", 10, 100, min(20 + i*15, 100), 5, key=f"rampup_{i}")
            rampup_profile.append(pct)

    # Peak vs Non-Peak Revenue
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Peak vs Non-Peak Revenue Patterns**")
        peak_days_per_month = st.slider("Peak Days per Month", 5, 20, 10, 1)
        peak_revenue_multiplier = st.slider("Peak Day Revenue Multiplier", 1.0, 3.0, 1.8, 0.1)

    with col2:
        st.markdown("**Seasonal Variation Factors**")
        q1_seasonal = st.slider("Q1 Seasonality Factor", 0.7, 1.3, 0.9, 0.05)
        q2_seasonal = st.slider("Q2 Seasonality Factor", 0.7, 1.3, 0.95, 0.05)
        q3_seasonal = st.slider("Q3 Seasonality Factor", 0.7, 1.3, 1.05, 0.05)
        q4_seasonal = st.slider("Q4 Seasonality Factor", 0.7, 1.3, 1.2, 0.05)

    # Payment Method Mix
    st.markdown("---")
    st.markdown("**💳 Payment Method Mix**")
    col1, col2, col3 = st.columns(3)

    with col1:
        cash_payment_pct = st.slider("Cash Payment %", 0, 100, 15, 5)

    with col2:
        card_payment_pct = st.slider("Card Payment %", 0, 100, 70, 5)

    with col3:
        installment_payment_pct = 100 - cash_payment_pct - card_payment_pct
        st.info(f"**Installment: {installment_payment_pct}%**")

    # Year-over-Year Growth Rates
    st.markdown("---")
    st.markdown("**📊 Year-over-Year Revenue Growth Rates**")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        year2_revenue_growth = st.slider("Year 2 Growth %", 0, 50, 15, 1)
    with col2:
        year3_revenue_growth = st.slider("Year 3 Growth %", 0, 50, 12, 1)
    with col3:
        year4_revenue_growth = st.slider("Year 4 Growth %", 0, 50, 10, 1)
    with col4:
        year5_revenue_growth = st.slider("Year 5+ Growth %", 0, 50, 8, 1)

    # Cost Assumptions
    st.markdown("---")
    st.markdown('<div class="subsection-header">💵 Cost Assumptions</div>', unsafe_allow_html=True)

    # Note: Gross margins already captured in Section 1
    st.info(f"""
    **Gross Margins (from Section 1):**
    - Watches: {watch_gross_margin}%
    - Jewelry: {jewelry_gross_margin}%
    - Accessories: {accessories_gross_margin}%
    """)

    # Staffing Costs
    st.markdown("**👥 Staffing Costs**")

    col1, col2 = st.columns(2)

    with col1:
        store_manager_salary = st.number_input("Store Manager Monthly Salary (AED)", 
            min_value=0, value=15000, step=1000)
        store_manager_count = st.number_input("Store Manager Count", min_value=0, value=1, step=1)

        sales_staff_salary = st.number_input("Sales Staff Monthly Salary (AED)", 
            min_value=0, value=6000, step=500)
        sales_staff_count = st.number_input("Sales Staff Count", min_value=1, value=4, step=1)

        cashier_salary = st.number_input("Cashier Monthly Salary (AED)", 
            min_value=0, value=4000, step=500)
        cashier_count = st.number_input("Cashier Count", min_value=0, value=2, step=1)

    with col2:
        security_salary = st.number_input("Security Monthly Salary (AED)", 
            min_value=0, value=3500, step=500)
        security_count = st.number_input("Security Staff Count", min_value=0, value=2, step=1)

        annual_salary_increase = st.slider("Annual Salary Increase %", 0.0, 10.0, 3.0, 0.5)
        staff_benefits_pct = st.slider("Staff Benefits & Insurance (% of Salary)", 
            5.0, 30.0, 15.0, 1.0)

    total_monthly_salaries = (store_manager_salary * store_manager_count +
                             sales_staff_salary * sales_staff_count + 
                             cashier_salary * cashier_count + 
                             security_salary * security_count)

    total_staff_cost = total_monthly_salaries * (1 + staff_benefits_pct/100)

    st.success(f"**Total Monthly Staff Cost: AED {total_staff_cost:,.0f}** (Base: AED {total_monthly_salaries:,.0f} + Benefits)")

    # Other Operating Expenses
    st.markdown("---")
    st.markdown("**🏢 Other Operating Expenses**")

    col1, col2, col3 = st.columns(3)

    with col1:
        utilities_per_sqft = st.number_input("Utilities per sq ft/Month (AED)", 
            min_value=1.0, value=15.0, step=1.0)
        marketing_pct_revenue = st.slider("Marketing (% of Revenue)", 1.0, 10.0, 3.0, 0.5)
        marketing_fixed_launch = st.number_input("Fixed Launch Marketing (AED)", 
            min_value=0, value=150000, step=10000)

    with col2:
        insurance_annual = st.number_input("Annual Insurance (AED)", 
            min_value=0, value=80000, step=5000)
        maintenance_annual = st.number_input("Repairs & Maintenance Annual (AED)", 
            min_value=0, value=50000, step=5000)
        professional_fees_annual = st.number_input("Professional Fees Annual (AED)", 
            min_value=0, value=60000, step=5000)

    with col3:
        pos_subscription_monthly = st.number_input("POS/IT Subscriptions Monthly (AED)", 
            min_value=0, value=5000, step=500)
        security_services_monthly = st.number_input("Security Services Monthly (AED)", 
            min_value=0, value=8000, step=500)
        consumables_monthly = st.number_input("Consumables & Supplies Monthly (AED)", 
            min_value=0, value=3000, step=500)

    # Payment Processing & Loyalty
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        credit_card_fee_pct = st.slider("Credit Card Processing Fee %", 1.0, 4.0, 2.5, 0.1)
        installment_fee_pct = st.slider("Installment Processing Fee %", 1.0, 6.0, 3.5, 0.1)

    with col2:
        loyalty_program_pct = st.slider("Loyalty Program Costs (% of Sales)", 0.0, 5.0, 1.5, 0.1)

    # Working Capital Assumptions
    st.markdown("---")
    st.markdown('<div class="subsection-header">💼 Working Capital Assumptions</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        receivables_days = st.number_input("Receivables Days (B2B)", 
            min_value=0, value=0, step=5)

    with col2:
        payables_days = st.number_input("Payables Days to Suppliers", 
            min_value=0, value=30, step=5)

    with col3:
        min_cash_balance = st.number_input("Minimum Cash Balance (AED)", 
            min_value=0, value=200000, step=10000)

    # Financing Assumptions
    st.markdown("---")
    st.markdown('<div class="subsection-header">🏦 Financing Assumptions</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        equity_contribution = st.number_input("Equity Contribution (AED)", 
            min_value=0, value=2000000, step=100000)
        debt_amount = st.number_input("Debt/Loan Amount (AED)", 
            min_value=0, value=1500000, step=100000)

        total_funding = equity_contribution + debt_amount
        st.info(f"**Total Funding Available: AED {total_funding:,.0f}**")

    with col2:
        interest_rate = st.slider("Annual Interest Rate %", 0.0, 15.0, 6.0, 0.5)
        loan_tenure_years = st.number_input("Loan Tenure (Years)", min_value=1, value=5, step=1)
        moratorium_months = st.number_input("Principal Moratorium (Months)", 
            min_value=0, value=6, step=1)

    col1, col2 = st.columns(2)

    with col1:
        hurdle_rate = st.slider("Minimum Required IRR (Hurdle Rate) %", 
            10.0, 40.0, 20.0, 1.0)

    with col2:
        discount_rate = st.slider("Discount Rate for NPV %", 5.0, 25.0, 12.0, 1.0)

    # Tax & Depreciation
    st.markdown("---")
    st.markdown('<div class="subsection-header">📋 Tax & Depreciation</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        corporate_tax_rate = st.slider("Corporate Tax Rate %", 0.0, 15.0, 9.0, 0.5)

    with col2:
        depreciation_rate = st.slider("Annual Depreciation Rate %", 10.0, 33.0, 20.0, 1.0)

    with col3:
        amortization_years = st.number_input("Fit-out Amortization (Years)", 
            min_value=1, value=5, step=1)

# =============================================================================
# SECTION 3: DETAILED P&L
# =============================================================================
with tab3:
    st.markdown('<div class="section-header">Detailed Profit & Loss Projection</div>', unsafe_allow_html=True)

    if st.button("🔄 Calculate Financial Projections", type="primary", use_container_width=True):
        with st.spinner("Calculating comprehensive financial projections..."):

            # Calculate stabilized monthly revenue
            stabilized_monthly_transactions = year1_daily_footfall * (conversion_rate/100) * 30

            # Build monthly projection
            months = projection_years * 12
            monthly_data = []

            # Track cumulative values
            cumulative_cash_flow = -(total_capex + security_deposit + total_initial_inventory)

            for month in range(1, months + 1):
                year = (month - 1) // 12 + 1
                month_in_year = (month - 1) % 12 + 1
                quarter = (month_in_year - 1) // 3 + 1

                # Footfall calculation with year-over-year growth
                if year == 1:
                    daily_footfall = year1_daily_footfall
                elif year == 2:
                    daily_footfall = year1_daily_footfall * (1 + year2_footfall_growth/100)
                elif year == 3:
                    daily_footfall = year1_daily_footfall * (1 + year2_footfall_growth/100) * (1 + year3_footfall_growth/100)
                else:
                    daily_footfall = (year1_daily_footfall * 
                                     (1 + year2_footfall_growth/100) * 
                                     (1 + year3_footfall_growth/100) * 
                                     (1 + year4plus_footfall_growth/100) ** (year - 3))

                # Peak vs non-peak adjustment
                peak_days = peak_days_per_month
                nonpeak_days = 30 - peak_days
                avg_daily_revenue_base = daily_footfall * (conversion_rate/100) * blended_avg_txn

                peak_daily_revenue = avg_daily_revenue_base * peak_revenue_multiplier
                nonpeak_daily_revenue = avg_daily_revenue_base * ((30 - peak_days * peak_revenue_multiplier) / nonpeak_days)

                monthly_revenue_base = (peak_daily_revenue * peak_days + 
                                       nonpeak_daily_revenue * nonpeak_days)

                # Apply ramp-up in early months
                if month <= rampup_months:
                    monthly_revenue_base *= (rampup_profile[month-1] / 100)

                # Apply year-over-year revenue growth
                if year == 2:
                    monthly_revenue_base *= (1 + year2_revenue_growth/100)
                elif year == 3:
                    monthly_revenue_base *= ((1 + year2_revenue_growth/100) * 
                                            (1 + year3_revenue_growth/100))
                elif year == 4:
                    monthly_revenue_base *= ((1 + year2_revenue_growth/100) * 
                                            (1 + year3_revenue_growth/100) * 
                                            (1 + year4_revenue_growth/100))
                elif year >= 5:
                    monthly_revenue_base *= ((1 + year2_revenue_growth/100) * 
                                            (1 + year3_revenue_growth/100) * 
                                            (1 + year4_revenue_growth/100) * 
                                            (1 + year5_revenue_growth/100) ** (year - 4))

                # Apply seasonality
                seasonal_factors = {1: q1_seasonal, 2: q2_seasonal, 3: q3_seasonal, 4: q4_seasonal}
                revenue = monthly_revenue_base * seasonal_factors[quarter]

                # Revenue breakdown by category
                watch_revenue = revenue * (watch_mix_pct / 100)
                jewelry_revenue = revenue * (jewelry_mix_pct / 100)
                accessories_revenue = revenue * (accessories_mix_pct / 100)

                # COGS calculation with landed costs
                watch_cogs_base = watch_revenue * (1 - watch_gross_margin/100)
                watch_cogs = watch_cogs_base * (1 + landed_cost_pct/100 + forex_hedging_cost/100)

                jewelry_cogs_base = jewelry_revenue * (1 - jewelry_gross_margin/100)
                jewelry_cogs = jewelry_cogs_base * (1 + landed_cost_pct/100 + forex_hedging_cost/100)

                accessories_cogs_base = accessories_revenue * (1 - accessories_gross_margin/100)
                accessories_cogs = accessories_cogs_base * (1 + landed_cost_pct/100 + forex_hedging_cost/100)

                # Add shrinkage costs
                watch_shrinkage_cost = watch_revenue * (watch_shrinkage / 100)
                jewelry_shrinkage_cost = jewelry_revenue * (jewelry_shrinkage / 100)
                accessories_shrinkage_cost = accessories_revenue * (accessories_shrinkage / 100)

                total_cogs = (watch_cogs + jewelry_cogs + accessories_cogs + 
                             watch_shrinkage_cost + jewelry_shrinkage_cost + accessories_shrinkage_cost)

                gross_profit = revenue - total_cogs
                gross_margin_pct = (gross_profit / revenue * 100) if revenue > 0 else 0

                # Operating expenses
                # Salaries with annual increase
                year_salary_multiplier = (1 + annual_salary_increase/100) ** (year - 1)
                monthly_salaries = total_staff_cost * year_salary_multiplier

                # Rent with escalation
                year_rent_multiplier = (1 + annual_rent_escalation/100) ** (year - 1)
                monthly_rent_expense = monthly_base_rent * year_rent_multiplier

                # Other operating expenses
                utilities = total_area * utilities_per_sqft

                # Marketing: variable + fixed launch cost in month 1
                marketing_variable = revenue * (marketing_pct_revenue / 100)
                marketing_fixed = marketing_fixed_launch if month == 1 else 0
                marketing = marketing_variable + marketing_fixed

                maintenance = maintenance_annual / 12
                insurance = insurance_annual / 12
                professional_fees = professional_fees_annual / 12
                pos_subscription = pos_subscription_monthly
                security_services = security_services_monthly
                consumables = consumables_monthly

                # Payment processing fees
                credit_card_fees = revenue * (card_payment_pct/100) * (credit_card_fee_pct/100)
                installment_fees = revenue * (installment_payment_pct/100) * (installment_fee_pct/100)
                total_payment_fees = credit_card_fees + installment_fees

                # Loyalty program costs
                loyalty_costs = revenue * (loyalty_program_pct / 100)

                total_opex = (monthly_salaries + monthly_rent_expense + utilities + marketing + 
                             maintenance + insurance + professional_fees + pos_subscription + 
                             security_services + consumables + total_payment_fees + loyalty_costs)

                ebitda = gross_profit - total_opex
                ebitda_margin_pct = (ebitda / revenue * 100) if revenue > 0 else 0

                # Depreciation & Amortization
                monthly_depreciation = (furniture_fixtures + pos_system + security_system + 
                                       signage_branding + other_capex) * (depreciation_rate/100) / 12
                monthly_amortization = (total_fitout + initial_renovation) / (amortization_years * 12)
                total_da = monthly_depreciation + monthly_amortization

                ebit = ebitda - total_da
                ebit_margin_pct = (ebit / revenue * 100) if revenue > 0 else 0

                # Interest expense
                if debt_amount > 0 and month <= loan_tenure_years * 12:
                    monthly_interest = debt_amount * (interest_rate/100) / 12
                else:
                    monthly_interest = 0

                # Profit before tax
                pbt = ebit - monthly_interest

                # Tax
                tax_expense = max(0, pbt * (corporate_tax_rate/100)) if pbt > 0 else 0

                # Net profit
                net_profit = pbt - tax_expense
                net_margin_pct = (net_profit / revenue * 100) if revenue > 0 else 0

                # Cash flow from operations
                operating_cash_flow = ebitda - tax_expense

                # Principal repayment
                if debt_amount > 0 and month > moratorium_months and month <= loan_tenure_years * 12:
                    monthly_principal = debt_amount / ((loan_tenure_years * 12) - moratorium_months)
                else:
                    monthly_principal = 0

                # Free cash flow
                free_cash_flow = operating_cash_flow - monthly_principal

                # Cumulative cash flow
                cumulative_cash_flow += free_cash_flow

                # Debt service coverage ratio
                if monthly_interest + monthly_principal > 0:
                    dscr = operating_cash_flow / (monthly_interest + monthly_principal)
                else:
                    dscr = None

                monthly_data.append({
                    'Month': month,
                    'Year': year,
                    'Month_in_Year': month_in_year,
                    'Quarter': quarter,
                    'Daily_Footfall': daily_footfall,
                    'Revenue': revenue,
                    'Watch_Revenue': watch_revenue,
                    'Jewelry_Revenue': jewelry_revenue,
                    'Accessories_Revenue': accessories_revenue,
                    'COGS': total_cogs,
                    'Gross_Profit': gross_profit,
                    'Gross_Margin_%': gross_margin_pct,
                    'Salaries': monthly_salaries,
                    'Rent': monthly_rent_expense,
                    'Utilities': utilities,
                    'Marketing': marketing,
                    'Maintenance': maintenance,
                    'Insurance': insurance,
                    'Professional_Fees': professional_fees,
                    'POS_Subscription': pos_subscription,
                    'Security_Services': security_services,
                    'Consumables': consumables,
                    'Payment_Processing_Fees': total_payment_fees,
                    'Loyalty_Costs': loyalty_costs,
                    'Total_Opex': total_opex,
                    'EBITDA': ebitda,
                    'EBITDA_Margin_%': ebitda_margin_pct,
                    'Depreciation': monthly_depreciation,
                    'Amortization': monthly_amortization,
                    'Total_D&A': total_da,
                    'EBIT': ebit,
                    'EBIT_Margin_%': ebit_margin_pct,
                    'Interest_Expense': monthly_interest,
                    'PBT': pbt,
                    'Tax': tax_expense,
                    'Net_Profit': net_profit,
                    'Net_Margin_%': net_margin_pct,
                    'Operating_Cash_Flow': operating_cash_flow,
                    'Principal_Repayment': monthly_principal,
                    'Free_Cash_Flow': free_cash_flow,
                    'Cumulative_Cash_Flow': cumulative_cash_flow,
                    'DSCR': dscr
                })

            df_monthly = pd.DataFrame(monthly_data)

            # Store in session state
            st.session_state.df_monthly = df_monthly
            st.session_state.calculated = True
            st.session_state.total_investment = total_capex + security_deposit + total_initial_inventory

            st.success("✅ Financial projections calculated successfully!")

    if st.session_state.calculated:
        df = st.session_state.df_monthly

        # Year selector
        selected_year = st.selectbox("Select Year to View", 
            options=list(range(1, projection_years + 1)))

        df_year = df[df['Year'] == selected_year].copy()

        # Display options
        view_option = st.radio("View Format", ["Monthly Detail", "Annual Summary"], 
            horizontal=True)

        if view_option == "Monthly Detail":
            st.markdown(f"### Year {selected_year} - Monthly P&L Statement")

            # Key display columns
            display_cols = ['Month_in_Year', 'Revenue', 'COGS', 'Gross_Profit', 'Gross_Margin_%',
                           'Total_Opex', 'EBITDA', 'EBITDA_Margin_%', 'EBIT', 'EBIT_Margin_%',
                           'Net_Profit', 'Net_Margin_%', 'Operating_Cash_Flow', 
                           'Free_Cash_Flow', 'Cumulative_Cash_Flow']

            df_year_display = df_year[display_cols].copy()
            df_year_display.columns = ['Month', 'Revenue', 'COGS', 'Gross Profit', 'GP%',
                                       'Opex', 'EBITDA', 'EBITDA%', 'EBIT', 'EBIT%',
                                       'Net Profit', 'NP%', 'Operating CF', 
                                       'Free CF', 'Cumulative CF']

            # Format numbers
            for col in df_year_display.columns:
                if col not in ['Month', 'GP%', 'EBITDA%', 'EBIT%', 'NP%']:
                    df_year_display[col] = df_year_display[col].apply(lambda x: f"{x:,.0f}")
                elif col != 'Month':
                    df_year_display[col] = df_year_display[col].apply(lambda x: f"{x:.1f}%")

            st.dataframe(df_year_display, use_container_width=True, height=500)

            # Expense breakdown for selected month
            st.markdown("---")
            selected_month = st.slider("Select Month for Detailed Expense Breakdown", 
                1, 12, 6, key="expense_month")

            month_data = df_year[df_year['Month_in_Year'] == selected_month].iloc[0]

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Operating Expense Breakdown**")
                st.write(f"- Salaries: AED {month_data['Salaries']:,.0f}")
                st.write(f"- Rent: AED {month_data['Rent']:,.0f}")
                st.write(f"- Utilities: AED {month_data['Utilities']:,.0f}")
                st.write(f"- Marketing: AED {month_data['Marketing']:,.0f}")
                st.write(f"- Maintenance: AED {month_data['Maintenance']:,.0f}")
                st.write(f"- Insurance: AED {month_data['Insurance']:,.0f}")

            with col2:
                st.markdown("**Other Expenses**")
                st.write(f"- Professional Fees: AED {month_data['Professional_Fees']:,.0f}")
                st.write(f"- POS Subscription: AED {month_data['POS_Subscription']:,.0f}")
                st.write(f"- Security Services: AED {month_data['Security_Services']:,.0f}")
                st.write(f"- Consumables: AED {month_data['Consumables']:,.0f}")
                st.write(f"- Payment Processing: AED {month_data['Payment_Processing_Fees']:,.0f}")
                st.write(f"- Loyalty Program: AED {month_data['Loyalty_Costs']:,.0f}")

            # Download button
            csv = df_year.to_csv(index=False)
            st.download_button(
                label=f"📥 Download Year {selected_year} Data (CSV)",
                data=csv,
                file_name=f"Year_{selected_year}_Monthly_PL.csv",
                mime="text/csv"
            )

        else:
            st.markdown("### Annual Summary - All Years")

            # Calculate annual summaries
            annual_summary = []
            for year in range(1, projection_years + 1):
                df_yr = df[df['Year'] == year]

                annual_summary.append({
                    'Year': year,
                    'Revenue': df_yr['Revenue'].sum(),
                    'COGS': df_yr['COGS'].sum(),
                    'Gross_Profit': df_yr['Gross_Profit'].sum(),
                    'Total_Opex': df_yr['Total_Opex'].sum(),
                    'EBITDA': df_yr['EBITDA'].sum(),
                    'EBIT': df_yr['EBIT'].sum(),
                    'Net_Profit': df_yr['Net_Profit'].sum(),
                    'Operating_Cash_Flow': df_yr['Operating_Cash_Flow'].sum(),
                    'Free_Cash_Flow': df_yr['Free_Cash_Flow'].sum(),
                })

            df_annual = pd.DataFrame(annual_summary)

            # Calculate margins
            df_annual['Gross_Margin_%'] = (df_annual['Gross_Profit'] / df_annual['Revenue'] * 100)
            df_annual['EBITDA_Margin_%'] = (df_annual['EBITDA'] / df_annual['Revenue'] * 100)
            df_annual['EBIT_Margin_%'] = (df_annual['EBIT'] / df_annual['Revenue'] * 100)
            df_annual['Net_Margin_%'] = (df_annual['Net_Profit'] / df_annual['Revenue'] * 100)

            # Reorder columns
            df_annual = df_annual[['Year', 'Revenue', 'COGS', 'Gross_Profit', 'Gross_Margin_%',
                                   'Total_Opex', 'EBITDA', 'EBITDA_Margin_%', 'EBIT', 'EBIT_Margin_%',
                                   'Net_Profit', 'Net_Margin_%', 'Operating_Cash_Flow', 'Free_Cash_Flow']]

            # Format for display
            df_annual_display = df_annual.copy()
            df_annual_display.columns = ['Year', 'Revenue', 'COGS', 'Gross Profit', 'GP%',
                                        'Opex', 'EBITDA', 'EBITDA%', 'EBIT', 'EBIT%',
                                        'Net Profit', 'NP%', 'Operating CF', 'Free CF']

            for col in df_annual_display.columns:
                if col not in ['Year', 'GP%', 'EBITDA%', 'EBIT%', 'NP%']:
                    df_annual_display[col] = df_annual_display[col].apply(
                        lambda x: f"{x:,.0f}" if isinstance(x, (int, float)) else x)
                elif col != 'Year':
                    df_annual_display[col] = df_annual_display[col].apply(
                        lambda x: f"{x:.1f}%" if isinstance(x, (int, float)) else x)

            st.dataframe(df_annual_display, use_container_width=True)

            # Download complete data
            csv_full = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Complete P&L Data (All Years, CSV)",
                data=csv_full,
                file_name="Complete_PL_Projection.csv",
                mime="text/csv"
            )

        # Charts
        st.markdown("---")
        st.subheader("📊 Financial Visualizations")

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            # Revenue build-up trajectory
            fig_revenue = go.Figure()
            fig_revenue.add_trace(go.Scatter(
                x=df['Month'],
                y=df['Revenue'],
                mode='lines+markers',
                name='Monthly Revenue',
                line=dict(color='#3498db', width=3),
                fill='tozeroy',
                hovertemplate='Month %{x}<br>Revenue: AED %{y:,.0f}<extra></extra>'
            ))

            # Add ramp-up indicator
            if rampup_months > 0:
                fig_revenue.add_vrect(
                    x0=0, x1=rampup_months,
                    fillcolor="yellow", opacity=0.2,
                    layer="below", line_width=0,
                    annotation_text="Ramp-up Period",
                    annotation_position="top left"
                )

            fig_revenue.update_layout(
                title="Revenue Build-up Trajectory",
                xaxis_title="Month",
                yaxis_title="Revenue (AED)",
                hovermode='x unified',
                height=400
            )
            st.plotly_chart(fig_revenue, use_container_width=True)

        with chart_col2:
            # Margin trend analysis
            fig_margin = go.Figure()
            fig_margin.add_trace(go.Scatter(
                x=df['Month'], y=df['Gross_Margin_%'],
                mode='lines', name='Gross Margin %',
                line=dict(color='#2ecc71', width=2)
            ))
            fig_margin.add_trace(go.Scatter(
                x=df['Month'], y=df['EBITDA_Margin_%'],
                mode='lines', name='EBITDA Margin %',
                line=dict(color='#f39c12', width=2)
            ))
            fig_margin.add_trace(go.Scatter(
                x=df['Month'], y=df['Net_Margin_%'],
                mode='lines', name='Net Margin %',
                line=dict(color='#9b59b6', width=2)
            ))
            fig_margin.update_layout(
                title="Margin Trend Analysis",
                xaxis_title="Month",
                yaxis_title="Margin %",
                hovermode='x unified',
                height=400
            )
            st.plotly_chart(fig_margin, use_container_width=True)

        # Monthly cash flow waterfall
        st.markdown("### 💧 Monthly Cash Flow Waterfall")

        # Select year for waterfall
        waterfall_year = st.selectbox("Select Year for Cash Flow Waterfall", 
            options=list(range(1, projection_years + 1)), key="waterfall_year")

        df_waterfall = df[df['Year'] == waterfall_year].copy()

        fig_waterfall = go.Figure(go.Waterfall(
            name="Cash Flow",
            orientation="v",
            x=[f"M{i}" for i in df_waterfall['Month_in_Year']],
            y=df_waterfall['Free_Cash_Flow'],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))

        fig_waterfall.update_layout(
            title=f"Year {waterfall_year} - Monthly Free Cash Flow Waterfall",
            showlegend=False,
            height=400
        )

        st.plotly_chart(fig_waterfall, use_container_width=True)

        # Cumulative cash flow chart
        fig_cumulative = go.Figure()

        # Add initial investment point
        fig_cumulative.add_trace(go.Scatter(
            x=[0],
            y=[-(total_capex + security_deposit + total_initial_inventory)],
            mode='markers',
            name='Initial Investment',
            marker=dict(size=12, color='red'),
            hovertemplate='Month 0<br>Initial Investment: AED %{y:,.0f}<extra></extra>'
        ))

        fig_cumulative.add_trace(go.Scatter(
            x=df['Month'],
            y=df['Cumulative_Cash_Flow'],
            mode='lines+markers',
            name='Cumulative Cash Flow',
            line=dict(color='#e74c3c', width=3),
            fill='tozeroy',
            hovertemplate='Month %{x}<br>Cumulative CF: AED %{y:,.0f}<extra></extra>'
        ))

        fig_cumulative.add_hline(
            y=0, line_dash="dash", line_color="black",
            annotation_text="Break-even Line",
            annotation_position="right"
        )

        fig_cumulative.update_layout(
            title="Cumulative Cash Flow (Including Initial Investment)",
            xaxis_title="Month",
            yaxis_title="Cumulative Cash Flow (AED)",
            hovermode='x unified',
            height=450
        )

        st.plotly_chart(fig_cumulative, use_container_width=True)

# =============================================================================
# SECTION 4: EXECUTIVE SUMMARY
# =============================================================================
with tab4:
    st.markdown('<div class="section-header">Executive Summary & Key Metrics</div>', unsafe_allow_html=True)

    if not st.session_state.calculated:
        st.warning("⚠️ Please calculate financial projections in the 'Detailed P&L' tab first.")
    else:
        df = st.session_state.df_monthly
        total_investment = st.session_state.total_investment

        # Calculate key metrics

        # 1. Break-even month
        breakeven_month = None
        for idx, row in df.iterrows():
            if row['Cumulative_Cash_Flow'] >= 0:
                breakeven_month = row['Month']
                break

        # 2. NPV calculation
        cash_flows = [-(total_capex + security_deposit + total_initial_inventory)]
        cash_flows.extend(df['Free_Cash_Flow'].values)
        npv = np.npv(discount_rate/100/12, cash_flows)

        # 3. IRR calculation
        try:
            irr_monthly = np.irr(cash_flows)
            irr_annual = (1 + irr_monthly) ** 12 - 1
            irr_annual_pct = irr_annual * 100
        except:
            irr_annual_pct = None

        # 4. Payback period
        payback_month = breakeven_month  # Same as break-even

        # 5. Peak funding requirement
        peak_funding = min(cash_flows[0], df['Cumulative_Cash_Flow'].min())

        # 6. Return metrics
        total_free_cash_flow = df['Free_Cash_Flow'].sum()
        roi_pct = (total_free_cash_flow / abs(total_investment)) * 100

        # 7. Average stabilized metrics (last 12 months)
        df_stable = df.tail(12)
        avg_monthly_revenue = df_stable['Revenue'].mean()
        avg_monthly_profit = df_stable['Net_Profit'].mean()
        avg_ebitda_margin = df_stable['EBITDA_Margin_%'].mean()
        avg_net_margin = df_stable['Net_Margin_%'].mean()

        # 8. Debt service coverage ratio
        avg_dscr = df_stable['DSCR'].dropna().mean() if df_stable['DSCR'].dropna().shape[0] > 0 else None

        # 9. Annual summaries
        year_summaries = []
        for year in range(1, projection_years + 1):
            df_yr = df[df['Year'] == year]
            year_summaries.append({
                'Year': year,
                'Revenue': df_yr['Revenue'].sum(),
                'EBITDA': df_yr['EBITDA'].sum(),
                'Net_Profit': df_yr['Net_Profit'].sum(),
                'Free_Cash_Flow': df_yr['Free_Cash_Flow'].sum()
            })

        df_year_summary = pd.DataFrame(year_summaries)

        # FEASIBILITY ASSESSMENT with Traffic Light System
        st.markdown("---")
        st.markdown("### 🚦 Feasibility Assessment")

        feasibility_score = 0
        max_score = 4
        feasibility_criteria = []

        # Criterion 1: IRR vs Hurdle Rate
        if irr_annual_pct and irr_annual_pct >= hurdle_rate:
            feasibility_score += 1
            feasibility_criteria.append(f"✅ IRR ({irr_annual_pct:.1f}%) exceeds hurdle rate ({hurdle_rate}%)")
        elif irr_annual_pct:
            feasibility_criteria.append(f"❌ IRR ({irr_annual_pct:.1f}%) below hurdle rate ({hurdle_rate}%)")
        else:
            feasibility_criteria.append("❌ IRR cannot be calculated")

        # Criterion 2: NPV
        if npv > 0:
            feasibility_score += 1
            feasibility_criteria.append(f"✅ Positive NPV (AED {npv:,.0f})")
        else:
            feasibility_criteria.append(f"❌ Negative NPV (AED {npv:,.0f})")

        # Criterion 3: Payback Period
        if payback_month and payback_month <= 36:
            feasibility_score += 1
            feasibility_criteria.append(f"✅ Payback within 3 years ({payback_month} months)")
        elif payback_month and payback_month <= 48:
            feasibility_score += 0.5
            feasibility_criteria.append(f"⚠️ Payback within 4 years ({payback_month} months)")
        else:
            feasibility_criteria.append("❌ Payback > 4 years or not achieved")

        # Criterion 4: EBITDA Margin
        if avg_ebitda_margin >= 15:
            feasibility_score += 1
            feasibility_criteria.append(f"✅ Strong EBITDA margin ({avg_ebitda_margin:.1f}%)")
        elif avg_ebitda_margin >= 10:
            feasibility_score += 0.5
            feasibility_criteria.append(f"⚠️ Moderate EBITDA margin ({avg_ebitda_margin:.1f}%)")
        else:
            feasibility_criteria.append(f"❌ Weak EBITDA margin ({avg_ebitda_margin:.1f}%)")

        # Overall verdict with traffic light
        feasibility_pct = (feasibility_score / max_score) * 100

        if feasibility_pct >= 75:
            verdict = "🟢 HIGHLY FEASIBLE - GREEN LIGHT"
            verdict_class = "feasibility-green"
            verdict_text = "Strong financial returns expected. Project recommended for approval."
        elif feasibility_pct >= 50:
            verdict = "🟡 MODERATELY FEASIBLE - AMBER LIGHT"
            verdict_class = "feasibility-amber"
            verdict_text = "Acceptable returns with some risks. Consider optimization or proceed with caution."
        else:
            verdict = "🔴 NOT FEASIBLE - RED LIGHT"
            verdict_class = "feasibility-red"
            verdict_text = "Insufficient returns. Project not recommended unless major improvements made."

        st.markdown(f'<div class="{verdict_class}">{verdict}<br><span style="font-size:1rem; font-weight:normal;">{verdict_text}</span></div>', 
                   unsafe_allow_html=True)

        st.markdown(f"**Feasibility Score: {feasibility_score:.1f} / {max_score} ({feasibility_pct:.0f}%)**")

        st.markdown("#### Decision Criteria")
        for criterion in feasibility_criteria:
            st.markdown(f"- {criterion}")

        # Investment Overview
        st.markdown("---")
        st.markdown("### 💼 Investment Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Investment", f"AED {abs(total_investment):,.0f}")
            st.caption("Capex + Security + Inventory")

        with col2:
            if payback_month:
                payback_years = payback_month / 12
                st.metric("Payback Period", f"{payback_years:.1f} years")
                st.caption(f"{payback_month} months")
            else:
                st.metric("Payback Period", "Not Achieved")
                st.caption("Within projection period")

        with col3:
            npv_color = "normal" if npv > 0 else "inverse"
            st.metric("Net Present Value", f"AED {npv:,.0f}", 
                     delta="Positive" if npv > 0 else "Negative",
                     delta_color=npv_color)
            st.caption(f"@ {discount_rate}% discount rate")

        with col4:
            if irr_annual_pct is not None:
                irr_delta = f"{irr_annual_pct - hurdle_rate:+.1f}% vs hurdle"
                irr_color = "normal" if irr_annual_pct >= hurdle_rate else "inverse"
                st.metric("Internal Rate of Return", f"{irr_annual_pct:.1f}%",
                         delta=irr_delta, delta_color=irr_color)
            else:
                st.metric("Internal Rate of Return", "N/A")
                st.caption("Cannot calculate")

        # Key Performance Indicators
        st.markdown("---")
        st.markdown("### 📈 Key Performance Indicators")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Avg Monthly Revenue (Stabilized)", f"AED {avg_monthly_revenue:,.0f}")
            st.metric("Break-even Month", f"Month {breakeven_month}" if breakeven_month else "Not Achieved")

        with col2:
            st.metric("Avg Monthly Profit (Stabilized)", f"AED {avg_monthly_profit:,.0f}")
            st.metric("Peak Funding Requirement", f"AED {abs(peak_funding):,.0f}")

        with col3:
            st.metric("Avg EBITDA Margin (Stabilized)", f"{avg_ebitda_margin:.1f}%")
            st.metric("Total Free Cash Flow", f"AED {total_free_cash_flow:,.0f}")

        with col4:
            st.metric("Avg Net Margin (Stabilized)", f"{avg_net_margin:.1f}%")
            if avg_dscr:
                st.metric("Avg Debt Service Coverage", f"{avg_dscr:.2f}x")
            else:
                st.metric("Debt Service Coverage", "N/A")

        # Year-by-Year Summary
        st.markdown("---")
        st.markdown("### 📅 Year-by-Year Performance Summary")

        df_summary_display = df_year_summary.copy()

        # Add margin calculations
        df_summary_display['EBITDA_Margin'] = (df_summary_display['EBITDA'] / 
                                                df_summary_display['Revenue'] * 100).round(1)
        df_summary_display['Net_Margin'] = (df_summary_display['Net_Profit'] / 
                                            df_summary_display['Revenue'] * 100).round(1)

        # Format for display
        df_summary_display['Revenue'] = df_summary_display['Revenue'].apply(lambda x: f"AED {x:,.0f}")
        df_summary_display['EBITDA'] = df_summary_display['EBITDA'].apply(lambda x: f"AED {x:,.0f}")
        df_summary_display['Net_Profit'] = df_summary_display['Net_Profit'].apply(lambda x: f"AED {x:,.0f}")
        df_summary_display['Free_Cash_Flow'] = df_summary_display['Free_Cash_Flow'].apply(lambda x: f"AED {x:,.0f}")
        df_summary_display['EBITDA_Margin'] = df_summary_display['EBITDA_Margin'].apply(lambda x: f"{x}%")
        df_summary_display['Net_Margin'] = df_summary_display['Net_Margin'].apply(lambda x: f"{x}%")

        df_summary_display.columns = ['Year', 'Revenue', 'EBITDA', 'Net Profit', 
                                      'Free Cash Flow', 'EBITDA %', 'Net Margin %']

        st.dataframe(df_summary_display, use_container_width=True)

        # Sensitivity Analysis
        st.markdown("---")
        st.markdown("### 🔄 Sensitivity Analysis (What-If Scenarios)")

        st.info("Adjust key assumptions to see immediate impact on IRR and NPV")

        sens_col1, sens_col2, sens_col3 = st.columns(3)

        with sens_col1:
            revenue_change = st.slider("Revenue Change (%)", -30, 30, 0, 5, key="sens_revenue")

        with sens_col2:
            gross_margin_change = st.slider("Gross Margin Change (pp)", -10, 10, 0, 1, key="sens_margin")

        with sens_col3:
            opex_change = st.slider("Operating Expenses Change (%)", -20, 20, 0, 5, key="sens_opex")

        if st.button("🔍 Calculate Sensitivity Impact", type="secondary"):
            # Recalculate with adjusted assumptions
            adjusted_cash_flows = [cash_flows[0]]  # Keep initial investment

            for idx, row in df.iterrows():
                adj_revenue = row['Revenue'] * (1 + revenue_change/100)

                # Adjust gross margin
                original_gp_pct = row['Gross_Margin_%']
                adj_gp_pct = original_gp_pct + gross_margin_change
                adj_gross_profit = adj_revenue * (adj_gp_pct/100)

                # Adjust opex
                adj_opex = row['Total_Opex'] * (1 + opex_change/100)

                # Calculate adjusted EBITDA
                adj_ebitda = adj_gross_profit - adj_opex

                # Keep other items same
                adj_fcf = (adj_ebitda - row['Total_D&A'] - row['Interest_Expense'] - 
                          max(0, (adj_ebitda - row['Total_D&A'] - row['Interest_Expense']) * 
                          (corporate_tax_rate/100)) - row['Principal_Repayment'])

                adjusted_cash_flows.append(adj_fcf)

            try:
                adj_irr_monthly = np.irr(adjusted_cash_flows)
                adj_irr_annual = ((1 + adj_irr_monthly) ** 12 - 1) * 100
                adj_npv = np.npv(discount_rate/100/12, adjusted_cash_flows)

                col1, col2 = st.columns(2)

                with col1:
                    irr_change = adj_irr_annual - irr_annual_pct if irr_annual_pct else 0
                    st.metric("Adjusted IRR", f"{adj_irr_annual:.1f}%", 
                             delta=f"{irr_change:+.1f}pp",
                             delta_color="normal" if irr_change >= 0 else "inverse")
                    st.caption(f"Original: {irr_annual_pct:.1f}%")

                with col2:
                    npv_change = adj_npv - npv
                    st.metric("Adjusted NPV", f"AED {adj_npv:,.0f}",
                             delta=f"AED {npv_change:+,.0f}",
                             delta_color="normal" if npv_change >= 0 else "inverse")
                    st.caption(f"Original: AED {npv:,.0f}")

                # Show new feasibility status
                if adj_irr_annual >= hurdle_rate:
                    st.success(f"✅ Adjusted IRR still exceeds hurdle rate ({hurdle_rate}%)")
                else:
                    st.error(f"❌ Adjusted IRR falls below hurdle rate ({hurdle_rate}%)")

            except:
                st.error("⚠️ Cannot calculate IRR with adjusted assumptions")

        # Store Information
        st.markdown("---")
        st.markdown("### 🏪 Store & Investment Details")

        info_col1, info_col2 = st.columns(2)

        with info_col1:
            st.markdown("**Location Information**")
            st.write(f"- **Store Name:** {store_name}")
            st.write(f"- **City:** {city}")
            st.write(f"- **Location Type:** {location_type}")
            st.write(f"- **Zone Classification:** {zone_class}")
            st.write(f"- **Total Area:** {total_area:,.0f} sq ft")
            st.write(f"- **Monthly Rent:** AED {monthly_base_rent:,.0f}")

        with info_col2:
            st.markdown("**Investment Structure**")
            st.write(f"- **Capital Expenditure:** AED {total_capex:,.0f}")
            st.write(f"- **Security Deposit:** AED {security_deposit:,.0f}")
            st.write(f"- **Initial Inventory:** AED {total_initial_inventory:,.0f}")
            st.write(f"- **Equity Contribution:** AED {equity_contribution:,.0f}")
            st.write(f"- **Debt Amount:** AED {debt_amount:,.0f}")
            st.write(f"- **Total Funding:** AED {equity_contribution + debt_amount:,.0f}")

        # Export options
        st.markdown("---")
        st.markdown("### 📥 Export Complete Report")

        col1, col2 = st.columns(2)

        with col1:
            # Export full dataset
            csv_complete = df.to_csv(index=False)
            st.download_button(
                label="📊 Download Complete P&L (CSV)",
                data=csv_complete,
                file_name=f"{store_name.replace(' ', '_')}_Complete_Financial_Projections.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col2:
            # Export summary
            summary_data = {
                'Store Name': [store_name],
                'City': [city],
                'Total Investment': [total_investment],
                'Payback (Months)': [payback_month if payback_month else 'N/A'],
                'IRR %': [f"{irr_annual_pct:.2f}" if irr_annual_pct else 'N/A'],
                'NPV': [f"{npv:,.0f}"],
                'Hurdle Rate %': [hurdle_rate],
                'Feasibility': [verdict],
                'Avg Monthly Revenue': [f"{avg_monthly_revenue:,.0f}"],
                'Avg EBITDA Margin %': [f"{avg_ebitda_margin:.1f}"],
                'Break-even Month': [breakeven_month if breakeven_month else 'N/A']
            }

            df_summary_export = pd.DataFrame(summary_data)
            csv_summary = df_summary_export.to_csv(index=False)

            st.download_button(
                label="📋 Download Executive Summary (CSV)",
                data=csv_summary,
                file_name=f"{store_name.replace(' ', '_')}_Executive_Summary.csv",
                mime="text/csv",
                use_container_width=True
            )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 2rem;'>
    <p><strong>💎 Luxury Retail Store Feasibility Study Tool</strong></p>
    <p>Comprehensive Financial Analysis for Watches & Jewelry Retail Business</p>
    <p>Developed for Financial Professionals | © 2025 | Powered by Streamlit</p>
    <p style='font-size: 0.9rem; margin-top: 1rem;'>
        Features: Granular Input Controls | Multi-Year Projections | Sensitivity Analysis | 
        Traffic Light Feasibility System | Complete P&L Modeling
    </p>
</div>
""", unsafe_allow_html=True)
