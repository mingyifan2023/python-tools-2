

#使用Faker模块批量生成写入MySQL的数据， 只需要5个字段即可，给出python写入代码以及生成数据表的SQL


from faker import Faker
import mysql.connector
from mysql.connector import errorcode

# Connect to MySQL
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456',
        database='vt'
    )
    cursor = conn.cursor()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Error: Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Error: Database does not exist")
    else:
        print(err)

# Create fake data and insert into MySQL
fake = Faker()
num_records = 100  # Number of records to generate

for _ in range(num_records):
    name = fake.name()
    address = fake.address()
    email = fake.email()
    phone_number = fake.phone_number()
    birthdate = fake.date_of_birth()

    sql = "INSERT INTO v_t (name, address, email, phone_number, birthdate) VALUES (%s, %s, %s, %s, %s)"
    val = (name, address, email, phone_number, birthdate)

    cursor.execute(sql, val)

conn.commit()
print(f"{num_records} records inserted.")

# Close connection
cursor.close()
conn.close()
