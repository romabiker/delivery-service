"""Transport Company

Revision ID: 0ca83a793b71
Revises: 04a8e2a258de
Create Date: 2025-01-11 07:18:50.759035

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0ca83a793b71'
down_revision: Union[str, None] = '04a8e2a258de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transportcompanys',
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_transportcompanys'))
    )
    op.add_column('deliverys', sa.Column('transport_company_id', sa.Integer(), nullable=True))
    op.create_foreign_key(op.f('fk_deliverys_transport_company_id_transportcompanys'), 'deliverys', 'transportcompanys', ['transport_company_id'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_deliverys_transport_company_id_transportcompanys'), 'deliverys', type_='foreignkey')
    op.drop_column('deliverys', 'transport_company_id')
    op.drop_table('transportcompanys')
    # ### end Alembic commands ###
