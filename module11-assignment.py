# Module 11 Assignment: Data Visualization with Matplotlib
# SunCoast Retail Visual Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Welcome message
print("=" * 60)
print("SUNCOAST RETAIL VISUAL ANALYSIS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
np.random.seed(42)
quarters = pd.date_range(start='2022-01-01', periods=8, freq='Q')
quarter_labels = ['Q1 2022', 'Q2 2022', 'Q3 2022', 'Q4 2022',
                  'Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023']
locations = ['Tampa', 'Miami', 'Orlando', 'Jacksonville']
categories = ['Electronics', 'Clothing', 'Home Goods', 'Sporting Goods', 'Beauty']

quarterly_data = []
for quarter_idx, quarter in enumerate(quarters):
    for location in locations:
        for category in categories:
            base_sales = np.random.normal(loc=100000, scale=20000)
            seasonal_factor = 1.3 if quarter.quarter == 4 else (0.8 if quarter.quarter == 1 else 1.0)
            location_factor = {'Tampa': 1.0, 'Miami': 1.2, 'Orlando': 0.9, 'Jacksonville': 0.8}[location]
            category_factor = {'Electronics': 1.5, 'Clothing': 1.0, 'Home Goods': 0.8, 'Sporting Goods': 0.7, 'Beauty': 0.9}[category]
            growth_factor = (1 + 0.05/4) ** quarter_idx
            sales = base_sales * seasonal_factor * location_factor * category_factor * growth_factor
            sales = sales * np.random.normal(loc=1.0, scale=0.1)
            ad_spend = (sales ** 0.7) * 0.05 * np.random.normal(loc=1.0, scale=0.2)
            quarterly_data.append({
                'Quarter': quarter,
                'QuarterLabel': quarter_labels[quarter_idx],
                'Location': location,
                'Category': category,
                'Sales': round(sales, 2),
                'AdSpend': round(ad_spend, 2),
                'Year': quarter.year
            })

customer_data = []
total_customers = 2000
age_params = {'Tampa': (45, 15), 'Miami': (35, 12), 'Orlando': (38, 14), 'Jacksonville': (42, 13)}

for location in locations:
    mean_age, std_age = age_params[location]
    customer_count = int(total_customers * {'Tampa': 0.3, 'Miami': 0.35, 'Orlando': 0.2, 'Jacksonville': 0.15}[location])
    ages = np.random.normal(loc=mean_age, scale=std_age, size=customer_count)
    ages = np.clip(ages, 18, 80).astype(int)
    for age in ages:
        if age < 30: category_preference = np.random.choice(categories, p=[0.3, 0.3, 0.1, 0.2, 0.1])
        elif age < 50: category_preference = np.random.choice(categories, p=[0.25, 0.2, 0.25, 0.15, 0.15])
        else: category_preference = np.random.choice(categories, p=[0.15, 0.1, 0.35, 0.1, 0.3])
        
        base_amount = np.random.gamma(shape=5, scale=20)
        price_tier = np.random.choice(['Budget', 'Mid-range', 'Premium'], p=[0.3, 0.5, 0.2])
        tier_factor = {'Budget': 0.7, 'Mid-range': 1.0, 'Premium': 1.8}[price_tier]
        purchase_amount = base_amount * tier_factor
        customer_data.append({
            'Location': location, 'Age': age, 'Category': category_preference,
            'PurchaseAmount': round(purchase_amount, 2), 'PriceTier': price_tier
        })

sales_df = pd.DataFrame(quarterly_data)
customer_df = pd.DataFrame(customer_data)
sales_df['Quarter_Num'] = sales_df['Quarter'].dt.quarter
sales_df['SalesPerDollarSpent'] = sales_df['Sales'] / sales_df['AdSpend']
# ----- END OF DATA CREATION -----

# TODO 1: Time Series Visualization
#create a line chart showing overall quarterly sales trends
def plot_quarterly_sales_trend():
    fig, ax = plt.subplots(figsize=(10, 6))
    trend = sales_df.groupby('QuarterLabel')['Sales'].sum()
    trend = trend.reindex(quarter_labels)
    ax.plot(trend.index, trend.values, marker='o', linestyle='-', color='b')
    ax.set_title('Overall Quarterly Sales Trend (2022-2023)')
    ax.set_xlabel('Quarter')
    ax.set_ylabel('Sales')
    ax.grid(True, linestyle='--', alpha=0.7)
    return fig

#create a multi line chart comparing sales trends across locations
def plot_location_sales_comparison():
    fig, ax = plt.subplots(figsize=(10, 6))
    for loc in locations:
        loc_data = sales_df[sales_df['Location'] == loc].groupby('QuarterLabel')['Sales'].sum()
        loc_data = loc_data.reindex(quarter_labels)
        ax.plot(loc_data.index, loc_data.values, marker='s', label=loc)
    ax.set_title('Sales Comparison by Location')
    ax.legend()
    ax.grid(True, alpha=0.3)
    return fig

# TODO 2: Categorical Comparison
#create a grouped bar chart comparing category performance by location
def plot_category_performance_by_location():
    fig, ax = plt.subplots(figsize=(12, 6))
    latest_q = sales_df[sales_df['QuarterLabel'] == 'Q4 2023']
    pivot_df = latest_q.pivot(index='Category', columns='Location', values='Sales')
    pivot_df.plot(kind='bar', ax=ax)
    ax.set_title('Category Performance by Location (Q4 2023)')
    ax.set_ylabel('Sales ($)')
    return fig

#create a stacked bar chart showing the composition of sales in each location
def plot_sales_composition_by_location():
    fig, ax = plt.subplots(figsize=(10, 6))
    composition = sales_df.groupby(['Location', 'Category'])['Sales'].sum().unstack()
    composition_pct = composition.div(composition.sum(axis=1), axis=0) * 100
    composition_pct.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title('Sales Composition by Location (%)')
    ax.set_ylabel('Percentage of Total Sales')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    return fig

# TODO 3: Relationship Analysis
#create a scatter plot to examine the relationship between ad spend and sales
def plot_ad_spend_vs_sales():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(sales_df['AdSpend'], sales_df['Sales'], alpha=0.5)
    #best fit line
    m, b = np.polyfit(sales_df['AdSpend'], sales_df['Sales'], 1)
    ax.plot(sales_df['AdSpend'], m*sales_df['AdSpend'] + b, color='red', label='Trendline')
    ax.set_title('Ad Spend vs. Sales Relationship')
    ax.set_xlabel('Advertising Spend ($)')
    ax.set_ylabel('Sales ($)')
    return fig

#create a line chart showing sales per dollar spent on advertising over time
def plot_ad_efficiency_over_time():
    fig, ax = plt.subplots(figsize=(10, 6))
    efficiency = sales_df.groupby('QuarterLabel')['SalesPerDollarSpent'].mean().reindex(quarter_labels)
    ax.plot(efficiency.index, efficiency.values, color='green', marker='^')
    ax.set_title('Advertising Efficiency (Sales per $1 spent)')
    ax.annotate('Highest Efficiency', xy=('Q4 2023', efficiency['Q4 2023']), xytext=(4, efficiency.max()+2),
                arrowprops=dict(facecolor='black', shrink=0.05))
    return fig

# TODO 4: Distribution Analysis
#create histograms of customer age distribution
def plot_customer_age_distribution():
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    for i, loc in enumerate(locations):
        data = customer_df[customer_df['Location'] == loc]['Age']
        axes[i].hist(data, bins=15, color='skyblue', edgecolor='black')
        axes[i].axvline(data.mean(), color='red', label=f'Mean: {data.mean():.1f}')
        axes[i].axvline(data.median(), color='yellow', label=f'Median: {data.median():.1f}')
        axes[i].set_title(f'Age Distribution: {loc}')
        axes[i].legend()
    plt.tight_layout()
    return fig

#create box plots comparing purchase amounts by age groups
def plot_purchase_by_age_group():
    fig, ax = plt.subplots(figsize=(10, 6))
    bins = [18, 30, 45, 60, 80]
    labels = ['18-30', '31-45', '46-60', '61+']
    customer_df['AgeGroup'] = pd.cut(customer_df['Age'], bins=bins, labels=labels)
    customer_df.boxplot(column='PurchaseAmount', by='AgeGroup', ax=ax)
    ax.set_title('Purchase Amount by Age Group')
    plt.suptitle('') #remove automatic title
    return fig

# TODO 5: Sales Distribution
#create a histogram of purchase amounts
def plot_purchase_amount_distribution():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(customer_df['PurchaseAmount'], bins=30, color='coral', edgecolor='white')
    ax.set_title('Distribution of Individual Purchase Amounts')
    ax.set_xlabel('Amount ($)')
    return fig

#create a pie chart showing sales breakdown by price tier
def plot_sales_by_price_tier():
    fig, ax = plt.subplots(figsize=(8, 8))
    tier_sales = customer_df.groupby('PriceTier')['PurchaseAmount'].sum()
    explode = [0.1 if i == tier_sales.idxmax() else 0 for i in tier_sales.index]
    ax.pie(tier_sales, labels=tier_sales.index, autopct='%1.1f%%', explode=explode, startangle=140)
    ax.set_title('Sales Breakdown by Price Tier')
    return fig

# TODO 6: Market Share Analysis
#create pie chart showing sales breakdown by category
def plot_category_market_share():
    fig, ax = plt.subplots(figsize=(8, 8))
    cat_sales = sales_df.groupby('Category')['Sales'].sum()
    explode = [0.1 if i == cat_sales.idxmax() else 0 for i in cat_sales.index]
    ax.pie(cat_sales, labels=cat_sales.index, autopct='%1.1f%%', explode=explode)
    ax.set_title('Market Share by Product Category')
    return fig

#create pie chart showing sales breakdown by location
def plot_location_sales_distribution():
    fig, ax = plt.subplots(figsize=(8, 8))
    loc_sales = sales_df.groupby('Location')['Sales'].sum()
    ax.pie(loc_sales, labels=loc_sales.index, autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
    ax.set_title('Sales Distribution by Location')
    return fig

# TODO 7: Comprehensive Dashboard
#create comprehensive dashboard with multiple subplots highlighting key business insights
def create_business_dashboard():
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    #Subplot 1: Sales Trend
    trend = sales_df.groupby('QuarterLabel')['Sales'].sum().reindex(quarter_labels)
    axes[0,0].plot(trend.index, trend.values, marker='o')
    axes[0,0].set_title('Quarterly Revenue Trend')
    
    #Subplot 2: Category Share
    cat_sales = sales_df.groupby('Category')['Sales'].sum()
    axes[0,1].pie(cat_sales, labels=cat_sales.index, autopct='%1.1f%%')
    axes[0,1].set_title('Revenue by Category')
    
    #Subplot 3: Ad Efficiency
    eff = sales_df.groupby('QuarterLabel')['SalesPerDollarSpent'].mean().reindex(quarter_labels)
    axes[1,0].bar(eff.index, eff.values, color='purple')
    axes[1,0].set_title('Ad Efficiency over Time')
    
    #Subplot 4: Location Performance
    loc_sales = sales_df.groupby('Location')['Sales'].sum()
    loc_sales.plot(kind='barh', ax=axes[1,1], color='orange')
    axes[1,1].set_title('Total Sales by Location')
    
    fig.suptitle('SunCoast Retail Performance Dashboard', fontsize=20)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    return fig

#main function to execute all visualizations
def main():
    print("\n" + "=" * 60)
    print("SUNCOAST RETAIL VISUAL ANALYSIS RESULTS")
    print("=" * 60)

    # Call and store figures
    fig1 = plot_quarterly_sales_trend()
    fig2 = plot_location_sales_comparison()
    fig3 = plot_category_performance_by_location()
    fig4 = plot_sales_composition_by_location()
    fig5 = plot_ad_spend_vs_sales()
    fig6 = plot_ad_efficiency_over_time()
    fig7 = plot_customer_age_distribution()
    fig8 = plot_purchase_by_age_group()
    fig9 = plot_purchase_amount_distribution()
    fig10 = plot_sales_by_price_tier()
    fig11 = plot_category_market_share()
    fig12 = plot_location_sales_distribution()
    fig13 = create_business_dashboard()

    print("\nKEY BUSINESS INSIGHTS:")
    print("1. Seasonal Growth: Significant sales spikes occur in Q4 across all locations, likely due to holiday shopping.")
    print("2. Market Dominance: Miami leads in total sales, while Electronics remains the highest-grossing category.")
    print("3. Ad Efficiency: There is a strong positive correlation between ad spend and sales, with peak efficiency in Q4.")
    print("4. Demographics: Tampa attracts an older demographic (Mean ~45), whereas Miami trends significantly younger.")
    print("5. Pricing: 'Mid-range' items contribute the bulk of revenue, but 'Premium' items show higher variance in purchase amounts.")

    plt.show()

if __name__ == "__main__":
    main()