CREATE DATABASE shop;
\c shop;

-- Tabla Category
CREATE TABLE IF NOT EXISTS Category (
    CategoryID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Description TEXT
);

-- Tabla Brand
CREATE TABLE IF NOT EXISTS Brand (
    BrandID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Country VARCHAR(100)
);

-- Tabla Instrument
CREATE TABLE IF NOT EXISTS Instrument (
    InstrumentID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Description TEXT,
    Price DECIMAL(10,2) NOT NULL CHECK (Price > 0),
    Stock INT NOT NULL CHECK (Stock >= 0),
    CategoryID INT NOT NULL,
    BrandID INT NOT NULL,
    FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID),
    FOREIGN KEY (BrandID) REFERENCES Brand(BrandID)
);

-- Tabla Accessory
CREATE TABLE IF NOT EXISTS Accessory (
    AccessoryID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Description TEXT,
    Price DECIMAL(10,2) NOT NULL CHECK (Price > 0),
    Stock INT NOT NULL CHECK (Stock >= 0),
    CategoryID INT NOT NULL,
    BrandID INT NOT NULL,
    FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID),
    FOREIGN KEY (BrandID) REFERENCES Brand(BrandID)
);

-- Tabla users
CREATE TABLE IF NOT EXISTS users (
    UserID SERIAL PRIMARY KEY,
    Username VARCHAR(100) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Role VARCHAR(50) NOT NULL CHECK (Role IN ('administrator', 'customer')),
    Email VARCHAR(255) UNIQUE NOT NULL
);

-- Tabla Supplier
CREATE TABLE IF NOT EXISTS Supplier (
    SupplierID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Address VARCHAR(255),
    ContactInfo VARCHAR(255) NOT NULL
);

-- Tabla Receipt
CREATE TABLE IF NOT EXISTS Receipt (
    ReceiptID SERIAL PRIMARY KEY,
    UserID INT NOT NULL,
    SupplierID INT,
    "Date" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    TotalAmount DECIMAL(10,2) NOT NULL CHECK (TotalAmount >= 0),
    ReceiptType VARCHAR(50) NOT NULL CHECK (ReceiptType IN ('purchase', 'sale')),
    FOREIGN KEY (UserID) REFERENCES users(UserID),
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
);

-- Tabla Inventory
CREATE TABLE IF NOT EXISTS Inventory (
    InventoryID SERIAL PRIMARY KEY,
    InstrumentID INT,
    AccessoryID INT,
    Quantity INT NOT NULL CHECK (Quantity >= 0),
    DateUpdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (InstrumentID) REFERENCES Instrument(InstrumentID),
    FOREIGN KEY (AccessoryID) REFERENCES Accessory(AccessoryID)
);

-- Tabla History_Receipts
CREATE TABLE IF NOT EXISTS History_Receipts (
    HistoryID SERIAL PRIMARY KEY,
    ReceiptID INT NOT NULL,
    "Date" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Status VARCHAR(50) NOT NULL CHECK (Status IN ('completed', 'refunded')),
    FOREIGN KEY (ReceiptID) REFERENCES Receipt(ReceiptID)
);

-- Tabla Inventory_Receipt
CREATE TABLE IF NOT EXISTS Inventory_Receipt (
    InventoryReceiptID SERIAL PRIMARY KEY,
    InventoryID INT NOT NULL,
    ReceiptID INT NOT NULL,
    Quantity INT NOT NULL CHECK (Quantity >= 0),
    FOREIGN KEY (InventoryID) REFERENCES Inventory(InventoryID),
    FOREIGN KEY (ReceiptID) REFERENCES Receipt(ReceiptID)
);
