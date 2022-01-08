from app import db
from app import newsletter

new_newsletter = newsletter(link="https://www.youtube.com/watch?v=TWdSi0Xw4u0", date="2022/01/22")

for i in range(14):
    db.session.add(new_newsletter)
    db.session.commit()
