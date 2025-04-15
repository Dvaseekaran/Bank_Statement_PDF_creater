import mysql.connector
import sys
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime

def create_database_and_table():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Vasee@2002'
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS bank_statements")
        cursor.execute("USE bank_statements")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date DATE,
                description VARCHAR(255),
                debit DECIMAL(10,2),
                credit DECIMAL(10,2),
                balance DECIMAL(10,2)
            )
        """)
        connection.commit()
        return True
    except mysql.connector.Error as e:
        print(f"Database creation error: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def insert_sample_data():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Vasee@2002',
            database='bank_statements'
        )
        cursor = connection.cursor()
        
        sample_data = [
            ('2024-03-02', 'Salary Credit', None, 7700.00, 5250.00),
            ('2024-03-05', 'ATM Withdrawal', 500.00, None, 4750.00),
            ('2024-03-08', 'Giro Payment', 300.00, None, 4450.00),
            ('2024-03-12', 'Bill Payment', 150.00, None, 4300.00),
            ('2024-03-18', 'Funds Transfer', None, 1200.00, 5500.00),
            ('2024-03-20', 'Cash Deposit', None, 200.00, 5700.00),
            ('2024-03-22', 'POS Purchase', 250.00, None, 5450.00),
            ('2024-03-28', 'ATM Withdrawal', 50.00, None, 5400.00),
            ('2024-03-30', 'Cheque Deposit', 500.00, 500.00, 5350.00)
        ]
        
        cursor.executemany("""
            INSERT INTO transactions (date, description, debit, credit, balance)
            VALUES (%s, %s, %s, %s, %s)
        """, sample_data)
        
        connection.commit()
        return True
    except mysql.connector.Error as e:
        print(f"Data insertion error: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def generate_statement():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Vasee@2002',
            database='bank_statements'
        )
        cursor = connection.cursor()
        
        cursor.execute("SELECT date, description, debit, credit, balance FROM transactions ORDER BY date")
        transactions = cursor.fetchall()
        
        if not transactions:
            print("No transactions found in the database")
            return False

        pdf_file = os.path.join(os.path.dirname(__file__), "ocbc_bank_statement.pdf")
        document = SimpleDocTemplate(pdf_file, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)

        styles = getSampleStyleSheet()
        style_normal = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            leading=14
        )
        
        elements = []

        # Add bank logo
        logo_path = os.path.join(os.path.dirname(__file__), "ocbc_logo.png")
        if os.path.exists(logo_path):
            im = Image(logo_path, width=2*inch, height=1*inch)
            im.hAlign = 'LEFT'
            elements.append(im)
            elements.append(Spacer(1, 20))

        # Account Information
        account_info = """
        <b>Account Number</b><br/>
        John Doe<br/>
        123-456789-0<br/><br/>
        <b>Statement Period</b><br/>
        31 Mar 2025 - 31 Mar 2025
        """
        elements.append(Paragraph(account_info, style_normal))
        elements.append(Spacer(1, 20))

        # Account Summary
        elements.append(Paragraph("<b>Account Summary</b>", style_normal))
        elements.append(Spacer(1, 10))

        summary_data = [
            ['Beginning Balance', 'MYR 2,500.00'],
            ['Total Credits', 'MYR 4,200.00'],
            ['Total Debits', 'MYR 1,350.00'],
            ['Ending Balance', 'MYR 5,350.00']
        ]
        
        summary_table = Table(summary_data, colWidths=[200, 100])
        summary_table.setStyle(TableStyle([
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 20))

        # Transaction History
        elements.append(Paragraph("<b>Transaction History</b>", style_normal))
        elements.append(Spacer(1, 10))

        # Transaction Table
        table_data = [['Date', 'Description', 'Debit', 'Credit', 'Balance']]
        
        for row in transactions:
            date, description, debit, credit, balance = row
            table_data.append([
                date.strftime('%d %b'),
                description,
                f"{debit:,.2f}" if debit else '—',
                f"{credit:,.2f}" if credit else '—',
                f"{balance:,.2f}"
            ])

        transaction_table = Table(table_data, colWidths=[60, 200, 80, 80, 80])
        transaction_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))

        elements.append(transaction_table)

        # Footer
        elements.append(Spacer(1, 30))
        footer_text = """
        This is a computer-generated document. No signature is required.<br/><br/>
        For assistance, please call our Customer Service Hotline at 1800 363 3333<br/>
        or visit www.ocbc.com.
        """
        elements.append(Paragraph(footer_text, style_normal))

        document.build(elements)
        print("PDF statement generated successfully:", pdf_file)
        return True

    except Exception as e:
        print(f"Error generating statement: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def main():
    if not create_database_and_table():
        sys.exit(1)
    
    if not insert_sample_data():
        sys.exit(1)
    
    if not generate_statement():
        sys.exit(1)

if __name__ == "__main__":
    main()
