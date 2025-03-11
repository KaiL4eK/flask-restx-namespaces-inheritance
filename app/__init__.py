from flask import Blueprint, Flask
from flask_restx import Api, Resource, fields, Namespace, Model

## Models

sample_model = Model(
    "sample_response",
    {
        "data": fields.String(example="1"),
    }
)


## Endpoints int

api_metrics_ns = Namespace("api/internal/v1/metrics", description="Endpoints for metrics")

@api_metrics_ns.route("")
class Metrics(Resource):
    @api_metrics_ns.response(200, "Success", sample_model)
    def get(self):
        return {"data": "Hello Int"}

## Endpoints ext

api_ext_metrics_ns = Namespace("v1/metrics", description="Endpoints for metrics")

# @api_ext_metrics_ns.route("")
class MetricsExt(Resource):
    @api_ext_metrics_ns.response(200, "Success", sample_model)
    def get(self):
        return {"data": "Hello Ext"}

## Internal __init__.py

internal_bp = Blueprint("internal", __name__)
internal_api = Api(internal_bp,
                        catch_all_404s=True,
                        version="1.1.1",
                        title=f"Rest API for product",
                        description="Rest API")

internal_api.add_namespace(api_metrics_ns)
api_metrics_ns.add_model(sample_model.name, sample_model)

## External __init__.py

external_bp = Blueprint("external", __name__)
external_api = Api(external_bp,
                    catch_all_404s=True,
                    doc="/swagger-ui",  
                    version="1.1.1",
                    title=f"Rest API for product",
                    description="Rest API")

external_api.add_namespace(api_ext_metrics_ns)
api_ext_metrics_ns.add_model(sample_model.name, sample_model)

api_ext_metrics_ns.add_resource(MetricsExt, "")

## App

app = Flask(__name__)

# Just to repeat our schema
# TODO: Maybe register internal to /api/internal
app.register_blueprint(internal_bp)
app.register_blueprint(external_bp, url_prefix='/api/external')
