"""01_initial-db and add initial events

Revision ID: a3a3092713e6
Revises: 
Create Date: 2024-12-11 23:54:03.256982

"""
from typing import Sequence, Union
from datetime import datetime, timezone

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a3a3092713e6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table("event",
    sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
    sa.Column("team1", sa.String(), nullable=False),
    sa.Column("team2", sa.String(), nullable=False),
    sa.Column("odds", sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column("deadline", sa.DateTime(), nullable=False),
    sa.Column("status", sa.Enum("NEW", "WON", "LOST", name="eventstatus"), nullable=False),
    sa.Column("created_at", sa.DateTime(), nullable=True),
    sa.Column("updated_at", sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint("id")
    )
    # ### end Alembic commands ###
    # event_table = sa.table(
    #     "event",
    #     sa.column("id", sa.Integer),
    #     sa.column("team1", sa.String),
    #     sa.column("team2", sa.String),
    #     sa.column("odds", sa.DECIMAL),
    #     sa.column("deadline", sa.DateTime),
    #     sa.column("status", sa.Enum),
    #     sa.column("created_at", sa.DateTime),
    #     sa.column("updated_at", sa.DateTime),
    # )
    #
    # op.bulk_insert(event_table, [
    #     {
    #         "id": 1,
    #         "team1": "Team A",
    #         "team2": "Team B",
    #         "odds": 1.50,
    #         "deadline": datetime(2024, 12, 12, 18, 0, tzinfo=timezone.utc).replace(tzinfo=None),
    #         "status": "NEW",
    #         "created_at": datetime.now(timezone.utc).replace(tzinfo=None),
    #         "updated_at": datetime.now(timezone.utc).replace(tzinfo=None),
    #     },
    #     {
    #         "id": 2,
    #         "team1": "Team C",
    #         "team2": "Team D",
    #         "odds": 2.00,
    #         "deadline": datetime(2024, 12, 15, 20, 0, tzinfo=timezone.utc).replace(tzinfo=None),
    #         "status": "NEW",
    #         "created_at": datetime.now(timezone.utc).replace(tzinfo=None),
    #         "updated_at": datetime.now(timezone.utc).replace(tzinfo=None),
    #     },
    #     {
    #         "id": 3,
    #         "team1": "Team E",
    #         "team2": "Team F",
    #         "odds": 2.50,
    #         "deadline": datetime(2024, 12, 20, 12, 0, tzinfo=timezone.utc).replace(tzinfo=None),
    #         "status": "NEW",
    #         "created_at": datetime.now(timezone.utc).replace(tzinfo=None),
    #         "updated_at": datetime.now(timezone.utc).replace(tzinfo=None),
    #     },
    #     {
    #         "id": 4,
    #         "team1": "Team G",
    #         "team2": "Team K",
    #         "odds": 3.00,
    #         "deadline": datetime(2024, 12, 6, 16, 0, tzinfo=timezone.utc).replace(tzinfo=None),
    #         "status": "NEW",
    #         "created_at": datetime.now(timezone.utc).replace(tzinfo=None),
    #         "updated_at": datetime.now(timezone.utc).replace(tzinfo=None),
    #     },
    # ])


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("event")
    # ### end Alembic commands ###
