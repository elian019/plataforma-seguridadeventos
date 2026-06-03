"""initial schema

Revision ID: 20260603_0001
Revises:
Create Date: 2026-06-03
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260603_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ubicacion",
        sa.Column("id_ubicacion", sa.Integer(), nullable=False),
        sa.Column("direccion", sa.String(length=255), nullable=True),
        sa.Column("zona", sa.String(length=100), nullable=True),
        sa.Column("latitud", sa.Float(), nullable=True),
        sa.Column("longitud", sa.Float(), nullable=True),
        sa.Column("referencia", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id_ubicacion"),
    )
    op.create_index(op.f("ix_ubicacion_id_ubicacion"), "ubicacion", ["id_ubicacion"], unique=False)

    op.create_table(
        "empresa_seguridad",
        sa.Column("id_empresa", sa.Integer(), nullable=False),
        sa.Column("nombre_empresa", sa.String(length=255), nullable=False),
        sa.Column("direccion", sa.String(length=255), nullable=True),
        sa.Column("telefono", sa.String(length=50), nullable=True),
        sa.Column("email", sa.String(length=150), nullable=True),
        sa.PrimaryKeyConstraint("id_empresa"),
    )
    op.create_index(
        op.f("ix_empresa_seguridad_id_empresa"),
        "empresa_seguridad",
        ["id_empresa"],
        unique=False,
    )

    op.create_table(
        "nivel_riesgo",
        sa.Column("id_nivel_riesgo", sa.Integer(), nullable=False),
        sa.Column("nivel", sa.String(length=100), nullable=False),
        sa.Column("puntaje", sa.Integer(), nullable=True),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id_nivel_riesgo"),
    )
    op.create_index(
        op.f("ix_nivel_riesgo_id_nivel_riesgo"),
        "nivel_riesgo",
        ["id_nivel_riesgo"],
        unique=False,
    )

    op.create_table(
        "tipo_evento",
        sa.Column("id_tipo_evento", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=150), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id_tipo_evento"),
    )
    op.create_index(
        op.f("ix_tipo_evento_id_tipo_evento"),
        "tipo_evento",
        ["id_tipo_evento"],
        unique=False,
    )

    op.create_table(
        "fuente_evento",
        sa.Column("id_fuente_evento", sa.Integer(), nullable=False),
        sa.Column("nombre_fuente", sa.String(length=255), nullable=False),
        sa.Column("tipo_fuente", sa.String(length=100), nullable=True),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id_fuente_evento"),
    )
    op.create_index(
        op.f("ix_fuente_evento_id_fuente_evento"),
        "fuente_evento",
        ["id_fuente_evento"],
        unique=False,
    )

    op.create_table(
        "rol",
        sa.Column("id_rol", sa.Integer(), nullable=False),
        sa.Column("nombre_rol", sa.String(length=150), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id_rol"),
    )
    op.create_index(op.f("ix_rol_id_rol"), "rol", ["id_rol"], unique=False)

    op.create_table(
        "permiso",
        sa.Column("id_permiso", sa.Integer(), nullable=False),
        sa.Column("nombre_permiso", sa.String(length=150), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id_permiso"),
    )
    op.create_index(op.f("ix_permiso_id_permiso"), "permiso", ["id_permiso"], unique=False)

    op.create_table(
        "centro_monitoreo",
        sa.Column("id_centro", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=255), nullable=False),
        sa.Column("direccion", sa.String(length=255), nullable=True),
        sa.Column("telefono", sa.String(length=50), nullable=True),
        sa.Column("id_empresa", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["id_empresa"], ["empresa_seguridad.id_empresa"]),
        sa.PrimaryKeyConstraint("id_centro"),
    )
    op.create_index(
        op.f("ix_centro_monitoreo_id_centro"),
        "centro_monitoreo",
        ["id_centro"],
        unique=False,
    )

    op.create_table(
        "dispositivo",
        sa.Column("id_dispositivo", sa.Integer(), nullable=False),
        sa.Column("nombre_dispositivo", sa.String(length=255), nullable=False),
        sa.Column("tipo_dispositivo", sa.String(length=100), nullable=True),
        sa.Column("estado", sa.String(length=50), nullable=True),
        sa.Column("id_ubicacion", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["id_ubicacion"], ["ubicacion.id_ubicacion"]),
        sa.PrimaryKeyConstraint("id_dispositivo"),
    )
    op.create_index(
        op.f("ix_dispositivo_id_dispositivo"),
        "dispositivo",
        ["id_dispositivo"],
        unique=False,
    )

    op.create_table(
        "usuario",
        sa.Column("id_usuario", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=150), nullable=False),
        sa.Column("apellido", sa.String(length=150), nullable=True),
        sa.Column("correo", sa.String(length=255), nullable=False),
        sa.Column("contrasena", sa.String(length=255), nullable=False),
        sa.Column("estado", sa.String(length=50), nullable=True),
        sa.Column("fecha_creacion", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id_usuario"),
        sa.UniqueConstraint("correo"),
    )
    op.create_index(op.f("ix_usuario_id_usuario"), "usuario", ["id_usuario"], unique=False)

    op.create_table(
        "evento",
        sa.Column("id_evento", sa.Integer(), nullable=False),
        sa.Column("fecha_hora", sa.DateTime(), nullable=True),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.Column("estado", sa.String(length=50), nullable=True),
        sa.Column("id_tipo_evento", sa.Integer(), nullable=True),
        sa.Column("id_dispositivo", sa.Integer(), nullable=True),
        sa.Column("id_nivel_riesgo", sa.Integer(), nullable=True),
        sa.Column("id_centro", sa.Integer(), nullable=True),
        sa.Column("id_fuente_evento", sa.Integer(), nullable=True),
        sa.Column("id_ubicacion", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["id_centro"], ["centro_monitoreo.id_centro"]),
        sa.ForeignKeyConstraint(["id_dispositivo"], ["dispositivo.id_dispositivo"]),
        sa.ForeignKeyConstraint(["id_fuente_evento"], ["fuente_evento.id_fuente_evento"]),
        sa.ForeignKeyConstraint(["id_nivel_riesgo"], ["nivel_riesgo.id_nivel_riesgo"]),
        sa.ForeignKeyConstraint(["id_tipo_evento"], ["tipo_evento.id_tipo_evento"]),
        sa.ForeignKeyConstraint(["id_ubicacion"], ["ubicacion.id_ubicacion"]),
        sa.PrimaryKeyConstraint("id_evento"),
    )
    op.create_index(op.f("ix_evento_id_evento"), "evento", ["id_evento"], unique=False)

    op.create_table(
        "auditoria",
        sa.Column("id_auditoria", sa.Integer(), nullable=False),
        sa.Column("fecha_hora", sa.DateTime(), nullable=True),
        sa.Column("accion", sa.String(length=100), nullable=True),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.Column("ip_usuario", sa.String(length=50), nullable=True),
        sa.Column("id_usuario", sa.Integer(), nullable=True),
        sa.Column("id_evento", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["id_evento"], ["evento.id_evento"]),
        sa.ForeignKeyConstraint(["id_usuario"], ["usuario.id_usuario"]),
        sa.PrimaryKeyConstraint("id_auditoria"),
    )
    op.create_index(
        op.f("ix_auditoria_id_auditoria"),
        "auditoria",
        ["id_auditoria"],
        unique=False,
    )

    op.create_table(
        "rol_permiso",
        sa.Column("id_rol_permiso", sa.Integer(), nullable=False),
        sa.Column("id_rol", sa.Integer(), nullable=True),
        sa.Column("id_permiso", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["id_permiso"], ["permiso.id_permiso"]),
        sa.ForeignKeyConstraint(["id_rol"], ["rol.id_rol"]),
        sa.PrimaryKeyConstraint("id_rol_permiso"),
    )
    op.create_index(
        op.f("ix_rol_permiso_id_rol_permiso"),
        "rol_permiso",
        ["id_rol_permiso"],
        unique=False,
    )

    op.create_table(
        "usuario_rol",
        sa.Column("id_usuario_rol", sa.Integer(), nullable=False),
        sa.Column("id_usuario", sa.Integer(), nullable=True),
        sa.Column("id_rol", sa.Integer(), nullable=True),
        sa.Column("id_evento", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["id_evento"], ["evento.id_evento"]),
        sa.ForeignKeyConstraint(["id_rol"], ["rol.id_rol"]),
        sa.ForeignKeyConstraint(["id_usuario"], ["usuario.id_usuario"]),
        sa.PrimaryKeyConstraint("id_usuario_rol"),
    )
    op.create_index(
        op.f("ix_usuario_rol_id_usuario_rol"),
        "usuario_rol",
        ["id_usuario_rol"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_usuario_rol_id_usuario_rol"), table_name="usuario_rol")
    op.drop_table("usuario_rol")
    op.drop_index(op.f("ix_rol_permiso_id_rol_permiso"), table_name="rol_permiso")
    op.drop_table("rol_permiso")
    op.drop_index(op.f("ix_auditoria_id_auditoria"), table_name="auditoria")
    op.drop_table("auditoria")
    op.drop_index(op.f("ix_evento_id_evento"), table_name="evento")
    op.drop_table("evento")
    op.drop_index(op.f("ix_usuario_id_usuario"), table_name="usuario")
    op.drop_table("usuario")
    op.drop_index(op.f("ix_dispositivo_id_dispositivo"), table_name="dispositivo")
    op.drop_table("dispositivo")
    op.drop_index(op.f("ix_centro_monitoreo_id_centro"), table_name="centro_monitoreo")
    op.drop_table("centro_monitoreo")
    op.drop_index(op.f("ix_permiso_id_permiso"), table_name="permiso")
    op.drop_table("permiso")
    op.drop_index(op.f("ix_rol_id_rol"), table_name="rol")
    op.drop_table("rol")
    op.drop_index(op.f("ix_fuente_evento_id_fuente_evento"), table_name="fuente_evento")
    op.drop_table("fuente_evento")
    op.drop_index(op.f("ix_tipo_evento_id_tipo_evento"), table_name="tipo_evento")
    op.drop_table("tipo_evento")
    op.drop_index(op.f("ix_nivel_riesgo_id_nivel_riesgo"), table_name="nivel_riesgo")
    op.drop_table("nivel_riesgo")
    op.drop_index(op.f("ix_empresa_seguridad_id_empresa"), table_name="empresa_seguridad")
    op.drop_table("empresa_seguridad")
    op.drop_index(op.f("ix_ubicacion_id_ubicacion"), table_name="ubicacion")
    op.drop_table("ubicacion")
