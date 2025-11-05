from DB import Base
from sqlalchemy.orm import relationship
from enum import Enum
from sqlalchemy import (
    Column, Integer, String, ForeignKey, Enum as SqlEnum,
    DateTime, Boolean, UniqueConstraint
)

class Role(Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SqlEnum(Role), default=Role.USER, nullable=False)

    bookings = relationship("Booking", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role.value})>"



class Theater(Base):
    __tablename__ = "theaters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    location = Column(String, nullable=False)

    screens = relationship("Screen", back_populates="theater", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Theater(id={self.id}, name={self.name}, location={self.location})>"


class Screen(Base):
    __tablename__ = "screens"

    id = Column(Integer, primary_key=True, index=True)
    theater_id = Column(Integer, ForeignKey("theaters.id"), nullable=False)
    screen_number = Column(Integer, nullable=False)
    total_seats = Column(Integer, nullable=False)

    theater = relationship("Theater", back_populates="screens")
    seats = relationship("Seat", back_populates="screen", cascade="all, delete-orphan")
    shows = relationship("Show", back_populates="screen", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Screen(id={self.id}, theater_id={self.theater_id}, screen_number={self.screen_number})>"

class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    screen_id = Column(Integer, ForeignKey("screens.id"), nullable=False)
    seat_number = Column(String, nullable=False)  # e.g., A1, A2, B3
    seat_type = Column(String, default="Regular")  # Optional: Regular, Premium, Recliner

    screen = relationship("Screen", back_populates="seats")
    seat_statuses = relationship("SeatStatus", back_populates="seat", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint("screen_id", "seat_number", name="_screen_seat_uc"),)

    def __repr__(self):
        return f"<Seat(id={self.id}, screen_id={self.screen_id}, seat_number={self.seat_number})>"



class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)  # in minutes

    shows = relationship("Show", back_populates="movie", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Movie(id={self.id}, title={self.title}, genre={self.genre})>"



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