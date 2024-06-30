def create_table(cursor): 
    # cursor.execute("drop table Vehicle_Record ;")

    CREATE_VEHICLE_TABLE =("CREATE TABLE IF NOT EXISTS Vehicle_Record ( id SERIAL PRIMARY KEY,carNo VARCHAR(20), inTime TIMESTAMP,outTime TIMESTAMP);")
    # CREATE_VEHICLE_TABLE =("Alter table Vehicle_Record Modify column carNo VARCHAR(20)")
    cursor.execute(CREATE_VEHICLE_TABLE)

def insert_data(cursor,car_no, in_time):
    INSERT_VEHICLE = "INSERT INTO Vehicle_Record (carNo, inTime) VALUES (%s, %s);"
    cursor.execute(INSERT_VEHICLE, (car_no, in_time))