"""initial

Revision ID: a305d5896f20
Revises:
Create Date: 2025-05-18 07:08:47.522326

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import geoalchemy2

# revision identifiers, used by Alembic.
revision: str = 'a305d5896f20'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activity',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('activity_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['activity_id'], ['activity.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('title', 'activity_id', name='activity_child_title_un')
    )
    op.create_index(op.f('ix_activity_id'), 'activity', ['id'], unique=False)
    op.create_table('building',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('coordinates', geoalchemy2.types.Geography(geometry_type='POINT', from_text='ST_GeogFromText', name='geography', nullable=False), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('coordinates')
    )
    op.create_table('organization',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('phone_numbers', sa.ARRAY(sa.String()), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('building_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['building_id'], ['building.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('org_activity',
        sa.Column('activity_id', sa.Integer(), nullable=True),
        sa.Column('organization_id', sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(['activity_id'], ['activity.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('activity_id', 'organization_id', name='org_activity_un')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('org_activity')
    op.drop_table('organization')
    op.drop_index('idx_building_coordinates', table_name='building', postgresql_using='gist')
    op.drop_table('building')
    op.drop_index(op.f('ix_activity_id'), table_name='activity')
    op.drop_table('activity')
    # ### end Alembic commands ###