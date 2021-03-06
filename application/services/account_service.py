
# flask
from flask import g, abort

# google
from google.appengine.ext import db
from google.appengine.api import mail
from google.appengine.api import users

# victory
from application.models.datastore.user_model import *
from base_service import BaseService
from application import config


class AccountService(BaseService):
    """
    Account Service
    """
    def authorization(self):
        """
        User Authorization.
        * Do not use return object to update user entity.

        @returns UserModel / None
        """
        google_user = users.get_current_user()
        if google_user: google_user = google_user.email().lower()
        if google_user is None: return None

        total_user = db.GqlQuery('select * from UserModel limit 1')
        if total_user.count(1) == 0:
            # set up default user with google account
            user = UserModel()
            user.email = google_user
            user.name = google_user
            user.level = UserLevel.root
            user.put()
            user.get(user.key())    # sync
            return user

        if google_user:
            # auth with google account
            members = db.GqlQuery('select * from UserModel where email = :1 limit 1', google_user).fetch(1)
            if len(members) > 0:
                return members[0]
            elif config.allow_register:
                # register a new user
                user = UserModel()
                user.email = google_user
                user.name = google_user
                user.put()
                user.get(user.key())    # sync
                return user

        return None

    def update_profile(self, name):
        """
        Update user's profile

        :param name: user's name
        """
        user = UserModel().get(g.user.key())
        user.name = name
        user.put()
        user.get(user.key())    # sync

    def invite_user(self, email):
        """
        Invite user to join Takanash with email

        :param email: invited user's email
        :return: UserModel(new user)
        """
        # clear up input value
        email = email.lower()

        user = db.GqlQuery('select * from UserModel where email = :1 limit 1', email)
        if user.count(1) > 0:
            # user is exist
            return UserModel().get(user[0].key())

        # add a new user
        user = UserModel()
        user.email = email
        user.name = email
        user.put()

        # send a invite email
        message = mail.EmailMessage(sender=config.gae_account, subject="%s has invited you to join Victory." % g.user.name)
        message.to = email
        message.body = 'Victory https://%s\n\nAccount: %s' % (config.domain, email)
        message.send()

        user.get(user.key())    #sync
        return user

    def get_users(self):
        """
        Get all users (for root)

        @returns [UserModel.dict()] / []
        """
        if g.user.level != UserLevel.root:
            return abort(403)

        result = []
        members = db.GqlQuery('select * from UserModel order by create_time')
        for user in members:
            result.append(user.dict())
        return result

    def delete_user(self, user_id):
        """
        Delete user with id (for root)

        :param user_id: user id
        """
        # delete self
        if user_id == g.user.key().id():
            return abort(400)

        user = UserModel.get_by_id(user_id)
        if user is None :
            return abort(404)

        # delete relational from application
        applications = db.GqlQuery('select * from ApplicationModel where viewer in :1', [user_id])
        for application in applications:
            application.viewer.remove(user_id)
            application.put()
        applications = db.GqlQuery('select * from ApplicationModel where owner = :1', user_id)
        for application in applications:
            application.delete()

        # delete user
        user.delete()
