"""add postgis support to ubicacion

Revision ID: 20260609_0002
Revises: 20260603_0001
Create Date: 2026-06-09
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geography, Geometry


revision: str = "20260609_0002"
down_revision: Union[str, None] = "20260603_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    op.add_column(
        "ubicacion",
        sa.Column(
            "geom",
            Geometry(geometry_type="POINT", srid=4326, spatial_index=False),
            sa.Computed(
                "CASE WHEN latitud IS NULL OR longitud IS NULL "
                "THEN NULL ELSE ST_SetSRID(ST_MakePoint(longitud, latitud), 4326) END",
                persisted=True,
            ),
            nullable=True,
        ),
    )
    op.add_column(
        "ubicacion",
        sa.Column(
            "geog",
            Geography(geometry_type="POINT", srid=4326, spatial_index=False),
            sa.Computed(
                "CASE WHEN latitud IS NULL OR longitud IS NULL "
                "THEN NULL ELSE ST_SetSRID(ST_MakePoint(longitud, latitud), 4326)::geography END",
                persisted=True,
            ),
            nullable=True,
        ),
    )
    op.create_index(
        "ix_ubicacion_geom_gist",
        "ubicacion",
        ["geom"],
        unique=False,
        postgresql_using="gist",
    )
    op.create_index(
        "ix_ubicacion_geog_gist",
        "ubicacion",
        ["geog"],
        unique=False,
        postgresql_using="gist",
    )


def downgrade() -> None:
    op.drop_index("ix_ubicacion_geog_gist", table_name="ubicacion")
    op.drop_index("ix_ubicacion_geom_gist", table_name="ubicacion")
    op.drop_column("ubicacion", "geog")
    op.drop_column("ubicacion", "geom")
    op.execute("DROP EXTENSION IF EXISTS postgis")
