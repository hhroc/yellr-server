import os
import sys
import uuid
import datetime
import json

import hashlib

import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    Base,
    UserGeoFences,
    UserTypes,
    MediaTypes,
    Languages,
    Users,
    Assignments,
    Questions,
    QuestionAssignments,
    QuestionTypes,
    Subscribers,
    Zipcodes,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    #with transaction.manager:
    if True:
        #
        # User Types
        #
        usertype_system = UserTypes.get_from_name(DBSession, 'system')
        #print "usertype_system: {0}".format(usertype_system)
        if usertype_system == None:
            usertype_system = UserTypes.add_user_type(
                session = DBSession,
                description = 'The system user.',
                name = 'system',
            )
            #DBSession.add(usertype_system)
            #print "System user added."        

        usertype_admin = UserTypes.get_from_name(DBSession, 'admin')
        if usertype_admin == None:
            usertype_admin = UserTypes.add_user_type(
                session = DBSession,
                description = 'A system administrator.  This user type has the highest level of permissions.',
                name = 'admin',
            )
            #DBSession.add(usertype_admin)

        usertype_mod = UserTypes.get_from_name(DBSession, 'moderator')
        if usertype_mod == None:
            usertype_mod = UserTypes.add_user_type(
                session = DBSession,
                description = 'A system moderator.  This user type moderators content produced by users.',
                name = 'moderator',
            )
            #DBSession.add(usertype_mod)

        usertype_sub = UserTypes.get_from_name(DBSession, 'subscriber')
        if usertype_sub == None:
            usertype_sub = UserTypes.add_user_type(
                session = DBSession,
                description = 'A system subscriber.  This user type uses content produced by moderators and users.',
                name = 'subscriber',
            )
            #DBSession.add(usertype_sub)
        
        #usertype_user = UserTypes(
        #    description = 'A basic user.  Accesses the system via mobile app or webpage.',
        #    name = 'user',
        #)
        #DBSession.add(usertype_user)

        #
        # Media Types
        #
        mediatype_image = MediaTypes.from_value(DBSession, 'image')
        if mediatype_image == None:
            mediatype_image = MediaTypes.add_media_type(
                session = DBSession,
                description = 'An Image.',
                name = 'image',
            )

        mediatype_audio = MediaTypes.from_value(DBSession, 'audio')
        if mediatype_audio == None:
            mediatype_audio = MediaTypes.add_media_type(
                session = DBSession,
                description = 'An Audio Clip.',
                name = 'audio',
            )

        mediatype_video = MediaTypes.from_value(DBSession, 'video')
        if mediatype_video == None:
            mediatype_video = MediaTypes.add_media_type(
                session = DBSession,
                description = 'A Video.',
                name = 'video',
            )

        mediatype_text = MediaTypes.from_value(DBSession, 'text')
        if mediatype_text == None:
            mediatype_text = MediaTypes.add_media_type(
                session = DBSession,
                description = 'Text.',
                name = 'text',
            )

        # Languages
        language_english = Languages.get_from_code(DBSession, 'en')
        if language_english == None:
            language_english = Languages.add_language(
                session = DBSession,
                language_code = 'en',
                name = 'English',
            )

        language_spanish = Languages.get_from_code(DBSession, 'es')
        if language_spanish == None:
            language_spanish = Languages.add_language(
                session = DBSession,
                language_code = 'es',
                name = 'Spanish',
            )

        transaction.commit()

    #with transaction.manager:

    if not Users.check_exists(DBSession, 'system'):
        #system_user_client_id = str(uuid.uuid4())
        system_user_type = UserTypes.get_from_name(DBSession,'system')

        # create the systme user geofence, of the entire earth
        system_user_fence = UserGeoFences.create_fence(
            session = DBSession,
            top_left_lat = 90.0,
            top_left_lng = -180.0,
            bottom_right_lat = -90.0,
            bottom_right_lng = -180.0,
        )

        # create the system user
        system_user = Users.create_new_user(
            session = DBSession,
            user_type_id = system_user_type.user_type_id,
            user_geo_fence_id = system_user_fence.user_geo_fence_id,
            #client_id = system_user_client_id,
            #verified = True,
            #user_name = '',
            user_name = 'system',
            password = hashlib.sha256('password').hexdigest(),
            first_name = 'SYSTEM',
            last_name = 'USER',
            email = '',
            organization = 'Yellr',
            #pass_salt = '',
            #pass_hash = 'hash', # NOTE: will never be the result of a md5 hash
        )

        # set the system user as verified
        #system_user = Users.verify_user(
        #    session = DBSession,
        #    client_id = system_user_client_id,
        #    user_name = 'system',
        #    # we hash the password since we will be getting the password
        #    # pre-hashed from the web front-end
        #    password = hashlib.sha256('password').hexdigest(),
        #    email=''
        #)

    #with transaction.manager:
    if True:
        
        question_type_free_text = QuestionTypes.get_from_type(DBSession, 'free_text')
        if question_type_free_text == None:
            question_type_free_text = QuestionTypes.add_question_type(
                session = DBSession,
                question_type = 'free_text',
                question_type_description = 'Free form text response.',
            )

        question_type_multiple_choice = QuestionTypes.get_from_type(DBSession, 'multiple_choice')
        if question_type_multiple_choice == None:
            question_type_multiple_choice = QuestionTypes.add_question_type(
                session = DBSession,
                question_type = 'multiple_choice',
                question_type_description = \
                    ('Allows for up to ten multiple'
                     'choice options')
            )

        #transaction.commit()
    '''
    if Zipcodes.get_count(DBSession) == 0:

        with open("zipcodes/zipcode.csv", "r") as f:
            csv = f.read()

        rows = csv.split("\n")
        index = 0
        for row in rows:
            if index != 0 and row != '':
                values = row.replace('"','').split(',')
            
                Zipcodes.add_zipcode(
                    session = DBSession,
                    _zipcode = values[0],
                    city = values[1],
                    state_code = values[2],
                    lat = float(values[3]),
                    lng = float(values[4]),
                    timezone = values[5],
                )
            index += 1
    '''

    #subscriber = Subscribers.add_subscriber(
    #    session = DBSession,
    #    email = 'test_users@mahtests.net',
    #    name = 'Frank Testuserian',
    #    organization = 'WXXI',
    #    profession = 'Elmo Stunt Double',
    #    receive_updates = True,
    #    receive_version_announcement = False,
    #    interested_in_partnering = False,
    #    want_to_know_more = True,
    #)
