from uuid import uuid4
import hashlib

from time import sleep
from random import randint
import datetime

from sqlalchemy.sql import func
from sqlalchemy_utils import UUIDType
from sqlalchemy import (
    Column,
    cast,
    Date,
    ForeignKey,
    Integer,
    Float,
    Boolean,
    UnicodeText,
    DateTime,
    Index,
    CHAR,
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    relationship,
    scoped_session,
    sessionmaker,
)

DBSession = scoped_session(sessionmaker(expire_on_commit=False))
Base = declarative_base()


class TimeStampMixin(object):
    creation_datetime = Column(DateTime, server_default=func.now())
    modified_datetime = Column(DateTime, server_default=func.now())

class CreationMixin():

    id = Column(UUIDType(binary=False), primary_key=True, unique=True)

    @classmethod
    def add(cls, **kwargs):
        thing = cls(**kwargs)
        if thing.id is None:
            thing.id = str(uuid4())
        DBSession.add(thing)
        DBSession.commit()
        return thing

    @classmethod
    def get_all(cls):
        things = DBSession.query(
            cls,
        ).all()
        return things

    @classmethod
    def get_paged(cls, start=0, count=50):
        things = DBSession.query(
            cls,
        ).slice(start, count).all()
        return things

    @classmethod
    def get_by_id(cls, id):
        thing = DBSession.query(
            cls,
        ).filter(
            cls.id == id,
        ).first()
        return thing

    @classmethod
    def delete_by_id(cls, id):
        thing = cls.get_by_id(id)
        if thing is not None:
            DBSession.delete(thing)
            DBSession.commit()
        return thing

    @classmethod
    def update_by_id(cls, id, **kwargs):
        keys = set(cls.__dict__)
        thing = DBSession.query(cls).filter(cls.id==id).first() #cls.get_by_id(id)
        if thing is not None:
            for k in kwargs:
                if k in keys:
                    setattr(thing, k, kwargs[k])
            thing.modified_datetime = datetime.datetime.now()
            DBSession.add(thing)
            DBSession.commit()
        return thing

    @classmethod
    def reqkeys(cls):
        keys = []
        for key in cls.__table__.columns:
            if '__required__' in type(key).__dict__:
                keys.append(str(key).split('.')[1])
        return keys

    def to_dict(self):
        return {
            'id': str(self.id),
            'creation_datetime': str(self.creation_datetime),
        }


'''
class UserTypes(Base, TimeStampMixin, CreationMixin):

    """
    Different types of users.  Administrators have the most access/privs,
    Moderators have the next leve, Subscribers the next, and then users only
    have the ability to post and view.
    """

    __tablename__ = 'user_types'
    name = Column(UnicodeText, nullable=False)
    description = Column(UnicodeText, nullable=False)

    @classmethod
    def get_from_name(cls, session, name):
        with transaction.manager:
            user_type = DBSession.query(
                UserTypes
            ).filter(
                UserTypes.name == name
            ).first()
            transaction.commit()
        #DBSession.flush()
        return user_type

    def to_dict(self):
        resp = super.to_dict(UserTypes, self).to_dict()
        resp.update(
            name = self.name,
            description = self.description,
        )
        return resp


Index('index_user_types_id', UserTypes.id, unique=True)
'''

class Users(Base, TimeStampMixin, CreationMixin):

    """
    This is the user table.  It holds information for administrators, moderators,
    subscribers, and users.  If the type is a user, than a uniqueid is used to
    idenfity them.  if the user wants to be verified then, then the rest of the
    information is used.  All fields are used for admins, mods, and subs.
    """

    __tablename__ = 'users'
    user_type = Column(UnicodeText, nullable=False)
    username = Column(UnicodeText, nullable=False)
    first = Column(UnicodeText, nullable=False)
    last = Column(UnicodeText, nullable=False)
    #organization_id = Column(UUIDType(binary=False), ForeignKey('organizations.id'), nullable=True)
    #organization = relationship('Organizations', backref='user')
    email = Column(UnicodeText, nullable=False)
    pass_salt = Column(UnicodeText, nullable=False)
    pass_hash = Column(UnicodeText, nullable=False)
    user_geo_fence_id = Column(UUIDType(binary=False),
        ForeignKey('user_geo_fences.id'), nullable=True)
    user_geo_fence = relationship('UserGeoFences', backref='user')
    token = Column(UnicodeText, nullable=True)
    token_expire_datetime = Column(DateTime, nullable=True)

    @classmethod
    def create_new_user(cls, user_type, user_geo_fence_id, 
            username, password, first, last, email): #, organization_id):
        user = None
        salt_bytes = hashlib.sha256(str(uuid4()).encode('utf-8')).hexdigest()
        pass_bytes = hashlib.sha256(password.encode('utf-8')).hexdigest()
        pass_val = pass_bytes + salt_bytes
        pass_hash = hashlib.sha256(pass_val.encode('utf-8')).hexdigest()
        user = Users.add(
            user_type = user_type,
            first = first,
            last = last,
            #organization_id = organization_id,
            #organization = organization,
            email = email,
            username = username,
            pass_salt = salt_bytes,
            pass_hash = pass_hash,
            user_geo_fence_id = user_geo_fence_id,
            token = None,
            token_expire_datetime = None,
        )
        return user

    
    @classmethod
    def get_by_username(cls, username):
        user = DBSession.query(
            Users,
        ).filter(
            Users.username == username,
        ).first()
        return user
    
    @classmethod
    def get_by_token(cls, token):
        user = DBSession.query(
            Users,
        ).filter(
            Users.token == token,
        ).first()
        return user

    @classmethod
    def authenticate(cls, username, password):
        _user = Users.get_by_username(username)
        user = None
        if _user is not None:
            if isinstance(_user.pass_salt, bytes):
                salt_bytes = _user.pass_salt.decode('utf-8')
            elif isinstance(_user.pass_salt, str):
                salt_bytes = _user.pass_salt
            else:
                salt_bytes = _user.pass_salt
            pass_bytes = hashlib.sha256(password.encode('utf-8')).hexdigest()
            pass_val = pass_bytes + salt_bytes
            pass_hash = hashlib.sha256(pass_val.encode('utf-8')).hexdigest()
            if (_user.pass_hash == pass_hash):
                token = str(uuid4())
                token_expire_datetime = datetime.datetime.now() + datetime.timedelta(hours=24*30)
                user = Users.update_by_id(
                    _user.id,
                    token=token,
                    token_expire_datetime=token_expire_datetime,
                )
        return user


    @classmethod
    def validate_token(cls, token):
        user = Users.get_by_token(token)
        valid = False
        if user != None:
            if user.token_expire_datetime > datetime.datetime.now():
                valid = True
        return valid, user


    @classmethod
    def invalidate_token(cls, token):
        user = Users.get_by_token(token)
        if user != None:
            user = Users.update_by_id(
                user.id,
                token=None,
                token_expire_datetime=None,
            )
        return user


    # TODO: make this work with new salt scheme
    '''
    @classmethod
    def change_password(cls, user, old_password, new_password):
        old_pass_bytes = old_password.encode('utf-8')
        old_salt_bytes = user.pass_salt.encode('utf-8')
        old_pass_hash = hashlib.sha256(
            old_pass_bytes + old_salt_bytes
        ).hexdigest()
        success = False
        if user != None and old_pass_hash == user.pass_hash:
            pass_salt = str(uuid4())
            pass_hash = hashlib.sha256('{0}{1}'.format(
                new_password,
                pass_salt
            )).hexdigest()
            user = Users.update_by_id(
                user.id,
                pass_salt=pass_salt,
                pass_hash=pass_hash,
            )
            success = True
        return user, success
    '''

    def to_dict(self):
        resp = super(Users, self).to_dict()
        resp.update(
            username = self.username,
            first = self.first,
            last = self.last,
            email = self.email, 
            user_geo_fence = self.user_geo_fence.to_dict() if self.user_geo_fence != None else None,
            token = self.token, 
            token_expire_datetime = str(self.token_expire_datetime),
        )
        return resp

Index('index_users_id', Users.id, unique=True)
Index('index_users_username', Users.username, mysql_length=32, unique=True)
Index('index_users_token', Users.token, mysql_length=32, unique=True)

class UserGeoFences(Base, TimeStampMixin, CreationMixin):

    """
    Admins, Moderators, and Subscribers all have default geo fences that they
    are set to.  That is, that they can not post of view outside of this fence.
    """

    __tablename__ = 'user_geo_fences'
    top_left_lat = Column(Float)
    top_left_lng = Column(Float)
    bottom_right_lat = Column(Float)
    bottom_right_lng = Column(Float)
    center_lat = Column(Float)
    center_lng = Column(Float)

    def to_dict(self):
        resp = super(UserGeoFences, self).to_dict()
        resp.update(
            #user_geo_fence_id = self.user_geo_fence_id,
            top_left_lat = self.top_left_lat,
            top_left_lng = self.top_left_lng,
            bottom_right_lat = self.bottom_right_lat,
            bottom_right_lng = self.bottom_right_lng,
            center_lat = self.center_lat,
            center_lng = self.center_lng,
        )
        return resp


Index('index_user_geo_fences_id', UserGeoFences.id, unique=True)


class Clients(Base, TimeStampMixin, CreationMixin):

    """
    Clients are users of the mobile app(s)
    """

    __tablename__ = 'clients'
    cuid = Column(UnicodeText, nullable=False)

    first = Column(UnicodeText, nullable=True)
    last = Column(UnicodeText, nullable=True)
    email = Column(UnicodeText, nullable=True)
    pass_hash = Column(UnicodeText, nullable=True)
    pass_salt = Column(UnicodeText, nullable=True)
    verified = Column(Boolean, nullable=False)
    verified_datetime = Column(DateTime, nullable=True)

    last_lat = Column(Float, nullable=False)
    last_lng = Column(Float, nullable=False)

    language_code = Column(UnicodeText, nullable=False)
    platform = Column(UnicodeText, nullable=False)

    deleted = Column(Boolean, nullable=False)

    @classmethod
    def check_in(cls, cuid, lat, lng, language_code, platform):
        client = Clients.get_by_cuid(cuid, lat, lng, language_code, platform)
        client = Clients.update_by_id(
            client.id,
            last_lat=lat,
            last_lng=lng,
            platform=platform,
            modified_datetime=datetime.datetime.now()
        )
        return client

    @classmethod
    def get_by_cuid(cls, cuid, lat, lng, language_code, platform, create=True):
        client = DBSession.query(
            Clients,
        ).filter(
            Clients.cuid == cuid,
        ).first()

        if not client and create == True:

            #
            # This is max gross, and is terrible.  Was done because when a
            # client first comes on line, the android app hammers the server
            # with lots of requests all in a row.  SQLAlchemy serves these up
            # in some kind of queue, which causes SELECT INSERT SELECT INSERT
            # rather than SELECT INSERT SELECT <none>
            #
            # we wait some random amount of time, in hopes that any other
            # 'first' time request, creates the user before we do, so we 
            # don't double create it.
            #
            # possible solutions in the future are to use a store proc that
            # locks the table.
            sleep_time = float(float(randint(1000,2000))/float(1000.0))
            sleep(sleep_time)

            # we do this SELECT again to see if the client has been created in
            # the random hold-off time.
            client = DBSession.query(
                Clients,
            ).filter(
                Clients.cuid == cuid,
            ).first()
            if not client:
                client = Clients.add(
                    cuid=cuid,
                    first='',
                    last='',
                    email='',
                    pass_hash='',
                    pass_salt='',
                    verified=False,
                    verified_datetime=None,
                    last_lat=lat,
                    last_lng=lng,
                    language_code=language_code,
                    platform=platform,
                    deleted=False,
                )
        return client

    @classmethod
    def verify_client(cls, cuid, first, last, email, password):
        client = DBSession.query(
            Clients,
        ).filter(
            Clients.cuid,
        ).first()
        pass_bytes = password.encode('utf-8')
        salt_bytes = hashlib.sha256(str(uuid4()).encode('utf-8'))
        pass_hash = hashlib.sha256('{0}{1}'.format(
            pass_bytes,
            salt_bytes
        )).hexdigest()
        client = Clients.update_by_id(
            client.id,
            first=first,
            last=last,
            email=email,
            pass_salt=salt_bytes,
            pass_hash=pass_hash,
        )
        return client

    def to_dict(self):
        resp = super(Clients, self).to_dict()
        resp.update(
            cuid = self.cuid,
            first = self.first,
            last = self.last,
            email = self.email,
            #passhash =
            #passsalt =
            verified = self.verified,
            verified_datetime = str(self.verified_datetime),
            creation_datetime = str(self.creation_datetime),
            #last_check_in_datetime = str(self.last_checking_datetime),
            #home_zipcode_id = self.home_zipcode_id,
            last_lat = self.last_lat,
            last_lng = self.last_lng,
            #post_view_count = self.post_view_count,
            #post_used_count = self.post_used_count,
            platform = self.platform,
        )
        return resp


Index('index_clients_id', Clients.id, unique=True)
Index('index_clients_cuid', Clients.cuid, mysql_length=32, unique=True)


class Assignments(Base, TimeStampMixin, CreationMixin):

    """
    An assignment is created by a moderator and available for users to pull down.
    Assignments hold a publish date, an experation date, and a geofence
    within them, as well as a user id to tie it to a specific user.
    """

    __tablename__ = 'assignments'
    user_id = Column(UUIDType(binary=False), ForeignKey('users.id'))
    expire_datetime = Column(DateTime)
    name = Column(UnicodeText)
    top_left_lat = Column(Float)
    top_left_lng = Column(Float)
    bottom_right_lat = Column(Float)
    bottom_right_lng = Column(Float)
    use_fence = Column(Boolean)

    questions = relationship('Questions', backref='assignment', lazy='joined')

    posts = relationship('Posts', backref='assignment', lazy='joined')

    @classmethod
    def get_all_open(cls, lat, lng):
        assignments = DBSession.query(
           Assignments,
        ).outerjoin(
           Posts,Posts.assignment_id == Assignments.id,
        ).filter(
            # we add offsets so we can do simple comparisons
            Assignments.top_left_lat + 90 > lat + 90,
            Assignments.top_left_lng + 180 < lng + 180,
            Assignments.bottom_right_lat + 90 < lat + 90,
            Assignments.bottom_right_lng + 180 > lng + 180,
            cast(Assignments.expire_datetime, Date) >= \
                cast(datetime.datetime.now(), Date),
            ).group_by(
                Assignments.id,
            ).all()
        return assignments

    def to_dict(self, client_id=None, simple=False):
        resp = super(Assignments, self).to_dict()
        resp.update(
            expire_datetime = str(self.expire_datetime),
            name = self.name,
            top_left_lat = self.top_left_lat,
            top_left_lng = self.top_left_lng,
            bottom_right_lat = self.bottom_right_lat,
            bottom_right_lng = self.bottom_right_lng,
            questions = [q.to_dict() for q in self.questions],
            response_count = len(self.posts),
        )
        if client_id != None:
            resp.update(
                has_responded = any(p.client_id == client_id for p in self.posts),
            )
        return resp 


Index('index_assignments_id', Assignments.id, unique=True)
Index('index_assignments_expire_datetime', Assignments.expire_datetime)


class Questions(Base, TimeStampMixin, CreationMixin):

    """
    A list of questions that assignments are tied to.  Each question has a language with
    it, thus the same question in multiple languages may exist.  There are 10 possible
    answer fields as to keep our options open.  Question type is used by the client
    on how to display the answer fields.
    """

    __tablename__ = 'questions'
    user_id = Column(UUIDType(binary=False), ForeignKey('users.id'))
    language_code = Column(UnicodeText)
    question_text = Column(UnicodeText)
    description = Column(UnicodeText)
    question_type = Column(UnicodeText)
    answer0 = Column(UnicodeText)
    answer1 = Column(UnicodeText)
    answer2 = Column(UnicodeText)
    answer3 = Column(UnicodeText)
    answer4 = Column(UnicodeText)
    answer5 = Column(UnicodeText)
    answer6 = Column(UnicodeText)
    answer7 = Column(UnicodeText)
    answer8 = Column(UnicodeText)
    answer9 = Column(UnicodeText)

    assignment_id = Column(UUIDType(binary=False), ForeignKey('assignments.id'))

    def to_dict(self):
        resp = super(Questions, self).to_dict()
        resp.update(
            user_id = str(self.user_id),
            language_code = self.language_code,
            question_text = self.question_text,
            description = self.description,
            question_type = self.question_type,
        )
        return resp


Index('index_questions_id', Questions.id, unique=True)
Index('index_questions_language_code', Questions.language_code, mysql_length=2)


class Languages(Base, TimeStampMixin, CreationMixin):

    """
    List of available languages.  The client is responciple for picking whicg language
    it wants.
    """

    __tablename__ = 'languages'
    #language_id = Column(Integer, primary_key=True)
    language_code = Column(UnicodeText)
    name = Column(UnicodeText)

    #questions = relationship('Questions', backref='language', lazy='joined')
    #posts = relationship('Posts', backref='language', lazy='joined')

    @classmethod
    def get_from_code(cls, language_code):
        with transaction.manager:
            language = DBSession.query(
                Languages
            ).filter(
                Languages.language_code == language_code
            ).first()
            transaction.commit()
        #DBSession.flush()
        return language

    def to_dict(self):
        resp = super(Languages, self).to_dict()
        resp.update(
            language_code = self.language_code,
            name = self.name,
        )
        return resp


Index('index_languages_id', Languages.id, unique=True)


class Posts(Base, TimeStampMixin, CreationMixin):

    """
    These are the posts by users.  They can be unsolicited, or associated with a
    assignment.  The post has the users id, the optional assignment id, date/time
    language, and the lat/lng of the post.  There is a boolean option for flagging
    the post as 'innapropreate'.
    """

    __tablename__ = 'posts'
    #post_id = Column(Integer, primary_key=True)
    #user_id = Column(UUIDType(binary=False), ForeignKey('users.user_id'))
    client_id = Column(UUIDType(binary=False), ForeignKey('clients.id'), nullable=False)
    assignment_id = Column(UUIDType(binary=False), ForeignKey('assignments.id'), nullable=True)
    #title = Column(UnicodeText)
    #post_datetime = Column(DateTime)
    #language_id = Column(UUIDType(binary=False), ForeignKey('languages.language_id'))
    language_code = Column(UnicodeText, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    contents = Column(UnicodeText, nullable=False)

    deleted = Column(Boolean, nullable=False)
    approved = Column(Boolean, nullable=False)
    flagged = Column(Boolean, nullable=False)

    media_objects = relationship('MediaObjects', backref='post')
    #assignment = relationship('Assignments', backref='posts', lazy='joined')
    votes = relationship('Votes', backref='post')

    @classmethod
    def get_approved_posts(cls, lat, lng, start=0, count=50):
        if True:
        #with transaction.manager:
            posts = DBSession.query(
                Posts,
            ).outerjoin(
                Assignments,
            ).filter(
                ((Assignments.top_left_lat + 90 > lat + 90) &
                    (Assignments.top_left_lng + 180 < lng + 180) &
                    (Assignments.bottom_right_lat + 90 < lat + 90) &
                    (Assignments.bottom_right_lng + 180 > lng + 180)) |
                (((lat + 0.5) + 90 > Posts.lat + 90) &
                    ((lng + 0.5) + 180 > Posts.lng + 180) &
                    ((lat - 0.5) + 90 < Posts.lat + 90) &
                    ((lng - 0.5) + 180 < Posts.lng + 180))
            ).filter(
                Posts.deleted == False,
                Posts.flagged == False,
                Posts.approved == True,
            ).slice(start, count).all()
        #DBSession.flush()
        return posts

    @classmethod
    def get_posts(cls, top_left_lat, top_left_lng, bottom_right_lat, bottom_right_lng, deleted=False, flagged=False, approved=True, start=0, count=50):
        if True:
        #with transaction.manager:
            posts = DBSession.query(
                Posts,
            #).join(
            #    Assignments,
            ).filter(
                ((top_left_lat + 90 > Posts.lat + 90) &
                    (top_left_lng + 180 > Posts.lng + 180) &
                    (bottom_right_lat + 90 < Posts.lat + 90) &
                    (bottom_right_lng + 180 < Posts.lng + 180))
            ).filter(
                Posts.deleted == deleted,
                #Posts.flagged == flagged,
                #Posts.approved == approved,
            ).slice(start, count).all()
        #DBSession.flush()
        return posts


    @classmethod
    def get_all_from_assignment_id(cls, assignment_id,
            deleted=False, start=0, count=0):
        if True:
        #with transaction.manager:
            posts = DBSession.query(
                Posts,
            ).filter(
                Posts.assignment_id == assignment_id,
                Posts.deleted == deleted,
            ).slice(start, start+count).all()
        #DBSession.flush()
        return posts

    # TODO; write this
    '''
    @classmethod
    def get_all_from_collection_id(cls, collection_id, deleted=False, 
            start=0, count=0):
        with transaction.manager:
            posts = DBSession.query(
                Posts,
            ).join(
                Assignment_id
            )
            posts = Posts._build_posts_query(session).filter(
                CollectionPosts.collection_id == collection_id,
            ).slice(start, start+count).all()
        return posts
    '''

    @classmethod
    def get_all_from_cuid(cls, cuid, deleted=False, start=0, count=0):
        if True:
        #with transaction.manager:
            client = Clients.get_by_cuid(cuid)
            posts = DBSession.query(
                Posts,
            ).filter(
                Poists.client_id == client.id,
            ).slice(start, start+count).all()
        #DBSession.flush()
        return posts #, total_post_count


    @classmethod
    def delete_post(cls, post_id):
        if True:
        #with transaction.manager:
            #post = DBSession.query(
            #    Posts,
            #).filter(
            #    Posts.post_id == post_id,
            #).first()
            #post.deleted = True
            #DBSession.add(post)
            #transaction.commit()
            post = Posts.update_by_id(
                post_id,
                deleted=True,
            )
        #DBSession.flush()
        return post


    @classmethod
    def approve_post(cls, post_id):
        post = Posts.get_by_id(post_id)
        if post.approved == False:
            approved = True
        else:
            approved = False
        post = Posts.update_by_id(
            post.id,
            approved=approved,
        )
        return post


    @classmethod
    def flag_post(cls, post_id):
        post = Posts.get_by_id(post_id)
        if post.flagged == False:
            flagged = True
        else:
            flagged = False
        post = Posts.update_by_id(
            post_id,
            flagged=flagged,
        )
        return post

    def to_dict(self, client_id):
        resp = super(Posts, self).to_dict()
        resp.update(
            assignment=self.assignment.to_dict() if self.assignment_id != None else {},
            language_code=self.language_code,
            lat=self.lat,
            lng=self.lng,
            contents = self.contents, 
            deleted=self.deleted,
            approved=self.approved,
            flagged=self.flagged,
            media_objects = [m.to_dict() for m in self.media_objects],
            #votes = [v.to_dict() for v in self.votes],
            up_count = sum(1 for v in self.votes if v.is_up_vote),
            down_count = sum(1 for v in self.votes if not v.is_up_vote),
        )
        if client_id:
            resp.update(
                has_voted = any(v.client_id == client_id for v in self.votes),
                is_up_vote = any(v.client_id == client_id and v.is_up_vote for v in self.votes),
            )
        return resp

# Posts indexes ... these will be important to implement soon

Index('index_posts_id', Posts.id, unique=True)
Index('index_posts_assignment_id', Posts.assignment_id, mysql_length=32)
Index('index_posts_language_code', Posts.language_code, mysql_length=2)
Index('index_posts_lat', Posts.lat)
Index('index_posts_lng', Posts.lng)
#Index('index_posts_post_datetime', Posts.creation_datetime)
#Index('index_posts_client_id', Posts.client_id)


class Votes(Base, TimeStampMixin, CreationMixin):

    __tablename__ = 'votes'
    #vote_id = Column(Integer, primary_key=True)
    post_id = Column(UUIDType(binary=False), ForeignKey('posts.id'))
    client_id = Column(UUIDType(binary=False), ForeignKey('clients.id'))
    is_up_vote = Column(Boolean)
    vote_datetime = Column(DateTime)

    @classmethod
    def register_vote(cls, post_id, client_id, is_up_vote):
        with transaction.manager:
            _vote = DBSession.query(
                Votes,
            ).filter(
                Votes.post_id == post_id,
                Votes.client_id == client_id,
            ).first()
            vote = None
            # if the client has not voted, register vote.
            if _vote == None:
                vote = Votes.add(
                    post_id=post_id,
                    client_id=client_id,
                    is_up_vote=is_up_vote,
                )
            # if the client has voted, but wants to remove it
            # (sending the vote a second time), then delete it
            elif _vote.is_up_vote == is_up_vote:
                #DBession.delete(_vote)
                #transaction.commit()
                Votes.delete_by_id(_vote.id)
                vote = _vote
            # the client has already voted, but wants to change
            # their vote.
            elif _vote.is_up_vote != is_up_vote:
                vote = Votes.update_by_id(
                    _vote.id,
                    is_up_vote=is_up_vote,
                )
        #DBSession.flush()
        return vote

    def to_dict(self):
        resp = super(Votes, self).to_dict()
        resp.update(
            post_id = self.post_id, 
            client_id = self.client_id,
            is_up_vote = self.is_up_vote,
            vote_datetime = str(self.vote_datetime),
        )
        return resp


Index('index_votes_id', Votes.id, unique=True)
Index('index_votes_post_id', Votes.post_id, mysql_length=32)
Index('index_votes_post_client_id', Votes.client_id, mysql_length=32)


class MediaObjects(Base, TimeStampMixin, CreationMixin):

    """
    Media objects are attached to a post.  A post can have any number of media objects.
    valid media_types are: video, audio, image
    """

    __tablename__ = 'mediaobjects'
    #media_object_id = Column(Integer, primary_key=True)
    post_id = Column(UUIDType(binary=False), ForeignKey('posts.id'), nullable=False)
    #user_id = Column(UUIDType(binary=False), ForeignKey('users.id'))
    client_id = Column(UUIDType(binary=False), ForeignKey('clients.id'), nullable=False)
    #media_type_id = Column(UUIDType(binary=False), ForeignKey('mediatypes.id'))
    media_type = Column(UnicodeText, nullable=False)
    #media_id = Column(UnicodeText)
    filename = Column(UnicodeText, nullable=False)
    preview_filename = Column(UnicodeText, nullable=False)
    #caption = Column(UnicodeText)
    #media_text = Column(UnicodeText)

    #post = relationship('Posts', backref='media_objects', lazy='joined')

    @classmethod
    def get_from_post_id(cls, post_id):
        with transaction.manager:
            media_objects = DBSession.query(
                MediaObjects,
            ).filter(
                MediaObjects.post_id == post_id,
            ).all()
        #DBSession.flush()
        return media_objects

    def to_dict(self):
        resp = super(MediaObjects, self).to_dict()
        resp.update(
            #media_object_id=self.media_object_id,
            post_id=str(self.post_id),
            client_id=str(self.client_id),
            #media_type=self.media_type.to_dict(),
            media_type=self.media_type,
            filename=self.filename,
            preview_filename=self.filename.split('.')[0] + 'p.jpg',
            #caption=self.caption,
            #media_text=self.media_text,
        )
        return resp


Index('index_media_objects_id', MediaObjects.id, unique=True)
Index('index_media_objects_post_id', MediaObjects.post_id, mysql_length=32)


class Organizations(Base, TimeStampMixin, CreationMixin):

    __tablename__ = 'organizations'
    #organization_id = Column(Integer, primary_key=True)
    name = Column(UnicodeText)
    description = Column(UnicodeText, nullable=False)
    contact_name = Column(UnicodeText, nullable=False)
    contact_email = Column(UnicodeText, nullable=False)
    #creation_datetime = Column(DateTime)

    #users = relationship('Users', backref='organization', lazy='joined')

    def to_dict(self):
        resp = super(Organizations, self).to_dict()
        resp.update(
            name = self.name,
            description = self.description,
            contact_name = self.contact_name,
            contact_email = self.contact_email,
            creation_datetime = str(self.creation_datetime),
        )
        return resp


Index('index_organizations_id', Organizations.id, unique=True)

