from core.app import app, HOST, PORT
from core.controllers.towers import bp as bp_towers
from core.controllers.apartments import bp as bp_apartments
from core.controllers.vehicles import bp as bp_vehicles


app.register_blueprint(bp_towers, url_prefix='/api/towers')
app.register_blueprint(bp_apartments, url_prefix='/api/apartments')
app.register_blueprint(bp_vehicles, url_prefix='/api/vehicles')


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
