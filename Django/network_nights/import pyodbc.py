from django.db import connection

def list_tables():
    with connection.cursor() as cursor:
        cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
        tables = cursor.fetchall()
        return [table[0] for table in tables]

# Usage example
print(list_tables())
