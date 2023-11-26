

# API Documentation (Ecommerce App Backend)

## User Registration

### Register a New Account
- **Endpoint:** `/user/register/`
- **Method:** `POST`
- **Parameters:**
  - `email` (required): User's email address
  - `password` (required): User's password
  - `address` (required): User's address
  - `phone_number` (required): User's phone number
  - `first_name` (optional): User's first name
  - `last_name` (optional): User's last name

## User Authentication

### Generate JWT Tokens
- **Endpoint:** `/user/token/`
- **Method:** `POST`
- **Parameters:**
  - `email` (required): User's email address
  - `password` (required): User's password

### Refresh Access Token
- **Endpoint:** `/user/token/refresh/`
- **Method:** `POST`
- **Parameters:**
  - `refresh_token` (required): User's refresh token

### Verify Token
- **Endpoint:** `/user/token/verify/`
- **Method:** `POST`
- **Parameters:**
  - `token` (required): Token to be verified

## Product Management

### Create a New Product
- **Endpoint:** `/products/create/`
- **Method:** `POST` (Admin Only)
- **Parameters:**
  - `name` (required): Product name
  - `description` (required): Product description
  - `stock_quantity` (required): Quantity of stock available
  - `price` (required): Product price
  - `image` (required): Product image

### View Product Details
- **Endpoint:** `/products/pk/`
- **Method:** `GET`
- **Parameters:**
  - `pk` (required): Unique ID of the product

### Update Product Details
- **Endpoint:** `/products/pk/`
- **Method:** `PUT/PATCH` (Admin Only)
- **Parameters:**
  - `pk` (required): Unique ID of the product
  - (Additional parameters for product details update)

### View All Products
- **Endpoint:** `/products/`
- **Method:** `GET`

## Cart Management

### View Cart Items
- **Endpoint:** `/cart/`
- **Method:** `GET`

### Add/Remove Item to/from Cart
- **Endpoint:** `/cart/`
- **Method:** `POST`
- **Parameters:**
  - `action` (required): Action to perform (add/remove)
  - `product_id` (required): ID of the product
  - `quantity` (required): Quantity of items to add/remove

## Order Management

### Create Order
- **Endpoint:** `/cart/orders/`
- **Method:** `POST`
- **Parameters:**
  - (No additional parameters)

### View Order Details
- **Endpoint:** `/order/pk/`
- **Method:** `GET`
- **Parameters:**
  - `pk` (required): ID of the order

### Update Order Status
- **Endpoint:** `/order/pk/`
- **Method:** `PUT/PATCH` (Admin Only)
- **Parameters:**
  - `pk` (required): ID of the order
  - (Additional parameters for status update)

# Endpoint Summary Table

| Endpoint | Task | Method | Required Parameters | Access Level |
| --- | --- | --- | --- | --- |
| `/user/register/` | Register a New Account | POST | email, password, address, phone_number | Public |
| `/user/token/` | Generate JWT Tokens | POST | email, password | Public |
| `/user/token/refresh/` | Refresh Access Token | POST | refresh_token | Public |
| `/user/token/verify/` | Verify Token | POST | token | Public |
| `/products/create/` | Create a New Product | POST | name, description, stock_quantity, price, image | Admin |
| `/products/pk/` | View Product Details | GET | pk | Public |
| `/products/pk/` | Update Product Details | PUT/PATCH | pk, (additional parameters) | Admin |
| `/products/` | View All Products | GET | - | Public |
| `/cart/` | View Cart Items | GET | - | User |
| `/cart/` | Add/Remove Item to/from Cart | POST | action, product_id, quantity | User |
| `/cart/orders/` | Create Order | POST | - | User |
| `/order/pk/` | View Order Details | GET | pk | User/Admin |
| `/order/pk/` | Update Order Status | PUT/PATCH | pk, (additional parameters) | Admin |


## Getting Started

1. **Clone the App:**

    ```bash
    git clone https://github.com/BloggingKIng/Ecommerce-Backend.git
    ```

2. **Install the Required Libraries:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4. **Create a Superuser/Admin Account:**

    ```bash
    python manage.py createsuperuser
    ```

5. **Start the Server:**

    ```bash
    python manage.py runserver
    ```


