from flask import Flask, render_template, request, session
from flask_session import Session
from flask_cors import CORS,cross_origin
from customLogger import custom_logger_class
from moviesExtract import movies_extract_class

custom_logger_obj = custom_logger_class("serverActivity.log", __name__)
custom_logger = custom_logger_obj.create_custom_logger()


application = Flask(__name__)
app=application
custom_logger.info("Configuring session variable")
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
custom_logger.info("Session variable is configured now")


@app.route("/", methods=["GET"])
@cross_origin()
def index():
    try:
        if "user" not in session:
            custom_logger.info("User is logged out")
            return render_template("signup.html")
        else:
            custom_logger.info("User is logged in")
            return render_template("index.html", user = session["user"], list_of_titles = session["titleList"])
    except Exception as e:
        custom_logger.error(str(e))


@app.route("/home", methods=["POST","GET"])
@cross_origin()
def homepage():
    try:
        if request.method == "POST":
            custom_logger.info("User is trying to access homepage from the form")
            name = request.form["name"]
            session["user"] = name
            custom_logger.info("Form input received")
            movie_extract_obj = movies_extract_class()
            list_of_movies = movie_extract_obj.fetch_list_of_movies()
            custom_logger.info("All the movies have been scraped")
            list_of_titles = []
            for movie in list_of_movies:
                list_of_titles.append(movie["title"])
            session["movieList"] = list_of_movies
            session["titleList"] = list_of_titles
            custom_logger.info("All the session keys are initialized")
            return render_template("index.html", user = session["user"], list_of_titles = session["titleList"])  
        else:
            custom_logger.info("User is trying to access homepage from the url bar")
            if "user" in session:
                custom_logger.info("User is logged in")
                custom_logger.info("User is redirected to homepage")
                return render_template("index.html", user = session["user"], list_of_titles = session["titleList"])
            else:
                custom_logger.info("User is logged out")
                custom_logger.info("User is redirected to signup page")
                return render_template("signup.html")  
    except Exception as e:
        custom_logger.error(str(e))


@app.route("/logout", methods=["POST","GET"])
@cross_origin()
def logout():
    try:
        if request.method == "POST":
            session.pop("user", None)
            session.pop("movieList", None)
            session.pop("titleList", None)
            custom_logger.info("All the the session keys are destroyed")
            return render_template("signup.html")  
        else:
            custom_logger.info("User is trying to logout from URL bar")
            if "user" in session:
                custom_logger.info("User is logged in")
                custom_logger.info("User is redirected to home page")
                return render_template("index.html", user = session["user"], list_of_titles = session["titleList"])
            else:
                custom_logger.info("User is logged out")
                custom_logger.info("User is redirected to signup page")
                return render_template("signup.html")  
    except Exception as e:
        custom_logger.error(str(e))
        

@app.route("/search", methods=["POST","GET"])
@cross_origin()
def search():
    try:
        if request.method == "POST":
            custom_logger.info("User is trying to search a movie from the home page form")
            title = request.form["titles"]
            custom_logger.info("Movie name is received from the form")
            for movie in session["movieList"]:
                if movie["title"] == title:
                    custom_logger.info("Movie is found and will be displayed on the search page")
                    return render_template("result.html", user = session["user"], movie = movie)
            custom_logger.info("Movie is not found and user is redirected to home page")
            return render_template("index.html", user = session["user"], list_of_titles = session["titleList"])  
        else:
            custom_logger.info("User is trying to access search page from url bar")
            if "user" in session:
                custom_logger.info("User is now logged in and will now be redirected to home page")
                return render_template("index.html", user = session["user"], list_of_titles = session["titleList"])
            else:
                custom_logger.info("User is logged out and will now be redirected to signup page")
                return render_template("signup.html")  
    except Exception as e:
        custom_logger.error(str(e))


if __name__ == "__main__":
    app.run(port=8000,debug=True)
