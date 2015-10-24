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
    CHAR,
    ForeignKey,
    Integer,
    Float,
    Boolean,
    UnicodeText,
    DateTime,
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    relationship,
    scoped_session,
    sessionmaker,
)

from zope.sqlalchemy import ZopeTransactionExtension
import transaction

DBSession = scoped_session(sessionmaker(
    extension=ZopeTransactionExtension(keep_session=True),
    expire_on_commit=False))
Base = declarative_base()


class TimeStampMixin(object):
    creation_datetime = Column(DateTime, server_default=func.now())
    modified_datetime = Column(DateTime, server_default=func.now())

class CreationMixin():

    id = Column(CHAR(32), primary_key=True)

    @classmethod
    def add(cls, **kwargs):
        with transaction.manager:
            thing = cls(**kwargs)
            if thing.id is None:
                thing.id = str(uuid4())
            DBSession.add(thing)
            transaction.commit()
        return thing

    @classmethod
    def get_all(cls):
        with transaction.manager:
            things = DBSession.query(
                cls,
            ).all()
        return things

    @classmethod
    def get_paged(cls, start=0, count=50):
        with transaction.manager:
            things = DBSession.query(
                cls,
            ).slice(start, count).all()
        return things

    @classmethod
    def get_by_id(cls, id):
        with transaction.manager:
            thing = DBSession.query(
                cls,
            ).filter(
                cls.id == id,
            ).first()
        return thing

    @classmethod
    def delete_by_id(cls, id):
        with transaction.manager:
            thing = cls.get_by_id(id)
            if thing is not None:
                DBSession.delete(thing)
            transaction.commit()
        return thing

    @classmethod
    def update_by_id(cls, id, **kwargs):
        with transaction.manager:
            keys = set(cls.__dict__)
            thing = cls.get_by_id(id)
            if thing is not None:
                for k in kwargs:
                    if k in keys:
                        setattr(thing, k, kwargs[k])
                DBSession.add(thing)
                transaction.commit()
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


class UserTypes(Base, CreationMixin, TimeStampMixin):

    """
    Different types of users.  Administrators have the most access/privs,
    Moderators have the next leve, Subscribers the next, and then users only
    have the ability to post and view.
    """

    __tablename__ = 'usertypes'
    #user_type_id = Column(Integer, primary_key=True)
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
        return user_type

    def to_dict(self):
        resp = super.to_dict(UserTypes, self).to_dict()
        resp.update(
            name = self.name,
            description = self.description,
        )
        return resp


class Users(Base, CreationMixin, TimeStampMixin):

    """
    This is the user table.  It holds information for administrators, moderators,
    subscribers, and users.  If the type is a user, than a uniqueid is used to
    idenfity them.  if the user wants to be verified then, then the rest of the
    information is used.  All fields are used for admins, mods, and subs.
    """

    __tablename__ = 'users'
    #user_id = Column(Integer, primary_key=True)
    #user_type_id = Column(Integer, ForeignKey('usertypes.id'))
    user_type = Column(UnicodeText, nullable=False)

    #client_id = Column(UnicodeText)

    username = Column(UnicodeText, nullable=False)
    first = Column(UnicodeText, nullable=False)
    last = Column(UnicodeText, nullable=False)
    #organization = Column(UnicodeText)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=True)
    email = Column(UnicodeText, nullable=False)
    pass_salt = Column(UnicodeText, nullable=False)
    pass_hash = Column(UnicodeText, nullable=False)
    user_geo_fence_id = Column(Integer,
        ForeignKey('user_geo_fences.id'), nullable=True)
    token = Column(UnicodeText, nullable=True)
    token_expire_datetime = Column(DateTime, nullable=True)

    assignments = relationship('Assignments', backref='author', lazy='joined')


    @classmethod
    def create_new_user(cls, user_type, user_geo_fence_id, \
            username, password, first, last, email, organization_id):
        user = None
        with transaction.manager:
            salt_bytes = str(uuid4()).encode('utf-8')
            pass_bytes = password.encode('utf-8')
            pass_hash = hashlib.sha256(pass_bytes + salt_bytes).hexdigest()
            user = Users.add(
                user_type = user_type,
                user_geo_fence_id = user_geo_fence_id,
                first = first,
                last = last,
                #organization = organization,
                organization_id = organization_id,
                email = email,
                username = username,
                pass_salt = salt_bytes,
                pass_hash = pass_hash,
                token = None,
                token_expire_datetime = None,
            )
        return user

    
    @classmethod
    def get_by_username(cls, username):
        with transaction.manager:
            user = DBSession.query(
                Users,
            ).filter(
                Users.username == username,
            ).first()
        return euser
    
    @classmethod
    def get_from_token(cls, token):
        with transaction.manager:
            user = DBSession.query(
                Users,
            ).filter(
                Users.token == token,
                Users.token != None,
                Users.token != "",
            ).first()
        return user

    @classmethod
    def authenticate(cls, username, password):
        with transaction.manager:
            user = DBSession.query(
                Users,
            ).filter(
                Users.username == username,
            ).first()
            org = None
            token = None
            if user is not None:
                pass_bytes = password.encode('utf-8')
                salt_bytes = user.pass_salt
                pass_hash = hashlib.sha256(pass_bytes + salt_bytes).hexdigest()
                if (user.pass_hash == pass_hash):
                    token = str(uuid4())
                    user.token = token
                    user.token_expire_datetime = datetime.datetime.now() + \
                        datetime.timedelta(hours=24)
                    DBSession.add(user)
                    transaction.commit()
                    #org = Organizations.get_from_id(session, user.organization_id)
        return user


    @classmethod
    def validate_token(cls, token):
        user = Users.get_from_token(token)
        valid = False
        if user != None:
            if user.token_expire_datetime > datetime.datetime.now():
                valid = True
        return valid, user


    @classmethod
    def invalidate_token(cls, token):
        with transaction.manager:
            user = Users.get_from_token(token)
            if user != None:
                user.token = None
                DBSession.add(user)
                transaction.commit()
        return user


    @classmethod
    def change_password(cls, user, old_password, new_password):
        with transaction.manager:
            #user = DBSession.query(
            #    Users,
            #).filter(
            #    Users.user_name == username,
            #).first()
            old_pass_bytes = old_password.encode('utf-8')
            old_salt_bytes = user.pass_salt.encode('utf-8')
            old_pass_hash = hashlib.sha256(
                old_pass_bytes + old_salt_bytes
            ).hexdigest()
            success = False
            if old_pass_hash == user.pass_hash:
                pass_salt = str(uuid4())
                pass_hash = hashlib.sha256('{0}{1}'.format(
                    new_password,
                    pass_salt
                )).hexdigest()
                user.pass_salt = pass_salt
                user.pass_hash = pass_hash
                DBSession.add(user)
                transaction.commit()
                success = True
        return user, success


    def to_dict(self):
        resp = super(Users, self).to_dict()
        resp.update(
            #user_id = self.user_id,
            username = self.username,
            first = self.first,
            last = self.last,
            organization = self.organization.to_dict() if self.organization != None else None,
            email = self.email, 
            #pass_salt = 
            #pass_hash = 
            user_geo_fence = self.geo_fence.to_dict() if self.geo_fence != None else None,
            token = self.token, 
            token_expire_datetime = str(self.token_expire_datetime),
        )
        return resp

class UserGeoFences(Base, CreationMixin, TimeStampMixin):

    """
    Admins, Moderators, and Subscribers all have default geo fences that they
    are set to.  That is, that they can not post of view outside of this fence.
    """

    __tablename__ = 'user_geo_fences'
    #user_geo_fence_id = Column(Integer, primary_key=True)
    top_left_lat = Column(Float)
    top_left_lng = Column(Float)
    bottom_right_lat = Column(Float)
    bottom_right_lng = Column(Float)
    center_lat = Column(Float)
    center_lng = Column(Float)

    users = relationship('Users', backref='geo_fence', lazy='joined')

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


class Clients(Base, CreationMixin, TimeStampMixin):

    """
    Clients are users of the mobile app(s)
    """

    __tablename__ = 'clients'
    #client_id = Column(Integer, primary_key=True)
    cuid = Column(UnicodeText, nullable=False)

    first = Column(UnicodeText, nullable=True)
    last = Column(UnicodeText, nullable=True)
    email = Column(UnicodeText, nullable=True)
    pass_hash = Column(UnicodeText, nullable=True)
    pass_salt = Column(UnicodeText, nullable=True)
    verified = Column(Boolean, nullable=False)
    verified_datetime = Column(DateTime, nullable=True)

    #creation_datetime = Column(DateTime)
    #last_check_in_datetime = Column(DateTime, nullable=False)

    #home_zipcode_id = Column(Integer, ForeignKey('zipcodes.id'))

    last_lat = Column(Float, nullable=False)
    last_lng = Column(Float, nullable=False)

    #post_view_count = Column(Integer)
    #post_used_count = Column(Integer)

    language_code = Column(UnicodeText, nullable=False)
    platform = Column(UnicodeText, nullable=False)

    deleted = Column(Boolean, nullable=False)

    @classmethod
    def check_in(cls, cuid, lat, lng, language_code, platform):
        with transaction.manager:
            #print "check_in(): cuid: {0}".format(cuid)
            #client = DBSession.query(
            #    Clients,
            #).filter(
            #    Clients.cuid == cuid,
            #).first()
            #print "check_in(): client.cuid: {0}, client.client_id: {1}".format(client.cuid, client.client_id)
            client = Clients.get_by_cuid(cuid, lat, lng, language_code, platform)
            client.last_lat = lat
            client.last_lng = lng
            client.modified_datetime = datetime.datetime.now()
            client.platform = platform
            DBSession.add(client)
            transaction.commit()
        return client

    @classmethod
    def get_by_cuid(cls, cuid, lat, lng, language_code, platform, create=True):
        client = None
        with transaction.manager:
            client = DBSession.query(
                Clients,
            ).filter(
                Clients.cuid == cuid,
            ).first()
            transaction.commit()

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
    def verify_client(cls, cuid, first_name, last_name, email, \
            password):
        with transaction.manager:
            client = DBSession.query(
                Clients,
            ).filter(
                Clients.cuid,
            ).first()
            client.first_name = first_name
            client.last_name = last_name
            client.email = email
            pass_bytes = password.encode('utf-8')
            salt_bytes =hashlib.sha256(str(uuid4()).encode('utf-8'))
            client.passhash = hashlib.sha256('{0}{1}'.format(
                pass_bytes,
                salt_bytes
            )).hexdigest()
            client.pass_salt = salt_bytes
            client.verified = True
            client.verified_datetime = datetime.datetime.now()
            DBSession.add(client)
            transaction.commit()
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

class Assignments(Base, CreationMixin, TimeStampMixin):

    """
    An assignment is created by a moderator and available for users to pull down.
    Assignments hold a publish date, an experation date, and a geofence
    within them, as well as a user id to tie it to a specific user.
    """

    __tablename__ = 'assignments'
    #assignment_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    #publish_datetime = Column(DateTime)
    expire_datetime = Column(DateTime)
    name = Column(UnicodeText)
    #assignment_unique_id = Column(UnicodeText)
    top_left_lat = Column(Float)
    top_left_lng = Column(Float)
    bottom_right_lat = Column(Float)
    bottom_right_lng = Column(Float)
    use_fence = Column(Boolean)
    collection_id = Column(Integer, ForeignKey('collections.id'), nullable=True)

    questions = relationship('Questions', backref='assignment', lazy='joined')

    posts = relationship('Posts', backref='assignment', lazy='joined')

    @classmethod
    def get_all_open(cls, lat, lng):
        with transaction.manager:
           assignments = DBSession.query(
               Assignments,
               #func.count(Posts.post_id),
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
                Assignments.id

            ).all()
        return assignments

    @classmethod
    def set_collection(cls, assignment_id, collection_id):
        with transaction.manager:
            assignment = DBSession.query(
                Assignments,
            ).filter(
                Assignments.assignment_id == assignment_id,
            ).first()
            assignment.collection_id = collection_id

            DBSession.add(assignment)
            transaction.commit()

        return assignment

    def to_dict(self, client_id=None, simple=False):
        resp = super(Assignments, self).to_dict()
        resp.update(
            #assignment_id = self.assignment_id,
            #user_id = self.user_id,
            author = self.author.to_dict() if not simple else {},
            #publish_datetime = str(self.publish_datetime),
            expire_datetime = str(self.expire_datetime),
            name = self.name,
            top_left_lat = self.top_left_lat,
            top_left_lng = self.top_left_lng,
            bottom_right_lat = self.bottom_right_lat,
            bottom_right_lng = self.bottom_right_lng,
            #use_fence = self.use_fence,
            collection_id = self.collection_id if not simple else 0,
            questions = [q.to_dict() for q in self.questions],
            response_count = len(self.posts),
        )
        if client_id != None:
            resp.update(
                has_responded = any(p.client_id == client_id for p in self.posts),
            )
        return resp 


class Questions(Base, CreationMixin, TimeStampMixin):

    """
    A list of questions that assignments are tied to.  Each question has a language with
    it, thus the same question in multiple languages may exist.  There are 10 possible
    answer fields as to keep our options open.  Question type is used by the client
    on how to display the answer fields.
    """

    __tablename__ = 'questions'
    #question_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    #language_id = Column(Integer, ForeignKey('languages.language_id'))
    language_code = Column(UnicodeText)
    question_text = Column(UnicodeText)
    description = Column(UnicodeText)
    #question_type_id = Column(Integer, ForeignKey('questiontypes.question_type_id'))
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

    assignment_id = Column(Integer, ForeignKey('assignments.id'))

    def to_dict(self):
        resp = super(Questions, self).to_dict()
        resp.update(
            user_id = self.user_id,
            language_code = self.language_code,
            question_text = self.question_text,
            description = self.description,
            question_type = self.question_type,
        )
        return resp

class Languages(Base, CreationMixin, TimeStampMixin):

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
    def get_from_code(cls, session, language_code):
        with transaction.manager:
            language = DBSession.query(
                Languages
            ).filter(
                Languages.language_code == language_code
            ).first()
        return language

    def to_dict(self):
        resp = super(Languages, self).to_dict()
        resp.update(
            language_code = self.language_code,
            name = self.name,
        )
        return resp


class Posts(Base, CreationMixin, TimeStampMixin):

    """
    These are the posts by users.  They can be unsolicited, or associated with a
    assignment.  The post has the users id, the optional assignment id, date/time
    language, and the lat/lng of the post.  There is a boolean option for flagging
    the post as 'innapropreate'.
    """

    __tablename__ = 'posts'
    #post_id = Column(Integer, primary_key=True)
    #user_id = Column(Integer, ForeignKey('users.user_id'))
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=True)
    #title = Column(UnicodeText)
    #post_datetime = Column(DateTime)
    #language_id = Column(Integer, ForeignKey('languages.language_id'))
    language_code = Column(UnicodeText, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    contents = Column(UnicodeText, nullable=False)

    deleted = Column(Boolean, nullable=False)
    approved = Column(Boolean, nullable=False)
    flagged = Column(Boolean, nullable=False)

    media_objects = relationship('MediaObjects', backref='post')
    #assignment = relationship('Assignments', backref='posts', lazy='joined')
    votes = relationship('Votes', backref='post', lazy='joined')

    @classmethod
    def get_approved_posts(cls, lat, lng, start=0, count=50):
        with transaction.manager:
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
        return posts

    @classmethod
    def get_posts(cls, top_left_lat, top_left_lng, bottom_right_lat, bottom_right_lng, deleted=False, flagged=False, approved=True, start=0, count=50):
        with transaction.manager:
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
        return posts


    @classmethod
    def get_all_from_assignment_id(cls, session, assignment_id,
            deleted=False, start=0, count=0):
        with transaction.manager:
            posts = Posts._build_posts_query(session).filter(
                Posts.assignment_id == assignment_id,
                Posts.deleted == deleted,
            ).slice(start, start+count).all()
        return posts #, total_post_count


    @classmethod
    def get_all_from_collection_id(cls, collection_id, deleted=False, 
            start=0, count=0):
        with transaction.manager:
            posts = Posts._build_posts_query(session).filter(
                CollectionPosts.collection_id == collection_id,
            ).slice(start, start+count).all()
        return posts


    @classmethod
    def get_all_from_cuid(cls, cuid, deleted=False, start=0, count=0):
        with transaction.manager:
            posts = Posts._build_posts_query(session).filter(
                Clients.cuid == cuid,
            ).slice(start, start+count).all()
        return posts #, total_post_count


    @classmethod
    def delete_post(cls, post_id):
        with transaction.manager:
            post = DBSession.query(
                Posts,
            ).filter(
                Posts.post_id == post_id,
            ).first()
            post.deleted = True
            DBSession.add(post)
            transaction.commit()
        return post


    @classmethod
    def approve_post(cls, post_id):
        with transaction.manager:
            post = DBSession.query(
                Posts,
            ).filter(
                Posts.post_id == post_id,
            ).first()
            # change the approved state of the post (T -> F, F -> T)
            if post.approved == False:
                post.approved = True
            else:
                post.approved = False
            DBSession.add(post)
            transaction.commit()
        return post


    @classmethod
    def flag_post(cls, post_id):
        with transaction.manager:
            post = DBSession.query(
                Posts,
            ).filter(
                Posts.post_id == post_id,
            ).first()
            if post.flagged == False:
                post.flagged = True
            else:
                post.flagged = False
            DBSession.add(post)
            transaction.commit()
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
            flagged=self.approved,
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

#Index('index_posts_post_id', Posts.post_id, unique=True)
#Index('index_posts_post_datetime', Posts.creation_datetime)
#Index('index_posts_client_id', Posts.client_id)

class Votes(Base, CreationMixin, TimeStampMixin):

    __tablename__ = 'votes'
    #vote_id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    client_id = Column(Integer, ForeignKey('clients.id'))
    is_up_vote = Column(Boolean)
    vote_datetime = Column(DateTime)

    @classmethod
    def register_vote(cls, session, post_id, client_id, is_up_vote):
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
                vote = Votes(
                    post_id = post_id,
                    client_id = client_id,
                    is_up_vote = is_up_vote,
                    vote_datetime = datetime.datetime.now(),
                )
                DBSession.add(vote)
                transaction.commit()
            # if the client has voted, but wants to remove it
            # (sending the vote a second time), then delete it
            elif _vote.is_up_vote == is_up_vote:
                session.delete(_vote)
                transaction.commit()
                vote = _vote
            # the client has already voted, but wants to change
            # their vote.
            elif _vote.is_up_vote != is_up_vote:
                _vote.is_up_vote = is_up_vote
                DBSession.add(_vote)
                transaction.commit()
                vote = _vote
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

class MediaObjects(Base, CreationMixin, TimeStampMixin):

    """
    Media objects are attached to a post.  A post can have any number of media objects.
    valid media_types are: video, audio, image
    """

    __tablename__ = 'mediaobjects'
    #media_object_id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    #user_id = Column(Integer, ForeignKey('users.id'))
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    #media_type_id = Column(Integer, ForeignKey('mediatypes.id'))
    media_type = Column(UnicodeText, nullable=False)
    #media_id = Column(UnicodeText)
    filename = Column(UnicodeText, nullable=False)
    preview_filename = Column(UnicodeText, nullable=False)
    #caption = Column(UnicodeText)
    #media_text = Column(UnicodeText)

    #post = relationship('Posts', backref='media_objects', lazy='joined')

    @classmethod
    def get_from_post_id(cls, session, post_id):
        with transaction.manager:
            media_objects = DBSession.query(
                MediaObjects,
                #MediaObjects.file_name,
                #MediaObjects.caption,
                #MediaObjects.media_text,
                #MediaTypes.name,
                #MediaTypes.description,
            ).join(
                #PostMediaObjects,
                #MediaTypes,
            ).filter(
                MediaObjects.post_id == post_id,
                #PostMediaObjects.media_object_id == MediaObjects.media_object_id,
                #PostMediaObjects.post_id == post_id,
                #MediaTypes.media_type_id == MediaObjects.media_type_id,
            ).all()
        return media_objects

    def to_dict(self):
        resp = super(MediaObjects, self).to_dict()
        resp.update(
            #media_object_id = self.media_object_id,
            post_id = self.post_id,
            client_id = self.client_id,
            #media_type = self.media_type.to_dict(),
            media_type = self.media_type,
            filename = self.filename,
            preview_filename = self.filename.split('.')[0] + 'p.jpg',
            #caption = self.caption,
            #media_text = self.media_text,
        )
        return resp


class CollectionPosts(Base, CreationMixin, TimeStampMixin):

    """
    Table to link posts to a collection.
    """

    __tablename__ = 'collection_posts'
    #collection_post_id = Column(Integer, primary_key=True)
    collection_id = Column(Integer, ForeignKey('collections.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)

    def to_dict(self):
        resp = super(CollectionPosts, self).to_dict()
        resp.update(
            collection_id = self.collection_id,
            post_id = self.post_id,
        )
        return resp


class Collections(Base, CreationMixin, TimeStampMixin):

    """
    Collections are a means to organize posts, and are used by moderators and
    subscribers.
    """

    __tablename__ = 'collections'
    #collection_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    #collection_datetime = Column(DateTime)
    name = Column(UnicodeText)
    description = Column(UnicodeText)
    tags = Column(UnicodeText)
    enabled = Column(Boolean)
    #private = Column(Boolean)

    assignment = relationship(
        "Assignments",
        backref='collection',
        lazy='joined'
    )

    posts = relationship(
        "Posts",
        secondary=CollectionPosts.__table__,
        backref='collections',
        lazy='joined'
    )

    @classmethod
    def get_all_from_user_id(cls, user_id):
        with transaction.manager:
            collections = Collections._build_collections_query(session).filter(
                Collections.user_id == user_id,
            ).all()
        return collections


    @classmethod
    def disable_collection(cls, collection_id):
        with transaction.manager:
            collection = DBSession.query(
                Collections,
            ).filter(
                Collections.collection_id == collection_id,
            ).first()
            collection.enabled = False
            DBSession.add(collection)
            transaction.commit()
        return collection


    @classmethod
    def add_post_to_collection(cls, session, collection_id, post_id):
        with transaction.manager:
            collection_post = CollectionPosts(
                collection_id = collection_id,
                post_id = post_id,
            )
            DBSession.add(collection_post)
            transaction.commit()
        return collection_post


    @classmethod
    def remove_post_from_collection(cls, session, collection_id, post_id):
        with transaction.manager:
            collection_post = DBSession.query(
                CollectionPosts,
            ).filter(
                CollectionPosts.collection_id == collection_id,
                CollectionPosts.post_id == post_id,
            ).first()
            success = False
            if collection_post != None:
                session.delete(collection_post)
                transaction.commit()
                success = True
        return success


    def to_dict(self):
        resp = super(Collections, self).to_dict()
        resp.update(
            #user_id = self.user_id,
            collection_datetime = str(collection_datetime),
            name = self.name,
            description = self.description,
            tags = self.tags,
            enabled = self.enabled,
            #posts = [p.to_dict() for p in self.posts], 
            post_count = len(self.posts),
        )
        return resp


class Organizations(Base, CreationMixin, TimeStampMixin):

    __tablename__ = 'organizations'
    #organization_id = Column(Integer, primary_key=True)
    name = Column(UnicodeText)
    description = Column(UnicodeText, nullable=False)
    contact_name = Column(UnicodeText, nullable=False)
    contact_email = Column(UnicodeText, nullable=False)
    #creation_datetime = Column(DateTime)

    users = relationship('Users', backref='organization', lazy='joined')

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

