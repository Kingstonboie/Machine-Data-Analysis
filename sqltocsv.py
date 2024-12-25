import mysql.connector
import csv
def create_connection():
 return mysql.connector.connect(
 host="localhost",
 user="gagan",
 password="password",
 database="machinedb"
 )
def export_data_to_csv(conn, table_name, csv_file_path):
 cursor = conn.cursor()
 query = f"SELECT * FROM {table_name}"
 cursor.execute(query)
 rows = cursor.fetchall()
 column_names = [i[0] for i in cursor.description]
 with open(csv_file_path, 'w', newline='') as csvfile:
 csvwriter = csv.writer(csvfile)
 csvwriter.writerow(column_names)
 csvwriter.writerows(rows)
 cursor.close()
if __name__ == "__main__":
 conn = create_connection()
 export_data_to_csv(conn, 'machine_data', 'ogmachine_data.csv')
 export_data_to_csv(conn, 'machine_details', 'ogmachine_details.csv')
 conn.close()
