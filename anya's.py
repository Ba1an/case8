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


class Booking:
    def __init__(self, reservation_data):
        self.date = reservation_data[0]
        self.surname = reservation_data[1]
        self.name = reservation_data[2]
        self.patronymic = reservation_data[3]
        self.num_people = reservation_data[4]
        self.check_in_date = int(reservation_data[5][:2])
        self.num_nights = reservation_data[6]
        self.max_price_per_person = reservation_data[7]

    def find_reservation(self):








rooms = Room('fund.txt')

with open('booking.txt', 'r', encoding='utf8') as f2:
    b = True
    while b:
        reservation = f2.readline()
        if reservation == '':
            b = False
        else:
            reservation = reservation.split()