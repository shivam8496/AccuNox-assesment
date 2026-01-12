import csv
import random

def generate_sample_csv(filename="sample_data.csv", rows=10):
    departments = ["Engineering", "Sales", "HR", "Marketing", "Finance"]
    roles = ["Dev", "Manager", "QA", "Lead"] # List of roles to pick from
    
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        
        # 1. New Header Matching Your Requirement
        writer.writerow(["RowID", "name", "email", "role", "department", "street", "pincode"])
        
        # 2. Generate Data
        for i in range(rows):
            name = f"User_{i}"
            email = f"user_{i}@company.com"
            
            # You can fix this to "Dev" or make it random. 
            # I used "Dev" to match your example, but you can swap to random.choice(roles)
            role = "Dev" 
            
            dept = random.choice(departments)
            
            # Your example showed User_0 -> s1, User_1 -> s2
            street = f"s{i+1}" 
            
            # Random variable length pincode
            pincode = random.randint(100, 999999)
            
            writer.writerow([i, name, email, role, dept, street, pincode])
            
    print(f"✅ Generated '{filename}' with {rows} rows matching your format.")

if __name__ == "__main__":
    generate_sample_csv(rows=99999)