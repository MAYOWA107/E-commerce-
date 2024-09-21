E-commerce Web API
This is a Django-based e-commerce platform utilizing Django Rest Framework (DRF) for API functionality. The platform features product management, cart and order functionality, and payment processing through Flutterwave.

Features
User Authentication: Users can register, login, and manage their profiles.
Product Management: CRUD operations for products and categories.
Cart and Order System: Add items to a cart, place orders, and manage orders.
Payment Integration: Integrated with Flutterwave for secure payment processing.
Admin Interface: Manage products, orders, and reviews through Django's admin panel.
Setup
Prerequisites
Python 3.x
Django 3.x
Django Rest Framework
Flutterwave API Key for payment processing
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/MAYOWA107/E-commerce-.git
cd E-commerce-
Set up a virtual environment:

bash
Copy code
python3 -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Configure environment variables:

Create a .env file at the root of your project and add the following variables:

bash
Copy code
FLW_SEC_KEY=your_flutterwave_secret_key
Apply migrations:

bash
Copy code
python manage.py migrate
Create a superuser for the admin panel:

bash
Copy code
python manage.py createsuperuser
Run the server:

bash
Copy code
python manage.py runserver
API Endpoints
Authentication
/api/auth/register/ - Register a new user
/api/auth/login/ - Login for existing users
Products
/api/products/ - List all products
/api/products/<id>/ - Retrieve, update, or delete a specific product
Cart
/api/cart/ - Manage items in the cart
/api/cart/add-item/ - Add an item to the cart
/api/cart/remove-item/ - Remove an item from the cart
Orders
/api/orders/ - List user orders
/api/orders/create/ - Create a new order
/api/orders/confirm_payment/ - Confirm payment through Flutterwave
Payment
Payments are processed using Flutterwave. You can initiate payments and confirm them through /api/orders/confirm_payment/.
Admin Access
The Django admin interface allows staff users to manage products, orders, categories, reviews, and more.
To access the admin dashboard, navigate to /admin/ and log in with the superuser credentials.

License
This project is licensed under the MIT License. See the LICENSE file for details.

