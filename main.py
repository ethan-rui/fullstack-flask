from flask import Flask
import os
from datetime import timedelta

"""
timedelta to limit the session duration
os makes pathing easier, if theres any file that needs pathing please use os.getcwd(), it gets the path leading up to this working directory
"""

basedir = os.getcwd()

app = Flask(
    __name__,
    template_folder=f"{basedir}/templates",
    static_folder=f"{basedir}/static",
)
app.config["SECRET_KEY"] = "1234"
app.permanent_session_lifetime = timedelta(days=3)
"""
saves user profile on browser for 3 days unless logged out.
Import your endpoints/blueprints below, endpoint first, then you register
"""
from services.common_ep import endpoint as EP_Common
from services.admin_ep import endpoint as EP_Admin


"""
import your endpoints from your respective routes file, please give it a name that makes sense
i dont want to mald over this shit
"""

app.register_blueprint(EP_Common, url_prefix="/")
app.register_blueprint(EP_Admin, url_prefix="/admin")
"""
give your endpoint an endpoint a prefix, eg for admin shit it may be /admin
"""
##########

if __name__ == "__main__":
    app.run(debug=True)
"""
checks if the server is started from this particular file
debug=True auto applies changes made to flask file, please =False when submitting
"""