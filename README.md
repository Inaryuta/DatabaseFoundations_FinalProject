# **Music Store Management Application - Database Design**

## Team Members

- *Esteban Villalba Delgadillo - 20212020064*
- *Santiago Marin Paez - 20231020159*

## Project Information

**Professor:** *Engineer Carlos Andrés Sierra Virgüez*  
**Career:** *Systems Engineer*  

## Introduction

This project focuses on the design and implementation of a **relational database** for a virtual music store management application. The database supports functionalities such as product management, inventory tracking, user registration, and transaction recording. It serves as the foundation for future development of the application.

---

## **Table of Contents**
1. [Project Overview](#project-overview)
2. [Database Design](#database-design)
3. [Entity-Relationship Diagram (ERD)](#entity-relationship-diagram-erd)
4. [Class Diagram](#class-diagram)
5. [Technologies Used](#technologies-used)
6. [Setup Instructions](#setup-instructions)
7. [API Endpoints](#api-endpoints)
8. [Future Improvements](#future-improvements)
9. [Contributors](#contributors)

---

## **Project Overview**
The database is designed to manage the following core functionalities:
- **Product Management**: Store and manage information about musical instruments and accessories.
- **Inventory Tracking**: Track stock levels and update inventory.
- **User Management**: Register users and assign roles (e.g., admin, customer).
- **Transaction Recording**: Record purchases and generate receipts.
- **Supplier Management**: Manage supplier information and orders.

The database is implemented using **PostgreSQL** and tested via **FastAPI** endpoints. The project is containerized using **Docker** for easy setup and deployment.

---

## **Database Design**
The database consists of the following tables:
- **Instrument**: Stores information about musical instruments.
- **Accessory**: Stores information about musical accessories.
- **Category**: Categorizes products (e.g., guitars, drums).
- **Brand**: Stores brand information for products.
- **Inventory**: Tracks product stock levels.
- **Receipt**: Records purchase transactions.
- **HistoryOfReceipts**: Stores historical data about receipts.
- **User**: Manages user accounts and roles.
- **Supplier**: Stores supplier information.
- **Inventory_Receipt**: Resolves the many-to-many relationship between `Inventory` and `Receipt`.

---

## **Entity-Relationship Diagram (ERD)**
Below is the Entity-Relationship Diagram (ERD) for the database:

![ER Diagram](./Attachments/ER_Ortizo_Shop.png)

---

## **Class Diagram**
The Class Diagram represents the structure of the database tables and their relationships:

![Class Diagram](./Attachments/CD_Ortizo_Shop.png)

---

## **Technologies Used**
- **Database**: PostgreSQL
- **API Framework**: FastAPI
- **Containerization**: Docker
- **Programming Language**: Python
- **Design Tools**: Lucidchart (for ERD and Class Diagrams)

---

## **Setup Instructions**
Follow these steps to set up the project locally:

### **Prerequisites**
- Docker installed on your machine.
- Docker Compose installed.

### **Steps**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/DatabaseFoundations_FinalProject.git
   cd DatabaseFoundations_FinalProject
    ```
2. Start the Docker containers:

```bash
docker-compose up -d
```
3. Access the FastAPI documentation:
- Open your browser and go to http://localhost:8000/docs.

4. Run database migrations (if applicable):

```bash
docker exec -it <container_id> python manage.py migrate
```
5. Test the API endpoints using the FastAPI interactive docs.

### **API Endpoints**
The following endpoints are available for testing the database:

#### Users
- **Create User**: `POST /users`
- **Get User by ID**: `GET /users/{user_id}`
- **Update User**: `PUT /users/{user_id}`
- **Delete User**: `DELETE /users/{user_id}`

#### Accessories
- **Create Accessory**: `POST /accessories`
- **Get All Accessories**: `GET /accessories`
- **Get Accessory by ID**: `GET /accessories/{accessory_id}`
- **Update Accessory**: `PUT /accessories/{accessory_id}`
- **Delete Accessory**: `DELETE /accessories/{accessory_id}`

#### Brands
- **Create Brand**: `POST /brands`
- **Get All Brands**: `GET /brands`
- **Get Brand by ID**: `GET /brands/{brand_id}`
- **Update Brand**: `PUT /brands/{brand_id}`
- **Delete Brand**: `DELETE /brands/{brand_id}`

#### Categories
- **Create Category**: `POST /categories`
- **Get All Categories**: `GET /categories`
- **Get Category by ID**: `GET /categories/{category_id}`
- **Update Category**: `PUT /categories/{category_id}`
- **Delete Category**: `DELETE /categories/{category_id}`

#### History Receipts
- **Create History Receipt**: `POST /history_receipts`
- **Get All History Receipts**: `GET /history_receipts`
- **Get History Receipt by ID**: `GET /history_receipts/{history_receipt_id}`
- **Update History Receipt**: `PUT /history_receipts/{history_receipt_id}`
- **Delete History Receipt**: `DELETE /history_receipts/{history_receipt_id}`

#### Instruments
- **Create Instrument**: `POST /instruments`
- **Get All Instruments**: `GET /instruments`
- **Get Instrument by ID**: `GET /instruments/{instrument_id}`
- **Update Instrument**: `PUT /instruments/{instrument_id}`
- **Delete Instrument**: `DELETE /instruments/{instrument_id}`

#### Inventory Receipts
- **Create Inventory Receipt**: `POST /inventory_receipts`
- **Get All Inventory Receipts**: `GET /inventory_receipts`
- **Get Inventory Receipt by ID**: `GET /inventory_receipts/{inventory_receipt_id}`
- **Update Inventory Receipt**: `PUT /inventory_receipts/{inventory_receipt_id}`
- **Delete Inventory Receipt**: `DELETE /inventory_receipts/{inventory_receipt_id}`

#### Inventory
- **Create Inventory**: `POST /inventory`
- **Get All Inventory**: `GET /inventory`
- **Get Inventory by ID**: `GET /inventory/{inventory_id}`
- **Update Inventory**: `PUT /inventory/{inventory_id}`
- **Delete Inventory**: `DELETE /inventory/{inventory_id}`

#### Receipts
- **Create Receipt**: `POST /receipts`
- **Get All Receipts**: `GET /receipts`
- **Get Receipt by ID**: `GET /receipts/{receipt_id}`
- **Update Receipt**: `PUT /receipts/{receipt_id}`
- **Delete Receipt**: `DELETE /receipts/{receipt_id}`

#### Suppliers
- **Create Supplier**: `POST /suppliers`
- **Get All Suppliers**: `GET /suppliers`
- **Get Supplier by ID**: `GET /suppliers/{supplier_id}`
- **Update Supplier**: `PUT /suppliers/{supplier_id}`
- **Delete Supplier**: `DELETE /suppliers/{supplier_id}`

### Future Improvements
- Implement a shopping cart feature.

- Add support for promotional discounts and multiple payment methods.

- Integrate the database with a frontend application (web or mobile).

- Optimize database performance for large datasets.

