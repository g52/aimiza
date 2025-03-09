import os

# Azure SQL Server credentials
SQL_SERVER = 'Aimiza.database.windows.net'
SQL_DATABASE = 'Aimiza'
SQL_USER = 'shegzter'
SQL_PASSWORD = 'Netflix2@'
SQL_DRIVER = 'ODBC+Driver+17+for+SQL+Server'

# Connection string for SQL Server
SQLALCHEMY_DATABASE_URI = f'mssql+pyodbc://{SQL_USER}:{SQL_PASSWORD}@{SQL_SERVER}/{SQL_DATABASE}?driver={SQL_DRIVER}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
