This project represents a RESTful web API for booking rooms in an imaginary school/faculty.
The API provides account, room and booking management systems, making easy adding, changing or deleting users, rooms and bookings.
Some of the functionalities:
    -search for free rooms (giving requirements)
    -make bookings
    -manage users

The API (maybe) also provides a sheduling system, where all users give requirements for dates and hours and the system makes an example shedule.

All the result data is in json format.

## Start me up

- [Install VirtualBox](https://www.virtualbox.org/)
- [Install Vagrant](https://www.vagrantup.com/downloads.html)
- Clone the repository somewhere ```git@github.com:ViktorMarinov/get-a-room.git```
- From inside the cloned directory run ```vagrant up``` and wait...
- From inside the cloned directory run ```vagrant ssh```

Now you are inside ubuntu virtual machine

    workon get_a_room && python get_a_room/manage.py runserver 0.0.0.0:8000

Open [localhost:8000](localhost:8000) from your browser.