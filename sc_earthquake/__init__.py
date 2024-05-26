from dotenv import load_dotenv
import dash
import dash_bootstrap_components.themes

load_dotenv()


def create_app():
    app = dash.Dash(
        __name__,
        external_stylesheets=[dash_bootstrap_components.themes.BOOTSTRAP],
        meta_tags=[
            {
                "name": "viewport",
                "content": "width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,",
            }
        ],
        suppress_callback_exceptions=True,
        # prevent_initial_callbacks=True,
    )

    return app
