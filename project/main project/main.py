import mysql.connector
import msvcrt
from reportlab.pdfgen import canvas
import os
from datetime import datetime
from decimal import Decimal
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import sys
import logging
from PIL import Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import random

logging.basicConfig(
    filename='bank_system.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
# After the imports, before LANGUAGES dictionary
try:
    font_paths = [
        'C:\\Windows\\Fonts\\latha.ttf',
        'C:\\Windows\\Fonts\\Latha.ttf',
        'C:\\WINDOWS\\Fonts\\latha.ttf',
        'C:\\WINDOWS\\Fonts\\Latha.ttf'
    ]
    TAMIL_FONT_AVAILABLE = False
    for font_path in font_paths:
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont('Latha', font_path))
            TAMIL_FONT_AVAILABLE = True
            break
    if not TAMIL_FONT_AVAILABLE:  # Fix indentation here
        logging.warning("Tamil font (Latha) not found in any standard locations")
except Exception as e:
    TAMIL_FONT_AVAILABLE = False
    logging.warning(f"Tamil font registration failed: {str(e)}") 
LANGUAGES = {
    'en': {
        'welcome': 'Welcome to OCBC Bank System',
        'login': 'Login',
        'create_account': 'Create Account', 
        'exit': 'Exit',
        'add_credit_card': 'Add Credit Card',
        'enter_choice': 'Enter your choice: ', 
        'balance': 'Current balance',
        'transaction_history': 'Transaction History',
        'date': 'Date',
        'type': 'Type',
        'amount': 'Amount',
        'make_credit_card_transaction': 'Make Credit Card Transaction',
        'description': 'Description',
        'generated_on': 'Generated on',
        'account': 'Account',
        'deposit': 'Deposit',
        'withdrawal': 'Withdrawal',
        'user_menu': 'User Menu',
        'show_balance': 'Show Balance',
        'deposit_money': 'Deposit Money',
        'withdraw_money': 'Withdraw Money',
        'show_history': 'Show Transaction History',
        'download_history': 'Download Transaction History as PDF',
        'logout': 'Logout',
        'goodbye': 'Thank you for using OCBC Bank System. Goodbye!',
        'invalid_choice': 'Invalid choice. Please try again.',
        'enter_amount': 'Enter amount: SGD ',
        'invalid_amount': 'Invalid amount. Please enter a positive value.',
        'insufficient_balance': 'Insufficient balance.',
        'account_not_found': 'Account not found.',
        'no_transactions': 'No transactions found.',
        'full_name': 'Full Name',
        'aadhar': 'Aadhaar Number',
        'email': 'Email',
        'phone': 'Phone Number',
        'password': 'Password',
        'account_created': 'Account created successfully!',
        'account_number': 'Your Account Number',
        'user_exists': 'This user already exists (duplicate email, phone, or Aadhaar).',
        'welcome_back': 'Welcome back',
        'invalid_credentials': 'Invalid credentials. Please try again.',
        'deposit_successful': 'Deposit successful! New balance',
        'withdrawal_successful': 'Withdrawal successful! New balance',
        'logged_out': 'Logged out successfully.',
        'pdf_generated': 'Transaction history PDF generated successfully!',
        'file_saved': 'File saved at',
        'choose_option': 'Choose an option',
        'statement_period': 'Statement Period',
        'beginning_balance': 'Beginning Balance',
        'ending_balance': 'Ending Balance',
        'total_credits': 'Total Credits',
        'total_debits': 'Total Debits',
        'account_summary': 'Account Summary',
        'debit': 'Debit',
        'credit': 'Credit',
        'credit_card_statement': 'Credit Card Statement',
        'no_credit_card': 'No credit card found',
        'credit_card_statement_generated': 'Credit card statement generated successfully!',
        'merchant': 'Merchant',
        'reward_points': 'Reward Points',
        'credit_limit': 'Credit Limit',
        'outstanding_balance': 'Outstanding Balance',
        'due_date': 'Due Date',
        'download_credit_card_statement': 'Download Credit Card Statement',
        'statement_date': 'Statement Date',
        'card_type': 'Card Type',
        'credit_card_statement': 'Credit Card Statement'
        
    },
    'ms': {
        'welcome': 'Selamat datang ke Sistem Bank OCBC',
        'login': 'Log Masuk',
        'create_account': 'Buat Akaun',
        'exit': 'Keluar',
        'add_credit_card': 'Tambah Kad Kredit',
        'balance': 'Baki semasa',
        'enter_choice': 'Masukkan pilihan anda: ',
        'transaction_history': 'Sejarah Transaksi',
        'date': 'Tarikh',
        'type': 'Jenis',
        'amount': 'Jumlah',
        'make_credit_card_transaction': 'Buat Transaksi Kad Kredit',
        'description': 'Keterangan',
        'generated_on': 'Dijana pada',
        'account': 'Akaun',
        'deposit': 'Deposit',
        'withdrawal': 'Pengeluaran',
        'user_menu': 'Menu Pengguna',
        'show_balance': 'Tunjuk Baki',
        'deposit_money': 'Deposit Wang',
        'withdraw_money': 'Pengeluaran Wang',
        'show_history': 'Tunjuk Sejarah Transaksi',
        'download_history': 'Muat Turun Sejarah Transaksi PDF',
        'logout': 'Log Keluar',
        'goodbye': 'Terima kasih kerana menggunakan Sistem Bank OCBC. Selamat tinggal!',
        'invalid_choice': 'Pilihan tidak sah. Sila cuba lagi.',
        'enter_amount': 'Masukkan jumlah: SGD ',
        'invalid_amount': 'Jumlah tidak sah. Sila masukkan nilai positif.',
        'insufficient_balance': 'Baki tidak mencukupi.',
        'account_not_found': 'Akaun tidak dijumpai.',
        'no_transactions': 'Tiada transaksi dijumpai.',
        'full_name': 'Nama Penuh',
        'aadhar': 'Nombor Aadhaar',
        'email': 'Emel',
        'phone': 'Nombor Telefon',
        'password': 'Kata Laluan',
        'account_created': 'Akaun berjaya dibuat!',
        'account_number': 'Nombor Akaun Anda',
        'user_exists': 'Pengguna ini sudah wujud (emel, telefon, atau Aadhaar pendua).',
        'welcome_back': 'Selamat kembali',
        'invalid_credentials': 'Kelayakan tidak sah. Sila cuba lagi.',
        'deposit_successful': 'Deposit berjaya! Baki baru',
        'withdrawal_successful': 'Pengeluaran berjaya! Baki baru',
        'logged_out': 'Berjaya log keluar.',
        'pdf_generated': 'PDF sejarah transaksi berjaya dijana!',
        'file_saved': 'Fail disimpan di',
        'choose_option': 'Pilih pilihan',
        'statement_period': 'Tempoh Penyata',
        'beginning_balance': 'Baki Permulaan',
        'ending_balance': 'Baki Akhir', 
        'total_credits': 'Jumlah Kredit',
        'total_debits': 'Jumlah Debit',
        'account_summary': 'Ringkasan Akaun',
        'debit': 'Debit',
        'credit': 'Kredit',
        'credit_card_statement': 'Penyata Kad Kredit',
        'no_credit_card': 'Tiada kad kredit dijumpai',
        'credit_card_statement_generated': 'Penyata kad kredit berjaya dijana!',
        'merchant': 'Peniaga',
        'reward_points': 'Mata Ganjaran',
        'credit_limit': 'Had Kredit',
        'outstanding_balance': 'Baki Tertunggak',
        'due_date': 'Tarikh Akhir',
        'statement_date': 'Tarikh Penyata',
        'card_type': 'Jenis Kad',
        'credit_card_statement': 'Penyata Kad Kredit',
        'no_credit_card': 'Tiada kad kredit dijumpai',
        'credit_card_statement_generated': 'Penyata kad kredit berjaya dijana!',
        'merchant': 'Peniaga',
        'reward_points': 'Mata Ganjaran',
        'download_credit_card_statement': 'Muat Turun Penyata Kad Kredit',
        'credit_limit': 'Had Kredit',
        'outstanding_balance': 'Baki Tertunggak',
        'due_date': 'Tarikh Akhir',
        'statement_date': 'Tarikh Penyata',
        'card_type': 'Jenis Kad'
    },
    'zh': {
        'welcome': 'OCBC银行系统欢迎您',
        'login': '登录',
        'add_credit_card': '添加信用卡',
        'create_account': '创建账户',
        'exit': '退出',
        'balance': '当前余额',
        'transaction_history': '交易历史',
        'date': '日期',
        'type': '类型',
        'enter_choice': '请输入您的选择：',
        'amount': '金额',
        'make_credit_card_transaction': '进行信用卡交易',
        'description': '说明',
        'generated_on': '生成于',
        'account': '账户',
        'deposit': '存款',
        'withdrawal': '取款',
        'user_menu': '用户菜单',
        'show_balance': '显示余额',
        'deposit_money': '存入资金',
        'withdraw_money': '取出资金',
        'show_history': '显示交易历史',
        'download_history': '下载交易历史PDF',
        'logout': '登出',
        'goodbye': '感谢使用OCBC银行系统。再见！',
        'invalid_choice': '选择无效。请重试。',
        'enter_amount': '输入金额：SGD ',
        'invalid_amount': '金额无效。请输入正值。',
        'insufficient_balance': '余额不足。',
        'account_not_found': '未找到账户。',
        'no_transactions': '未找到交易。',
        'full_name': '全名',
        'aadhar': 'Aadhaar号码',
        'email': '电子邮件',
        'phone': '电话号码',
        'password': '密码',
        'account_created': '账户创建成功！',
        'account_number': '您的账号',
        'user_exists': '该用户已存在（电子邮件、电话或Aadhaar重复）。',
        'welcome_back': '欢迎回来',
        'invalid_credentials': '凭据无效。请重试。',
        'deposit_successful': '存款成功！新余额',
        'withdrawal_successful': '取款成功！新余额',
        'logged_out': '成功登出。',
        'pdf_generated': '交易历史PDF生成成功！',
        'file_saved': '文件保存在',
        'choose_option': '选择选项',
        'statement_period': '对账单期间',
        'beginning_balance': '期初余额',
        'ending_balance': '期末余额',
        'total_credits': '总存入',
        'total_debits': '总支出',
        'account_summary': '账户摘要',
        'debit': '支出',
        'credit': '存入',
        'credit_card_statement': '信用卡对账单',
        'no_credit_card': '未找到信用卡',
        'credit_card_statement_generated': '信用卡对账单生成成功！',
        'merchant': '商户',
        'reward_points': '奖励积分',
        'credit_limit': '信用额度',
        'outstanding_balance': '未结余额',
        'due_date': '到期日',
        'statement_date': '账单日期',
        'card_type': '卡片类型',
        'credit_card_statement': '信用卡对账单',
        'no_credit_card': '未找到信用卡',
        'credit_card_statement_generated': '信用卡对账单生成成功！',
        'merchant': '商户',
        'download_credit_card_statement': '下载信用卡对账单',
        'reward_points': '奖励积分',
        'credit_limit': '信用额度',
        'outstanding_balance': '未结余额',
        'due_date': '到期日',
        'statement_date': '账单日期',
        'card_type': '卡片类型'
    },
    'ta': {
        'welcome': 'OCBC வங்கி அமைப்புக்கு வரவேற்கிறோம்',
        'login': 'உள்நுழைவு',
        'create_account': 'கணக்கை உருவாக்கு',
        'exit': 'வெளியேறு',
        'balance': 'தற்போதைய இருப்பு',
        'transaction_history': 'பரிவர்த்தனை வரலாறு',
        'date': 'தேதி',
        'add_credit_card': 'கிரெடிட் கார்டு சேர்க்க',
        'type': 'வகை',
        'amount': 'தொகை',
        'enter_choice': 'உங்கள் தேர்வை உள்ளிடவும்: ',
        'description': 'விளக்கம்',
        'generated_on': 'உருவாக்கப்பட்டது',
        'generated_document': 'இது கணினி உருவாக்கிய ஆவணம். கையொப்பம் தேவையில்லை.',
        'customer_service': 'உதவிக்கு, எங்கள் வாடிக்கையாளர் சேவை எண் 1800 363 3333ஐ அழைக்கவும்',
        'account': 'கணக்கு', 
        'deposit': 'வைப்பு',
        'make_credit_card_transaction': 'கிரெடிட் கார்டு பரிவர்த்தனை செய்க',
        'withdrawal': 'பணம் எடுப்பு',
        'user_menu': 'பயனர் மெனு',
        'show_balance': 'இருப்பைக் காட்டு',
        'deposit_money': 'பணம் வைப்பு',
        'withdraw_money': 'பணம் எடுப்பு',
        'show_history': 'பரிவர்த்தனை வரலாற்றைக் காட்டு',
        'download_history': 'பரிவர்த்தனை வரலாற்று PDF-ஐ பதிவிறக்கு',
        'logout': 'வெளியேறு',
        'goodbye': 'OCBC வங்கி அமைப்பைப் பயன்படுத்தியதற்கு நன்றி. பிரியாவிடை!',
        'invalid_choice': 'தவறான தேர்வு. மீண்டும் முயற்சிக்கவும்.',
        'enter_amount': 'தொகையை உள்ளிடவும்: SGD ',
        'invalid_amount': 'தவறான தொகை. நேர்மறை மதிப்பை உள்ளிடவும்.',
        'insufficient_balance': 'போதுமான இருப்பு இல்லை.',
        'account_not_found': 'கணக்கு கிடைக்கவில்லை.',
        'no_transactions': 'பரிவர்த்தனைகள் எதுவும் இல்லை.',
        'full_name': 'முழு பெயர்',
        'aadhar': 'ஆதார் எண்',
        'email': 'மின்னஞ்சல்',
        'phone': 'தொலைபேசி எண்',
        'password': 'கடவுச்சொல்',
        'account_created': 'கணக்கு வெற்றிகரமாக உருவாக்கப்பட்டது!',
        'account_number': 'உங்கள் கணக்கு எண்',
        'user_exists': 'இந்த பயனர் ஏற்கனவே உள்ளார் (மின்னஞ்சல், தொலைபேசி அல்லது ஆதார் நகல்).',
        'welcome_back': 'மீண்டும் வரவேற்கிறோம்',
        'invalid_credentials': 'தவறான சான்றுகள். மீண்டும் முயற்சிக்கவும்.',
        'deposit_successful': 'வைப்பு வெற்றி! புதிய இருப்பு',
        'withdrawal_successful': 'பணம் எடுப்பு வெற்றி! புதிய இருப்பு',
        'logged_out': 'வெற்றிகரமாக வெளியேறியது.',
        'pdf_generated': 'பரிவர்த்தனை வரலாற்று PDF வெற்றிகரமாக உருவாக்கப்பட்டது!',
        'file_saved': 'கோப்பு சேமிக்கப்பட்டது',
        'choose_option': 'விருப்பத்தை தேர்வு செய்க',
        'statement_period': 'அறிக்கை காலம்',
        'beginning_balance': 'தொடக்க இருப்பு',
        'ending_balance': 'இறுதி இருப்பு',
        'total_credits': 'மொத்த வரவு',
        'total_debits': 'மொத்த செலவு',
        'account_summary': 'கணக்கு சுருக்கம்',
        'debit': 'பற்று',
        'credit': 'வரவு',
        'credit_card_statement': 'கிரெடிட் கார்டு அறிக்கை',
        'no_credit_card': 'கிரெடிட் கார்டு கிடைக்கவில்லை',
        'credit_card_statement_generated': 'கிரெடிட் கார்டு அறிக்கை வெற்றிகரமாக உருவாக்கப்பட்டது!',
        'merchant': 'வணிகர்',
        'reward_points': 'ரிவார்டு புள்ளிகள்',
        'credit_limit': 'கிரெடிட் வரம்பு',
        'outstanding_balance': 'நிலுவை தொகை',
        'due_date': 'செலுத்த வேண்டிய தேதி',
        'statement_date': 'அறிக்கை தேதி',
        'card_type': 'கார்டு வகை',
        'credit_card_statement': 'கிரெடிட் கார்டு அறிக்கை',
        'no_credit_card': 'கிரெடிட் கார்டு கிடைக்கவில்லை',
        'credit_card_statement_generated': 'கிரெடிட் கார்டு அறிக்கை வெற்றிகரமாக உருவாக்கப்பட்டது!',
        'merchant': 'வணிகர்',
        'reward_points': 'ரிவார்டு புள்ளிகள்',
        'credit_limit': 'கிரெடிட் வரம்பு',
        'download_credit_card_statement': 'கிரெடிட் கார்டு அறிக்கையைப் பதிவிறக்கு',
        'outstanding_balance': 'நிலுவை தொகை',
        'due_date': 'செலுத்த வேண்டிய தேதி',
        'statement_date': 'அறிக்கை தேதி',
        'card_type': 'கார்டு வகை'
    }
}

def check_logo_exists():
    logo_path = os.path.join(os.path.dirname(__file__), "ocbc_logo.png")
    if not os.path.exists(logo_path):
        print("\n⚠️ Warning: Bank logo not found at:", logo_path)
        logging.warning(f"Bank logo not found at: {logo_path}")
        return False
    return True

def select_language():
    print("\nSelect Language / Pilih Bahasa / 选择语言 / மொழியைத் தேர்ந்தெடுக்கவும்:")
    print("1. English")
    print("2. Bahasa Melayu")
    print("3. 中文")
    print("4. தமிழ்")
    choice = input("Choose (1-4): ")
    
    lang_map = {'1': 'en', '2': 'ms', '3': 'zh', '4': 'ta'}
    return lang_map.get(choice, 'en')

def get_password():
    print("Password: ", end='', flush=True)
    password = ""
    while True:
        char = msvcrt.getch()
        if char == b'\r':
            print()
            return password
        elif char == b'\x08':
            if password:
                password = password[:-1]
                print('\b \b', end='', flush=True)
        else:
            try:
                char_decoded = char.decode('utf-8')
                password += char_decoded
                print('*', end='', flush=True)
            except UnicodeDecodeError:
                continue

def connect_to_database(max_attempts=3):
    attempt = 1
    while attempt <= max_attempts:
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Vasee@2002",
                database="ocbc_bank",
                connect_timeout=10
            )
            return db
        except mysql.connector.Error as err:
            if attempt == max_attempts:
                print(f"\n❌ Database Error: {err}")
                logging.error(f"Database connection error: {err}")
                sys.exit(1)
            print(f"\nAttempt {attempt} failed. Retrying...")
            logging.warning(f"Database connection attempt {attempt} failed: {err}")
            attempt += 1
            time.sleep(2)  # Wait 2 seconds before retrying

try:
    # Add import for time module at the top if not already present
    import time
    
    db = connect_to_database()
    cursor = db.cursor(buffered=True)
    
    cursor.execute("CREATE DATABASE IF NOT EXISTS ocbc_bank")
    cursor.execute("USE ocbc_bank")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(100) NOT NULL,
            aadhar_number VARCHAR(12) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone_number VARCHAR(15) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Accounts (
            account_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            account_number VARCHAR(20) UNIQUE NOT NULL,
            account_type VARCHAR(20) NOT NULL,
            balance DECIMAL(15,2) DEFAULT 0.00,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Transactions (
            transaction_id INT AUTO_INCREMENT PRIMARY KEY,
            account_id INT NOT NULL,
            transaction_type VARCHAR(20) NOT NULL,
            amount DECIMAL(15,2) NOT NULL,
            description TEXT,
            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CreditCards (
            card_id INT AUTO_INCREMENT PRIMARY KEY,
            account_id INT NOT NULL,
            card_number VARCHAR(16) UNIQUE NOT NULL,
            card_type VARCHAR(50) NOT NULL,
            credit_limit DECIMAL(15,2) NOT NULL,
            outstanding_balance DECIMAL(15,2) DEFAULT 0.00,
            statement_date DATE,
            due_date DATE,
            FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CardTransactions (
            transaction_id INT AUTO_INCREMENT PRIMARY KEY,
            card_id INT NOT NULL,
            transaction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            merchant_name VARCHAR(100) NOT NULL,
            amount DECIMAL(15,2) NOT NULL,
            transaction_type VARCHAR(20) NOT NULL,
            reward_points DECIMAL(10,2) DEFAULT 0,
            FOREIGN KEY (card_id) REFERENCES CreditCards(card_id)
        )
        """)
    db.commit()
    print("\n✅ Database connected successfully!")
    logging.info("Database connection established")

except mysql.connector.Error as err:
    print(f"\n❌ Database Error: {err}")
    logging.error(f"Database connection error: {err}")
    sys.exit(1)

def create_account(texts):
    print(f"\n--- {texts['create_account']} ---")
    
    # Add input validation
    while True:
        full_name = input(f"{texts['full_name']}: ").strip()
        if len(full_name) > 0:
            break
        print("Name cannot be empty")
        
    while True:
        aadhar = input(f"{texts['aadhar']}: ").strip()
        if aadhar.isdigit() and len(aadhar) == 12:
            break
        print("Aadhaar number must be 12 digits")
    email = input(f"{texts['email']}: ")
    phone = input(f"{texts['phone']}: ")
    password = get_password()
    
    password_hash = password[::-1]

    try:
        cursor.execute(
            "INSERT INTO Users (full_name, aadhar_number, email, phone_number, password_hash) VALUES (%s, %s, %s, %s, %s)",
            (full_name, aadhar, email, phone, password_hash)
        )
        db.commit()

        user_id = cursor.lastrowid
        account_number = f"AC{str(user_id).zfill(6)}"
        
        cursor.execute(
            "INSERT INTO Accounts (user_id, account_number, account_type, balance) VALUES (%s, %s, %s, %s)",
            (user_id, account_number, "Savings", Decimal('0.00'))
        )
        db.commit()
        
        print(f"\n✅ {texts['account_created']}")
        print(f"{texts['account_number']}: {account_number}")
        
    except mysql.connector.Error as err:
        db.rollback()
        if err.errno == 1062:
            print(f"\n❌ {texts['user_exists']}")
        else:
            print(f"\n❌ Error: {err}")

def login(texts):
    print(f"\n--- {texts['login']} ---")
    account_number = input(f"{texts['account_number']}: ")
    password = get_password()
    password_hash = password[::-1]

    try:
        cursor.execute("""
            SELECT U.user_id, U.full_name 
            FROM Users U
            JOIN Accounts A ON U.user_id = A.user_id
            WHERE A.account_number = %s AND U.password_hash = %s
        """, (account_number, password_hash))
        user = cursor.fetchone()
        
        if user:
            print(f"\n✅ {texts['welcome_back']}, {user[1]}!")
            user_menu(user[0], texts)
        else:
            print(f"\n❌ {texts['invalid_credentials']}")
    except mysql.connector.Error as err:
        print(f"\n❌ Error: {err}")

def deposit_money(user_id, texts):
    try:
        cursor.execute("""
            SELECT account_id, account_number, balance 
            FROM Accounts 
            WHERE user_id = %s
        """, (user_id,))
        account = cursor.fetchone()
        
        if not account:
            print(f"\n❌ {texts['account_not_found']}")
            return
            
        print(f"\n💰 {texts['balance']}: SGD {account[2]:,.2f}")
        amount = Decimal(input(f"{texts['enter_amount']}"))
        
        if amount <= Decimal('0'):
            print(f"\n❌ {texts['invalid_amount']}")
            return
            
        new_balance = account[2] + amount
        cursor.execute(
            "UPDATE Accounts SET balance = %s WHERE account_id = %s",
            (new_balance, account[0])
        )
        
        cursor.execute(
            "INSERT INTO Transactions (account_id, transaction_type, amount, description) VALUES (%s, %s, %s, %s)",
            (account[0], 'deposit', amount, texts['deposit'])
        )
        
        db.commit()
        print(f"\n✅ {texts['deposit_successful']}: SGD {new_balance:,.2f}")
        
    except mysql.connector.Error as err:
        db.rollback()
        print(f"\n❌ Error: {err}")
    except ValueError:
        print(f"\n❌ {texts['invalid_amount']}")

def withdraw_money(user_id, texts):
    try:
        cursor.execute("""
            SELECT account_id, account_number, balance 
            FROM Accounts 
            WHERE user_id = %s
        """, (user_id,))
        account = cursor.fetchone()
        
        if not account:
            print(f"\n❌ {texts['account_not_found']}")
            return
            
        print(f"\n💰 {texts['balance']}: SGD {account[2]:,.2f}")
        amount = Decimal(input(f"{texts['enter_amount']}"))
        
        if amount <= Decimal('0'):
            print(f"\n❌ {texts['invalid_amount']}")
            return
            
        if amount > account[2]:
            print(f"\n❌ {texts['insufficient_balance']}")
            return
            
        new_balance = account[2] - amount
        cursor.execute(
            "UPDATE Accounts SET balance = %s WHERE account_id = %s",
            (new_balance, account[0])
        )
        
        cursor.execute(
            "INSERT INTO Transactions (account_id, transaction_type, amount, description) VALUES (%s, %s, %s, %s)",
            (account[0], 'withdrawal', amount, texts['withdrawal'])
        )
        
        db.commit()
        print(f"\n✅ {texts['withdrawal_successful']}: SGD {new_balance:,.2f}")
        
    except mysql.connector.Error as err:
        db.rollback()
        print(f"\n❌ Error: {err}")
    except ValueError:
        print(f"\n❌ {texts['invalid_amount']}")

def show_balance(user_id, texts):
    try:
        cursor.execute("""
            SELECT account_number, balance 
            FROM Accounts 
            WHERE user_id = %s
        """, (user_id,))
        account = cursor.fetchone()
        if account:
            print(f"\n💰 {texts['account']} {account[0]}")
            print(f"{texts['balance']}: SGD {account[1]:,.2f}")
        else:
            print(f"\n❌ {texts['account_not_found']}")
    except mysql.connector.Error as err:
        print(f"\n❌ Error: {err}")

def show_transaction_history(user_id, texts):
    try:
        cursor.execute("""
            SELECT T.transaction_date, T.transaction_type, T.amount, T.description
            FROM Transactions T
            JOIN Accounts A ON T.account_id = A.account_id
            WHERE A.user_id = %s
            ORDER BY T.transaction_date DESC
        """, (user_id,))

        transactions = cursor.fetchall()
        if not transactions:
            print(f"\n📂 {texts['no_transactions']}")
            return

        print(f"\n📄 {texts['transaction_history']}:")
        print(f"{texts['date']} | {texts['type']} | {texts['amount']} | {texts['description']}")
        print("-" * 60)
        for txn in transactions:
            date, txn_type, amount, desc = txn
            trans_type = texts['deposit'] if txn_type == 'deposit' else texts['withdrawal']
            print(f"{date.strftime('%Y-%m-%d %H:%M')} | {trans_type} | SGD {amount:,.2f} | {desc}")

    except mysql.connector.Error as err:
        print(f"\n❌ Error: {err}")

def check_db_connection():
    try:
        if not db.is_connected():
            db.reconnect()
            logging.info("Database reconnected successfully")
    except Exception as e:
        logging.error(f"Database reconnection failed: {str(e)}")
        return False
    return True
    
def download_transaction_history(user_id, texts):
    try:
        cursor.execute("""
            SELECT 
                A.account_number,
                U.full_name,
                A.balance as current_balance,
                (SELECT COALESCE(SUM(amount), 0) FROM Transactions 
                 WHERE account_id = A.account_id AND transaction_type = 'deposit') as total_credits,
                (SELECT COALESCE(SUM(amount), 0) FROM Transactions 
                 WHERE account_id = A.account_id AND transaction_type = 'withdrawal') as total_debits,
                T.transaction_date,
                T.transaction_type,
                T.amount,
                T.description
            FROM Accounts A
            JOIN Users U ON A.user_id = U.user_id
            LEFT JOIN Transactions T ON A.account_id = T.account_id
            WHERE A.user_id = %s
            ORDER BY T.transaction_date DESC
        """, (user_id,))
        
        results = cursor.fetchall()
        if not results:
            print(f"\n📂 {texts['no_transactions']}")
            return
        
        if 'வரவேற்கிறோம்' in texts['welcome'] and TAMIL_FONT_AVAILABLE:
            pdf_font = 'Latha'
            pdf_font_bold = 'Latha'
        else:
            pdf_font = 'Helvetica'
            pdf_font_bold = 'Helvetica-Bold'

        account_number = results[0][0]
        customer_name = results[0][1]
        current_balance = results[0][2]
        total_credits = results[0][3]
        total_debits = results[0][4]

        reports_dir = os.path.join(os.getcwd(), "reports")
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)

        filename = f"Statement_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(reports_dir, filename)
        
        c = canvas.Canvas(filepath, pagesize=letter)
        c._doc.setTitle(texts['transaction_history'])
        
        logo_path = os.path.join(os.path.dirname(__file__), "ocbc_logo.png")
        if os.path.exists(logo_path):
            c.drawImage(logo_path, 50, 700, width=150, height=75, mask='auto')

        c.setFont(pdf_font_bold, 12)
        c.drawString(50, 670, texts['account'])
        c.setFont(pdf_font, 12)
        c.drawString(50, 650, customer_name)
        c.drawString(50, 630, account_number)

        start_date = datetime.now().replace(day=1).strftime('%d %b %Y')
        end_date = datetime.now().strftime('%d %b %Y')
        c.setFont(pdf_font_bold, 12)
        c.drawString(50, 600, texts['statement_period'])
        c.setFont(pdf_font_bold, 12)
        c.drawString(50, 580, f"{start_date} - {end_date}")

        c.setFont(pdf_font, 12)
        c.drawString(50, 550, texts['account_summary'])
        c.line(50, 545, 550, 545)
        
        c.setFont(pdf_font_bold, 11)
        c.drawString(50, 530, texts['beginning_balance'])
        c.drawString(450, 530, f"SGD {(current_balance - total_credits + total_debits):,.2f}")
        
        c.drawString(50, 515, texts['total_credits'])
        c.drawString(450, 515, f"SGD {total_credits:,.2f}")
        
        c.drawString(50, 500, texts['total_debits'])
        c.drawString(450, 500, f"SGD {total_debits:,.2f}")
        
        c.drawString(50, 485, texts['ending_balance'])
        c.drawString(450, 485, f"SGD {current_balance:,.2f}")

        c.setFont(pdf_font_bold, 12)
        c.drawString(50, 455, texts['transaction_history'])
        c.line(50, 450, 550, 450)

        y = 430
        c.setFont(pdf_font_bold, 11)
        c.drawString(50, y, texts['date'])
        c.drawString(150, y, texts['description'])
        c.drawString(300, y, texts['debit'])
        c.drawString(375, y, texts['credit'])
        c.drawString(450, y, texts['balance'])
        c.line(50, y-5, 550, y-5)

        running_balance = current_balance
        y -= 25
        c.setFont(pdf_font, 10)
        
        for transaction in results:
            if transaction[5]:
                if y < 50:
                    c.showPage()
                    y = 750
                    c.setFont(pdf_font, 10)

                date = transaction[5].strftime('%d %b')
                txn_type = transaction[6]
                amount = transaction[7]
                desc = transaction[8]
                desc = texts['deposit'] if txn_type == 'deposit' else texts['withdrawal']
                c.drawString(50, y, date)
                c.drawString(150, y, desc)
                
                if txn_type == 'withdrawal':
                    c.drawString(300, y, f"SGD {amount:,.2f}")
                    running_balance += amount
                else:
                    c.drawString(375, y, f"SGD {amount:,.2f}")
                    running_balance -= amount
                
                c.drawString(450, y, f"SGD {running_balance:,.2f}")
                y -= 20

        c.setFont(pdf_font, 8)
        c.drawString(50, 30, texts.get('generated_document', "This is a computer-generated document. No signature is required."))
        c.drawString(50, 15, texts.get('customer_service', "For assistance, please call our Customer Service Hotline at 1800 363 3333"))
        abs_filepath = os.path.abspath(filepath)
        c.save()
        print(f"\n✅ {texts['pdf_generated']}")
        print(f"📍 {texts['file_saved']}: {abs_filepath}")
        try:
            os.startfile(abs_filepath)
        except Exception as e:
            logging.error(f"Failed to open PDF: {str(e)}")
            print("PDF generated but could not be opened automatically.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        logging.error(f"PDF generation error: {str(e)}")
        
def add_credit_card(user_id, texts):
    try:
        # Check if user has an account
        cursor.execute("SELECT account_id FROM Accounts WHERE user_id = %s", (user_id,))
        account = cursor.fetchone()
        if not account:
            print(f"\n❌ {texts['account_not_found']}")
            return

        # Generate card number (16 digits)
        card_number = f"4532{str(account[0]).zfill(12)}"
        
        # Set default credit limit
        credit_limit = Decimal('5000.00')
        
        # Set statement date and due date
        statement_date = datetime.now().replace(day=1)
        due_date = statement_date.replace(day=25)
        
        cursor.execute("""
            INSERT INTO CreditCards 
            (account_id, card_number, card_type, credit_limit, statement_date, due_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (account[0], card_number, "Classic", credit_limit, statement_date, due_date))
        
        db.commit()
        print("\n✅ Credit card added successfully!")
        print(f"Card Number: ****{card_number[-4:]}")
        print(f"Credit Limit: SGD {credit_limit:,.2f}")
        
    except mysql.connector.Error as err:
        db.rollback()
        print(f"\n❌ Error: {err}")
        logging.error(f"Credit card creation error: {str(err)}")

# Update user_menu to include the new option
# def user_menu(user_id, texts):
    while True:
        if not check_db_connection():
            print("Database connection lost. Please try again later.")
            break
        print(f"\n--- {texts['user_menu']} ---")
        print(f"1. {texts['show_balance']}")
        print(f"2. {texts['deposit_money']}")
        print(f"3. {texts['withdraw_money']}")
        print(f"4. {texts['show_history']}")
        print(f"5. {texts['Add_credit_card']}")
        print(f"6. {texts['show_history']}")
        print(f"7. {texts['download_credit_card_statement']}")
        print(f"8. Extract Credit Card Data")
        print(f"9. {texts['logout']}")
        
        choice = input(texts['enter_choice'])
        
        if choice == '1':
            show_balance(user_id, texts)
        elif choice == '2':
            deposit_money(user_id, texts)
        elif choice == '3':
            withdraw_money(user_id, texts)
        elif choice == '4':
            show_transaction_history(user_id, texts)
        elif choice == '5':
            add_credit_card(user_id, texts)
        elif choice == '6':    
            show_credit_card_statement(user_id, texts)
        elif choice == '7':
            extract_credit_card_data(user_id, texts)
        elif choice == '8':
            add_credit_card(user_id, texts)
        elif choice == '9':
            print(texts['logged_out'])
            break
        else:
            print(texts['invalid_choice'])
def extract_credit_card_data(user_id, texts):
    try:
        cursor.execute("""
            SELECT 
                CC.card_number,
                CC.card_type,
                CC.credit_limit,
                CC.outstanding_balance,
                SUM(CASE WHEN CT.transaction_type = 'purchase' THEN CT.amount ELSE 0 END) as total_purchases,
                SUM(CT.reward_points) as total_reward_points,
                COUNT(CT.transaction_id) as transaction_count,
                MAX(CT.transaction_date) as last_transaction_date
            FROM CreditCards CC
            JOIN Accounts A ON CC.account_id = A.account_id
            LEFT JOIN CardTransactions CT ON CC.card_id = CT.card_id
            WHERE A.user_id = %s
            GROUP BY CC.card_id
        """, (user_id,))
        
        cards = cursor.fetchall()
        if not cards:
            print(f"\n❌ {texts['no_credit_card']}")
            return
        
        print("\n=== Credit Card Summary ===")
        for card in cards:
            card_number = f"****{card[0][-4:]}"  # Show only last 4 digits
            print(f"\nCard Number: {card_number}")
            print(f"Card Type: {card[1]}")
            print(f"Credit Limit: SGD {card[2]:,.2f}")
            print(f"Outstanding Balance: SGD {card[3]:,.2f}")
            print(f"Total Purchases: SGD {card[4]:,.2f}")
            print(f"Total Reward Points: {card[5]:,.0f}")
            print(f"Number of Transactions: {card[6]}")
            if card[7]:
                print(f"Last Transaction Date: {card[7].strftime('%Y-%m-%d %H:%M')}")
            print("-" * 40)
            
    except mysql.connector.Error as err:
        print(f"\n❌ Error: {err}")
        logging.error(f"Credit card data extraction error: {str(err)}")

def add_credit_cards(user_id, texts):
    try:
        # Check if user already has a credit card
        cursor.execute("""
            SELECT CC.card_number 
            FROM CreditCards CC
            JOIN Accounts A ON CC.account_id = A.account_id
            WHERE A.user_id = %s
        """, (user_id,))

         # Get account details
        cursor.execute("SELECT account_id FROM Accounts WHERE user_id = %s", (user_id,))
        account = cursor.fetchone()
        
        if not account:
            print(f"\n❌ {texts['account_not_found']}")
            return

        # Card type selection
        print("\nAvailable Card Types:")
        print("1. Classic (Credit Limit: SGD 5,000)")
        print("2. Gold (Credit Limit: SGD 10,000)")
        print("3. Platinum (Credit Limit: SGD 20,000)")
        
        card_choice = input("Select card type (1-3): ")

        card_types = {
            '1': ('Classic', Decimal('5000.00')),
            '2': ('Gold', Decimal('10000.00')),
            '3': ('Platinum', Decimal('20000.00'))
        }

        if card_choice not in card_types:
            print("\n❌ Invalid card type selection")
            return
            
        card_type, credit_limit = card_types[card_choice]
        
        # Generate card number (16 digits)
        random_numbers = str(random.randint(100000000000, 999999999999))
        card_number = f"4532{random_numbers}"
        # Set statement date and due date
        statement_date = datetime.now().replace(day=1)
        due_date = statement_date.replace(day=25)
        
        cursor.execute("""
            INSERT INTO CreditCards 
            (account_id, card_number, card_type, credit_limit, outstanding_balance, statement_date, due_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (account[0], card_number, card_type, credit_limit, Decimal('0.00'), statement_date, due_date))

        db.commit()
        print("\n✅ Credit card added successfully!")
        print(f"Card Number: ****{card_number[-4:]}")
        print(f"Card Type: {card_type}")
        print(f"Credit Limit: SGD {credit_limit:,.2f}")
        
    except mysql.connector.Error as err:
        db.rollback()
        print(f"\n❌ Error: {err}")
        logging.error(f"Credit card creation error: {str(err)}")

# Update the user_menu function to include the new option
def user_menu(user_id, texts):
    while True:
        if not check_db_connection():
            print("Database connection lost. Please try again later.")
            break
        print(f"\n--- {texts['user_menu']} ---")
        print(f"1. {texts['show_balance']}")
        print(f"2. {texts['deposit_money']}")
        print(f"3. {texts['withdraw_money']}")
        print(f"4. {texts['show_history']}")
        print(f"5. {texts['add_credit_card']}")
        print(f"6. {texts['make_credit_card_transaction']}")
        print(f"7. {texts['download_credit_card_statement']}")
        print(f"8. Extract Credit Card Data")
        print(f"9. {texts['logout']}")
        
        choice = input(texts['enter_choice'])
        
        if choice == '1':
            show_balance(user_id, texts)
        elif choice == '2':
            deposit_money(user_id, texts)
        elif choice == '3':
            withdraw_money(user_id, texts)
        elif choice == '4':
            show_transaction_history(user_id, texts)
        elif choice == '5':
            add_credit_cards(user_id, texts)
        elif choice == '6':
            make_credit_card_transaction(user_id, texts)
        elif choice == '7':
            show_credit_card_statement(user_id, texts)
        elif choice == '8':
            extract_credit_card_data(user_id, texts)
        elif choice == '9':
            print(texts['logged_out'])
            break
        else:
            print(texts['invalid_choice'])

def make_credit_card_transaction(user_id, texts):
    try:
        # Check if user has any credit cards
        cursor.execute("""
            SELECT CC.card_id, CC.card_number, CC.credit_limit, CC.outstanding_balance
            FROM CreditCards CC
            JOIN Accounts A ON CC.account_id = A.account_id
            WHERE A.user_id = %s
        """, (user_id,))
        
        cards = cursor.fetchall()
        if not cards:
            print(f"\n❌ {texts['no_credit_card']}")
            return

        # Display available cards
        print("\nAvailable Credit Cards:")
        for i, card in enumerate(cards, 1):
            available_credit = card[2] - card[3]
            print(f"{i}. Card ending in {card[1][-4:]} - Available Credit: SGD {available_credit:,.2f}")

        # Card selection
        card_choice = input("\nSelect card (number): ")
        try:
            selected_card = cards[int(card_choice) - 1]
        except (ValueError, IndexError):
            print("\n❌ Invalid card selection")
            return

        # Transaction details
        merchant = input("Enter merchant name: ")
        try:
            amount = Decimal(input("Enter transaction amount: SGD "))
        except ValueError:
            print("\n❌ Invalid amount")
            return

        # Check available credit
        available_credit = selected_card[2] - selected_card[3]
        if amount <= 0:
            print("\n❌ Amount must be positive")
            return
        if amount > available_credit:
            print(f"\n❌ Insufficient credit. Available credit: SGD {available_credit:,.2f}")
            return

        # Calculate reward points (1 point per SGD 5)
        reward_points = amount / Decimal('5.0')

        # Insert transaction and update balance
        cursor.execute("""
            INSERT INTO CardTransactions 
            (card_id, merchant_name, amount, transaction_type, reward_points)
            VALUES (%s, %s, %s, %s, %s)
        """, (selected_card[0], merchant, amount, 'purchase', reward_points))

        cursor.execute("""
            UPDATE CreditCards 
            SET outstanding_balance = outstanding_balance + %s 
            WHERE card_id = %s
        """, (amount, selected_card[0]))

        db.commit()
        print("\n✅ Transaction successful!")
        print(f"Amount: SGD {amount:,.2f}")
        print(f"Reward Points Earned: {reward_points:.0f}")
        print(f"New Available Credit: SGD {(available_credit - amount):,.2f}")

    except mysql.connector.Error as err:
        db.rollback()
        print(f"\n❌ Error: {err}")
        logging.error(f"Credit card transaction error: {str(err)}")

def show_credit_card_statement(user_id, texts):
    try:
        cursor.execute("""
            SELECT 
                CC.card_number,
                CC.card_type,
                CC.credit_limit,
                CC.outstanding_balance,
                CC.statement_date,
                CC.due_date,
                CT.transaction_date,
                CT.merchant_name,
                CT.amount,
                CT.transaction_type,
                CT.reward_points,
                U.full_name
            FROM CreditCards CC
            JOIN Accounts A ON CC.account_id = A.account_id
            JOIN Users U ON A.user_id = U.user_id
            LEFT JOIN CardTransactions CT ON CC.card_id = CT.card_id
            WHERE A.user_id = %s
            ORDER BY CT.transaction_date DESC
        """, (user_id,))
        
        results = cursor.fetchall()
        if not results:
            print(f"\n📂 {texts['no_credit_card']}")
            return

        # PDF Generation
        reports_dir = os.path.join(os.getcwd(), "reports")
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)

        filename = f"CreditCard_Statement_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(reports_dir, filename)
        
        
        if 'வரவேற்கிறோம்' in texts['welcome'] and TAMIL_FONT_AVAILABLE:
            pdf_font = 'Latha'
            pdf_font_bold = 'Latha'
        else:
            pdf_font = 'Helvetica'
            pdf_font_bold = 'Helvetica-Bold'

        c = canvas.Canvas(filepath, pagesize=letter)
        c._doc.setTitle(texts['credit_card_statement'])
        
        # Add logo
        logo_path = os.path.join(os.path.dirname(__file__), "ocbc_logo.png")
        if os.path.exists(logo_path):
            c.drawImage(logo_path, 50, 700, width=150, height=75, mask='auto')

        # Card Details
        card_number = results[0][0]
        card_type = results[0][1]
        credit_limit = results[0][2]
        outstanding_balance = results[0][3]
        statement_date = results[0][4]
        due_date = results[0][5]
        customer_name = results[0][11]

        # Header
        c.setFont(pdf_font_bold, 14)
        c.drawString(50, 670, texts['credit_card_statement'])
        
        # Card Information
        c.setFont(pdf_font, 10)
        c.drawString(50, 650, f"{texts['full_name']}: {customer_name}")
        c.drawString(50, 635, f"{texts['card_type']}: {card_type}")
        c.drawString(50, 620, f"{texts['credit_limit']}: SGD {credit_limit:,.2f}")
        c.drawString(50, 605, f"{texts['outstanding_balance']}: SGD {outstanding_balance:,.2f}")
        if statement_date:
            c.drawString(50, 590, f"{texts['statement_date']}: {statement_date.strftime('%d %b %Y')}")
        if due_date:
            c.drawString(50, 575, f"{texts['due_date']}: {due_date.strftime('%d %b %Y')}")

        # Transactions Table
        y = 540
        c.setFont(pdf_font_bold, 11)
        c.drawString(50, y, texts['date'])
        c.drawString(120, y, texts['merchant'])
        c.drawString(300, y, texts['amount'])
        c.drawString(400, y, texts['reward_points'])
        c.line(50, y-5, 550, y-5)

        y -= 20
        c.setFont(pdf_font, 9)
        
        for transaction in results:
            if transaction[6]:  # if there's transaction data
                if y < 50:  # New page if running out of space
                    c.showPage()
                    y = 750
                    c.setFont(pdf_font, 9)

                date = transaction[6].strftime('%d %b %Y')
                merchant = transaction[7]
                amount = transaction[8]
                points = transaction[10]

                c.drawString(50, y, date)
                c.drawString(120, y, merchant)
                c.drawString(300, y, f"SGD {amount:,.2f}")
                c.drawString(400, y, f"{points:,.2f}")
                
                y -= 20

        # Footer
        c.setFont(pdf_font, 8)
        c.drawString(50, 30, texts.get('generated_document', "This is a computer-generated document. No signature is required."))
        c.drawString(50, 15, texts.get('customer_service', "For assistance, please call our Customer Service Hotline at 1800 363 3333"))

        c.save()
        print(f"\n✅ {texts['credit_card_statement_generated']}")
        print(f"📍 {texts['file_saved']}: {filepath}")
        os.startfile(filepath)

    except mysql.connector.Error as err:
        print(f"\n❌ Error: {err}")
        logging.error(f"Credit card statement generation error: {str(err)}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        logging.error(f"Credit card statement generation error: {str(e)}")

def main():
    check_logo_exists()  # Check if logo exists before starting
    current_language = select_language()
    texts = LANGUAGES[current_language]
    print(f"====== {texts['welcome']} ======")

    while True:
        print(f"\n1. {texts['login']}")
        print(f"2. {texts['create_account']}")
        print(f"3. {texts['exit']}")
        choice = input(f"{texts['choose_option']}: ")

        if choice == '1':
            login(texts)
        elif choice == '2':
            create_account(texts)
        elif choice == '3':
            print(f"👋 {texts['goodbye']}")
            break
        else:
            print(f"❌ {texts['invalid_choice']}")

if __name__ == "__main__":
    try:
        main()
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()
            print("\nDatabase connection closed.")