from enum import Enum
from collections import defaultdict
from threading import Lock



class City(Enum):
           BANGALORE = 'Bangalore'
           DELHI     = 'Delhi'

class SeatCategory(Enum):
        SILVER   = 'SILVER'
        GOLD     = 'GOLD'
        PLATINUM = 'PLATINUM'

class Seat:
         
         def __init__(self,seat_id,row,category):
                 self.seat_id=seat_id
                 self.row=row
                 self.category=category

class Movie:
      
      def __init__(self,movie_id,name,duration_minutes):
              self.movie_id=movie_id
              self.name=name
              self.duration_minutes=duration_minutes

class Screen:
         
         def __init__(self,screen_id):
                 self.screen_id=screen_id
                 self.seats=[]

class Show:
         def __init__(self,show_id,movie,screen,start_time):
                 self.show_id=show_id
                 self.movie=movie
                 self.screen=screen
                 self.start_time=start_time
                 self.booked_seat_ids=[]
                 self._lock=Lock()

         def book_seat(self,seat_id):
                with self._lock:
                         if seat_id in self.booked_seat_ids:
                                 return False
                         self.booked_seat_ids.append(seat_id)
                         return True
    
class Theatre:
         def __init__(self,theatre_id,city,address):
                      self.theatre_id=theatre_id         
                      self.city=city
                      self.address=address
                      self.shows=[]
                      self.screens=[]
class Payment:
        
        def __init__(self,payment_id):
                self.payment_id=payment_id

class Booking:
        
        def __init__(self,show,seats):
                self.show=show
                self.booked_seats=seats
                self.payment=None
        
class MovieController:

        def __init__(self):
                self.city_wise_movies=defaultdict(list)
                self.all_movies={}

        def add_movie(self,movie,city):
                self.city_wise_movies[city].append(movie)
                self.all_movies[movie.movie_id]=movie             
        
        def remove_movie(self,movie_id,city):
                self.city_wise_movies[city]=[
                       m for m in self.city_wise_movies[city] if m.movie_id!=movie_id
                ]
                self.all_movies.pop(movie_id,None)
        
        def get_movie_by_name(self,name):
                return next((m for m in self.all_movies.values() if m.name==name),None)
        
        def get_movies_by_city(self,city):
                 return list(self.city_wise_movies[city])
        
class TheatreController:
        def __init__(self):
                self.city_wise_theatres=defaultdict(list)
                self.all_theatres={}
        
        def add_theatre(self,theatre):
                self.city_wise_theatres[theatre.city].append(theatre)
                self.all_theatres[theatre.theatre_id]=theatre  
                 
        def remove_theatre(self,theatre_id,city):
                self.city_wise_theatres[city]=[
                       m for m in self.city_wise_theatres[city] if m.theatre_id!=theatre_id
                       ]
                self.all_theatres.pop(theatre_id,None)

        def get_all_shows(self,movie,city):
                results={}
                for theatre in self.city_wise_theatres[city]:
                        matching=[s for s in theatre.shows if s.movie.movie_id==movie.movie_id]

                        if matching:
                            results[theatre]=matching
                return results


class BookMyShow:

        def __init__(self):
                self.movie_ctrl=MovieController()
                self.theatre_ctrl=TheatreController()
                self._next_movie_id=1
                self._next_theatre_id=1
                self._next_show_id=1

        def initialize(self):
                avengers = Movie(self._next_movie_id, 'AVENGERS', 128);   self._next_movie_id += 1
                baahubali = Movie(self._next_movie_id, 'BAAHUBALI', 180); self._next_movie_id += 1

                for city in City:
                        self.movie_ctrl.add_movie(avengers, city)
                        self.movie_ctrl.add_movie(baahubali, city)

            
                self._create_theatre(City.BANGALORE)
                self._create_theatre(City.DELHI)         

        def _create_theatre(self, city: City):
                        th = Theatre(self._next_theatre_id, city, address=f"Addr {self._next_theatre_id}")
                        self._next_theatre_id += 1

                        # make one screen
                        screen = Screen(screen_id=1)
                        screen.seats = self._create_seats()
                        th.screens.append(screen)

                        # two shows: morning/afternoon
                        movie_list = self.movie_ctrl.get_movies_by_city(city)
                        for idx, (movie, start) in enumerate(zip(movie_list, (8, 16)), start=1):
                                show = Show(self._next_show_id, movie, screen, start)
                                self._next_show_id += 1
                                th.shows.append(show)

                        self.theatre_ctrl.add_theatre(th)

        def _create_seats(self) -> list[Seat]:
                seats: list[Seat] = []
                # SILVER 0–39
                for i in range(40):
                         seats.append(Seat(i, row=(i//10)+1, category=SeatCategory.SILVER))
                # GOLD 40–69
                for i in range(40, 70):
                        seats.append(Seat(i, row=(i//10)+1, category=SeatCategory.GOLD))
                # PLATINUM 70–99
                for i in range(70, 100):
                        seats.append(Seat(i, row=(i//10)+1, category=SeatCategory.PLATINUM))
                return seats

        def create_booking(self, user_city: City, movie_name: str, seat_id: int):
                movie = self.movie_ctrl.get_movie_by_name(movie_name)
                if not movie:
                        print("Movie not found.")
                        return

                shows_map = self.theatre_ctrl.get_all_shows(movie, user_city)
                if not shows_map:
                        print("No shows for that movie in your city.")
                        return

                # pick first theatre & show
                theatre, shows = next(iter(shows_map.items()))
                show = shows[0]

                if show.book_seat(seat_id):
                # gather seat objects
                        seat_objs = [s for s in show.screen.seats if s.seat_id == seat_id]
                        booking = Booking(show, seat_objs)
                        booking.payment = Payment(payment_id=1)  # demo
                        print(f"Booking successful: {movie_name} @ {show.start_time}:00 in {user_city.value}")
                else:
                        print("Seat already booked, try again.")


if __name__ == '__main__':
    app = BookMyShow()
    app.initialize()
    app.create_booking(City.BANGALORE, 'BAAHUBALI', seat_id=30)
    app.create_booking(City.BANGALORE, 'BAAHUBALI', seat_id=31)                    
