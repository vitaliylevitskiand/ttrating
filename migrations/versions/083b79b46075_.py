"""empty message

Revision ID: 083b79b46075
Revises:
Create Date: 2018-03-30 11:04:57.351797

"""
from alembic import op
import sqlalchemy as sa
from models import db, Player

# revision identifiers, used by Alembic.
revision = '083b79b46075'
down_revision = None
branch_labels = None
depends_on = None


class PlayerInfo(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, db.ForeignKey('player.id'), primary_key=True)
    player = db.relationship('Player', backref="player.info")
    tournaments_total = db.Column(db.Integer)
    game_total = db.Column(db.Integer)
    game_won = db.Column(db.Integer)
    stability = db.Column(db.Integer)
    about = db.Column(db.Integer)
    photo_url = db.Column(db.String)


def _migrate_player_info():
    for player in Player.query.all():
        info = PlayerInfo.query.get(player.id)
        if not info:
            continue
        fields = ['tournaments_total', 'game_total', 'stability', 'about',
                  'photo_url', 'game_won']
        for f in fields:
            player.__setattr__(f, getattr(info, f))
        db.session.add(player)
    db.session.commit()


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('player', sa.Column('about', sa.Integer(), nullable=True))
    op.add_column('player',
                  sa.Column('game_total', sa.Integer(), nullable=True))
    op.add_column('player', sa.Column('game_won', sa.Integer(), nullable=True))
    op.add_column('player', sa.Column('photo_url', sa.String(), nullable=True))
    op.add_column('player',
                  sa.Column('stability', sa.Integer(), nullable=True))
    op.add_column('player',
                  sa.Column('tournaments_total', sa.Integer(), nullable=True))
    # # ### end Alembic commands ###

    _migrate_player_info()

    op.drop_table('player_info')


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('player', 'tournaments_total')
    op.drop_column('player', 'stability')
    op.drop_column('player', 'photo_url')
    op.drop_column('player', 'game_won')
    op.drop_column('player', 'game_total')
    op.drop_column('player', 'about')
    op.alter_column('city', 'name',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    op.drop_column('city', 'id')
    # ### end Alembic commands ###
