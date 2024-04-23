import random
import ru_local as ru


class Room:
    """
    It is a class representing all rooms in the hotel

    Attributes:
    - numbers: list of str, containing numbers of rooms
    - room_types: list of str, containing types of each room
    - capacities: list of int, containing maximum numbers of people in one room
    - comfort_levels: list of str, containing comfort levels of each room
    - base_prices: list of int, containing the whole price of each room for one day
    - are_occupied: list of lists, containing days when each room is occupied

    Methods:
    - get_price(type_r, comfort_r): counts the whole price of room for one day
    - find_available_room(days_to_book, max_price_per_person, num_people): finds rooms suitable for request
    - def find_other_rooms(days_to_book, max_price_per_person, num_people): finds rooms suitable for request considering
    discount when we couldn't find any rooms
    - max_price_room(available_rooms, max_price_per_person, num_people): chooses the room with maximum price including
    breakfast
    - add_booking(room, dates): adds days when the room is occupied
    """
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
        """
        counts the whole price of room for one day
        :param type_r: type of room
        :param comfort_r: level of comfort
        :return: price of the room for 1 day
        """
        prices = {ru.room_type_1: 2900, ru.room_type_2: 2300, ru.room_type_3: 3200, ru.room_type_4: 4100}
        comfort_ind = {ru.room_comfort_1: 1.0, ru.room_comfort_2: 1.2, ru.room_comfort_3: 1.5}
        return prices[type_r] * comfort_ind[comfort_r]

    def find_available_room(self, days_to_book, max_price_per_person, num_people):
        """
        finds rooms suitable for request
        :param days_to_book: days when guests are staying
        :param max_price_per_person: maximum affordable price for 1 person for 1 day
        :param num_people: number of guests
        :return: list of suitable rooms
        """
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
        """
        finds rooms suitable for request considering discount when we couldn't find any rooms
        :param days_to_book: days when guests are staying
        :param max_price_per_person: maximum affordable price for 1 person for 1 day
        :param num_people: number of guests
        :return: list of suitable rooms
        """
        all_available = []
        for i in range(len(self.numbers)):
            if max_price_per_person >= (self.base_prices[i] * 0.7):
                if num_people < self.capacities[i]:
                    if all(day not in self.are_occupied[i] for day in days_to_book):
                        all_available.append(self.numbers[i])
        return all_available

    def max_price_room(self, available_rooms, max_price_per_person, num_people):
        """
        chooses the room with maximum price including breakfast
        :param available_rooms: suitable rooms
        :param max_price_per_person: aximum affordable price for 1 person for 1 day
        :param num_people: number of guests
        :return: the most expensive room, how much it costs
        """
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
        """
        adds days when the room is occupied
        :param room: which room is booked
        :param dates: for what days the room is booked
        :return: None
        """
        self.are_occupied[int(room) - 1].extend(dates)


class Booking:
    """
    It is a class dealing with 1 booking request

    Attributes:
    - date: str, date of the request for reservation
    - surname: str, Surname of the person who made booking
    - name: str, name of the person who made booking
    - patronymic: str, patronymic of the person who made booking
    - num_people: int, or how many people was the request
    - check_in_date: int, when guests are arriving
    - num_nights: int, for how many nights guests want to stay
    - max_price_per_person: float, maximum price guests are ready to pay

    Class attributes:
    - earned_money: how much money the hotel earns each day of the month
    - lost_money: how much money the hotel looses each day of the month

    Methods:
    - reservation_dates(): make list of the days guests want to stay
    - will_they(): count the 25 % probability of the final denial of booking
    - lost(): counts how much money the hotels looses each day when the booking is canceled
    - earned(price): adds the price to earned money for reservation days

    """
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
        """
        make list of the days guests want to stay
        :return: list of reserved days
        """
        return [y for y in range(self.check_in_date, self.check_in_date + self.num_nights)]

    def will_they(self):
        """
        count the 25 % probability of the final denial of booking
        :return: True or False
        """
        will_he = random.randint(1, 4)
        if will_he == 1:
            return False
        else:
            return True

    def lost(self):
        """
        counts how much money the hotels looses each day when the booking is canceled
        :return: None
        """
        for i in self.reservation_dates():
            Booking.lost_money[int(i)-1] += self.num_people * self.max_price_per_person

    def earned(self, price):
        """
        adds the price to earned money for reservation days
        :param price: counted price for 1 day
        :return: None
        """
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
                    print(f'{booking.date}, {ru.booking_1} {r}, {ru.booking_2} {booking.surname} {booking.name} '
                          f'{booking.patronymic} {ru.booking_3} {booking.check_in_date} {ru.booking_4} '
                          f'{booking.check_in_date + booking.num_nights - 1} {ru.booking_5}.', file=f_b)
                    rooms.add_booking(r, reserved_dates)
                    booking.earned(p)
                else:
                    booking.lost()
            else:
                booking.lost()


with open('analytics.txt', 'w', encoding='utf8') as f_a:
    all_rooms = {ru.room_type_1: 0, ru.room_type_2: 0, ru.room_type_3: 0, ru.room_type_4: 0}
    for kind in rooms.room_types:
        for key in all_rooms.keys():
            if kind == key:
                all_rooms[key] += 1

    for j in range(1, 31):
        types = {ru.room_type_1: 0, ru.room_type_2: 0, ru.room_type_3: 0, ru.room_type_4: 0}
        rooms_book = 0
        rooms_free = 0
        for x in range(len(rooms.are_occupied)):
            if j in rooms.are_occupied[x]:
                rooms_book += 1
                types[rooms.room_types[x]] += 1
            else:
                rooms_free += 1
        print(ru.final_1, j, ru.final_2, rooms_book, ru.final_3, rooms_free, file=f_a)
        print(f"{ru.final_4} {(types[ru.room_type_1] * 100)//all_rooms[ru.room_type_1]}%, "
              f"{ru.final_5} {(types[ru.room_type_2] * 100)//all_rooms[ru.room_type_2]}%, "
              f"{ru.final_6} {(types[ru.room_type_3] * 100)//all_rooms[ru.room_type_3]}%, "
              f"{ru.final_7} {(types[ru.room_type_4] * 100)//all_rooms[ru.room_type_4]}%", file=f_a)
        a = (types[ru.room_type_1] + types[ru.room_type_2] + types[ru.room_type_3] +
             types[ru.room_type_4])*100//len(rooms.are_occupied)
        print(f"{ru.final_8} {a}%", file=f_a)
        print(ru.final_9, booking.lost_money[j-1], file=f_a)
        print(ru.final_10, booking.earned_money[j-1], file=f_a)
        print('', file=f_a)
