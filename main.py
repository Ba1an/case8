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
            self.capacities.append(int(number_data[2]))
            self.comfort_levels.append(number_data[3])
            self.are_occupied.append([])
            self.base_prices.append(self.get_price(number_data[1], number_data[3]))

    def get_price(self, type_r, comfort_r):
        prices = {'одноместный': 2900, 'двухместный': 2300, 'полулюкс': 3200, 'люкс': 4100}
        comfort_ind = {'стандарт': 1.0, 'стандарт_улучшенный': 1.2, 'апартамент': 1.5}
        return prices[type_r] * comfort_ind[comfort_r]

    def find_available_room(self, days_to_book, max_price_per_person, num_people):
        all_available = []
        for i in range(len(self.numbers)):
            if max_price_per_person * num_people >= self.base_prices[i]:
                if num_people == self.capacities[i]:
                    if all(day not in self.are_occupied[i] for day in days_to_book):
                        all_available.append(self.numbers[i])
        if not all_available:
            all_available = self.find_other_rooms(days_to_book, max_price_per_person, num_people)
        return all_available

    def find_other_rooms(self, days_to_book, max_price_per_person, num_people):
        all_available = []
        for i in range(len(self.numbers)):
            if max_price_per_person >= (self.base_prices[i] * 0.7):
                if num_people < self.capacities[i]:
                    if all(day not in self.are_occupied[i] for day in days_to_book):
                        all_available.append(self.numbers[i])
        return all_available

    def max_price_room(self, available_rooms, max_price_per_person, num_people):
        final_prices = []
        for i in available_rooms:
            i = int(i) - 1
            if self.base_prices[i] / num_people + 1000 <= max_price_per_person:
                final_prices.append(self.base_prices[i] + 1000 * num_people)
            elif self.base_prices[i] / num_people + 280 <= max_price_per_person:
                final_prices.append(self.base_prices[i] + 280 * num_people)
            else:
                final_prices.append(self.base_prices[i])
        max_price = max(final_prices)
        chosen_room = available_rooms[final_prices.index(max_price)]
        return chosen_room, max_price

    def add_booking(self, room, dates):
        self.are_occupied[int(room) - 1].extend(dates)




class Booking:
    earned_money = [0] * 31
    lost_money = [0] * 31
    def __init__(self, reservation_data):
        self.date = reservation_data[0]
        self.surname = reservation_data[1]
        self.name = reservation_data[2]
        self.patronymic = reservation_data[3]
        self.num_people = int(reservation_data[4])
        self.check_in_date = int(reservation_data[5][:2])
        self.num_nights = int(reservation_data[6])
        self.max_price_per_person = float(reservation_data[7])

    def reservation_dates(self):
        return [x for x in range(self.check_in_date, self.check_in_date + self.num_nights)]

    def will_they(self):
        will_he = random.randint(1, 4)
        if will_he == 1:
            return False
        else:
            return True

    def lost(self):
        for i in self.reservation_dates():
            Booking.lost_money[int(i)-1] += self.num_people * self.max_price_per_person

    def earned(self, price):
        for i in self.reservation_dates():
            Booking.earned_money[int(i)-1] += price



rooms = Room('fund.txt')
with open('booked.txt', 'w', encoding='utf8') as f_b:
    with open('booking.txt', 'r', encoding='utf8') as f2:
        for line in f2:
            reservation = line.split()
            booking = Booking(reservation)
            reserved_dates = booking.reservation_dates()
            av_r = rooms.find_available_room(reserved_dates, booking.max_price_per_person, booking.num_people)
            if av_r:
                r, p = rooms.max_price_room(av_r, booking.max_price_per_person, booking.num_people)
                res = booking.will_they()
                if res:
                    print(f'{booking.date}, комната номер {r}, была забронирована {booking.surname} {booking.name} '
                          f'{booking.patronymic} на период c {booking.check_in_date} до '
                          f'{booking.check_in_date + booking.num_nights - 1} числа.', file=f_b)
                    rooms.add_booking(r, reserved_dates)
                    booking.earned(p)
                else:
                    booking.lost()
            else:
                booking.lost()
        print('потеряли=', booking.lost_money)
        print('заработали=', booking.earned_money)


with open('analytics.txt', 'w', encoding='utf8') as f_a:
    all_rooms = {'одноместный': 0, 'двухместный': 0, 'полулюкс': 0, 'люкс': 0}
    for kind in rooms.room_types:
        for key in all_rooms.keys():
            if kind == key:
                all_rooms[key] += 1

    for i in range(1, 31):
        types = {'одноместный': 0, 'двухместный': 0, 'полулюкс': 0, 'люкс': 0}
        rooms_book = 0
        rooms_free = 0
        for x in range(len(rooms.are_occupied)):
            if i in rooms.are_occupied[x]:
                rooms_book += 1
                types[rooms.room_types[x]] += 1
            else:
                rooms_free += 1
        print('день', i, 'занято', rooms_book, ': свободно', rooms_free, file=f_a)
        print(f"одноместные номера заняты на {(types['одноместный'] * 100)//all_rooms['одноместный']}%, "
              f"двухместные номера заняты на {(types['двухместный'] * 100)//all_rooms['двухместный']}%, "
              f"полулюксовые номера заняты на {(types['полулюкс'] * 100)//all_rooms['полулюкс']}%, "
              f"люксовые номера заняты на {(types['люкс'] * 100)//all_rooms['люкс']}%", file=f_a)
        print(f"Гостинница загружена на {(types['одноместный'] +types['двухместный'] + types['полулюкс'] + types['люкс'])*100//len(rooms.are_occupied)}%", file=f_a)
        print('Потеряли за день', booking.lost_money[i-1], file=f_a)
        print('Заработали за день', booking.earned_money[i-1], file=f_a)
        print('', file=f_a)


