import streamlit as st
import plotly.express as px
import pandas as pd
import datetime
import os

_WAREHOUSE = 'CHANGE_ME'

if _WAREHOUSE.lower() == 'snowflake':
    from utils.connect_snowflake import download_data
elif _WAREHOUSE.lower() == 'bigquery':
    from utils.connect_bigquery import download_data
else:
    raise ValueError(f'{_WAREHOUSE} is not a currently supported warehouse, please choose from [Snowflake, BigQuery]')

data_sources = [
    ('products/brand_revenues', 'brand_revenues'),
    ('products/product_views', 'product_views'),
    ('products/revenue_categories', 'revenue_categories'),
    ('products/views_and_transactions', 'views_and_transactions'),
    ('products/product_list_performance', 'product_list_performance'),
    ('checkout/checkout_abandonment_rate', 'checkout_abandonment_rate'),
    ('checkout/checkout_funnel', 'checkout_funnel'),
    ('checkout/customer_order_count', 'customer_order_count'),
    ('checkout/guest_checkout_rate', 'guest_checkout_rate'),
    ('checkout/payment_methods', 'payment_methods'),
    ('checkout/transaction_quantity', 'transaction_quantity'),
    ('checkout/transaction_value', 'transaction_value'),
    ('carts/cart_abandonment_rate', 'cart_abandonment_rate'),
    ('carts/abandoned_products_top_5', 'abandoned_products_top_5'),
    ('sessions/sessions_funnel', 'sessions_funnel'),
]


def run_download_data(warehouse: str):
    data_load_state = st.text("Downloading data...")

    for query, name in data_sources:
        download_data(os.path.join('queries', f'{query}.sql'), f'{name}.csv')

    data_load_state.text("")
    st.experimental_rerun()




def main():

    # Set headers and titles
    st.set_page_config(layout="wide", page_title="Products")
    current_hour = datetime.datetime.now().hour
    if current_hour < 12:
        greeting = 'morning'
    elif current_hour < 18:
        greeting = 'afternoon'
    else:
        greeting = 'evening'
    st.title(f"Good {greeting}, welcome to your Snowplow E-commerce Insights dashboard")

    # Button to re-run and load the data
    if st.button('Refresh Data'):
        run_download_data(_WAREHOUSE)

    # Load the data from local files
    data = dict()
    data_load_state = st.text("Loading data...")
    for _, name in data_sources:
        data[name] = pd.read_csv(os.path.join('data', f'{name}.csv'))
    data_load_state.text("")


    ## Order Summary
    st.header("Order Summary")

    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

    with col1:
        st.metric(
            label = 'Transactions',
            value = sum(data['customer_order_count'].iloc[:,1])
        )

    with col2:
        st.metric(
            label = 'Avg. Order Value',
            value = '€' + str(round(data['transaction_value'].at[0, 'average_transaction_quantity'], 2))
        )

    with col3:
        st.metric(
            label = 'Avg. Basket Size',
            value = str(round(data['transaction_quantity'].at[0, 'average_transaction_quantity'], 2))
        )

    with col4:
        st.metric(
            label = 'Top Brand',
            value = data['brand_revenues'].at[0, 'product_brand'],
            delta= '€' + str(data['brand_revenues'].at[0, 'total_revenue'])
        )

    with col5:
        st.metric(
            label = 'Top Category',
            value = data['revenue_categories'].at[0, 'product_category'],
            delta= str(data['revenue_categories'].at[0, 'total_revenue']) + ' Units'
        )


    st.header("Product Summary")
    views_and_transactions = data['views_and_transactions'].rename(columns = {'views' : 'Views', 'transactions': 'Transactions'})
    col1, col2 = st.columns([1, 2])
    with col1:
        views_and_transactions["sizes"] = 2
        fig = px.scatter(views_and_transactions, x = 'Views', y= 'Transactions', hover_data = ['Views', 'Transactions', 'product_id'], size='sizes')

        fig.update_layout(
            height=300,
            width=700,
            margin={"l": 20, "r": 20, "t": 25, "b": 0},
            legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
            title_text="Views and Transactions of products"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.line(data['product_views'].rename(columns = {'product_views': 'Number of Views', 'date' : 'Date'}), x = 'Date', y = 'Number of Views')
        fig.update_layout(
            height=300,
            width=700,
            margin={"l": 20, "r": 20, "t": 25, "b": 0},
            legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
            title_text="Daily Product views"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.caption('Product List Performance')
    st.dataframe(data['product_list_performance'].rename(columns = {'product_list_name': 'Product List', 'list_views': 'List Views', 'product_viewed': 'Product List Clicks', 'cart_product': 'Product Adds to Basket', 'transact_product': 'Product Checkouts', 'unique_transactions': 'Unique Purchases', 'product_revenue': 'Product Revenue', 'CTR': ' Product List CTR'}), use_container_width = True)

    st.header("Checkout Overview")

    col1, col2 = st.columns([4, 1])
    with col2:
        st.metric(
                label = 'Checkout Abandonment Rate',
                value = str(round(data['checkout_abandonment_rate'].iat[0,0]* 100, 1)) + '%'
                )
        st.write('\n')
        st.write('\n')
        st.metric(
                label = 'Guest Checkout Rate',
                value = str(round(data['guest_checkout_rate'].iat[0,0]* 100, 1)) + '%'
                )

    with col1:
        fig = px.pie(data['payment_methods'], values = 'number_transactions', names = 'transaction_payment_method')
        fig.update_layout(
            height=300,
            width=700,
            xaxis=dict(tickformat=".2%"),
            yaxis=dict(tickformat=".2%"),
            margin={"l": 20, "r": 20, "t": 25, "b": 0},
            legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
            title_text="Payment Methods"
        )
        st.plotly_chart(fig, use_container_width=True)


    checkout_funnel = data['checkout_funnel'].rename(columns = {'session_entered_at_step' : 'Session Entered at Step', 'step' : 'Step', 'volume' : 'Volume'})
    fig = px.funnel(checkout_funnel, y='Volume', x='Step', color='Session Entered at Step')

    fig.update_layout(
        height=300,
        width=700,
        margin={"l": 20, "r": 20, "t": 25, "b": 0},
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
        title_text="Checkout Funnel"
    )
    st.plotly_chart(fig, use_container_width=True)

    grouped_checkout = checkout_funnel.drop(columns='Session Entered at Step').groupby(by = ['Step', 'checkout_step_number'], as_index=False).agg(Volume = ('Volume','sum')).sort_values('checkout_step_number')


    n_steps = len(grouped_checkout.index)

    cols = st.columns([1 for i in range(n_steps-1)])
    for i, col in enumerate(cols):
        with col:
            lost_num = grouped_checkout.at[i, 'Volume'] - grouped_checkout.at[i +1, 'Volume']
            lost_perc = round(lost_num/grouped_checkout.at[i, 'Volume']*100, 1)
            st.metric(
                label = '🔻'+ '\n' + f'Step {i+1} Dropoff',
                value =  str(lost_num)+ ' (' + str(lost_perc) +'%)'
                )

    st.header("Cart Insight")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.metric(
            label = 'Cart Abandonment Rate (daily)',
            value = str(round(data['cart_abandonment_rate'].at[0,'cart_abandonment_rate'] * 100, 1))+'%',
            delta = str(round((data['cart_abandonment_rate'].at[0,'cart_abandonment_rate'] - data['cart_abandonment_rate'].at[1,'cart_abandonment_rate'])*100, 1)) + '%',
            delta_color='inverse'
            )

    with col2:
        #TODO Last 5 abandoned products?
        fig = px.bar(data['abandoned_products_top_5'].rename(columns = {'total_abandoned': 'Total Abandoned'}), x = 'product_id', y = 'Total Abandoned')
        fig.update_layout(
            height=300,
            width=700,
            margin={"l": 20, "r": 20, "t": 25, "b": 0},
            legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
            title_text="Top 5 abandoned products"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Session Analysis")

    sessions_funnel = data['sessions_funnel'].rename(columns = {'session_entered_at_step' : 'Session Entered at Step', 'volume' : 'Volume', 'step' :'Step'})
    fig = px.funnel(sessions_funnel, y='Volume', x='Step', color='Session Entered at Step')

    fig.update_layout(
        height=300,
        width=700,
        margin={"l": 20, "r": 20, "t": 25, "b": 0},
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
        title_text="Sessions Funnel"
    )
    # fig.update_traces(marker_colorbar_yanchor='bottom', selector=dict(type='funnel'))
    fig.update_traces(marker_colorbar_xanchor='left', selector=dict(type='funnel'))
    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3, col4 , _ = st.columns([1, 1, 1, 1, 1])

    with col1:
        no_shop_num = sessions_funnel.at[0, 'Volume'] - sessions_funnel.at[1, 'Volume']
        no_shop_perc = round(no_shop_num/sessions_funnel.at[0, 'Volume']*100, 1)
        st.metric(
            label = '🔻'+ '\n' + 'No Shopping Activity',
            value = str(no_shop_num)+ ' (' + str(no_shop_perc) +'%)'
            )

    with col2:
        no_bask_num = sessions_funnel.at[1, 'Volume'] - sessions_funnel.at[2, 'Volume']
        no_bask_perc =  round(no_shop_num/sessions_funnel.at[1, 'Volume']*100, 1)
        st.metric(
            label = '🔻'+ '\n' + 'No Basket Addition',
            value = str(no_bask_num)+ ' (' + str(no_bask_perc) +'%)'
            )

    with col3:
        bask_adban_num = sessions_funnel.at[2, 'Volume'] - sessions_funnel.at[3, 'Volume']
        bask_adban_perc =  round(no_shop_num/sessions_funnel.at[2, 'Volume']*100, 1)
        st.metric(
            label = '🔻'+ '\n' + 'Basket Abandonment',
            value = str(bask_adban_num)+ ' (' + str(bask_adban_perc) +'%)'
            )

    with col4:
        check_aband_num = sessions_funnel.at[3, 'Volume'] - sessions_funnel.at[4, 'Volume']
        check_aband_perc =  round(check_aband_num/sessions_funnel.at[3, 'Volume']*100, 1)
        st.metric(
            label = '🔻'+ '\n' + 'Checkout Abandonment',
            value = str(check_aband_num)+ ' (' + str(check_aband_perc) +'%)'
            )


if __name__ == "__main__":
    main()
