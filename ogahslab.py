from app import create_app, db, cli
from app.models import User, Post, Permission, Role,Comment
#,Message , Notification

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post,'Role':Role,\
            'Permission':Permission,'Comment':Comment}
            #,'Message': Message,
            #'Notification': Notification}
 
@app.cli.command()
def deploy():
    Role.insert_roles()
