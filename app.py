from flask import Flask, render_template, request, jsonify
import pymysql

app = Flask(__name__)

# Function to connect to the MySQL database
def connect_to_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Feb01@siw',
        database='vv_erp_db',
    )

# Function to create the users table if it doesn't exist
def create_users_table(connection):
    # with connection.cursor() as cursor:
    #     cursor.execute("""
    #         CREATE TABLE IF NOT EXISTS customers (
    #             customer_id INT,
    #             order_id INT PRIMARY KEY,
    #             first_name VARCHAR(50),
    #             last_name VARCHAR(50),
    #             email VARCHAR(100),
    #             phone VARCHAR(20),
    #             address VARCHAR(255),
    #             order_date DATE,
    #             status VARCHAR(20),
    #             product_name VARCHAR(100),
    #             quantity INT,
    #             price DECIMAL(10, 2),
    #             total_price DECIMAL(10, 2)
    #         )
    #     """)
    #     connection.commit()
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                
                order_id VARCHAR(20) PRIMARY KEY,
                first_name VARCHAR(50),
               
                email VARCHAR(100),
                phone VARCHAR(20),
                address VARCHAR(255),
                product_name VARCHAR(225),
                price INT
               )
        """)
        connection.commit()

# Function to register a new user
def orders( order_id, first_name,  email, phone, address,product_name,price):
    connection = connect_to_db()
    create_users_table(connection)

    # Insert order data into the database
    try:
        with connection.cursor() as cursor:
            # for product in products:
            #     product_name = product['name']
            #     quantity = product['quantity']
            #     price = product['price']
            #     total_price = product['total']

                cursor.execute("""
                    INSERT INTO customers 
                    ( order_id, first_name, email, phone, address,product_name,price)
                    VALUES 
                    ( %s, %s, %s, %s, %s,%s,%s)
                """, (

                    order_id,
                    first_name,

                    email,
                    phone,
                    address,
                    product_name,
                    price



                ))



        connection.commit()

    except pymysql.err.IntegrityError as e:
        print(f"Error inserting order: {e}")
        # Handle the integrity error, such as logging it or informing the user


@app.route('/', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        array_data = request.json
        if isinstance(array_data, list):
            # Iterate over the array and process each object
            for obj in array_data:
                # Access individual properties of the object
                order_id = obj.get('id')
                nested_object = obj.get('billing', {})
                first_name = nested_object.get('first_name')
                email = nested_object.get('email')
                phone = nested_object.get('phone')
                address = nested_object.get('address_1')
                price = obj.get('total')
                line_items = obj.get('line_items', [])

                status = obj.get('status')

                product_details = [f"{item.get('quantity')} x {item.get('name')}" for item in line_items]
                product_name = ', '.join(product_details)



                # Do something with the object's properties
                print(
                    f"Object ID: {order_id}, firstname: {first_name}, Status: {status}, Email: {email}, Phone: {phone}, address_1: {address} , Line Items: {product_details}, total :{price}")

                # Process the order
                orders(order_id, first_name, email, phone, address,product_name,price)

            # After processing all orders, return the template
            return render_template('register.html')

        else:
            # Return an error response if the incoming data is not a list
            return jsonify({'error': 'Invalid data format. Expected an array of objects.'}), 400

    # If the request method is GET, simply return the template
    return render_template('register.html')

    # Assuming other order details are known
    # customer_id = 21474
    # order_id = 11790
    # first_name = "Sharmila "
    # last_name = "Banu"
    # email = "john@example.com"
    # phone = "1234567890"
    # address = "3/762, Thiruvalluvar Nagar, Vaikkal medu, Veerapandi po,"
    # order_date = "2024-03-18"
    # status = "Pending"

    # Register the order
    # orders(customer_id, order_id, first_name, last_name, email, phone, address, order_date, status,
    #        sample_products)


    # orders(order_id,first_name,email,phone,address)




    return render_template('register.html')

@app.route('/process_array', methods=['POST'])
def process_array():


    if request.method == 'POST':
            array_data = request.json
            if isinstance(array_data, list):
                # Iterate over the array and process each object
                for obj in array_data:
                    # Access individual properties of the object
                    id = obj.get('id')
                    nested_object = obj.get('billing', {})
                    first_name = nested_object.get('first_name')
                    status = obj.get('status')


                    # Do something with the object's properties
                    print(f"Object ID: {id},firstname:{first_name} Status: {status}")

                # Return a response indicating successful processing
                return jsonify({'message': 'Array data processed successfully'}), 200
            else:
                # Return an error response if the incoming data is not a list
                return jsonify({'error': 'Invalid data format. Expected an array of objects.'}), 400

if __name__ == "__main__":
    app.run(debug=True)
