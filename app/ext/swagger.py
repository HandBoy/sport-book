from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin


def init_app(app):
    app.config.update(
        {
            "APISPEC_SPEC": APISpec(
                title="pets",
                version="1.0.1",
                openapi_version="3.0.2",
                plugins=[MarshmallowPlugin()],
                options={
                    "termsOfService": "http://example.com/terms/",
                    "contact": {
                        "name": "API Support",
                        "url": "http://www.example.com/support",
                        "email": "support@example.com",
                    },
                    "license": {
                        "name": "Apache 2.0",
                        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
                    },
                    "servers": [
                        {
                            "url": "https://development.gigantic-server.com/v1",
                            "description": "Development server",
                        },
                        {
                            "url": "https://staging.gigantic-server.com/v1",
                            "description": "Staging server",
                        },
                        {
                            "url": "https://api.gigantic-server.com/v1",
                            "description": "Production server",
                        },
                    ],
                },
            ),
            "APISPEC_SWAGGER_URL": "/swagger/",
        }
    )
