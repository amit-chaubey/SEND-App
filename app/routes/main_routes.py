from flask import Blueprint

# # Define a Blueprint for the root route
# main_blueprint = Blueprint('main', __name__)

# @main_blueprint.route('/', methods=['GET'])
# def home():
#     return {"message": "Welcome to the Spelling App API!"}, 200



from flask import Blueprint, render_template

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    # Render the frontend HTML
    return render_template('index.html')
