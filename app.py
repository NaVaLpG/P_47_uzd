from models import db, Car
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
from serializers import CarScheme


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projektai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    search_text = request.args.get("searchbox")
    if search_text:
        all_cars = Car.query.filter(Car.brand.ilike(f"{search_text}%")).all()
        price_sum = sum(car.price for car in all_cars)
        price_avg = round(sum(car.price for car in all_cars) / len(all_cars))
        year_avg = round(sum(car.year for car in all_cars) / len(all_cars))
        age_avg = round(sum(car.age for car in all_cars) / len(all_cars))
        return render_template("index.html",
                               cars=all_cars,
                               price_sum=price_sum,
                               price_avg=price_avg,
                               year_avg=year_avg,
                               age_avg=age_avg
                               )
    else:
        all_cars = Car.query.all()
        price_sum = sum(car.price for car in all_cars)
        price_avg = round(sum(car.price for car in all_cars) / len(all_cars))
        year_avg = round(sum(car.year for car in all_cars) / len(all_cars))
        age_avg = round(sum(car.age for car in all_cars) / len(all_cars))
        return render_template("index.html",
                               cars=all_cars,
                               price_sum=price_sum,
                               price_avg=price_avg,
                               year_avg=year_avg,
                               age_avg=age_avg
                               )


@app.route("/car/<int:row_id>")
def one_project(row_id):
    car = Car.query.get(row_id)
    if car:
        return render_template("one_car.html", car=car)
    else:
        return f"Car with id {row_id} doesn't exist"


@app.route("/car/edit/<int:row_id>", methods=["get", "post"])
def update_project(row_id):
    car = Car.query.get(row_id)
    if not car:
        return f"Car with id {row_id} doesn't exist"
    if request.method == "GET":
        return render_template("update_car_info.html", car=car)

    elif request.method == "POST":
        brand = request.form.get("brandbox")
        model = request.form.get("modelbox")
        color = request.form.get("colorbox")
        year = request.form.get("yearbox")
        price = request.form.get("pricebox")
        car.brand = brand
        car.model = model
        car.color = color
        car.year = int(year)
        car.price = float(price)
        db.session.commit()

        return redirect(f"/car/{row_id}")


@app.route("/car/new", methods=["GET", "POST"])
def create_car():
    if request.method == "GET":
        return render_template("create_new_car.html")
    if request.method == "POST":
        brand = request.form.get("brandbox")
        model = request.form.get("modelbox")
        color = request.form.get("colorbox")
        year = request.form.get("yearbox")
        price = request.form.get("pricebox")
        if brand and model and color and year and price:
            new_car = Car(brand=brand, model=model, color=color, year=year, price=price)
            db.session.add(new_car)
            db.session.commit()
        else:
            return "All boxes must be filled"
    return redirect(url_for("home"))


@app.route("/car/remove/<int:row_id>", methods=["POST"])
def delete_project(row_id):
    car = Car.query.get(row_id)
    db.session.delete(car)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/cars/api")
def cars_api():
    all_cars = Car.query.all()

    cars_data = [CarScheme.model_validate(car).model_dump() for car in all_cars]
    return jsonify(cars_data)


if __name__ == "__main__":
    app.run(port=5001)
