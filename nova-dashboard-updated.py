"""
NovaSignals Growth Dashboard Generator (Enhanced)
==================================================
Comprehensive analytics dashboard for EdTech/SaaS growth tracking with:
- Corrected TAM (Total Addressable Market) calculation
- Team performance analysis and enrollment attribution
- User activity tracking and engagement metrics
- Multi-channel revenue analysis (lifetime, monthly, podcast)
- Monthly Recurring Payments Analysis with Charts
- Sales Funnel Visualization
- Interactive Plotly Charts

Requirements:
    pip install pandas plotly openpyxl

Usage:
    python nova_signals_dashboard.py

Output:
    - nova_signals_dashboard.html (interactive dashboard)
    - dashboard_report.txt (detailed text summary)
    
Created by: Aryan Agarwal
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

# ============================================================================
# CONFIGURATION
# ============================================================================

EXCEL_FILE = 'NovaSignals-Growth-Funnel-Demo.xlsx'
OUTPUT_HTML = 'nova_signals_dashboard.html'
OUTPUT_REPORT = 'dashboard_report.txt'

# Sheet name for premium campaign leads
PREMIUM_CAMPAIGN_SHEET = 'Premium Campaign'

# ============================================================================
# 1. DATA LOADING
# ============================================================================

def load_all_data():
    """Load all data sources from Excel file"""
    print("📂 Loading all data sources...")
    
    # Sales funnel data (COC sheet)
    df_coc = pd.read_excel(EXCEL_FILE, sheet_name='COC')
    df_coc['DATE'] = pd.to_datetime(df_coc['DATE'], errors='coerce')
    df_coc['Month'] = df_coc['DATE'].dt.strftime('%Y-%m')
    
    # All time class enrollments (lifetime/2yr plans)
    df_payments = pd.read_excel(EXCEL_FILE, sheet_name='All time class enrllments')
    df_payments['PaymentDate'] = pd.to_datetime(df_payments['PaymentDate'])
    df_payments['Month'] = df_payments['PaymentDate'].dt.strftime('%Y-%m')
    
    # Monthly subscription payments
    df_monthly = pd.read_excel(EXCEL_FILE, sheet_name='payments(Monthly)')
    df_monthly['Date'] = pd.to_datetime(df_monthly['Date'])
    df_monthly['Month'] = df_monthly['Date'].dt.strftime('%Y-%m')
    
    # Podcast leads
    df_podcast = pd.read_excel(EXCEL_FILE, sheet_name='PODCAST LEADS')
    df_podcast['subscription_date'] = pd.to_datetime(df_podcast['subscription_date'])
    
    # Premium campaign leads
    try:
        df_premium = pd.read_excel(EXCEL_FILE, sheet_name=PREMIUM_CAMPAIGN_SHEET)
        # Normalize column name
        if 'phone' in df_premium.columns and 'Phone' not in df_premium.columns:
            df_premium.rename(columns={'phone': 'Phone'}, inplace=True)
    except Exception as e:
        print(f"⚠️  Warning: Could not load '{PREMIUM_CAMPAIGN_SHEET}': {e}")
        df_premium = pd.DataFrame(columns=['Phone'])
    
    print(f"✅ Loaded Sales Funnel (COC): {df_coc.shape}")
    print(f"✅ Loaded All Time Enrollments: {df_payments.shape}")
    print(f"✅ Loaded Monthly Subscriptions: {df_monthly.shape}")
    print(f"✅ Loaded Podcast Leads: {df_podcast.shape}")
    print(f"✅ Loaded Premium Campaign Leads: {df_premium.shape}")
    
    return df_coc, df_payments, df_monthly, df_podcast, df_premium

# ============================================================================
# 2. CALCULATE MONTHLY RECURRING METRICS
# ============================================================================

def calculate_monthly_recurring_metrics(df_monthly):
    """Calculate comprehensive monthly recurring payment metrics"""
    
    print("\n📊 Calculating monthly recurring payment metrics...")
    
    # Overall metrics
    total_subscriptions = len(df_monthly)
    active_subscriptions = int((df_monthly['Current subscription status'] == 'active').sum())
    cancelled_subscriptions = total_subscriptions - active_subscriptions
    
    total_revenue = float(df_monthly['Amount'].sum())
    avg_subscription_value = float(df_monthly['Amount'].mean())
    
    # Active subscription MRR
    active_df = df_monthly[df_monthly['Current subscription status'] == 'active']
    active_mrr = float(active_df['Amount'].sum())
    
    # Churn metrics
    churn_rate = (cancelled_subscriptions / total_subscriptions * 100) if total_subscriptions > 0 else 0.0
    retention_rate = 100 - churn_rate
    
    # Month-over-month trends
    monthly_trends = df_monthly.groupby('Month').agg({
        'Amount': ['sum', 'count', 'mean']
    }).reset_index()
    monthly_trends.columns = ['Month', 'Revenue', 'Count', 'AvgValue']
    monthly_trends = monthly_trends.sort_values('Month')
    
    # Revenue by status
    revenue_by_status = df_monthly.groupby('Current subscription status')['Amount'].sum().to_dict()
    
    recurring_metrics = {
        'total_subscriptions': total_subscriptions,
        'active_subscriptions': active_subscriptions,
        'cancelled_subscriptions': cancelled_subscriptions,
        'total_revenue': total_revenue,
        'active_mrr': active_mrr,
        'avg_subscription_value': avg_subscription_value,
        'churn_rate': churn_rate,
        'retention_rate': retention_rate,
        'monthly_trends': monthly_trends,
        'revenue_by_status': revenue_by_status
    }
    
    print(f"✅ Monthly recurring metrics calculated")
    print(f"   Total Subscriptions: {total_subscriptions:,}")
    print(f"   Active MRR: ₹{active_mrr:,.0f}")
    print(f"   Churn Rate: {churn_rate:.1f}%")
    
    return recurring_metrics

# ============================================================================
# 3. CALCULATE TEAM PERFORMANCE METRICS
# ============================================================================

def calculate_team_performance(df_coc):
    """Calculate team member performance from 'Alloted to' column"""
    
    print("\n📊 Calculating team performance metrics...")
    
    if 'Alloted to' not in df_coc.columns:
        print("⚠️  No 'Alloted to' column found in COC sheet")
        return {}
    
    df_team = df_coc[df_coc['Alloted to'].notna()].copy()
    
    if len(df_team) == 0:
        print("⚠️  No 'Alloted to' data found")
        return {}
    
    # Aggregate by team member
    team_stats = df_team.groupby('Alloted to').agg({
        'Total Sales': 'sum',
        'Revenue': 'sum',
        'peakAttendance': 'sum',
        'pitchAttendance': 'sum'
    }).reset_index()
    
    # Calculate conversion rates
    team_stats['conversion_rate'] = (team_stats['Total Sales'] / team_stats['peakAttendance'] * 100).fillna(0)
    team_stats['revenue_per_sale'] = (team_stats['Revenue'] / team_stats['Total Sales']).fillna(0)
    
    # Sort by revenue
    team_stats = team_stats.sort_values('Revenue', ascending=False)
    
    # Top performer
    if len(team_stats) > 0:
        top_performer = team_stats.iloc[0]['Alloted to']
        top_revenue = float(team_stats.iloc[0]['Revenue'])
        top_sales = int(team_stats.iloc[0]['Total Sales'])
    else:
        top_performer = "N/A"
        top_revenue = 0.0
        top_sales = 0
    
    team_metrics = {
        'team_stats': team_stats,
        'top_performer': top_performer,
        'top_revenue': top_revenue,
        'top_sales': top_sales,
        'total_team_members': len(team_stats)
    }
    
    print(f"✅ Team performance calculated")
    print(f"   Team members tracked: {len(team_stats)}")
    print(f"   Top performer: {top_performer} (₹{top_revenue:,.0f})")
    
    return team_metrics

# ============================================================================
# 4. CALCULATE TEAM ENROLLMENT ATTRIBUTION
# ============================================================================

def calculate_team_enrollment_attribution(df_coc, df_payments):
    """Map enrollments to team members via phone number matching"""
    
    print("\n📊 Calculating team enrollment attribution...")
    
    if 'Alloted to' not in df_coc.columns or 'Phone' not in df_coc.columns:
        print("⚠️  Missing required columns for attribution")
        return {
            'team_enrollment_stats': None,
            'total_mapped_enrollments': 0,
            'total_unmapped_enrollments': len(df_payments),
            'mapping_coverage': 0.0
        }
    
    # Clean phone numbers
    df_coc['Phone_Clean'] = df_coc['Phone'].astype(str).str.replace('.0', '', regex=False).str.strip()
    df_payments['Phone_Clean'] = df_payments['Phone'].astype(str).str.replace('.0', '', regex=False).str.strip()
    
    # Create phone to team member mapping from COC
    phone_to_team = df_coc[df_coc['Alloted to'].notna()].drop_duplicates('Phone_Clean')[['Phone_Clean', 'Alloted to']]
    phone_to_team_dict = dict(zip(phone_to_team['Phone_Clean'], phone_to_team['Alloted to']))
    
    # Map enrollments to team members
    df_payments['Team_Member'] = df_payments['Phone_Clean'].map(phone_to_team_dict)
    
    # Calculate attribution metrics
    mapped_enrollments = df_payments[df_payments['Team_Member'].notna()]
    unmapped_enrollments = df_payments[df_payments['Team_Member'].isna()]
    
    total_mapped = len(mapped_enrollments)
    total_unmapped = len(unmapped_enrollments)
    mapping_coverage = (total_mapped / len(df_payments) * 100) if len(df_payments) > 0 else 0.0
    
    # Team-level aggregation
    if total_mapped > 0:
        team_enrollment_stats = mapped_enrollments.groupby('Team_Member').agg({
            'Phone': 'count',
            'Amount': ['sum', 'mean']
        }).reset_index()
        
        team_enrollment_stats.columns = ['Team_Member', 'Enrollment_Count', 'Total_Revenue', 'Avg_Revenue']
        team_enrollment_stats = team_enrollment_stats.sort_values('Total_Revenue', ascending=False)
    else:
        team_enrollment_stats = None
    
    attribution_metrics = {
        'team_enrollment_stats': team_enrollment_stats,
        'total_mapped_enrollments': total_mapped,
        'total_unmapped_enrollments': total_unmapped,
        'mapping_coverage': mapping_coverage
    }
    
    print(f"✅ Team enrollment attribution calculated")
    print(f"   Mapped enrollments: {total_mapped:,} ({mapping_coverage:.1f}%)")
    print(f"   Unmapped enrollments: {total_unmapped:,}")
    
    return attribution_metrics

# ============================================================================
# 5. CALCULATE USER ACTIVITY METRICS
# ============================================================================

def calculate_activity_metrics(df_payments):
    """Calculate user activity metrics based on PaymentDate"""
    
    print("\n📊 Calculating user activity metrics...")
    
    today = pd.Timestamp.now()
    
    # Use PaymentDate as last activity indicator
    df_payments['days_since_payment'] = (today - df_payments['PaymentDate']).dt.days
    
    # Activity segmentation
    active_7d = int((df_payments['days_since_payment'] <= 7).sum())
    active_30d = int((df_payments['days_since_payment'] <= 30).sum())
    active_90d = int((df_payments['days_since_payment'] <= 90).sum())
    dormant = int((df_payments['days_since_payment'] > 90).sum())
    
    # Churn risk
    churn_risk_14d = int((df_payments['days_since_payment'] > 14).sum())
    churn_risk_30d = int((df_payments['days_since_payment'] > 30).sum())
    
    # Average days since last payment
    avg_days_inactive = float(df_payments['days_since_payment'].mean())
    
    # Engagement rate
    total_users = len(df_payments)
    engagement_rate = (active_30d / total_users * 100) if total_users > 0 else 0.0
    
    # Most recent activity
    most_recent_date = df_payments['PaymentDate'].max()
    
    activity_metrics = {
        'active_7d': active_7d,
        'active_30d': active_30d,
        'active_90d': active_90d,
        'dormant': dormant,
        'churn_risk_14d': churn_risk_14d,
        'churn_risk_30d': churn_risk_30d,
        'avg_days_inactive': avg_days_inactive,
        'engagement_rate': engagement_rate,
        'total_users': total_users,
        'most_recent_date': most_recent_date
    }
    
    print(f"✅ Activity metrics calculated")
    print(f"   Active (30d): {active_30d} | Dormant (90d+): {dormant}")
    
    return activity_metrics

# ============================================================================
# 6. CALCULATE USER SEGMENTATION METRICS (CORRECTED TAM)
# ============================================================================

def calculate_user_segments(df_coc, df_payments, df_monthly, df_podcast, df_premium, team_enrollment_metrics):
    """
    Calculate comprehensive user segmentation metrics with corrected TAM
    TAM = Paying users + Pure unconverted leads (no double-counting)
    """
    
    print("\n📊 Calculating user segmentation (TAM corrected)...")
    
    # 1. ALL TIME CLASS ENROLLMENTS
    all_time_count = len(df_payments)
    all_time_revenue = float(df_payments['Amount'].sum())
    all_time_avg = float(df_payments['Amount'].mean())
    
    # 2. MONTHLY SUBSCRIPTIONS
    monthly_total = len(df_monthly)
    monthly_active = int((df_monthly['Current subscription status'] == 'active').sum())
    monthly_revenue = float(df_monthly['Amount'].sum())
    monthly_avg = float(df_monthly['Amount'].mean())
    monthly_mrr = monthly_active * monthly_avg
    
    # 3. PODCAST LEADS
    podcast_total = len(df_podcast)
    podcast_active = int((df_podcast['subscription_status'] == 'active').sum())
    podcast_cancelled = int((df_podcast['subscription_status'] == 'cancelled').sum())
    podcast_mrr = podcast_active * 999
    
    # 4. PREMIUM CAMPAIGN - Cross-match with payments
    df_premium['Phone_Clean'] = df_premium['Phone'].astype(str).str.replace('.0', '', regex=False).str.strip()
    df_payments['Phone_Clean'] = df_payments['Phone'].astype(str).str.replace('.0', '', regex=False).str.strip()
    
    premium_phones = set(df_premium['Phone_Clean'])
    payment_phones = set(df_payments['Phone_Clean'])
    
    # Customers who converted from premium campaign
    premium_customer_phones = premium_phones.intersection(payment_phones)
    
    # Pure leads who haven't converted yet
    premium_pure_lead_phones = premium_phones - payment_phones
    
    # Filter payment data for premium customers
    premium_customers_df = df_payments[df_payments['Phone_Clean'].isin(premium_customer_phones)]
    
    # Calculate metrics
    premium_customer_count = len(premium_customer_phones)
    premium_pure_lead_count = len(premium_pure_lead_phones)
    premium_customer_revenue = float(premium_customers_df['Amount'].sum())
    premium_avg_revenue = float(premium_customers_df['Amount'].mean()) if premium_customer_count > 0 else 0.0
    premium_pct_all_time = (premium_customer_count / all_time_count * 100) if all_time_count > 0 else 0.0
    
    # Lead-level metrics
    premium_total_leads = len(df_premium)
    premium_unique_phones = df_premium['Phone_Clean'].nunique()
    premium_quality = (premium_unique_phones / premium_total_leads * 100) if premium_total_leads > 0 else 0.0
    premium_conversion_rate = (premium_customer_count / premium_total_leads * 100) if premium_total_leads > 0 else 0.0
    
    # Most recent activity
    if premium_customer_count > 0:
        premium_recent_date = premium_customers_df['PaymentDate'].max()
    else:
        premium_recent_date = pd.NaT
    
    # 5. SALES FUNNEL PERFORMANCE
    funnel_revenue = float(df_coc['Revenue'].sum())
    funnel_sales = int(df_coc['Total Sales'].sum())
    total_peak = int(df_coc['peakAttendance'].sum())
    total_pitch = int(df_coc['pitchAttendance'].sum())
    conversion_rate = (funnel_sales / total_peak) * 100 if total_peak > 0 else 0.0
    
    # 6. COMBINED METRICS
    total_paying_users = all_time_count + monthly_total + podcast_total
    combined_revenue = all_time_revenue + monthly_revenue + podcast_mrr
    active_recurring = monthly_active + podcast_active
    
    # 7. REVENUE-BASED METRICS
    revenue_per_customer = combined_revenue / total_paying_users if total_paying_users > 0 else 0.0
    revenue_per_attendee = combined_revenue / total_peak if total_peak > 0 else 0.0
    
    arr = monthly_mrr * 12
    arr_percentage = (arr / combined_revenue * 100) if combined_revenue > 0 else 0.0
    
    lifetime_revenue_per_user = all_time_revenue / all_time_count if all_time_count > 0 else 0.0
    monthly_revenue_per_user = monthly_revenue / monthly_total if monthly_total > 0 else 0.0
    
    show_up_rate = (total_pitch / total_peak * 100) if total_peak > 0 else 0.0
    sales_per_attendee = funnel_sales / total_peak if total_peak > 0 else 0.0
    
    # 8. CORRECTED TAM CALCULATION
    corrected_tam = total_paying_users + premium_pure_lead_count
    
    # Premium unique market
    premium_unique_market = premium_customer_count + premium_pure_lead_count
    
    metrics = {
        'all_time': {
            'count': all_time_count,
            'revenue': all_time_revenue,
            'avg_payment': all_time_avg,
            'revenue_per_user': lifetime_revenue_per_user
        },
        'team_enrollments': team_enrollment_metrics,
        'monthly': {
            'total': monthly_total,
            'active': monthly_active,
            'revenue': monthly_revenue,
            'avg_payment': monthly_avg,
            'mrr': monthly_mrr,
            'revenue_per_user': monthly_revenue_per_user,
            'churn_rate': ((monthly_total - monthly_active) / monthly_total * 100) if monthly_total > 0 else 0.0
        },
        'podcast': {
            'total': podcast_total,
            'active': podcast_active,
            'cancelled': podcast_cancelled,
            'mrr': podcast_mrr,
            'retention': (podcast_active / podcast_total * 100) if podcast_total > 0 else 0.0
        },
        'premium_campaign': {
            'total_leads': premium_total_leads,
            'unique_phones': premium_unique_phones,
            'quality': premium_quality,
            'customers': premium_customer_count,
            'pure_leads': premium_pure_lead_count,
            'conversion_rate': premium_conversion_rate,
            'revenue': premium_customer_revenue,
            'avg_revenue': premium_avg_revenue,
            'percentage': premium_pct_all_time,
            'recent_date': premium_recent_date,
            'unique_market': premium_unique_market
        },
        'funnel': {
            'revenue': funnel_revenue,
            'sales': funnel_sales,
            'peak': total_peak,
            'pitch': total_pitch,
            'conversion_rate': conversion_rate,
            'show_up_rate': show_up_rate,
            'sales_per_attendee': sales_per_attendee
        },
        'combined': {
            'paying_users': total_paying_users,
            'revenue': combined_revenue,
            'active_recurring': active_recurring
        },
        'revenue_metrics': {
            'revenue_per_customer': revenue_per_customer,
            'revenue_per_attendee': revenue_per_attendee,
            'arr': arr,
            'arr_percentage': arr_percentage,
            'mrr': monthly_mrr,
            'average_ltv': all_time_avg,
            'total_addressable_market': corrected_tam
        }
    }
    
    print(f"✅ User segmentation calculated (TAM CORRECTED)")
    print(f"   TAM: {corrected_tam:,} ({total_paying_users:,} paying + {premium_pure_lead_count:,} leads)")
    
    return metrics

# ============================================================================
# 7. CREATE PLOTLY CHARTS
# ============================================================================

def create_funnel_chart(metrics):
    """Create sales funnel visualization"""
    
    stages = ['Peak Attendance', 'Pitch Attendance', 'Total Sales']
    values = [
        metrics['funnel']['peak'],
        metrics['funnel']['pitch'],
        metrics['funnel']['sales']
    ]
    
    fig = go.Figure(go.Funnel(
        y=stages,
        x=values,
        textposition="inside",
        textinfo="value+percent initial",
        marker=dict(color=['#667eea', '#764ba2', '#f093fb'])
    ))
    
    fig.update_layout(
        title="Sales Funnel Analysis",
        height=400,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig.to_html(include_plotlyjs='cdn', div_id='funnel_chart')

def create_monthly_trend_chart(recurring_metrics):
    """Create monthly revenue trend chart"""
    
    df_trends = recurring_metrics['monthly_trends']
    
    fig = go.Figure()
    
    # Revenue line
    fig.add_trace(go.Scatter(
        x=df_trends['Month'],
        y=df_trends['Revenue'],
        mode='lines+markers',
        name='Revenue',
        line=dict(color='#667eea', width=3),
        marker=dict(size=8)
    ))
    
    # Subscription count (secondary axis)
    fig.add_trace(go.Bar(
        x=df_trends['Month'],
        y=df_trends['Count'],
        name='Subscription Count',
        marker_color='#764ba2',
        opacity=0.6,
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="Monthly Recurring Revenue Trend",
        xaxis_title="Month",
        yaxis_title="Revenue (₹)",
        yaxis2=dict(
            title="Subscription Count",
            overlaying='y',
            side='right'
        ),
        height=400,
        hovermode='x unified',
        margin=dict(l=20, r=60, t=60, b=60)
    )
    
    return fig.to_html(include_plotlyjs=False, div_id='monthly_trend_chart')

def create_team_performance_chart(team_metrics):
    """Create team performance comparison chart"""
    
    team_data = team_metrics.get('team_stats')
    
    if team_data is None or len(team_data) == 0:
        return "<p>No team performance data available</p>"
    
    # Top 10 performers
    top_team = team_data.head(10)
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Revenue by Team Member', 'Conversion Rate by Team Member'),
        specs=[[{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Revenue chart
    fig.add_trace(
        go.Bar(
            x=top_team['Alloted to'],
            y=top_team['Revenue'],
            name='Revenue',
            marker_color='#667eea',
            text=top_team['Revenue'].apply(lambda x: f'₹{x/1000:.0f}K'),
            textposition='outside'
        ),
        row=1, col=1
    )
    
    # Conversion rate chart
    fig.add_trace(
        go.Bar(
            x=top_team['Alloted to'],
            y=top_team['conversion_rate'],
            name='Conversion Rate',
            marker_color='#764ba2',
            text=top_team['conversion_rate'].apply(lambda x: f'{x:.1f}%'),
            textposition='outside'
        ),
        row=1, col=2
    )
    
    fig.update_xaxes(tickangle=-45)
    fig.update_layout(
        height=500,
        showlegend=False,
        margin=dict(l=20, r=20, t=80, b=120)
    )
    
    return fig.to_html(include_plotlyjs=False, div_id='team_performance_chart')

# ============================================================================
# 8. CREATE HTML DASHBOARD
# ============================================================================

def create_html_dashboard(metrics, activity_metrics, team_metrics, recurring_metrics):
    """Create comprehensive HTML dashboard with charts"""
    
    team_data = team_metrics.get('team_stats')
    if team_data is not None and len(team_data) > 0:
        team_names = team_data['Alloted to'].tolist()
        team_revenue = team_data['Revenue'].tolist()
        team_sales = team_data['Total Sales'].tolist()
        team_conversion = team_data['conversion_rate'].tolist()
    else:
        team_names, team_revenue, team_sales, team_conversion = [], [], [], []
    
    team_enroll_data = metrics['team_enrollments'].get('team_enrollment_stats')
    if team_enroll_data is not None and len(team_enroll_data) > 0:
        team_enroll_members = team_enroll_data['Team_Member'].tolist()
        team_enroll_revenue = team_enroll_data['Total_Revenue'].tolist()
        team_enroll_count = team_enroll_data['Enrollment_Count'].tolist()
        team_enroll_avg = team_enroll_data['Avg_Revenue'].tolist()
    else:
        team_enroll_members, team_enroll_revenue, team_enroll_count, team_enroll_avg = [], [], [], []
    
    # TAM breakdown
    tam_paying = metrics['combined']['paying_users']
    tam_leads = metrics['premium_campaign']['pure_leads']
    tam_total = metrics['revenue_metrics']['total_addressable_market']
    
    # Premium campaign unique market
    premium_customers = metrics['premium_campaign']['customers']
    premium_pure_leads = metrics['premium_campaign']['pure_leads']
    premium_unique_market = metrics['premium_campaign']['unique_market']
    
    # Recent activity
    recent_date_str = "N/A"
    if pd.notna(metrics['premium_campaign']['recent_date']):
        recent_date_str = metrics['premium_campaign']['recent_date'].strftime('%Y-%m-%d')
    
    # Generate charts
    funnel_chart_html = create_funnel_chart(metrics)
    monthly_trend_html = create_monthly_trend_chart(recurring_metrics)
    team_chart_html = create_team_performance_chart(team_metrics)
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NovaSignals Growth Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        .container {{
            max-width: 1800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            padding: 40px;
        }}
        header {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 3px solid #667eea;
        }}
        h1 {{ font-size: 3em; color: #667eea; margin-bottom: 10px; }}
        .subtitle {{ font-size: 1.3em; color: #764ba2; font-weight: 600; }}
        .section-header {{
            font-size: 1.8em;
            color: #667eea;
            margin: 40px 0 20px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid #e0e0e0;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .grid-3 {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }}
        .metric-card {{
            background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
            border-radius: 12px;
            padding: 25px;
            border: 2px solid #e0e0e0;
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        .metric-card:hover {{ transform: translateY(-5px); box-shadow: 0 8px 20px rgba(0,0,0,0.1); }}
        .metric-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 1.4em;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #667eea;
        }}
        .metric-icon {{ font-size: 1.5em; }}
        .metric-value {{
            font-size: 2.5em;
            font-weight: 700;
            color: #667eea;
            margin: 15px 0;
        }}
        .metric-label {{
            font-size: 1em;
            color: #666;
            margin-bottom: 5px;
        }}
        .metric-subvalue {{
            font-size: 1.2em;
            color: #888;
            margin-top: 10px;
        }}
        .tam-box {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 40px;
        }}
        .tam-box h3 {{ font-size: 1.5em; margin-bottom: 20px; }}
        .tam-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .tam-item {{
            background: rgba(255, 255, 255, 0.2);
            padding: 20px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }}
        .tam-item h4 {{
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .tam-item .value {{ font-size: 2em; font-weight: bold; }}
        .tam-item .insight {{ font-size: 0.85em; margin-top: 8px; opacity: 0.9; }}
        .chart-container {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin: 30px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .team-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .team-table th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        .team-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e0e0e0;
        }}
        .team-table tr:last-child td {{ border-bottom: none; }}
        .team-table tr:hover {{ background: #f8f9fa; }}
        .highlight-box {{
            background: linear-gradient(135deg, #fff3cd 0%, #fffaed 100%);
            border-left: 4px solid #ffc107;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .highlight-box h4 {{ color: #856404; margin-bottom: 10px; }}
        footer {{
            text-align: center;
            margin-top: 50px;
            padding-top: 30px;
            border-top: 2px solid #e0e0e0;
            color: #666;
        }}
        .creator-badge {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 0.95em;
            font-weight: 600;
            margin-top: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 NovaSignals Growth Dashboard</h1>
            <p class="subtitle">Comprehensive Analytics | Team Performance | TAM Tracking</p>
            <p style="margin-top: 10px; color: #666;">Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p IST')}</p>
        </header>

        <h2 class="section-header">
            <span>🎯</span>
            Total Addressable Market (TAM) - CORRECTED
        </h2>
        
        <div class="tam-box">
            <h3>📊 TAM Calculation (No Double-Counting)</h3>
            <div class="tam-grid">
                <div class="tam-item">
                    <h4>Current Paying Users</h4>
                    <div class="value">{tam_paying:,}</div>
                    <div class="insight">All time + Monthly + Podcast</div>
                </div>
                <div class="tam-item">
                    <h4>+ Pure Leads (Not Converted)</h4>
                    <div class="value">{tam_leads:,}</div>
                    <div class="insight">Premium campaign unconverted</div>
                </div>
                <div class="tam-item">
                    <h4>= Total Addressable Market</h4>
                    <div class="value">{tam_total:,}</div>
                    <div class="insight">Unique addressable users</div>
                </div>
            </div>
            <div style="background: rgba(0,0,0,0.1); padding: 15px; border-left: 4px solid #fff; margin-top: 20px; font-size: 0.9em;">
                <strong>✅ Correction Applied:</strong> Premium campaign customers ({premium_customers:,}) are a SUBSET of all-time enrollments ({metrics['all_time']['count']:,}). 
                They're not double-counted in TAM. Only the {tam_leads:,} unconverted leads are added.
            </div>
        </div>

        <h2 class="section-header">
            <span>📈</span>
            Sales Funnel Performance
        </h2>
        
        <div class="grid-3">
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-icon">👥</span>
                    <span>Peak Attendance</span>
                </div>
                <div class="metric-value">{metrics['funnel']['peak']:,}</div>
                <div class="metric-label">Total Attendees</div>
                <div class="metric-subvalue">Funnel Entry Point</div>
            </div>

            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-icon">🎯</span>
                    <span>Pitch Attendance</span>
                </div>
                <div class="metric-value">{metrics['funnel']['pitch']:,}</div>
                <div class="metric-label">Show-up Rate: {metrics['funnel']['show_up_rate']:.1f}%</div>
                <div class="metric-subvalue">Engaged Prospects</div>
            </div>

            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-icon">💰</span>
                    <span>Conversion Rate</span>
                </div>
                <div class="metric-value">{metrics['funnel']['conversion_rate']:.1f}%</div>
                <div class="metric-label">Total Sales: {metrics['funnel']['sales']:,}</div>
                <div class="metric-subvalue">Revenue: ₹{metrics['funnel']['revenue']/1000:.0f}K</div>
            </div>
        </div>

        <div class="chart-container">
            {funnel_chart_html}
        </div>

        <h2 class="section-header">
            <span>💳</span>
            Monthly Recurring Revenue Analysis
        </h2>
        
        <div class="grid-3">
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-icon">📊</span>
                    <span>Active MRR</span>
                </div>
                <div class="metric-value">₹{recurring_metrics['active_mrr']/1000:.1f}K</div>
                <div class="metric-label">Monthly Recurring Revenue</div>
                <div class="metric-subvalue">ARR: ₹{recurring_metrics['active_mrr']*12/1000:.1f}K</div>
            </div>

            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-icon">✅</span>
                    <span>Active Subscriptions</span>
                </div>
                <div class="metric-value">{recurring_metrics['active_subscriptions']:,}</div>
                <div class="metric-label">Out of {recurring_metrics['total_subscriptions']:,} Total</div>
                <div class="metric-subvalue">Retention: {recurring_metrics['retention_rate']:.1f}%</div>
            </div>

            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-icon">⚠️</span>
                    <span>Churn Rate</span>
                </div>
                <div class="metric-value">{recurring_metrics['churn_rate']:.1f}%</div>
                <div class="metric-label">Cancelled: {recurring_metrics['cancelled_subscriptions']:,}</div>
                <div class="metric-subvalue">Avg Value: ₹{recurring_metrics['avg_subscription_value']:,.0f}</div>
            </div>
        </div>

        <div class="chart-container">
            {monthly_trend_html}
        </div>

        <h2 class="section-header">
            <span>🏢</span>
            Premium Campaign - Unique Market Analysis
        </h2>
        
        <div class="grid-3">
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-icon">📋</span>
                    <span>Lead Pool</span>
                </div>
                <div class="metric-value">{metrics['premium_campaign']['total_leads']:,}</div>
                <div class="metric-label">Total Leads</div>
                <div class="metric-subvalue">
                    Quality: {metrics['premium_campaign']['quality']:.1f}% | 
                    Conversion: {metrics['premium_campaign']['conversion_rate']:.1f}%
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-icon">✅</span>
                    <span>Converted Customers</span>
                </div>
                <div class="metric-value">{premium_customers:,}</div>
                <div class="metric-label">Subset of {metrics['all_time']['count']:,} All-Time ({metrics['premium_campaign']['percentage']:.1f}%)</div>
                <div class="metric-subvalue">
                    Revenue: ₹{metrics['premium_campaign']['revenue']/1000:.1f}K | 
                    Avg: ₹{metrics['premium_campaign']['avg_revenue']:,.0f}
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-icon">🔥</span>
                    <span>Warm Leads</span>
                </div>
                <div class="metric-value">{premium_pure_leads:,}</div>
                <div class="metric-label">Not Yet Converted</div>
                <div class="metric-subvalue">
                    Potential: ₹{premium_pure_leads * metrics['premium_campaign']['avg_revenue']/1000:.1f}K | 
                    Recent: {recent_date_str}
                </div>
            </div>
        </div>

        <div class="highlight-box">
            <h4>💡 Premium Campaign Unique Market Summary:</h4>
            <p><strong>Total Unique Market: {premium_unique_market:,}</strong> ({premium_customers:,} converted + {premium_pure_leads:,} warm leads)</p>
            <p style="margin-top: 10px;">Premium customers are already part of the {metrics['all_time']['count']:,} all-time enrollments.</p>
        </div>

        <h2 class="section-header">
            <span>👥</span>
            Team Performance Analysis
        </h2>
        
        <div class="chart-container">
            {team_chart_html}
        </div>
        
        {"<table class='team-table'><thead><tr><th>Team Member</th><th>Total Sales</th><th>Revenue</th><th>Conversion Rate</th><th>Revenue/Sale</th></tr></thead><tbody>" + "".join([f"<tr><td><strong>{name}</strong></td><td>{int(sales):,}</td><td>₹{revenue:,.0f}</td><td>{conv:.1f}%</td><td>₹{revenue/sales if sales > 0 else 0:,.0f}</td></tr>" for name, sales, revenue, conv in zip(team_names, team_sales, team_revenue, team_conversion)]) + "</tbody></table>" if team_names else "<p style='color: #888; padding: 20px;'>No team performance data available</p>"}

        <h2 class="section-header">
            <span>🎓</span>
            Team Enrollment Attribution
        </h2>
        
        <div class="highlight-box" style="background: linear-gradient(135deg, #e3f2fd 0%, #f0f8ff 100%); border-left: 4px solid #2196f3;">
            <h4 style="color: #1565c0;">📊 Enrollment Mapping Coverage:</h4>
            <p><strong>Mapped Enrollments: {metrics['team_enrollments']['total_mapped_enrollments']:,}</strong> ({metrics['team_enrollments']['mapping_coverage']:.1f}% of all enrollments)</p>
            <p style="margin-top: 10px;">Unmapped: {metrics['team_enrollments']['total_unmapped_enrollments']:,} enrollments</p>
        </div>
        
        {"<table class='team-table'><thead><tr><th>Team Member</th><th>Enrollments</th><th>Total Revenue</th><th>Avg Revenue/Enrollment</th><th>% of Mapped Revenue</th></tr></thead><tbody>" + "".join([f"<tr><td><strong>{member}</strong></td><td>{int(count):,}</td><td>₹{revenue:,.0f}</td><td>₹{avg:,.0f}</td><td>{revenue/sum(team_enroll_revenue)*100:.1f}%</td></tr>" for member, count, revenue, avg in zip(team_enroll_members, team_enroll_count, team_enroll_revenue, team_enroll_avg)]) + "</tbody></table>" if team_enroll_members else "<p style='color: #888; padding: 20px;'>No enrollment attribution data available</p>"}

        <h2 class="section-header">
            <span>📈</span>
            User Activity & Engagement
        </h2>
        
        <div class="grid-3">
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-icon">🔥</span>
                    <span>Active (30d)</span>
                </div>
                <div class="metric-value">{activity_metrics.get('active_30d', 0):,}</div>
                <div class="metric-label">Recent Activity</div>
                <div class="metric-subvalue">Engagement: {activity_metrics.get('engagement_rate', 0):.1f}%</div>
            </div>

            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-icon">⏰</span>
                    <span>Dormant (90d+)</span>
                </div>
                <div class="metric-value">{activity_metrics.get('dormant', 0):,}</div>
                <div class="metric-label">Need Reactivation</div>
                <div class="metric-subvalue">Churn Risk: {activity_metrics.get('churn_risk_30d', 0):,}</div>
            </div>

            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-icon">📅</span>
                    <span>Most Recent</span>
                </div>
                <div class="metric-value" style="font-size: 1.5em;">{activity_metrics.get('most_recent_date', pd.NaT).strftime('%Y-%m-%d') if pd.notna(activity_metrics.get('most_recent_date')) else 'N/A'}</div>
                <div class="metric-label">Latest Payment Date</div>
                <div class="metric-subvalue">Avg Days Inactive: {activity_metrics.get('avg_days_inactive', 0):.0f}</div>
            </div>
        </div>

        <h2 class="section-header">
            <span>💰</span>
            Revenue Overview
        </h2>
        
        <div class="grid-3">
            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-icon">💵</span>
                    <span>Total Revenue</span>
                </div>
                <div class="metric-value">₹{metrics['combined']['revenue']/1000000:.2f}M</div>
                <div class="metric-label">Combined (All Sources)</div>
                <div class="metric-subvalue">
                    Lifetime: ₹{metrics['all_time']['revenue']/1000000:.2f}M | 
                    Monthly: ₹{metrics['monthly']['revenue']/1000000:.2f}M
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-icon">📊</span>
                    <span>Revenue/Customer</span>
                </div>
                <div class="metric-value">₹{metrics['revenue_metrics']['revenue_per_customer']:,.0f}</div>
                <div class="metric-label">Average per Paying User</div>
                <div class="metric-subvalue">ARR: ₹{metrics['revenue_metrics']['arr']/1000000:.2f}M</div>
            </div>

            <div class="metric-card">
                <div class="metric-header">
                    <span class="metric-icon">👥</span>
                    <span>Total Users</span>
                </div>
                <div class="metric-value">{tam_paying:,}</div>
                <div class="metric-label">Current Paying Users</div>
                <div class="metric-subvalue">Active Recurring: {metrics['combined']['active_recurring']:,}</div>
            </div>
        </div>

        <footer>
            <p><strong>Dashboard Generated:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p IST')}</p>
            <p style="margin-top: 10px;">🚀 NovaSignals Growth Analytics</p>
            <div class="creator-badge">Created by Aryan Agarwal</div>
        </footer>
    </div>
</body>
</html>"""
    
    return html_content

# ============================================================================
# 9. GENERATE TEXT REPORT
# ============================================================================

def create_text_report(metrics, activity_metrics, team_metrics, recurring_metrics):
    """Generate comprehensive text report"""
    
    tam_paying = metrics['combined']['paying_users']
    tam_leads = metrics['premium_campaign']['pure_leads']
    tam_total = metrics['revenue_metrics']['total_addressable_market']
    
    premium_customers = metrics['premium_campaign']['customers']
    premium_pure_leads = metrics['premium_campaign']['pure_leads']
    premium_unique_market = metrics['premium_campaign']['unique_market']
    
    team_summary = ""
    if 'team_stats' in team_metrics and team_metrics['team_stats'] is not None:
        team_df = team_metrics['team_stats']
        team_summary = "\nTOP PERFORMERS:\n"
        for idx, row in team_df.head(5).iterrows():
            team_summary += f"  {row['Alloted to']:15} | Sales: {int(row['Total Sales']):4} | Revenue: ₹{row['Revenue']:,.0f} | Conv: {row['conversion_rate']:.1f}%\n"
    else:
        team_summary = "  No team performance data available"
    
    team_enroll_summary = ""
    if 'team_enrollment_stats' in metrics['team_enrollments'] and metrics['team_enrollments']['team_enrollment_stats'] is not None:
        team_enroll_df = metrics['team_enrollments']['team_enrollment_stats']
        team_enroll_summary = "\nTOP ENROLLMENT CONTRIBUTORS:\n"
        for idx, row in team_enroll_df.head(10).iterrows():
            team_enroll_summary += f"  {row['Team_Member']:15} | Enrollments: {int(row['Enrollment_Count']):4} | Revenue: ₹{row['Total_Revenue']:,.0f}\n"
    else:
        team_enroll_summary = "  No enrollment attribution data available"
    
    report = f"""
{'='*80}
NOVASIGNALS GROWTH DASHBOARD - COMPREHENSIVE REPORT
{'='*80}

Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p IST')}
Created by: Aryan Agarwal

{'='*80}
TOTAL ADDRESSABLE MARKET (TAM) - CORRECTED
{'='*80}

Current Paying Users:           {tam_paying:,}
+ Pure Leads (Not Converted):   {tam_leads:,}
= Total Addressable Market:     {tam_total:,}

{'='*80}
SALES FUNNEL PERFORMANCE
{'='*80}

Peak Attendance:                {metrics['funnel']['peak']:,}
Pitch Attendance:               {metrics['funnel']['pitch']:,}
Show-up Rate:                   {metrics['funnel']['show_up_rate']:.1f}%
Total Sales:                    {metrics['funnel']['sales']:,}
Conversion Rate:                {metrics['funnel']['conversion_rate']:.1f}%
Funnel Revenue:                 ₹{metrics['funnel']['revenue']:,.2f}

{'='*80}
MONTHLY RECURRING REVENUE
{'='*80}

Total Subscriptions:            {recurring_metrics['total_subscriptions']:,}
Active Subscriptions:           {recurring_metrics['active_subscriptions']:,}
Cancelled Subscriptions:        {recurring_metrics['cancelled_subscriptions']:,}
Active MRR:                     ₹{recurring_metrics['active_mrr']:,.2f}
Annual Run Rate (ARR):          ₹{recurring_metrics['active_mrr']*12:,.2f}
Avg Subscription Value:         ₹{recurring_metrics['avg_subscription_value']:,.2f}
Churn Rate:                     {recurring_metrics['churn_rate']:.1f}%
Retention Rate:                 {recurring_metrics['retention_rate']:.1f}%

{'='*80}
PREMIUM CAMPAIGN - UNIQUE MARKET ANALYSIS
{'='*80}

Total Leads:                    {metrics['premium_campaign']['total_leads']:,}
Converted Customers:            {premium_customers:,}
Pure Leads (Not Converted):     {premium_pure_leads:,}
Conversion Rate:                {metrics['premium_campaign']['conversion_rate']:.1f}%
Total Revenue:                  ₹{metrics['premium_campaign']['revenue']:,.2f}

{'='*80}
TEAM PERFORMANCE
{'='*80}

Total Team Members:             {team_metrics.get('total_team_members', 0)}
Top Performer:                  {team_metrics.get('top_performer', 'N/A')}
{team_summary}

{'='*80}
TEAM ENROLLMENT ATTRIBUTION
{'='*80}

Mapped Enrollments:             {metrics['team_enrollments']['total_mapped_enrollments']:,}
Mapping Coverage:               {metrics['team_enrollments']['mapping_coverage']:.1f}%
{team_enroll_summary}

{'='*80}
USER ACTIVITY & ENGAGEMENT
{'='*80}

Active (30d):                   {activity_metrics.get('active_30d', 0):,}
Dormant (90d+):                 {activity_metrics.get('dormant', 0):,}
Engagement Rate:                {activity_metrics.get('engagement_rate', 0):.1f}%

{'='*80}
REVENUE SUMMARY
{'='*80}

Total Revenue:                  ₹{metrics['combined']['revenue']:,.2f}
Revenue per Customer:           ₹{metrics['revenue_metrics']['revenue_per_customer']:,.2f}
ARR:                            ₹{metrics['revenue_metrics']['arr']:,.2f}
MRR:                            ₹{metrics['revenue_metrics']['mrr']:,.2f}

{'='*80}
Created by: Aryan Agarwal
{'='*80}
"""
    
    return report

# ============================================================================
# 10. MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    
    print("\n" + "="*80)
    print("  NOVASIGNALS GROWTH DASHBOARD GENERATOR (ENHANCED)")
    print("  Comprehensive Analytics | Team Performance | TAM Tracking")
    print("  Created by: Aryan Agarwal")
    print("="*80 + "\n")
    
    try:
        # Load all data
        df_coc, df_payments, df_monthly, df_podcast, df_premium = load_all_data()
        
        # Calculate monthly recurring metrics
        recurring_metrics = calculate_monthly_recurring_metrics(df_monthly)
        
        # Calculate team performance
        team_metrics = calculate_team_performance(df_coc)
        
        # Calculate team enrollment attribution
        team_enrollment_metrics = calculate_team_enrollment_attribution(df_coc, df_payments)
        
        # Calculate activity metrics
        activity_metrics = calculate_activity_metrics(df_payments)
        
        # Calculate user segmentation
        metrics = calculate_user_segments(df_coc, df_payments, df_monthly, df_podcast, df_premium, team_enrollment_metrics)
        
        # Generate HTML dashboard
        print("\n📝 Generating dashboard with charts...")
        html_content = create_html_dashboard(metrics, activity_metrics, team_metrics, recurring_metrics)
        
        with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Dashboard saved: {OUTPUT_HTML}")
        
        # Generate text report
        print("📄 Generating report...")
        report = create_text_report(metrics, activity_metrics, team_metrics, recurring_metrics)
        
        with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ Report saved: {OUTPUT_REPORT}")
        
        print("\n" + "="*80)
        print("🎉 SUCCESS! Enhanced Dashboard Created!")
        print("="*80)
        print(f"\n📊 Key Metrics:")
        print(f"  • TAM: {metrics['revenue_metrics']['total_addressable_market']:,}")
        print(f"  • Premium Market: {metrics['premium_campaign']['unique_market']:,}")
        print(f"  • Active MRR: ₹{recurring_metrics['active_mrr']:,.0f}")
        print(f"  • Funnel Conversion: {metrics['funnel']['conversion_rate']:.1f}%")
        print(f"  • Team Members: {team_metrics.get('total_team_members', 0)}")
        print(f"  • Active Users (30d): {activity_metrics.get('active_30d', 0):,}")
        
        print(f"\n🚀 Next: Open {OUTPUT_HTML} in your browser")
        print(f"\n✨ Created by: Aryan Agarwal\n")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: Could not find '{EXCEL_FILE}'")
        print(f"   Make sure the Excel file is in the same directory.\n")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
