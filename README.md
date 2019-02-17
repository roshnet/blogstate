# blogstate
    A blogging platform for wannabe bloggers.

## Current production environment
	Site hosted (beta) at https://blogstate.pythonanywhere.com

## Setup Locally
Here's how.
> It is assumed that you have `mysql-server` and `mysql-client` configured.
> If not, install them by
    `sudo apt install mysql-server mysql-client`
> and set a password in the prompt asked.
### Using `pipenv`
1. Clone the repo (or fork if you plan to contribute).
	- To just test the site:
		  `git clone https://github.com/roshnet/blogstate`
	- To enable contributions and send PRs:
		`git clone <url-of-fork>`

2. Install `pipenv` if not already by `pip install pipenv`.
After installing it, `cd` to the cloned repository, and run 
`pipenv install` to install all dependencies.
3. Now, the Python part is all set up. The database needs to be configured.
4. Copy all contents of `dbconfig/setup.sql` to clipboard.
5. Run `sudo mysql -u root -p` and enter the MySQL password, which you entered during installation of MySQL Server ("root" is default, it may be something else on your machine).
6. In the `mysql` console, paste what you copied from `setup.sql`, and execute it. Things may become easier if there's a database manager tool, like phpMyAdmin or something.
7. Now, the database is setup along with the required table(s).
8. Run `python app.py` to start the development server.
9. Links maybe broken since it's under development.
So, manually change the URL to whatever route you like.
Refer to `app.py` for all routes, and manually change the URLs to navigate.
For example, change the URL to `127.0.0.1:5000/signup` to view the signup page.

### Using traditional virtual environment
1. Follow step-1 from above (clone/fork).
2. `cd` to your favourite directory, and run `python3 -m venv bs-env`.
3. Activate it by `source bs-venv/bin/activate`. You may use any other name than `bs-venv`, but the same name.
4. Run `pip install --upgrade pip` to, as expected, upgrade pip, and then install the dependencies by:
> `pip install flask flask-login flask-mysql`
5. Now `cd` to the cloned `blogstate` directory, and run `python app.py` (ensure venv is activated).
6. The project can run only when the environment is activated. Or perhaps you have the dependencies globally installed.

# Useful links
  - [pipenv](https://realpython.com/pipenv-guide)
  - [phpMyAdmin](https://connectwww.com/how-to-install-and-configure-apache-php-mysql-and-phpmyadmin-on-linux-mint/1443/)
  - [A random gist to help in installing stuff](https://gist.github.com/roshnet/41931a5401db8e38c5f3ef6732272f4c)
