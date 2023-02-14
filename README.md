# Olx Apartment Finder

I wrote the program while I was looking for a flat for myself in Krakow. 
I noticed that most owners cheat potential customers on olx.pl.
Owners only give the price od the rent, and the rest of the costs only after entering the ad. Such as administrative rent, utilities, etc.
I added a GUI to make it easier for my friends to use this program and some useful features that I will describe later.

## Usage examples

- The user selects the list of districts in which he wants to search, he can also select all. If he does not know where the districts are, he can display the map
of districts with the button

- The user chooses whether he wants to look for an apartment or a room

- The user chooses whether he wants to search all offers or let the program run in the background and refresh olx and send him the latest offers by email

- The user enters the minimum and maximum price

- The user selects the search button

## Detailed description 

- <b>Apartments, all offers</b>: Browses all olx offers, according to the filters we have chosen (price, districts). Saves the results in an excel file.
In format: link, price, rent, price+rent

- <b>Rooms, all offers</b>: Browses all olx offers, according to the filters we have chosen (price, districts). 
Here we are looking only at the price from the announcement because there is no administrative rent in the offers of rented rooms.
Also reviewed in this case are descriptions in which the program tries to catch additional fees, such as internet, media, etc.
Saves the results in an excel file.
In format: link, price, bills, price+bills. 

- <b>Rooms, new offers</b>: The program refreshes olx every 30 seconds and checks if there is a new offer that matches our filters. 
If so, it saves this announcement to an Excel file, but also sends this announcement to us at the e-mail address we provided

- <b>Apartments, new offers</b>: same as above :)

## Supported cities

- Kraków
- Warszawa
- Wrocław
- Poznań
- Łódź
- Gdańsk
- Białystok
- Sopot
- Katowice
- Gdynia
- Gliwice

## Libraries

- <b> PyQt6 </b>: GUI
- <b> bs4 </b>: For scrapping Olx
- <b> threading </b>: With this library I could browse every page asynchronously, so if there were 30 pages to browse, I speed up the program almost 30 times
- <b> re </b>: Searching for additional costs in descriptions
- <b> smtplib, EmailMessage, ssl </b>: Automatic sending of e-mails
- <b> dataclass </b>: Data storage
- <b> pandas </b> Saving data in dataframe and saving it to excel
- <b> pillow </b> gets the size of the photo to set the size of the window in which map of districts is displayed

## Screens shots

<img
  src="/pictures/menu.png"
  alt="menu"
  title="menu"
  width="500"
  height="375"
  style="display: inline-block; margin: 0 auto">

<img
  src="/pictures/menu1.png"
  alt="menu"
  title="menu"
  width="500"
  height="375"
  style="display: inline-block; margin: 0 auto">

<img
  src="/pictures/menu2.png"
  alt="menu"
  title="menu"
  width="500"
  height="375"
  style="display: inline-block; margin: 0 auto">
