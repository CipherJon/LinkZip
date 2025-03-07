from flask import Blueprint
from app.controllers.url_controller import (
    create_short_url,
    redirect_to_original_url,
    get_url_analytics
)

url_blueprint = Blueprint('url_shortener', __name__, url_prefix='/api/v1')

@url_blueprint.route('/shorten', methods=['POST'])
def create_short_url_route():
    return create_short_url()

@url_blueprint.route('/<string:short_code>', methods=['GET'])
def redirect_route(short_code):
    return redirect_to_original_url(short_code)

@url_blueprint.route('/<string:short_code>/analytics', methods=['GET'])
def analytics_route(short_code):
    return get_url_analytics(short_code)
