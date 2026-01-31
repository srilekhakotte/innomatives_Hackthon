import pandas as pd

def solve_mcqs():
    # 1. Load the Final Dataset
    try:
        df = pd.read_csv('final_food_delivery_dataset.csv')
        print("✓ Loaded final_food_delivery_dataset.csv")
    except FileNotFoundError:
        print("Error: Could not find 'final_food_delivery_dataset.csv'.")
        return

    # Ensure correct data types
    df['total_amount'] = pd.to_numeric(df['total_amount'], errors='coerce')
    df['order_date'] = pd.to_datetime(df['order_date'], dayfirst=True) # Assuming DD-MM-YYYY format

    print("\n--- ANSWERS TO QUESTIONS ---")

    # Q1: Which city has the highest total revenue from Gold members?
    q1 = df[df['membership'] == 'Gold'].groupby('city')['total_amount'].sum().idxmax()
    print(f"Q1 (Gold Revenue City): {q1}")

    # Q2: Which cuisine has the highest average order value?
    q2 = df.groupby('cuisine')['total_amount'].mean().idxmax()
    print(f"Q2 (Highest AOV Cuisine): {q2}")

    # Q3: Distinct users with orders worth > 1000
    user_totals = df.groupby('user_id')['total_amount'].sum()
    q3 = (user_totals > 1000).sum()
    print(f"Q3 (Users > 1000): {q3}")

    # Q4: Which restaurant rating range generated the highest total revenue?
    # Create bins: 0-3.0, 3.0-3.5, 3.5-4.0, 4.0-4.5, 4.5-5.0
    # Note: Adjust logic slightly if needed to match options exactly.
    # Options: 3.0-3.5, 3.6-4.0, 4.1-4.5, 4.6-5.0
    def get_range(r):
        if 3.0 <= r <= 3.5: return '3.0-3.5'
        if 3.6 <= r <= 4.0: return '3.6-4.0'
        if 4.1 <= r <= 4.5: return '4.1-4.5'
        if 4.6 <= r <= 5.0: return '4.6-5.0'
        return 'Other'
    
    df['rating_range'] = df['rating'].apply(get_range)
    q4 = df.groupby('rating_range')['total_amount'].sum().idxmax()
    print(f"Q4 (Highest Revenue Rating): {q4}")

    # Q5: Among Gold members, which city has the highest average order value?
    q5 = df[df['membership'] == 'Gold'].groupby('city')['total_amount'].mean().idxmax()
    print(f"Q5 (Gold Highest AOV City): {q5}")

    # Q6: Cuisine with lowest distinct restaurants but significant revenue?
    q6 = df.groupby('cuisine')['restaurant_id'].nunique().idxmin()
    print(f"Q6 (Lowest Restaurant Count): {q6}")

    # Q7: What percentage of total orders were placed by Gold members?
    gold_pct = (len(df[df['membership'] == 'Gold']) / len(df)) * 100
    print(f"Q7 (Gold Order %): {round(gold_pct)}%")

    # Q8: Restaurant with highest AOV but less than 20 total orders?
    # Note: Uses 'restaurant_name_order' (from orders.csv) to match options like "Ruchi Foods Chinese"
    # Ensure column name matches your dataset. It might be 'restaurant_name_x' or 'restaurant_name_order'
    name_col = 'restaurant_name_order' if 'restaurant_name_order' in df.columns else 'restaurant_name_x'
    
    if name_col in df.columns:
        stats = df.groupby(name_col).agg(
            count=('order_id', 'count'), 
            aov=('total_amount', 'mean')
        )
        q8 = stats[stats['count'] < 20].sort_values('aov', ascending=False).index[0]
        print(f"Q8 (Highest AOV < 20 orders): {q8}")
    else:
        print("Q8: Could not find restaurant name column to check specific names.")

    # Q9: Which combination contributes the highest revenue?
    q9 = df.groupby(['membership', 'cuisine'])['total_amount'].sum().idxmax()
    print(f"Q9 (Highest Revenue Combo): {q9}")

    # Q10: During which quarter of the year is the total revenue highest?
    df['quarter'] = df['order_date'].dt.quarter
    q10 = df.groupby('quarter')['total_amount'].sum().idxmax()
    print(f"Q10 (Highest Revenue Quarter): Q{q10}")

if __name__ == "__main__":
    solve_mcqs()