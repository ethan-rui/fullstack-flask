import data

db = data.Database("inquiries")
print(db.objects())
db.close()