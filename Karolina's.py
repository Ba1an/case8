class Room:
    def __init__(self, number, room_type, capacity, comfort_level):
        self.number = number
        self.room_type = room_type
        self.capacity = capacity
        self.comfort_level = comfort_level
        self.base_price = self.get_price()
        self.is_occupied = False

    def get_price(self):
        prices = {'одноместный': 2900, 'двухместный': 2300, 'полулюкс': 3200, 'люкс': 4100}
        comfort_ind = {'стандарт': 1.0, 'стандарт улучшенный': 1.2, 'апартамент': 1.5}
        return prices[self.room_type] * comfort_ind[self.comfort_level]/ self.capacity

class Booking:
    def __init__(self, date, surname, name, patronymic, num_people, check_in_date, num_nights, max_price_per_person):
        self.date = date
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.num_people = num_people
        self.check_in_date = check_in_date
        self.num_nights = num_nights
        self.max_price_per_person = max_price_per_person

class Hotel:
    def __init__(self):
        self.rooms = []
        self.bookings = []

    def add_room(self, room):
        self.rooms.append(room)

    def add_booking(self, booking):
        self.bookings.append(booking)

    def find_available_rooms(self, check_in_date, num_nights, num_people, max_price_per_person):
        available_rooms = []
        for room in self.rooms:
            if not room.is_occupied and room.capacity >= num_people and room.get_price() <= max_price_per_person:
                available_rooms.append(room)
        return available_rooms

    def book_room(self, room, booking):
        room.is_occupied = True
        print(f'Room {room.number} has been booked for {booking.num_nights} nights.')

    def process_bookings(self):
        for booking in self.bookings:
            available_rooms = self.find_available_rooms(booking.check_in_date, booking.num_nights,
                                                        booking.num_people, booking.max_price_per_person)
            if available_rooms:
                optimal_room = self.find_optimal_room(available_rooms)
                self.book_room(optimal_room, booking)
            else:
                print("No available rooms for booking.")

    def find_optimal_room(self, available_rooms): !