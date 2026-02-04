# 📊 NovaSignals Growth Dashboard

> **Comprehensive Analytics Dashboard for EdTech/SaaS Growth Tracking**

A powerful Python-based analytics dashboard that provides deep insights into business performance, team metrics, and revenue tracking with interactive visualizations.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Latest-green.svg)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## ✨ Features

### 📈 **Sales Funnel Analytics**
- Visual funnel from Peak Attendance → Pitch Attendance → Sales
- Conversion rate tracking and optimization insights
- Interactive Plotly funnel charts

### 💳 **Monthly Recurring Revenue (MRR) Analysis**
- Active vs Cancelled subscription tracking
- Churn rate and retention metrics
- Month-over-month revenue trends with interactive charts
- Annual Run Rate (ARR) projections

### 🎯 **Total Addressable Market (TAM)**
- Corrected TAM calculation (no double-counting)
- Premium campaign lead tracking
- Conversion analysis from leads to customers

### 👥 **Team Performance Analytics**
- Individual team member performance metrics
- Revenue and sales attribution
- Conversion rate comparisons
- Enrollment attribution via phone number matching

### 📊 **User Engagement Metrics**
- 7-day, 30-day, 90-day activity tracking
- Dormant user identification
- Churn risk analysis
- Engagement rate monitoring

### 💰 **Multi-Channel Revenue Tracking**
- Lifetime enrollments
- Monthly subscriptions
- Podcast leads revenue
- Combined revenue analytics

---

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.8 or higher
```

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/novasignals-dashboard.git
   cd novasignals-dashboard
   ```

2. **Install required packages**
   ```bash
   pip install pandas plotly openpyxl
   ```

3. **Prepare your data**
   - Place your Excel file (`NovaSignals-Growth-Funnel-Demo.xlsx`) in the project directory
   - Ensure the following sheets exist:
     - `COC` (Sales funnel data)
     - `All time class enrllments` (Lifetime enrollments)
     - `payments(Monthly)` (Monthly subscriptions)
     - `PODCAST LEADS` (Podcast-sourced leads)
     - `Premium Campaign` (Premium campaign leads)

4. **Run the dashboard generator**
   ```bash
   python nova_signals_dashboard.py
   ```

5. **View your dashboard**
   - Open `nova_signals_dashboard.html` in your browser
   - Check `dashboard_report.txt` for detailed text summary

---

## 📁 Project Structure

```
novasignals-dashboard/
│
├── nova_signals_dashboard.py      # Main dashboard generator
├── NovaSignals-Growth-Funnel-Demo.xlsx  # Your data file
├── nova_signals_dashboard.html    # Generated interactive dashboard
├── dashboard_report.txt           # Generated text report
├── README.md                      # This file
└── requirements.txt               # Python dependencies
```

---

## 📊 Data Requirements

### Expected Excel Sheet Structure

#### 1. **COC Sheet** (Sales Funnel)
- `DATE` - Date of activity
- `Alloted to` - Team member name
- `Total Sales` - Number of sales
- `Revenue` - Revenue amount
- `peakAttendance` - Peak attendance count
- `pitchAttendance` - Pitch attendance count
- `Phone` - Contact phone number

#### 2. **All time class enrllments Sheet**
- `PaymentDate` - Date of payment
- `Phone` - Contact phone number
- `Amount` - Payment amount

#### 3. **payments(Monthly) Sheet**
- `Date` - Payment date
- `Amount` - Payment amount
- `Current subscription status` - "active" or "cancelled"

#### 4. **PODCAST LEADS Sheet**
- `subscription_date` - Subscription date
- `subscription_status` - "active" or "cancelled"

#### 5. **Premium Campaign Sheet**
- `Phone` or `phone` - Contact phone number

---

## 🎨 Dashboard Sections

### 1. **TAM Overview**
- Total Addressable Market calculation
- Breakdown of paying users vs unconverted leads
- Premium campaign market analysis

### 2. **Sales Funnel**
- Interactive funnel visualization
- Stage-by-stage conversion metrics
- Show-up rates and conversion rates

### 3. **Monthly Recurring Revenue**
- Active MRR tracking
- Subscription status breakdown
- Churn and retention analytics
- Monthly trend charts

### 4. **Premium Campaign Analysis**
- Lead pool metrics
- Conversion tracking
- Revenue from converted customers
- Warm lead identification

### 5. **Team Performance**
- Individual team member metrics
- Revenue and sales comparisons
- Interactive performance charts
- Enrollment attribution

### 6. **User Activity**
- Recent activity tracking (7d, 30d, 90d)
- Dormant user identification
- Engagement rate metrics
- Churn risk analysis

### 7. **Revenue Overview**
- Total revenue across all channels
- Revenue per customer
- ARR/MRR metrics
- Active recurring subscriptions

---

## 🔧 Configuration

Edit the configuration section in `nova_signals_dashboard.py`:

```python
# File paths
EXCEL_FILE = 'NovaSignals-Growth-Funnel-Demo.xlsx'
OUTPUT_HTML = 'nova_signals_dashboard.html'
OUTPUT_REPORT = 'dashboard_report.txt'

# Sheet names
PREMIUM_CAMPAIGN_SHEET = 'Premium Campaign'
```

---

## 📈 Sample Output

### Console Output
```
================================================================================
  NOVASIGNALS GROWTH DASHBOARD GENERATOR (ENHANCED)
  Comprehensive Analytics | Team Performance | TAM Tracking
  Created by: Aryan Agarwal
================================================================================

📂 Loading all data sources...
✅ Loaded Sales Funnel (COC): (150, 12)
✅ Loaded All Time Enrollments: (85, 8)
✅ Loaded Monthly Subscriptions: (45, 6)
✅ Loaded Podcast Leads: (32, 5)
✅ Loaded Premium Campaign Leads: (120, 3)

📊 Calculating monthly recurring payment metrics...
✅ Monthly recurring metrics calculated
   Total Subscriptions: 45
   Active MRR: ₹125,000
   Churn Rate: 15.5%

📝 Generating dashboard with charts...
✅ Dashboard saved: nova_signals_dashboard.html
📄 Generating report...
✅ Report saved: dashboard_report.txt

================================================================================
🎉 SUCCESS! Enhanced Dashboard Created!
================================================================================

📊 Key Metrics:
  • TAM: 162
  • Premium Market: 120
  • Active MRR: ₹125,000
  • Funnel Conversion: 12.5%
  • Team Members: 8
  • Active Users (30d): 42

🚀 Next: Open nova_signals_dashboard.html in your browser

✨ Created by: Aryan Agarwal
```

---

## 🎯 Key Metrics Explained

### **TAM (Total Addressable Market)**
Total unique users who are either current customers or qualified leads. Calculated without double-counting to avoid inflated numbers.

### **MRR (Monthly Recurring Revenue)**
Revenue from active monthly subscriptions. Used to calculate ARR (Annual Run Rate = MRR × 12).

### **Churn Rate**
Percentage of customers who cancelled their subscriptions out of total customers.

### **Conversion Rate**
Percentage of attendees (peak attendance) who became paying customers.

### **Show-up Rate**
Percentage of registered attendees (peak) who actually attended the pitch.

---

## 🛠️ Customization

### Adding New Metrics

1. Add calculation logic in the appropriate function
2. Update the `metrics` dictionary structure
3. Add visualization in `create_html_dashboard()`
4. Update text report in `create_text_report()`

### Changing Chart Styles

Modify the Plotly chart functions:
- `create_funnel_chart()` - Funnel visualization
- `create_monthly_trend_chart()` - Revenue trends
- `create_team_performance_chart()` - Team comparisons

### Adjusting Color Schemes

Edit CSS in the `create_html_dashboard()` function:
```python
# Primary gradient
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

# Card colors
background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
```

---

## 📝 Requirements

```txt
pandas>=1.5.0
plotly>=5.0.0
openpyxl>=3.0.0
```

Save as `requirements.txt` and install with:
```bash
pip install -r requirements.txt
```

---

## 🐛 Troubleshooting

### Issue: "Excel file not found"
**Solution:** Ensure your Excel file is in the same directory as the Python script and named correctly.

### Issue: "Sheet not found"
**Solution:** Verify sheet names match exactly (case-sensitive). Update `PREMIUM_CAMPAIGN_SHEET` if needed.

### Issue: "Column not found"
**Solution:** Check that your Excel sheets have the required columns listed in [Data Requirements](#-data-requirements).

### Issue: Charts not displaying
**Solution:** Ensure you have internet connection (Plotly CDN required) or save Plotly library locally.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Aryan Agarwal**

- GitHub: [@Aryan-Ag02](https://github.com/Aryan-Ag02)
- LinkedIn: [Aryan Agarwal](http://www.linkedin.com/in/aryan-agarwal-a07394209)
- Email: aryaagarwal0205@gmail.com

---

## 🙏 Acknowledgments

- Built with [Plotly](https://plotly.com/) for interactive visualizations
- Data processing powered by [Pandas](https://pandas.pydata.org/)
- Excel integration via [openpyxl](https://openpyxl.readthedocs.io/)

---

## 🔮 Future Enhancements

- [ ] Real-time data refresh
- [ ] Email report automation
- [ ] Custom date range filtering
- [ ] Export to PDF
- [ ] Database integration (PostgreSQL/MySQL)
- [ ] API endpoints for external integrations
- [ ] Mobile-responsive dashboard
- [ ] Dark mode toggle
- [ ] Multi-language support
- [ ] Advanced forecasting models

---

## 📞 Support

If you encounter any issues or have questions, please:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Search existing [Issues](https://github.com/Aryan-Ag02/novasignals-dashboard/issues)
3. Create a new issue with detailed description

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Made with ❤️ by Aryan Agarwal**
