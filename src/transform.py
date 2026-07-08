import csv

input_file = "data/users.csv"
output_file = "data/users_cleaned.csv"

with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ["age_group"]
    
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        age = int(row["age"])

        if age < 30:
            row["age_group"] = "young"
        else:
            row["age_group"] = "adult"

        writer.writerow(row)

print("Transformation complete!")