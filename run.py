# this is to in theory run flask without having to input the user or db variables

from app import app, db
from app.blueprints.auth.models import User
# from app.blueprints.portfolio.models import Post

if __name__ == '__main__':
    app.run()


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        # 'Post': Post
    }