# Week 2 Homework

## Question:
1. Data Loading: Once the dataset is loaded, what's the shape of the data?

> 266,855 rows x 20 cols
2.  Data Transformation: Upon filtering the dataset where the passenger count is equal to 0 or the trip distance is equal to zero, how many rows are left?

> 257,400 rows

3. Which of the following creates a new column lpep_pickup_date by converting lpep_pickup_datetime to a date?

> data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
4. What are the existing values of VendorID in the dataset?

> 1 or 2

5. How many columns need to be renamed to snake case?

> 4
6. Once exported, how many partitions (folders) are present in Google Cloud?

> 96
