# this is to in theory run flask without having to input the user or db variables every time i'm testing it out

from app import app, db
from app.blueprints.auth.models import User
from app.blueprints.portfolio.models import Stock, Transaction


@app.shell_context_processor
def make_shell_context():
    return {
        'app': app,
        'db': db,
        'User': User,
        'Stock': Stock,
        'Transaction': Transaction,
    }


if __name__ == '__main__':
    import sys
    print(sys.argv, 'BULLOCKS')

    if len(sys.argv) > 1 and sys.argv[1] == 'shell':
        # Run Flask shell if 'shell' argument is provided
        from flask.globals import _app_ctx_stack
        with app.app_context():
            ctx = _app_ctx_stack.top
            ctx.app = app
            ctx.push()
            import code
            code.interact(local=make_shell_context())
    else:
        # Otherwise, run the development server
        print("neither: len(sys.argv) > 1 and sys.argv[1] == 'shell'")
        # app.run()