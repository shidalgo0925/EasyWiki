"""add coach_treatment_profiles

Revision ID: c3a8f1d2e4b5
Revises: 81ae6eb1cc9a
Create Date: 2026-06-10 22:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c3a8f1d2e4b5"
down_revision: Union[str, None] = "81ae6eb1cc9a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "coach_treatment_profiles",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("current_situation", sa.Text(), nullable=True),
        sa.Column("main_problem", sa.Text(), nullable=True),
        sa.Column("primary_area", sa.String(length=100), nullable=True),
        sa.Column("goal_30_days", sa.Text(), nullable=True),
        sa.Column("goal_90_days", sa.Text(), nullable=True),
        sa.Column("success_definition", sa.Text(), nullable=True),
        sa.Column("obstacles", sa.Text(), nullable=True),
        sa.Column("current_routine", sa.Text(), nullable=True),
        sa.Column("commitment_level", sa.String(length=20), nullable=True),
        sa.Column("coaching_preferences", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("wizard_step", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("coach_treatment_profiles", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_coach_treatment_profiles_user_id"), ["user_id"], unique=False)


def downgrade() -> None:
    with op.batch_alter_table("coach_treatment_profiles", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_coach_treatment_profiles_user_id"))
    op.drop_table("coach_treatment_profiles")
