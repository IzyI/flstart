from main import create_app
from main.user.models import User
import os
from main.database import db

node=create_app()

# Декоратор app.shell_context_processor регистрирует функцию как функцию контекста оболочки. Когда запускается команда
# flask shell, она будет вызывать эту функцию и регистрировать элементы, возвращаемые ею в сеансе оболочки.
@node.shell_context_processor
def make_shell_context():
    return {'db': db,'User': User}



