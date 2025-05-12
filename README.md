# 📦 Inventory Management System
A simple, object-oriented Inventory Management System in Python that supports adding, selling, viewing, saving, and loading products via a user-friendly CLI. It demonstrates key OOP concepts like inheritance, encapsulation, polymorphism, and abstraction, along with robust error handling using custom exceptions.

# 🧰 Features

🛒 Add Electronics or Clothing products

📉 Sell products and update stock

🔍 View product details by ID

💾 Save and load inventory from a .json file

⚠️ Handles common errors (e.g., duplicate products, invalid files, insufficient stock)

💡 Clean CLI menu using a while loop

# 🧠 Object-Oriented Concepts Used

# Concept	Usage

Encapsulation	Private attributes in Product class (__name, __price, etc.)

Inheritance	Electronics and Clothing extend the abstract base Product

Polymorphism	Overridden display_info() and to_dict() methods in each class

Abstraction	Product is an abstract base class with abstract methods

Exception Handling	Custom exceptions for realistic edge cases

# 🖥️ CLI Menu

 ===== Inventory Menu =====
1. Add Product
2. Sell Product
3. View Product
4. Save Inventory to File
5. Load Inventory from File
6. List All Products
7. Exit

# 🚀 Getting Started
✅ Prerequisites
Python 3.6+

# ▶️ Run the Application

APP.py

# 🧪 Test Features
Add both Electronics & Clothing items

Try selling more than available stock

Save and load from file

View error handling in edge cases


