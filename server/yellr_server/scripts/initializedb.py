import os
import sys
import transaction
import hashlib
import uuid

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    UserGeoFences,
    Users,
    Base,
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
    #    model = MyModel(name='one', value=1)
    #    DBSession.add(model)
 
    system_user_geo_fence = UserGeoFences.add(
        top_left_lat = 90,
        top_left_lng = 180,
        bottom_right_lat = -90,
        bottom_right_lng = -180,
        center_lat = 0,
        center_lng = 0,
    )

    system_user = Users.create_new_user(
        user_type = 'SYSTEM',
        user_geo_fence_id = system_user_geo_fence.id,
        username = 'system',
        password = hashlib.sha256('password'.encode('utf-8')).hexdigest(),
        first = 'SYSTEM',
        last = 'USER',
        email = '',
        organization_id = None,
    )
