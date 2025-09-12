# Python Generators Project

A comprehensive project demonstrating advanced usage of Python generators for efficient database operations, batch processing, and memory-efficient data handling.

## 📋 Project Overview

This project introduces advanced Python generator concepts to efficiently handle large datasets, process data in batches, and simulate real-world scenarios involving live updates and memory-efficient computations. All tasks focus on leveraging Python's `yield` keyword to implement generators that provide iterative access to data.

## 🎯 Learning Objectives

- **Master Python Generators**: Create and utilize generators for iterative data processing
- **Handle Large Datasets**: Implement batch processing and lazy loading
- **Memory Efficiency**: Process data without overloading memory
- **SQL Integration**: Use generators with database operations
- **Performance Optimization**: Calculate aggregate functions efficiently

## 🛠️ Prerequisites

- Python 3.x
- MySQL Server
- `mysql-connector-python` package
- Basic understanding of SQL and generators

## 📦 Installation

```bash
# Install MySQL connector
pip install mysql-connector-python

# Start MySQL service (if not running)
sudo systemctl start mysql
# or
sudo service mysql start
```

## 🏗️ Project Structure

```
python-generators-0x00/
├── seed.py              # Database setup and seeding
├── user_data.csv        # Sample data file
├── 0-stream_users.py    # Task 1: Basic generator streaming
├── 1-batch_processing.py # Task 2: Batch processing with generators
├── 2-lazy_paginate.py   # Task 3: Lazy pagination
├── 4-stream_ages.py     # Task 4: Memory-efficient aggregation
├── 0-main.py           # Test file for Task 0
├── 1-main.py           # Test file for Task 1
├── 2-main.py           # Test file for Task 2
├── 3-main.py           # Test file for Task 3
└── README.md           # This file
```

## 📊 Database Schema

### Database: `ALX_prodev`
### Table: `user_data`
| Column    | Type         | Constraints           |
|-----------|-------------|-----------------------|
| user_id   | VARCHAR(36)  | PRIMARY KEY, INDEXED |
| name      | VARCHAR(255) | NOT NULL             |
| email     | VARCHAR(255) | NOT NULL             |
| age       | DECIMAL(3,0) | NOT NULL             |

## 🚀 Tasks Overview

### Task 0: Database Setup (`seed.py`)
**Objective**: Set up MySQL database with user data

**Functions**:
- `connect_db()` - Connects to MySQL server
- `create_database()` - Creates ALX_prodev database
- `connect_to_prodev()` - Connects to ALX_prodev database
- `create_table()` - Creates user_data table
- `insert_data()` - Populates table from CSV

**Usage**:
```bash
python3 0-main.py
```

### Task 1: Stream Users Generator (`0-stream_users.py`)
**Objective**: Create generator to stream database rows one by one

**Function**: `stream_users()` - Yields user records as dictionaries

**Key Features**:
- Uses single loop
- Memory-efficient streaming
- Returns dictionary format

**Usage**:
```bash
python3 1-main.py
```

### Task 2: Batch Processing (`1-batch_processing.py`)
**Objective**: Process large datasets in batches

**Functions**:
- `stream_users_in_batches(batch_size)` - Fetches data in batches
- `batch_processing(batch_size)` - Filters users over 25

**Key Features**:
- Maximum 3 loops total
- Batch processing for efficiency
- Age filtering

**Usage**:
```bash
python3 2-main.py | head -n 5
```

### Task 3: Lazy Pagination (`2-lazy_paginate.py`)
**Objective**: Implement lazy loading for paginated data

**Functions**:
- `paginate_users(page_size, offset)` - Fetches specific page
- `lazy_pagination(page_size)` - Generator for lazy loading

**Key Features**:
- Single loop constraint
- On-demand page loading
- Automatic offset management

**Usage**:
```bash
python3 3-main.py | head -n 7
```

### Task 4: Memory-Efficient Aggregation (`4-stream_ages.py`)
**Objective**: Calculate average age without loading entire dataset

**Functions**:
- `stream_user_ages()` - Yields ages one by one
- `calculate_average_age()` - Computes average using generator

**Key Features**:
- Maximum 2 loops
- No SQL AVERAGE function
- Memory-efficient calculation

**Usage**:
```bash
python3 4-stream_ages.py
```

## 🔧 Setup Instructions

### 1. Configure MySQL Credentials
Update connection parameters in all Python files:
```python
connection = mysql.connector.connect(
    host='localhost',
    user='your_username',    # Usually 'root'
    password='your_password', # Your MySQL password
    database='ALX_prodev'    # Where applicable
)
```

### 2. Create CSV Data File
Ensure `user_data.csv` exists with proper format:
```csv
user_id,name,email,age
00234e50-34eb-4ce2-94ec-26e3fa749796,Dan Altenwerth Jr.,Molly59@gmail.com,67
...
```

### 3. Run Tasks in Order
```bash
# Task 0: Setup database
python3 0-main.py

# Task 1: Stream users
python3 1-main.py

# Task 2: Batch processing
python3 2-main.py

# Task 3: Lazy pagination
python3 3-main.py

# Task 4: Average calculation
python3 4-stream_ages.py
```

## 💡 Key Generator Concepts Demonstrated

### 1. **Basic Generator Pattern**
```python
def my_generator():
    for item in data:
        yield item  # Returns one item at a time
```

### 2. **Memory Efficiency**
- Generators don't load entire datasets into memory
- Process one item at a time
- Ideal for large datasets

### 3. **Lazy Evaluation**
- Data computed only when needed
- Perfect for pagination and streaming

### 4. **Pipeline Processing**
- Chain generators together
- Process data in stages

## 🔍 Expected Output Examples

### Task 0:
```
Connection successful
Table user_data created successfully
Database ALX_prodev is present
[('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67), ...]
```

### Task 1:
```
{'user_id': '00234e50-34eb-4ce2-94ec-26e3fa749796', 'name': 'Dan Altenwerth Jr.', 'email': 'Molly59@gmail.com', 'age': 67}
{'user_id': '006bfede-724d-4cdd-a2a6-59700f40d0da', 'name': 'Glenda Wisozk', 'email': 'Miriam21@gmail.com', 'age': 119}
...
```

### Task 4:
```
Average age of users: 64.8
```

## 🐛 Troubleshooting

### Common Issues:

1. **Connection Errors**: Check MySQL service and credentials
2. **File Not Found**: Ensure CSV file exists in project directory
3. **Empty Results**: Verify database has data
4. **Import Errors**: Check file names match exactly

### Debug Commands:
```bash
# Check MySQL connection
mysql -u root -p

# Verify data
USE ALX_prodev;
SELECT COUNT(*) FROM user_data;

# List files
ls -la *.py *.csv
```

## 📚 Repository Information

- **GitHub Repository**: `alx-backend-python`
- **Directory**: `python-generators-0x00`
- **Required Files**: `seed.py`, `0-stream_users.py`, `1-batch_processing.py`, `2-lazy_paginate.py`, `4-stream_ages.py`, `README.md`

## 🏆 Benefits of This Approach

- **Memory Efficient**: Process large datasets without memory overflow
- **Scalable**: Works with datasets of any size
- **Pythonic**: Uses Python's native generator features
- **Real-world Application**: Patterns used in production systems
- **Educational**: Demonstrates advanced Python concepts

---

**Note**: This project demonstrates practical applications of Python generators in database operations, providing foundation skills for handling large-scale data processing efficiently.