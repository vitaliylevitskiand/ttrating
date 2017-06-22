from services import parser
from services import translator
import models
from models import db


def every_day():
    updated_date = parser.parse_ua()
    parser.parse_world_rating()

    translator.add_translations(updated_date['players'], 'ua')
    translator.add_translations(updated_date['cities'], 'ua')
    translator.add_translations(updated_date['tournaments'], 'ua')

    update_player_info()


def update_ratings():
    models.db.engine.execute("")


def update_player_info():
    print('progress: ')
    n = 10000
    player_infos = models.PlayerInfo.query.all()

    for p in player_infos:
        p.game_total = 0
        p.game_won = 0
        p.tournaments_total = 0
        models.db.session.add(p)
    models.db.session.commit()

    page = 0
    pages = 1
    while page < pages:
        page += 1
        _games = models.Game.query.paginate(page=page, per_page=n)
        if page == 1:
            print('Count: %s' % _games.total)
            print('Pages %s' % _games.pages)
            pages = _games.pages
        games = _games.items
        player_games = {}
        for g in games:
            if not player_games.get(g.player_id):
                player_games[g.player_id] = list()
            player_games[g.player_id].append(g)
        for i, p in enumerate(player_infos):
            if not player_games.get(p.id):
                continue
            won = [g for g in player_games[p.id] if g.result]
            tourns = set([g.tournament_id for g in player_games[p.id]])
            p.game_total += len(player_games[p.id])
            p.game_won += len(won)
            p.tournaments_total += len(tourns)
            db.session.add(p)
        db.session.commit()
        print('+')
