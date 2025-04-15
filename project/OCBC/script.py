import mysql.connector
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from datetime import datetime

# Register font for multi-language support
pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",        # ✅ Change this
    password="Vasee@2002",    # ✅ Change this
    database="bank_db"
)

cursor = db.cursor()

# Fetch customers
cursor.execute("SELECT customer_name, account_number, address FROM customers")
customers = cursor.fetchall()

for customer in customers:
    customer_name, account_number, address = customer

    # Prepare PDF filename
    filename = f"statement_{account_number}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)

    # Draw bank logo
    logo = ImageReader('OCBC_logo.png')
    c.drawImage(logo, 50, 700, width=120, height=50)

    # Header
    c.setFont("DejaVuSans", 18)
    c.drawString(200, 730, "OCBC Bank Statement")

    # Customer Details
    c.setFont("DejaVuSans", 12)
    c.drawString(50, 680, f"Customer Name: {customer_name}")
    c.drawString(50, 660, f"Account Number: {account_number}")
    c.drawString(50, 640, f"Address: {address}")
    c.drawString(50, 620, f"Statement Date: {datetime.now().strftime('%Y-%m-%d')}")

    # Table Headers
    c.drawString(50, 590, "Date")
    c.drawString(150, 590, "Description")
    c.drawString(350, 590, "Amount")
    c.drawString(450, 590, "Type")

    # Fetch transactions
    cursor.execute("SELECT date, description, amount, type FROM transactions WHERE account_number = %s", (account_number,))
    transactions = cursor.fetchall()

    y = 570
    for transaction in transactions:
        date, description, amount, type_ = transaction
        c.drawString(50, y, date.strftime('%Y-%m-%d'))
        c.drawString(150, y, description)
        c.drawString(350, y, f"{amount:.2f}")
        c.drawString(450, y, type_)
        y -= 20

        if y < 100:  # New page if space runs out
            c.showPage()
            c.setFont("DejaVuSans", 12)
            y = 750

    c.save()

print("PDF Statements generated successfully!")
