import uuid
from datetime import datetime
from typing import Optional, Any

from sqlalchemy.orm import sessionmaker

from models import User, Dialog, engine


class Database:

    def __init__(self):
        self.engine = engine
        self.session = sessionmaker(bind=self.engine)()

    def check_if_user_exists(self, user_id: str, raise_exception: bool = False):
        if self.session.query(User).filter_by(user_id=user_id).count() > 0:
            return True
        else:
            if raise_exception:
                raise ValueError(f"User {user_id} does not exist")
            else:
                return False

    def add_new_user(self, user_id: str, chat_id: int, username: str = "", first_name: str = "", last_name: str = ""):
        if not self.check_if_user_exists(user_id):
            user = User(**{'user_id': user_id, 'chat_id': chat_id, 'username': username, 'first_name': first_name,
                           'last_name': last_name})
            self.session.add(user)
            self.session.commit()

    def start_new_dialog(self, user_id: str):
        self.check_if_user_exists(user_id, raise_exception=True)
        user = self.session.query(User).filter_by(user_id=user_id).first()
        dialog_id = str(uuid.uuid4())
        dialog = Dialog(
            **{'dialog_id': dialog_id, 'user_id': user_id, 'chat_mode': user.current_chat_mode,
               'start_time': datetime.now(),
               'messages': []})
        self.session.add(dialog)
        self.session.commit()

        self.session.query(User).filter_by(user_id=user_id).update({'current_dialog_id': dialog_id})
        return dialog_id

    def get_user_attribute(self, user_id: str, key: str):
        self.check_if_user_exists(user_id, raise_exception=True)
        user = self.session.query(User).filter_by(user_id=user_id).first()
        if not hasattr(user, key):
            raise ValueError(f"User {user_id} does not have a value for {key}")
        return getattr(user, key)

    def set_user_attribute(self, user_id: str, key: str, value: Any):
        self.check_if_user_exists(user_id, raise_exception=True)
        self.session.query(User).filter_by(user_id=user_id).update({key: value})
        self.session.commit()

    def get_dialog_messages(self, user_id: str, dialog_id: Optional[str] = None):
        self.check_if_user_exists(user_id, raise_exception=True)
        if dialog_id is None:
            dialog_id = self.get_user_attribute(user_id, "current_dialog_id")
        dialog = self.session.query(Dialog).filter_by(dialog_id=dialog_id).first()
        return dialog.messages

    def set_dialog_messages(self, user_id: str, dialog_messages: list, dialog_id: Optional[str] = None):
        self.check_if_user_exists(user_id, raise_exception=True)
        if dialog_id is None:
            dialog_id = self.get_user_attribute(user_id, "current_dialog_id")
        self.session.query(Dialog).filter_by(dialog_id=dialog_id).update({'messages': dialog_messages})
        self.session.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        self.engine.dispose()
