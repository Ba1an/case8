import random

class Room:
    def __init__(self, path_1):
        self.numbers = []
        self.room_types = []
        self.capacities = []
        self.comfort_levels = []
        self.base_prices = []
        self.are_occupied = []
        with open(path_1, 'r', encoding='utf8') as f1:
            numbers_data = f1.readlines()
        for number in numbers_data:
            number_data = number.split()
            self.numbers.append(number_data[0])
            self.room_types.append(number_data[1])
            self.capacities.append(number_data[2])
            self.comfort_levels.append(number_data[3])
            self.are_occupied.append([])
            self.base_prices.append(self.get_price(number_data[1], number_data[3]))

    def get_price(self, type_r, comfort_r):
        prices = {'одноместный': 2900, 'двухместный': 2300, 'полулюкс': 3200, 'люкс': 4100}
        comfort_ind = {'стандарт': 1.0, 'стандарт_улучшенный': 1.2, 'апартамент': 1.5}
        return prices[type_r] * comfort_ind[comfort_r]

    def find_other_rooms(self, days_to_book, max_price_per_person, num_people):
        all_available = []
        for i in range(len(self.numbers)):
            if max_price_per_person * num_people >= (self.base_prices[i] * 0.7):
                if num_people < self.capacities[i]:
                    if all(day not in self.are_occupied[i] for day in days_to_book):
                        all_available.append(self.numbers[i])
        return all_available



class Booking:
    def __init__(self, reservation_data):
        self.date = reservation_data[0]
        self.surname = reservation_data[1]
        self.name = reservation_data[2]
        self.patronymic = reservation_data[3]
        self.num_people = reservation_data[4]
        self.check_in_date = int(reservation_data[5][:2])
        self.num_nights = int(reservation_data[6])
        self.max_price_per_person = float(reservation_data[7])

    def will_they(self):
        will_he = random.randint(1, 4)
        if will_he == 1:
            return False
        return True


def reservation_dates(self):
        return [x for x in range(self.check_in_date, self.check_in_date + self.num_nights)]

rooms = Room('fund.txt')

with open('booking.txt', 'r', encoding='utf8') as f2:
    for line in f2:
        reservation = line.split()
        booking = Booking(reservation)
        reserved_dates = booking.reservation_dates()