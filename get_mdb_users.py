# pylint: disable=invalid-name
# pylint: disable=missing-docstring

import rethinkdb as r

import tweepy 
from tweepy_conf import init

from tag_user import get_user_tags
from extract_fields import extract_fields
from db_conf import get_conf

rdb_config = get_conf()

r.connect(**rdb_config).repl()

api = init()

mdb_list_ids = {
    'spd': 912246144289386496, # @spdbt: https://twitter.com/spdbt/lists/spd-mdbs-der-wp-19
    'cdu_csu': 12971627, # @cducsubt: https://twitter.com/cducsubt/lists/mdbs-19-wp1/members
    'csu': 101365010, # @cducsubt: https://twitter.com/cducsubt/lists/csu-mdbs
    'gruene': 912229293786267648, # @GrueneBundestag: https://twitter.com/GrueneBundestag/lists/mdb19
    'fdp': 913015139045183488, # @fdpbt: https://twitter.com/fdpbt/lists/fdp-bundestagsabgeordnete
    'linke': 912252646953758720, # @Linksfraktion: https://twitter.com/Linksfraktion/lists/mdb-die-linke-19-wp
    'afd': 912313478706286593, # @AfDimBundestag: https://twitter.com/AfDimBundestag/lists/afd-abgeordnete1
}

mdb_lists = []

for party in mdb_list_ids:
    mdb_lists.append(tweepy.Cursor(api.list_members, list_id=mdb_list_ids[party], count=100).items())

for userlist in mdb_lists:
    for user in userlist:
        userdata = extract_fields(user)
        print("Kategorisiere " + userdata['screen_name']+ "...")

        if not userdata['protected']:
            userdata['list_tags'] = get_user_tags(api, userdata['id_str'])
        print(userdata['list_tags'])

        try:
            with r.connect(**rdb_config) as conn:
                r.table('users').insert(userdata).run(conn)
        except Exception as e:
            print("Error inserting userdata into DB ", e)
