!!!!!!
PLEASE DO NOT REFRESH THE PAGE TOO FAST OR DO TOO MANY ACTIONS TOO FAST OR SHELVES WILL DIE AND THE SERVER WILL CRASH
!!!!!!
^ this happens because your system wont have enough time to close the shelves before opening again,
this causes the shelves to get corrupted and the site to crash


setting up the site:
--------------------
1) python -m venv env (for windows)
1) python3 -m venv env (for macOS)

2) source env/bin/activate (for macOS)
2) env\Scripts\activate (for windows)

3) pip install -r requirements.txt

3) python main.py (to run the server)


basic credentials:
---------------------
DEFAULT SUPERUSER
username: admin
password: password


how to use the nets qr payment:
---------------------
-> open the NETSPAY Wallet.pdf


compulsory folders: (create the folders if they are missing or the site will die :)))
---------------------
static/media/img_carousl
static/media/img_products
static/media/logos
data/db



when in doubt:
----------------------
open the documentation folder
the file tree is the same as the root filetree
find the python file you have trouble understanding and open the html file inside documentation