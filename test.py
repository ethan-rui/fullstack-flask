from data.user_pages import TableUserPages
import data


db = TableUserPages()
print(db.sub_tables())
print(db.objects())
db.close()