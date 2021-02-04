from data.users import TableUser, User

db = TableUser()
objects = db.objects()
db.close()

for x in objects:
    print(x.cart)