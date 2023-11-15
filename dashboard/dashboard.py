import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_percentage_review_products_df(df):
    group_products_df = df.groupby(by=["product_category_name_english", "product_category_name"]).agg({
        "product_id": "first",
        "review_score": ["sum", "count", "mean"],
    })
    group_products_df["percentage"] = (group_products_df[("review_score", "sum")] / group_products_df[("review_score", "sum")].sum() * 100).round(3)
    
    return group_products_df

def create_monthly_orders_df(df):
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    df["order_purchase_date"] = df["order_purchase_timestamp"].dt.to_period("M")
    
    delivered_orders = df[df['order_status'] == 'delivered']
    
    grouped_data = delivered_orders.groupby(by="order_purchase_date").agg({
        "order_purchase_date": ["first", "count"]
    })
    
    grouped_data['monthly_value'] = grouped_data[('order_purchase_date', "first")].dt.strftime('%B')
    
    grouped_data_2017 = grouped_data.loc[grouped_data.index.to_timestamp().year == 2017]
    
    return grouped_data_2017

main_data_df = pd.read_csv("dashboard/main_data.csv")

percentage_review_products_df = create_percentage_review_products_df(main_data_df)
monthly_orders_df = create_monthly_orders_df(main_data_df)

st.header('Hendro Submissions')

st.subheader('Most and Fewest Review Product Category')
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="percentage", y="product_category_name_english", hue="product_category_name_english", data=percentage_review_products_df.sort_values(by=("review_score", "sum"), ascending=False).head(5), palette=colors, ax=ax[0], legend=False)
ax[0].set_ylabel(None)
ax[0].set_xlabel("Percentage - %")
ax[0].set_title("Most Review Product Category", loc="center", fontsize=15)
ax[0].tick_params(axis="y", labelsize=12)

sns.barplot(x="percentage", y="product_category_name_english", hue="product_category_name_english", data=percentage_review_products_df.sort_values(by=("review_score", "sum"), ascending=True).head(5), palette=colors, ax=ax[1], legend=False)
ax[1].set_ylabel(None)
ax[1].set_xlabel("Percentage - %")
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Fewest Review Product Category", loc="center", fontsize=15)
ax[1].tick_params(axis="y", labelsize=12)

plt.suptitle("Most and Fewest Review Product Category (%)", fontsize=20)
st.pyplot(fig)


st.subheader('Number of Order with status Delivered per Month (2017)')

fig, ax = plt.subplots(figsize=(20, 10))

ax.plot(
    monthly_orders_df["monthly_value"],
    monthly_orders_df[("order_purchase_date", "count")],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_title("Number of Order with status Delivered per Month (2017)", fontsize=25)
st.pyplot(fig)