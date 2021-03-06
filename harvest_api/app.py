from config.config import DevelopmentConfig, ProductionConfig, DockerConfig, Config
import getpass, sys, getopt
from server import create_app
from database import create_orm
from waitress import serve

# Get aguments
argv = sys.argv[1:]
opts, args = getopt.getopt(argv, "e:h:u:p:")


# Get the input arguments and store them in a list
config_arg = {}

for opt, arg in opts:
    # Get the host adress of the database
    if(opt == "-h" or opt == "--host"):
        config_arg["db_adress"] = arg
    # Get the user of the database
    elif(opt == "-u" or opt == "--user"):
        config_arg["db_user"] = arg
    # Get the port of the flask flask server
    elif(opt == "-p" or opt == "--port"):
        config_arg["app_port"] = arg

# If the -e dev argument has been passed use development configuration
if ("-e", "dev") in opts or ("-e", "development") in opts:
    # Get password from user
    config_arg["db_password"] = getpass.getpass("Database password: ")
    config = DevelopmentConfig(**config_arg)
# If the -e prod argument has been passed use production configuration
elif ("-e", "prod") in opts or ("-e", "production") in opts:
    config_arg["db_password"] = ""
    config = ProductionConfig(**config_arg)
# If the -e docker argument has been passed use docker configuration
elif ("-e", "docker") in opts:
    config_arg["db_password"] = ""
    config = DockerConfig(**config_arg)
# If the no -e argument has been passed use default configuration
else:
    config_arg["db_password"] = ""
    config = Config(**config_arg)


# Create the orm engines from the config
engines, sessions = create_orm(config)
# Create the flask app from the config
app = create_app(config)


# Start the flask application
if __name__ == '__main__':
    if config.environment == "prod":
        pass
        # If we are in production serve with waitress
        serve(app, host=config.app_host, port=config.app_port)
    elif config.environment == "dev":
        pass
        # If we are in development serve with flask
        app.run(debug = config.DEBUG, host=config.app_host, port=config.app_port)
    else:
        pass
        # By default serve with flask
        app.run(debug = config.DEBUG, host=config.app_host, port=config.app_port)
