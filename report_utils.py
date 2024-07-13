import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from fpdf import FPDF
import tempfile
import os
import streamlit as st

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Data Analysis Report', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_image(self, image_path):
        self.image(image_path, x=10, w=190)
        self.ln(10)

def generate_pdf_report(df):
    """
    Generates a PDF report with analysis and visualizations based on the provided DataFrame.

    :param df: DataFrame containing the sales data.
    :return: Tuple containing the PDF buffer and the temporary PDF file path.
    """
    fig_paths = []
    analysis_summaries = []

    # Sales Distribution
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['SALES'], bins=30, kde=True, ax=ax)
    ax.set_title('Sales Distribution')
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_img:
        fig.savefig(tmp_img.name, format='PNG')
        fig_paths.append(tmp_img.name)
    analysis_summaries.append({
        'title': 'Sales Distribution',
        'body': 'The sales distribution chart shows the spread of sales amounts. The histogram reveals the frequency of sales within certain ranges, while the KDE line provides a smoother representation of the distribution.'
    })

    # Sales by Order Status
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='STATUS', y='SALES', data=df, ax=ax)
    ax.set_title('Sales by Order Status')
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_img:
        fig.savefig(tmp_img.name, format='PNG')
        fig_paths.append(tmp_img.name)
    analysis_summaries.append({
        'title': 'Sales by Order Status',
        'body': 'This boxplot shows the sales amounts categorized by order status. It highlights the distribution of sales for each status, including the median, quartiles, and potential outliers.'
    })

    # Sales by Quarter
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='QTR_ID', y='SALES', data=df, estimator=sum, ci=None, ax=ax)
    ax.set_title('Sales by Quarter')
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_img:
        fig.savefig(tmp_img.name, format='PNG')
        fig_paths.append(tmp_img.name)
    analysis_summaries.append({
        'title': 'Sales by Quarter',
        'body': 'This bar chart depicts the total sales for each quarter. It helps in understanding the seasonal sales patterns and identifying the quarters with the highest sales.'
    })

    # Sales by Product Line
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='PRODUCTLINE', y='SALES', data=df, estimator=sum, ci=None, ax=ax)
    ax.set_title('Sales by Product Line')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_img:
        fig.savefig(tmp_img.name, format='PNG')
        fig_paths.append(tmp_img.name)
    analysis_summaries.append({
        'title': 'Sales by Product Line',
        'body': 'This bar chart shows the total sales for each product line. It provides insights into which product lines contribute the most to the overall sales.'
    })

    # Top 10 Customers by Sales
    top_customers = df.groupby('CUSTOMERNAME')['SALES'].sum().nlargest(10).reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='SALES', y='CUSTOMERNAME', data=top_customers, ax=ax)
    ax.set_title('Top 10 Customers by Sales')
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_img:
        fig.savefig(tmp_img.name, format='PNG')
        fig_paths.append(tmp_img.name)
    analysis_summaries.append({
        'title': 'Top 10 Customers by Sales',
        'body': 'This bar chart identifies the top 10 customers by their total sales. It helps in recognizing key customers and understanding their importance to the business.'
    })

    pdf = PDF()
    pdf.add_page()
    
    for summary in analysis_summaries:
        pdf.chapter_title(summary['title'])
        pdf.chapter_body(summary['body'])

    for img_path in fig_paths:
        pdf.add_page()
        pdf.add_image(img_path)

    # Save PDF to a known location
    report_path = "./data_analysis_report.pdf"
    pdf.output(report_path)

    # Return the PDF buffer and path
    with open(report_path, 'rb') as f:
        pdf_buffer = f.read()

    # Clean up temporary image files
    for img_path in fig_paths:
        if os.path.exists(img_path):
            os.remove(img_path)

    return pdf_buffer, report_path



#code for testing mail and report
""" st.title('CSV to PDF Report Generator')

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Data Analysis")
    st.write(df.head())

    if st.button("Generate PDF Report"):
        pdf_buffer, tmp_pdf_path = generate_pdf_report(df)
        st.success('PDF report generated.')
        st.download_button(label="Download PDF", data=pdf_buffer, file_name="data_analysis_report.pdf")

        send_datetime_str = st.text_input("Enter the send date and time (YYYY-MM-DD HH:MM) if you want to schedule the email", "")
        if send_datetime_str:
            send_datetime = datetime.strptime(send_datetime_str, "%Y-%m-%d %H:%M")
        else:
            send_datetime = None

        send_email("management@example.com", "Data Analysis Report", "Please find attached the data analysis report.", tmp_pdf_path, "data_analysis_report.pdf", send_datetime)
 """