from flask import jsonify, render_template, Blueprint
from apispec import APISpec
from apispec.exceptions import APISpecError
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin


class FlaskRestfulPlugin(FlaskPlugin):
    """Small plugin override to handle flask-restful resources
    """

    @staticmethod
    def _rule_for_view(view, app=None):
        view_funcs = app.view_functions
        endpoint = None

        for ept, view_func in view_funcs.items():
            if hasattr(view_func, "view_class"):
                view_func = view_func.view_class

            if view_func == view:
                endpoint = ept

        if not endpoint:
            raise APISpecError("Could not find endpoint for view {0}".format(view))

        # WARNING: Assume 1 rule per view function for now
        rule = app.url_map._rules_by_endpoint[endpoint][0]
        return rule


class APISpecExt:
    """Very simple and small extension to use apispec with this API as a flask extension
    """

    def __init__(self, app=None, **kwargs):
        self.spec = None

        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        app.config.setdefault("APISPEC_TITLE", "HHUCheckin")
        app.config.setdefault("APISPEC_VERSION", "1.0.0")
        app.config.setdefault("OPENAPI_VERSION", "3.0.2")
        app.config.setdefault("SWAGGER_JSON_URL", "/swagger.json")
        app.config.setdefault("SWAGGER_UI_URL", "/swagger-ui")
        app.config.setdefault("SWAGGER_URL_PREFIX", None)

        self.spec = APISpec(
            title=app.config["APISPEC_TITLE"],
            version=app.config["APISPEC_VERSION"],
            openapi_version=app.config["OPENAPI_VERSION"],
            plugins=[MarshmallowPlugin(), FlaskRestfulPlugin()],
            **kwargs
        )

        blueprint = Blueprint(
            "swagger",
            __name__,
            template_folder="./templates",
            url_prefix=app.config["SWAGGER_URL_PREFIX"],
        )

        blueprint.add_url_rule(
            app.config["SWAGGER_JSON_URL"], "swagger_json", self.swagger_json
        )
        blueprint.add_url_rule(
            app.config["SWAGGER_UI_URL"], "swagger_ui", self.swagger_ui
        )

        app.register_blueprint(blueprint)

    def swagger_json(self):
        return jsonify(self.spec.to_dict())

    def swagger_ui(self):
        return render_template("swagger.j2")
