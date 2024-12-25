import mysql.connector
import random
from datetime import datetime
import time
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="gagan",
        password="password",
        database="machine_db2"
    )
def truncate_tables(conn):
    cursor = conn.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    cursor.execute("TRUNCATE TABLE machine_data")
    cursor.execute("TRUNCATE TABLE machine_details")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
    conn.commit()
    cursor.close()
def populate_dummy_data(conn, num_machines, num_samples):
    cursor = conn.cursor()
    for i in range(1, num_machines + 1):
        machine_id = f"machine_{i}"
        machine_name = f"Machine_{i}"
        machine_oem = f"OEM_{i % 3 + 1}"
        cursor.execute("INSERT INTO machine_details (machine_id, machine_name, machine_oem) VALUES (%s, %s, %s)",
            (machine_id, machine_name, machine_oem))
    for i in range(1, num_machines + 1):
        machine_id = f"machine_{i}"
        for _ in range(num_samples):
            temperature = random.uniform(125, 145)
            pressure = random.uniform(130, 140)
            update_ts_temp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("INSERT INTO machine_data (machine_id, param_name, param_value, update_ts) VALUES (%s, %s, %s, %s)",
            (machine_id, 'temperature', temperature, update_ts_temp))
            time.sleep(1)
            update_ts_pressure = datetime.now().strftime('%Y-%m-%d %H:%M:%S') cursor.execute("INSERT INTO machine_data (machine_id,
            param_name, param_value, update_ts) VALUES (%s, %s, %s, %s)",
            (machine_id, 'pressure', pressure, update_ts_pressure))
            time.sleep(1)
    conn.commit()
    cursor.close()
if __name__ == "__main__":
 conn = create_connection()
 truncate_tables(conn)
 num_machines = 3
 num_samples = 100
 populate_dummy_data(conn, num_machines, num_samples)
 conn.close()