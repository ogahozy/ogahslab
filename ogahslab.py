import os
import sys
import click
from flask_migrate import Migrate, upgrade
from app import create_app, db, cli
from app.models import User, Post, Permission, Role,Comment
#,Message , Notification

app = create_app()
migrate = Migrate(app, db)
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post,'Role':Role,\
            'Permission':Permission,'Comment':Comment}
            #,'Message': Message,
            #'Notification': Notification}
 
 
@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()

    # create or update user roles
    Role.insert_roles()

