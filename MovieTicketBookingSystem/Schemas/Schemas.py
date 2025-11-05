from  pydantic import BaseModel
from enum import Enum


'''
Models.py

class Show(Base):
    __tablename__ = "shows"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    screen_id = Column(Integer, ForeignKey("screens.id"), nullable=False)
    show_time = Column(DateTime, nullable=False)

    movie = relationship("Movie", back_populates="shows")
    screen = relationship("Screen", back_populates="shows")
    seat_statuses = relationship("SeatStatus", back_populates="show", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="show", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Show(id={self.id}, movie_id={self.movie_id}, screen_id={self.screen_id}, show_time={self.show_time})>"



class SeatStatus(Base):
    __tablename__ = "seat_statuses"

    id = Column(Integer, primary_key=True, index=True)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False)
    show_id = Column(Integer, ForeignKey("shows.id"), nullable=False)
    is_booked = Column(Boolean, default=False)

    seat = relationship("Seat", back_populates="seat_statuses")
    show = relationship("Show", back_populates="seat_statuses")

    __table_args__ = (UniqueConstraint("seat_id", "show_id", name="_seat_show_uc"),)

    def __repr__(self):
        return f"<SeatStatus(seat_id={self.seat_id}, show_id={self.show_id}, is_booked={self.is_booked})>"



class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    show_id = Column(Integer, ForeignKey("shows.id"), nullable=False)
    seats = Column(String, nullable=False)  
    user = relationship("User", back_populates="bookings")
    show = relationship("Show", back_populates="bookings")

    def __repr__(self):
        return f"<Booking(id={self.id}, user_id={self.user_id}, show_id={self.show_id}, seats={self.seats})>"


  Now we need design pydantic scehmas for the above models.




                
'''        

class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"

class UserSchema(BaseModel):
    id: int
    email: str
    full_name: str
    role: Role

    class Config:
        orm_mode = True

class TheaterSchema(BaseModel):
    id: int
    name: str
    location: str
    total_screens: int

    class Config:
        orm_mode = True

class ScreenSchema(BaseModel):
    id: int
    theater_id: int
    screen_number: int
    total_seats: int

    class Config:
        orm_mode = True


class SeatSchema(BaseModel):
    id: int
    screen_id: int
    seat_number: str
    seat_type: str

    class Config:
        orm_mode = True

class MovieSchema(BaseModel):
    id: int
    title: str
    genre: str
    duration: int

    class Config:
        orm_mode = True


 