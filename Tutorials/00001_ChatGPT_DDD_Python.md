# 1. ChatGPT, Domain driven design and python - Using openAI to dive into software development

## 1.1. Table of contents

- [1. ChatGPT, Domain driven design and python - Using openAI to dive into software development](#1-chatgpt-domain-driven-design-and-python---using-openai-to-dive-into-software-development)
  - [1.1. Table of contents](#11-table-of-contents)
  - [1.2. What is ChatGPT?](#12-what-is-chatgpt)
  - [1.3. What is domain driven design?](#13-what-is-domain-driven-design)
  - [1.4. Example python project 1](#14-example-python-project-1)
  - [1.5. Example python project 2](#15-example-python-project-2)
  - [1.6. Example python project 3](#16-example-python-project-3)
  - [1.7. Example python project 4](#17-example-python-project-4)
  - [1.8. Example python project 5](#18-example-python-project-5)
  - [1.9. Example python project 6](#19-example-python-project-6)

## 1.2. What is ChatGPT?

From openAI's website,

> We’ve trained a model called ChatGPT which interacts in a conversational way. The dialogue format makes it possible for ChatGPT to answer followup questions, admit its mistakes, challenge incorrect premises, and reject inappropriate requests. ChatGPT is a sibling model to InstructGPT, which is trained to follow an instruction in a prompt and provide a detailed response.

Go try it out [here](https://chat.openai.com/chat)

## 1.3. What is domain driven design?

Domain-driven design (DDD) is a software development approach that focuses on defining the business domain, identifying key concepts and vocabulary, and developing a model that reflects the business requirements. In the context of a Python project, implementing DDD would involve the following steps:

Identify the business domain for the project and define the key concepts and vocabulary for that domain. This will involve working closely with domain experts to understand the business requirements and identify the key entities, relationships, and operations involved in the domain.

Develop a domain model that reflects the key concepts and vocabulary identified in the previous step. This model should capture the structure and behavior of the domain, including the entities, relationships, and operations involved.

Define the interfaces and implementations for the entities, relationships, and operations in the domain model. This will involve designing classes and methods that can be used to manipulate the domain model and perform the operations required by the business domain.

Implement the domain model using Python. This will involve writing the code for the classes and methods defined in the previous step, and testing them to ensure they work as expected.

Refine and iterate on the domain model as needed. As the project progresses, it may be necessary to make changes to the domain model in order to better reflect the business requirements or to improve its design. This can be done by updating the interfaces and implementations, and testing the changes to ensure they work as expected.

Overall, implementing DDD in a Python project involves a deep understanding of the business domain, careful design of the domain model, and diligent implementation and testing of the model. It can be a challenging but rewarding process that can lead to more effective and maintainable software.

## 1.4. Example python project 1

```Python
"""
In this example, we have defined a User class to represent a domain entity (in this case, a user of a system), a UserRepository class to manage User objects, and a UserService class to provide business logic for working with User objects. The UserService class uses the UserRepository to perform persistence operations, such as saving and finding User objects.

By using this approach, we are able to clearly separate the different concerns of our software system and build a flexible and maintainable solution.
"""

# Import the necessary libraries
from typing import List

# Define a class to represent the domain entity
class User:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email
        
# Define a repository class to manage User objects
class UserRepository:
    def __init__(self):
        self.users = []
        
    def save(self, user: User):
        # Implement logic to save the user to a database or other persistence layer
        pass
        
    def find_by_id(self, id: int) -> User:
        # Implement logic to find a user by their ID
        pass
        
    def find_by_email(self, email: str) -> User:
        # Implement logic to find a user by their email address
        pass
        
# Define a service class to provide business logic
class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
        
    def register_user(self, name: str, email: str):
        # Implement logic to create a new user and save it using the repository
        pass
        
    def get_user_by_id(self, id: int) -> User:
        # Use the repository to find a user by their ID
        return self.repository.find_by_id(id)
        
    def get_user_by_email(self, email: str) -> User:
        # Use the repository to find a user by their email address
        return self.repository.find_by_email(email)
```

## 1.5. Example python project 2

```python
"""
In this example, the Product and Cart classes represent the domain entities in our system. The CartService class is the application layer, which defines the business logic for managing a shopping cart. The InMemoryRepository class is the infrastructure layer, which handles storing and retrieving products from memory.

In DDD, the domain layer is the heart of the application, containing the core business logic and entities. The application and infrastructure layers serve as supporting layers, providing the means for the domain layer to interact with external resources (e.g. databases) and define the application's business logic.
"""

from typing import List

# Domain layer

class Product:
    def __init__(self, id: int, name: str, price: float):
        self.id = id
        self.name = name
        self.price = price


class Cart:
    def __init__(self, products: List[Product]):
        self.products = products

    def add_product(self, product: Product):
        self.products.append(product)

    def remove_product(self, product_id: int):
        self.products = [p for p in self.products if p.id != product_id]

    def get_total(self):
        return sum(p.price for p in self.products)

# Application layer

class CartService:
    def __init__(self, cart: Cart):
        self.cart = cart

    def add_product_to_cart(self, product: Product):
        self.cart.add_product(product)

    def remove_product_from_cart(self, product_id: int):
        self.cart.remove_product(product_id)

    def get_cart_total(self):
        return self.cart.get_total()

# Infrastructure layer

class InMemoryRepository:
    def __init__(self):
        self.products = []

    def add_product(self, product: Product):
        self.products.append(product)

    def get_product(self, product_id: int):
        return next(p for p in self.products if p.id == product_id)

    def remove_product(self, product_id: int):
        self.products = [p for p in self.products if p.id != product_id]

    def get_all_products(self):
        return self.products

# Usage

repo = InMemoryRepository()
repo.add_product(Product(1, 'Test product', 10.99))

cart = Cart([])
service = CartService(cart)

service.add_product_to_cart(repo.get_product(1))
service.get_cart_total()  # 10.99

service.remove_product_from_cart(1)
service.get_1cart_total()  # 0.0

```

## 1.6. Example python project 3

```Python

"""
In this example, the Employee class is a representation of the concept of an employee in the business domain. The EmployeeRepository class is responsible for managing a collection of employees, and provides methods for adding and retrieving employees. Finally, the PayrollSystem class uses the EmployeeRepository to calculate the payroll for a given employee.

By dividing the program into these distinct classes, each with a specific responsibility, the design of the software follows the principles of DDD. The Employee class provides a clear and concise representation of the business domain, the EmployeeRepository class manages the employees in a way that is consistent with the real-world domain, and the PayrollSystem class uses the EmployeeRepository to support the complex business process of calculating payroll. This helps to ensure that the software accurately reflects the real-world domain and can support the complex business rules and processes that exist within it.
"""
class Employee:
    def __init__(self, employee_id, first_name, last_name):
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class EmployeeRepository:
    def __init__(self):
        self.employees = []

    def add_employee(self, employee):
        self.employees.append(employee)

    def get_employee_by_id(self, employee_id):
        for employee in self.employees:
            if employee.employee_id == employee_id:
                return employee

        return None


class PayrollSystem:
    def __init__(self, employee_repository):
        self.employee_repository = employee_repository

    def calculate_payroll(self, employee_id):
        employee = self.employee_repository.get_employee_by_id(employee_id)

        if employee is None:
            raise ValueError(f"Employee with ID {employee_id} not found")

        payroll_amount = 0

        # Calculate payroll amount based on employee's salary and hours worked

        return payroll_amount

```

## 1.7. Example python project 4

```Python

"""
In this example, the UserApplication class uses the UserController and InMemoryUserService classes to create a complete application that can perform operations on User objects. This is an example of onion architecture, because the application is built in layers, with the core domain layer at the center, surrounded by layers of infrastructure and application logic. This allows the application to be easily adapted to different infrastructure implementations.
"""

from abc import ABC, abstractmethod

# Domain Layer
class UserService(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> User:
        pass

    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

class User:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

# Application Layer
class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def get_user(self, user_id: int) -> User:
        return self.user_service.get_user(user_id)

    def create_user(self, user: User) -> User:
        return self.user_service.create_user(user)

# Infrastructure Layer
class InMemoryUserService(UserService):
    def __init__(self):
        self.users = {}

    def get_user(self, user_id: int) -> User:
        return self.users.get(user_id)

    def create_user(self, user: User) -> User:
        self.users[user.id] = user
        return user

# Onion Architecture
class UserApplication:
    def __init__(self):
        user_service = InMemoryUserService()
        self.user_controller = UserController(user_service)
```

## 1.8. Example python project 5

```Python

"""
To give a more detailed example of how domain-driven design might be implemented in a Python project, let's consider a simple banking system. In this system, we have the following key concepts and entities:

Account: represents a bank account, with an account number, balance, and list of transactions.
Customer: represents a customer of the bank, with a name, address, and list of accounts.
Transaction: represents a transaction on an account, with a date, amount, and description.
First, we would define a common language for the domain that can be used by all stakeholders. This might include terminology such as "account", "customer", and "transaction", as well as concepts such as "deposit" and "withdrawal".

Next, we would model the business domain using classes and objects in Python. For example, we might define the following classes:


These classes capture the key concepts and entities in the business domain, and define the business logic for managing accounts, customers, and transactions. Note how the common language of the domain is used in the names of the classes, methods, and variables, to make the code more readable and understandable.

Finally, we would use object-oriented design techniques to create a flexible and extensible design that can accommodate changes to the business domain over time. For example, we might define additional subclasses of Account, such as SavingsAccount and CheckingAccount, to represent different types of accounts with different business rules and logic.

Overall, by using domain-driven design principles in our Python project, we can create software that is closely aligned with the needs of the business, and that is easy to understand and maintain.

"""

class Account:
    def __init__(self, number, balance=0):
        self.number = number
        self.balance = balance
        self.transactions = []
    
    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(Transaction(datetime.now(), amount, "Deposit"))
    
    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self.transactions.append(Transaction(datetime.now(), amount, "Withdrawal"))


class Customer:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.accounts = []
    
    def open_account(self, number):
        self.accounts.append(Account(number))


class Transaction:
    def __init__(self, date, amount, description):
        self.date = date
        self.amount = amount
        self.description = description
```

## 1.9. Example python project 6

In domain-driven design (DDD), the "ports and adapters" architecture (also known as the "hexagonal" or "onion" architecture) is a way of organizing the structure of a software application to make it more flexible and scalable. It separates the core domain logic from the technical details of the application, such as the user interface, database access, and other external dependencies.

To implement the ports and adapters architecture in Python, you would need to define the core domain logic in the center of your application, and then implement the various adapters that connect the domain to the external dependencies. The adapters would be responsible for translating the domain concepts and objects into the specific formats and protocols used by the external dependencies.

Here is an example of a simple Python class that represents a domain object in the domain layer of a DDD-based application:

```Python
class Order:
    def __init__(self, customer, items):
        self.customer = customer
        self.items = items

    def calculate_total(self):
        total = 0
        for item in self.items:
            total += item.price
        return total
```

This class represents an order in a hypothetical online store. It contains a reference to the customer who placed the order, as well as a list of items that were included in the order. It also has a method for calculating the total price of the order.

To implement the ports and adapters architecture for this domain, you would need to define the "ports" that the domain layer exposes to the outside world. These could be interfaces or abstract base classes that define the methods and data structures that the adapters must implement. For example:

```Python
class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> None:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Order]:
        pass
```

This is an abstract base class that defines the methods that an adapter must implement in order to provide access to the order data in the domain layer. The save method is used to store a new order, and the find_by_id method is used to retrieve an existing order by its ID.

To implement the adapters, you would create concrete classes that inherit from these abstract base classes and provide the specific implementation for a particular external dependency. For example, you could create an adapter for a relational database using the Python sqlite3 module:

```Python
class SqliteOrderRepository(OrderRepository):
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def save(self, order: Order) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO orders (customer_id, items) VALUES (?, ?)",
            (order.customer.id, json.dumps(order.items)),
        )
        cursor.connection.commit()

    def find_by_id(self, id: int) -> Optional[Order]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM orders WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Order(
            customer=Customer(id=row["customer_id"]), items=json.loads(row["items"])
```
