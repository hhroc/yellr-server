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
    distinct,
    func,
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
        ).slice(start, start+count).all()
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
    organization_id = Column(UUIDType(binary=False),
        ForeignKey('organizations.id'), nullable=True)
    organization = relationship('Organizations', backref='user')
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
            username, password, first, last, email, organization_id):
        user = None
        salt_bytes = hashlib.sha256(str(uuid4()).encode('utf-8')).hexdigest()
        pass_bytes = hashlib.sha256(password.encode('utf-8')).hexdigest()
        pass_val = pass_bytes + salt_bytes
        pass_hash = hashlib.sha256(pass_val.encode('utf-8')).hexdigest()
        user = Users.add(
            user_type = user_type,
            first = first,
            last = last,
            organization_id = organization_id,
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
            top_left_lat=self.top_left_lat,
            top_left_lng=self.top_left_lng,
            bottom_right_lat=self.bottom_right_lat,
            bottom_right_lng=self.bottom_right_lng,
            center_lat=self.center_lat,
            center_lng=self.center_lng,
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
        client = Clients.update(
            client,
            last_lat=lat,
            last_lng=lng,
            platform=platform,
            modified_datetime=datetime.datetime.now()
        )
        return client


    @classmethod
    def update(cls, client, **kwargs):
        keys = set(cls.__dict__)
        if client is not None:
            for k in kwargs:
                if k in keys:
                    setattr(client, k, kwargs[k])
            client.modified_datetime = datetime.datetime.now()
            DBSession.add(client)
            DBSession.commit()
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
    question_type = Column(UnicodeText, nullable=False)
    questions = relationship('Questions', backref='assignment', lazy='joined')
    response_count = 0
    has_responded = False
    answer0_count = 0
    answer1_count = 0
    answer2_count = 0
    answer3_count = 0
    answer4_count = 0


    @classmethod
    def get_all_assignments(cls, admin, client_id=None, lat=0, lng=0):
        _results = DBSession.query(
            Assignments,
            DBSession.query(
                func.count(distinct(Posts.id)).label('response_count'),
            ).filter(
                Posts.assignment_id == Assignments.id,
            ).label('response_count'),
            DBSession.query(
                func.count(distinct(Posts.id)).label('has_responded'),
            ).filter(
                Posts.assignment_id == Assignments.id,
                Posts.client_id == client_id,
            ).label('has_resonded'),
            DBSession.query(
                func.count(distinct(Posts.id)).label('answer0_count'),
            ).filter(
                Posts.assignment_id == Assignments.id,
                Posts.poll_response == 0,
            ).label('answer0_count'),
            DBSession.query(
                func.count(distinct(Posts.id)).label('answer1_count'),
            ).filter(
                Posts.assignment_id == Assignments.id,
                Posts.poll_response == 1,
            ).label('answer1_count'),
            DBSession.query(
                func.count(distinct(Posts.id)).label('answer2_count'),
            ).filter(
                Posts.assignment_id == Assignments.id,
                Posts.poll_response == 2,
            ).label('answer2_count'),
            DBSession.query(
                func.count(distinct(Posts.id)).label('answer3_count'),
            ).filter(
                Posts.assignment_id == Assignments.id,
                Posts.poll_response == 3,
            ).label('answer3_count'),
            DBSession.query(
                func.count(distinct(Posts.id)).label('answer4_count'),
            ).filter(
                Posts.assignment_id == Assignments.id,
                Posts.poll_response == 4,
            ).label('answer4_count'),        
        )
        if not admin:
            _results = _results.filter(
                # we add offsets so we can do simple comparisons
                Assignments.top_left_lat + 90 > lat + 90,
                Assignments.top_left_lng + 180 < lng + 180,
                Assignments.bottom_right_lat + 90 < lat + 90,
                Assignments.bottom_right_lng + 180 > lng + 180,
                cast(Assignments.expire_datetime, Date) >= \
                    cast(datetime.datetime.now(), Date),
            )
        _results = _results.all()

        assignments = []
        for result in _results:
            assignment = result[0]
            assignment.response_count = result[1]
            assignment.has_responded = result[2]
            assignment.answer0_count = result[3]
            assignment.answer1_count = result[4]
            assignment.answer2_count = result[5]
            assignment.answer3_count = result[6]
            assignment.answer4_count = result[7]
            assignments.append(assignment)
        return assignments

    @classmethod
    def get_assignment_by_id(cls, assignment_id, client_id=None):
        _result = DBSession.query(
            Assignments,
            DBSession.query(
                func.count(distinct(Posts.id)).label('response_count'),
            ).filter(
                Posts.assignment_id == Assignments.id,
            ).label('response_count'),
            DBSession.query(
                func.count(distinct(Posts.id)).label('has_responded'),
            ).filter(
                Posts.assignment_id == Assignments.id,
                Posts.client_id == client_id,
            ).label('has_resonded'),
            DBSession.query(
                func.count(distinct(Posts.id)).label('answer0_count'),
            ).filter(
                Posts.assignment_id == Assignments.id,
                Posts.poll_response == 0,
            ).label('answer0_count'),
            DBSession.query(
                func.count(distinct(Posts.id)).label('answer1_count'),
            ).filter(
                Posts.assignment_id == Assignments.id,
                Posts.poll_response == 1,
            ).label('answer1_count'),
            DBSession.query(
                func.count(distinct(Posts.id)).label('answer2_count'),
            ).filter(
                Posts.assignment_id == Assignments.id,
                Posts.poll_response == 2,
            ).label('answer2_count'),
            DBSession.query(
                func.count(distinct(Posts.id)).label('answer3_count'),
            ).filter(
                Posts.assignment_id == Assignments.id,
                Posts.poll_response == 3,
            ).label('answer3_count'),
            DBSession.query(
                func.count(distinct(Posts.id)).label('answer4_count'),
            ).filter(
                Posts.assignment_id == Assignments.id,
                Posts.poll_response == 4,
            ).label('answer4_count'),
        ).filter(
            Assignments.id == assignment_id,
        ).first()
        assignment = _result[0]
        assignment.response_count = _result[1]
        assignment.has_responded = _result[2]
        assignment.answer0_count = _result[3]
        assignment.answer1_count = _result[4]
        assignment.answer2_count = _result[5]
        assignment.answer3_count = _result[6]
        assignment.answer4_count = _result[7]
        return assignment


    def to_dict(self, client_id=None, simple=False):
        resp = super(Assignments, self).to_dict()
        resp.update(
            expire_datetime=str(self.expire_datetime),
            name=self.name,
            top_left_lat=self.top_left_lat,
            top_left_lng=self.top_left_lng,
            bottom_right_lat=self.bottom_right_lat,
            bottom_right_lng=self.bottom_right_lng,
            use_fence=self.use_fence,
            question_type=self.question_type,
            questions=[q.to_dict() for q in self.questions],
            response_count=self.response_count,
            answer0_count=self.answer0_count,
            answer1_count=self.answer1_count,
            answer2_count=self.answer2_count,
            answer3_count=self.answer3_count,
            answer4_count=self.answer4_count,
            has_responded = self.has_responded,
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
            answer0=self.answer0,
            answer1=self.answer1,
            answer2=self.answer2,
            answer3=self.answer3,
            answer4=self.answer4,
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
    language_code = Column(UnicodeText)
    name = Column(UnicodeText)

    @classmethod
    def get_from_code(cls, language_code):
        language = DBSession.query(
            Languages
        ).filter(
            Languages.language_code == language_code
        ).first()
        transaction.commit()
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
    client_id = Column(UUIDType(binary=False), ForeignKey('clients.id'), nullable=False)
    assignment_id = Column(UUIDType(binary=False), ForeignKey('assignments.id'), nullable=True)
    language_code = Column(UnicodeText, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    contents = Column(UnicodeText, nullable=False)

    poll_response = Column(Integer, nullable=False)

    deleted = Column(Boolean, nullable=False)
    approved = Column(Boolean, nullable=False)
    flagged = Column(Boolean, nullable=False)

    media_objects = None

    up_vote_count = 0
    down_vote_count = 0
    has_voted = False
    is_up_vote = False
    
    assignment = None
    

    @classmethod
    def get_approved_posts(cls, client_id, lat, lng, start=0, count=50):
        _posts = DBSession.query(
            Posts,
            DBSession.query(
                func.count(distinct(Votes.id)).label('up_count'),
            ).filter(
                Votes.post_id == Posts.id,
                Votes.is_up_vote == True,
            ).label('up_vote_count'),
            DBSession.query(
                func.count(distinct(Votes.id)).label('down_count'),
            ).filter(
                Votes.post_id == Posts.id,
                Votes.is_up_vote == False,
            ).label('down_vote_count'),
            DBSession.query(
                func.count(distinct(Votes.id)),
            ).filter(
                Votes.client_id == client_id,
                Votes.post_id == Posts.id,
            ).label('has_voted'),
            DBSession.query(
                func.count(distinct(Votes.id)),
            ).filter(
                Votes.client_id == client_id,
                Votes.post_id == Posts.id,
                Votes.is_up_vote == True,
            ).label('is_up_vote'),
            MediaObjects,
            Assignments,
        ).outerjoin(
            Assignments, Assignments.id == Posts.assignment_id,
        ).outerjoin(
            MediaObjects, MediaObjects.post_id == Posts.id,
        ).filter(
            ((Assignments.top_left_lat + 90 > lat + 90) &
                (Assignments.top_left_lng + 180 < lng + 180) &
                (Assignments.bottom_right_lat + 90 < lat + 90) &
                (Assignments.bottom_right_lng + 180 > lng + 180)) |
            (((lat + 0.5) + 90 > Posts.lat + 90) &
                ((lng + 0.5) + 180 > Posts.lng + 180) &
                ((lat - 0.5) + 90 < Posts.lat + 90) &
                ((lng - 0.5) + 180 < Posts.lng + 180)),
        ).filter(
            Posts.contents != '',
        ).filter(
            Posts.deleted == False,
            Posts.flagged == False,
            Posts.approved == True,
        ).slice(start, start+count).all()

        posts = []
        for p in _posts:
            post = p[0]
            post.up_vote_count = p[1]
            post.down_vote_count = p[2]
            post.has_voted = p[3]
            post.is_up_vote = p[4]
            # TODO: add logic to support more than one media object 
            #       when we decide to support that ...
            post.media_objects = p[5] if p[5] != None else None
            post.assignment = p[6] if p[6] != None else None
            posts.append(post)

        return posts


    @classmethod
    def get_posts(cls, top_left_lat, top_left_lng, bottom_right_lat,
            bottom_right_lng, deleted=False, flagged=False, approved=True,
            start=0, count=50):
        _results = DBSession.query(
            Posts,
            MediaObjects,
        ).outerjoin(
            MediaObjects, MediaObjects.post_id == Posts.id,
        ).filter(
            ((top_left_lat + 90 > Posts.lat + 90) &
                (top_left_lng + 180 > Posts.lng + 180) &
                (bottom_right_lat + 90 < Posts.lat + 90) &
                (bottom_right_lng + 180 < Posts.lng + 180)),
        ).filter(
            Posts.contents != '',
        ).filter(
            Posts.deleted == deleted,
        ).slice(start, start+count).all()
        posts = []
        for result in _results:
            post = result[0]
            post.media_objects = result[1] if result[1] != None else None
            posts.append(post)
        return posts


    @classmethod
    def get_post_by_id(cls, id, use_filters=True):
        _post = DBSession.query(
            Posts,
            DBSession.query(
                func.count(distinct(Votes.id)).label('up_count'),
            ).filter(
                Votes.post_id == Posts.id,
                Votes.is_up_vote == True,
            ).label('up_vote_count'),
            DBSession.query(
                func.count(distinct(Votes.id)).label('down_count'),
            ).filter(
                Votes.post_id == Posts.id,
                Votes.is_up_vote == False,
            ).label('down_vote_count'),
            #DBSession.query(
            #    func.count(distinct(Votes.id)),
            #).filter(
            #    Votes.client_id == client_id,
            #    Votes.post_id == Posts.id,
            #).label('has_voted'),
            #DBSession.query(
            #    func.count(distinct(Votes.id)),
            #).filter(
            #    Votes.client_id == client_id,
            #    Votes.post_id == Posts.id,
            #    Votes.is_up_vote == True,
            #).label('is_up_vote'),
            MediaObjects,
            Assignments,
        ).outerjoin(
            Assignments, Assignments.id == Posts.assignment_id,
        ).outerjoin(
            MediaObjects, MediaObjects.post_id == Posts.id,
        ).filter(
            Posts.id == id,
        )
        if use_filters:
            _post = _post.filter(
                Posts.deleted == False,
                Posts.flagged == False,
                Posts.approved == True,
            )
        _post = _post.first()

        post = None
        if _post:
            post = _post[0]
            post.up_vote_count = _post[1]
            post.down_vote_count = _post[2]
            # TODO: add logic to support more than one media object 
            #       when we decide to support that ...
            post.media_objects = _post[3] if _post[3] != None else None
            post.assignment = _post[4] if _post[4] != None else None
        return post


    @classmethod
    def get_all_by_assignment_id(cls, assignment_id,
            deleted=False, start=0, count=50):
        _results = DBSession.query(
            Posts,
            MediaObjects,
        ).outerjoin(
            MediaObjects, MediaObjects.post_id == Posts.id,
        ).filter(
            Posts.assignment_id == assignment_id,
        ).filter(
            Posts.contents != '',
        ).filter(
            Posts.deleted == deleted,
        ).slice(start, start+count).all()
        posts = []
        for result in _results:
            post = result[0]
            post.media_objects = result[1] if result[1] != None else None
            posts.append(post)
        return posts


    @classmethod
    def get_all_by_cuid(cls, cuid, deleted=False, start=0, count=50):
        client = Clients.get_by_cuid(cuid)
        posts = DBSession.query(
            Posts,
        ).filter(
            Poists.client_id == client.id,
        ).slice(start, start+count).all()
        return posts


    @classmethod
    def delete_post(cls, post_id):
        post = Posts.update_by_id(
            post_id,
            deleted=True,
         )
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
            assignment=self.assignment.to_dict() if self.assignment != None else {},
            language_code=self.language_code,
            lat=self.lat,
            lng=self.lng,
            contents=self.contents, 
            poll_response=self.poll_response,
            deleted=self.deleted,
            approved=self.approved,
            flagged=self.flagged,
            media_objects = [self.media_objects.to_dict()] if self.media_objects != None else [],
            up_vote_count = self.up_vote_count,
            down_vote_count = self.down_vote_count,
            has_voted=self.has_voted,
            is_up_vote=self.is_up_vote,
        )
        return resp


Index('index_posts_id', Posts.id, unique=True)
Index('index_posts_assignment_id', Posts.assignment_id, mysql_length=32)
Index('index_posts_language_code', Posts.language_code, mysql_length=2)
Index('index_posts_lat', Posts.lat)
Index('index_posts_lng', Posts.lng)
Index('index_posts_poll_response', Posts.poll_response)


class Votes(Base, TimeStampMixin, CreationMixin):

    __tablename__ = 'votes'
    post_id = Column(UUIDType(binary=False), ForeignKey('posts.id'))
    client_id = Column(UUIDType(binary=False), ForeignKey('clients.id'))
    is_up_vote = Column(Boolean)
    vote_datetime = Column(DateTime)

    @classmethod
    def register_vote(cls, post_id, client_id, is_up_vote):
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
            Votes.delete_by_id(_vote.id)
            vote = _vote
        # the client has already voted, but wants to change
        # their vote.
        elif _vote.is_up_vote != is_up_vote:
            vote = Votes.update_by_id(
                _vote.id,
                is_up_vote=is_up_vote,
            )
        return vote

    def to_dict(self):
        resp = super(Votes, self).to_dict()
        resp.update(
            post_id = str(self.post_id),
            client_id = str(self.client_id),
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
    post_id = Column(UUIDType(binary=False), ForeignKey('posts.id'), nullable=False)
    client_id = Column(UUIDType(binary=False), ForeignKey('clients.id'), nullable=False)
    media_type = Column(UnicodeText, nullable=False)
    filename = Column(UnicodeText, nullable=False)
    preview_filename = Column(UnicodeText, nullable=False)

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
            post_id=str(self.post_id),
            client_id=str(self.client_id),
            media_type=self.media_type,
            filename=self.filename,
            preview_filename=self.preview_filename,
        )
        return resp


Index('index_media_objects_id', MediaObjects.id, unique=True)
Index('index_media_objects_post_id', MediaObjects.post_id, mysql_length=32)


class Organizations(Base, TimeStampMixin, CreationMixin):

    __tablename__ = 'organizations'
    name = Column(UnicodeText)
    description = Column(UnicodeText, nullable=False)
    contact_name = Column(UnicodeText, nullable=False)
    contact_email = Column(UnicodeText, nullable=False)

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

