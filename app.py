import json
from abc import ABC, abstractmethod

# Custom Exceptions
class DuplicateProductError(Exception):
    pass

class InsufficientStockError(Exception):
    pass

class InvalidProductDataError(Exception):
    pass

# Abstract Product Base Class
class Product(ABC):
    def __init__(self, product_id, name, price, quantity):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__quantity = quantity

    def get_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_quantity(self):
        return self.__quantity

    def update_quantity(self, quantity):
        self.__quantity = quantity

    def reduce_quantity(self, quantity):
        if quantity > self.__quantity:
            raise InsufficientStockError(f"Only {self.__quantity} items available.")
        self.__quantity -= quantity

    @abstractmethod
    def display_info(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass

    @staticmethod
    @abstractmethod
    def from_dict(data):
        pass

# Electronics Class
class Electronics(Product):
    def __init__(self, product_id, name, price, quantity, brand, warranty):
        super().__init__(product_id, name, price, quantity)
        self.brand = brand
        self.warranty = warranty

    def display_info(self):
        return (f"[Electronics] ID: {self.get_id()}, Name: {self.get_name()}, "
                f"Price: ${self.get_price()}, Quantity: {self.get_quantity()}, "
                f"Brand: {self.brand}, Warranty: {self.warranty} months")

    def to_dict(self):
        return {
            "type": "Electronics",
            "product_id": self.get_id(),
            "name": self.get_name(),
            "price": self.get_price(),
            "quantity": self.get_quantity(),
            "brand": self.brand,
            "warranty": self.warranty
        }

    @staticmethod
    def from_dict(data):
        try:
            return Electronics(
                data["product_id"], data["name"], data["price"],
                data["quantity"], data["brand"], data["warranty"]
            )
        except KeyError:
            raise InvalidProductDataError("Missing fields in Electronics data.")

# Clothing Class
class Clothing(Product):
    def __init__(self, product_id, name, price, quantity, size, material):
        super().__init__(product_id, name, price, quantity)
        self.size = size
        self.material = material

    def display_info(self):
        return (f"[Clothing] ID: {self.get_id()}, Name: {self.get_name()}, "
                f"Price: ${self.get_price()}, Quantity: {self.get_quantity()}, "
                f"Size: {self.size}, Material: {self.material}")

    def to_dict(self):
        return {
            "type": "Clothing",
            "product_id": self.get_id(),
            "name": self.get_name(),
            "price": self.get_price(),
            "quantity": self.get_quantity(),
            "size": self.size,
            "material": self.material
        }

    @staticmethod
    def from_dict(data):
        try:
            return Clothing(
                data["product_id"], data["name"], data["price"],
                data["quantity"], data["size"], data["material"]
            )
        except KeyError:
            raise InvalidProductDataError("Missing fields in Clothing data.")

# Inventory Class
class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        if product.get_id() in self.products:
            raise DuplicateProductError(f"Product ID {product.get_id()} already exists.")
        self.products[product.get_id()] = product
        print(f"Product '{product.get_name()}' added successfully.")

    def sell_product(self, product_id, quantity):
        product = self.products.get(product_id)
        if not product:
            print("Product not found.")
            return
        try:
            product.reduce_quantity(quantity)
            print(f"Sold {quantity} units of {product.get_name()}.")
        except InsufficientStockError as e:
            print(f"Error: {e}")

    def view_product(self, product_id):
        product = self.products.get(product_id)
        if product:
            print(product.display_info())
        else:
            print("Product not found.")

    def list_inventory(self):
        print("\n--- Inventory ---")
        if not self.products:
            print("No products in inventory.")
        else:
            for p in self.products.values():
                print(p.display_info())
        print("------------------")

    def save_to_file(self, filename):
        try:
            with open(filename, 'w') as f:
                json.dump([p.to_dict() for p in self.products.values()], f)
            print(f"Inventory saved to '{filename}'.")
        except Exception as e:
            print(f"Error saving inventory: {e}")

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                data_list = json.load(f)
            for data in data_list:
                product_type = data.get("type")
                if product_type == "Electronics":
                    product = Electronics.from_dict(data)
                elif product_type == "Clothing":
                    product = Clothing.from_dict(data)
                else:
                    raise InvalidProductDataError("Unknown product type.")
                self.products[product.get_id()] = product
            print(f"Inventory loaded from '{filename}'.")
        except FileNotFoundError:
            print("File not found.")
        except (InvalidProductDataError, json.JSONDecodeError) as e:
            print(f"Error loading inventory: {e}")

# ------------------------------
# ✅ CLI Menu Interaction
# ------------------------------
def cli_menu():
    inventory = Inventory()
    while True:
        print("\n===== Inventory Menu =====")
        print("1. Add Product")
        print("2. Sell Product")
        print("3. View Product")
        print("4. Save Inventory to File")
        print("5. Load Inventory from File")
        print("6. List All Products")
        print("7. Exit")
        choice = input("Enter choice (1-7): ")

        try:
            if choice == '1':
                p_type = input("Enter product type (Electronics/Clothing): ").strip()
                pid = input("Product ID: ")
                name = input("Name: ")
                price = float(input("Price: "))
                qty = int(input("Quantity: "))

                if p_type.lower() == "electronics":
                    brand = input("Brand: ")
                    warranty = int(input("Warranty (months): "))
                    product = Electronics(pid, name, price, qty, brand, warranty)
                elif p_type.lower() == "clothing":
                    size = input("Size: ")
                    material = input("Material: ")
                    product = Clothing(pid, name, price, qty, size, material)
                else:
                    print("Invalid product type.")
                    continue

                inventory.add_product(product)

            elif choice == '2':
                pid = input("Enter Product ID to sell: ")
                qty = int(input("Enter quantity to sell: "))
                inventory.sell_product(pid, qty)

            elif choice == '3':
                pid = input("Enter Product ID to view: ")
                inventory.view_product(pid)

            elif choice == '4':
                filename = input("Enter filename to save: ")
                inventory.save_to_file(filename)

            elif choice == '5':
                filename = input("Enter filename to load: ")
                inventory.load_from_file(filename)

            elif choice == '6':
                inventory.list_inventory()

            elif choice == '7':
                print("Exiting system. Goodbye!")
                break

            else:
                print("Invalid choice. Try again.")

        except ValueError as ve:
            print(f"Input error: {ve}")
        except DuplicateProductError as de:
            print(f"Error: {de}")
        except Exception as e:
            print(f"Unexpected error: {e}")

# Entry point
if __name__ == "__main__":
    cli_menu()
