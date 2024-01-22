from datetime import datetime, timedelta

def get_birthdays_per_week(users):
    today = datetime.now().date()
    current_day_of_week = today.weekday()
    days_until_monday = (7 - current_day_of_week) % 7
    next_monday = today + timedelta(days=days_until_monday)

    days_of_week = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}

    birthday_groups = {}
    for user in users:
        birthday = user["birthday"].date()
        if birthday <= next_monday + timedelta(days=6):
            day_of_week = days_of_week[birthday.weekday()]
            if day_of_week not in birthday_groups:
                birthday_groups[day_of_week] = []
            birthday_groups[day_of_week].append(user["name"])

    for day, names in birthday_groups.items():
        print(f"{day}: {', '.join(names)}")

users = [
    {"name": "Maciek", "birthday": datetime(2005, 12, 15)},
    {"name": "Oskar", "birthday": datetime(2001, 2, 17)},
    {"name": "Mateusz", "birthday": datetime(1996, 1, 13)},
    {"name": "Anna", "birthday": datetime(1992, 6, 30)},
]

get_birthdays_per_week(users)
