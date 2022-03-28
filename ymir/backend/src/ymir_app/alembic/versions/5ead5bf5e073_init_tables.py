"""update

Revision ID: 9241f19996ab
Revises:
Create Date: 2022-03-28 17:01:03.287128

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "9241f19996ab"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "dataset",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("hash", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=100), nullable=True),
        sa.Column("version_num", sa.Integer(), nullable=False),
        sa.Column("result_state", sa.SmallInteger(), nullable=False),
        sa.Column("dataset_group_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("keywords", sa.Text(length=20000), nullable=True),
        sa.Column("ignored_keywords", sa.Text(length=20000), nullable=True),
        sa.Column("negative_info", sa.String(length=100), nullable=True),
        sa.Column("asset_count", sa.Integer(), nullable=True),
        sa.Column("keyword_count", sa.Integer(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("create_datetime", sa.DateTime(), nullable=False),
        sa.Column("update_datetime", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_dataset_dataset_group_id"), "dataset", ["dataset_group_id"], unique=False)
    op.create_index(op.f("ix_dataset_hash"), "dataset", ["hash"], unique=True)
    op.create_index(op.f("ix_dataset_id"), "dataset", ["id"], unique=False)
    op.create_index(op.f("ix_dataset_name"), "dataset", ["name"], unique=False)
    op.create_index(op.f("ix_dataset_project_id"), "dataset", ["project_id"], unique=False)
    op.create_index(op.f("ix_dataset_result_state"), "dataset", ["result_state"], unique=False)
    op.create_index(op.f("ix_dataset_task_id"), "dataset", ["task_id"], unique=False)
    op.create_index(op.f("ix_dataset_user_id"), "dataset", ["user_id"], unique=False)
    op.create_index(op.f("ix_dataset_version_num"), "dataset", ["version_num"], unique=False)
    op.create_table(
        "dataset_group",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=100), nullable=True),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("create_datetime", sa.DateTime(), nullable=False),
        sa.Column("update_datetime", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_dataset_group_id"), "dataset_group", ["id"], unique=False)
    op.create_index(op.f("ix_dataset_group_name"), "dataset_group", ["name"], unique=False)
    op.create_index(op.f("ix_dataset_group_project_id"), "dataset_group", ["project_id"], unique=False)
    op.create_index(op.f("ix_dataset_group_user_id"), "dataset_group", ["user_id"], unique=False)
    op.create_table(
        "docker_image",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("url", sa.String(length=100), nullable=False),
        sa.Column("hash", sa.String(length=100), nullable=True),
        sa.Column("description", sa.String(length=100), nullable=True),
        sa.Column("state", sa.Integer(), nullable=False),
        sa.Column("is_shared", sa.Boolean(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("create_datetime", sa.DateTime(), nullable=False),
        sa.Column("update_datetime", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_docker_image_hash"), "docker_image", ["hash"], unique=False)
    op.create_index(op.f("ix_docker_image_id"), "docker_image", ["id"], unique=False)
    op.create_index(op.f("ix_docker_image_name"), "docker_image", ["name"], unique=False)
    op.create_index(op.f("ix_docker_image_state"), "docker_image", ["state"], unique=False)
    op.create_index(op.f("ix_docker_image_url"), "docker_image", ["url"], unique=False)
    op.create_table(
        "docker_image_config",
        sa.Column("image_id", sa.Integer(), nullable=False),
        sa.Column("type", sa.Integer(), nullable=False),
        sa.Column("config", sa.Text(length=20000), nullable=False),
        sa.PrimaryKeyConstraint("image_id", "type"),
        sa.UniqueConstraint("image_id", "type", name="unique_image_type"),
    )
    op.create_index(op.f("ix_docker_image_config_image_id"), "docker_image_config", ["image_id"], unique=False)
    op.create_index(op.f("ix_docker_image_config_type"), "docker_image_config", ["type"], unique=False)
    op.create_table(
        "docker_image_relationship",
        sa.Column("src_image_id", sa.Integer(), nullable=False),
        sa.Column("dest_image_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("src_image_id", "dest_image_id"),
        sa.UniqueConstraint("src_image_id", "dest_image_id", name="unique_image_relationship"),
    )
    op.create_index(
        op.f("ix_docker_image_relationship_dest_image_id"), "docker_image_relationship", ["dest_image_id"], unique=False
    )
    op.create_index(
        op.f("ix_docker_image_relationship_src_image_id"), "docker_image_relationship", ["src_image_id"], unique=False
    )
    op.create_table(
        "iteration",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("description", sa.String(length=100), nullable=True),
        sa.Column("iteration_round", sa.Integer(), nullable=False),
        sa.Column("current_stage", sa.SmallInteger(), nullable=False),
        sa.Column("mining_input_dataset_id", sa.Integer(), nullable=True),
        sa.Column("mining_output_dataset_id", sa.Integer(), nullable=True),
        sa.Column("label_output_dataset_id", sa.Integer(), nullable=True),
        sa.Column("training_input_dataset_id", sa.Integer(), nullable=True),
        sa.Column("training_output_model_id", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("create_datetime", sa.DateTime(), nullable=False),
        sa.Column("update_datetime", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_iteration_current_stage"), "iteration", ["current_stage"], unique=False)
    op.create_index(op.f("ix_iteration_id"), "iteration", ["id"], unique=False)
    op.create_index(op.f("ix_iteration_iteration_round"), "iteration", ["iteration_round"], unique=False)
    op.create_index(op.f("ix_iteration_project_id"), "iteration", ["project_id"], unique=False)
    op.create_index(op.f("ix_iteration_user_id"), "iteration", ["user_id"], unique=False)
    op.create_table(
        "model",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("hash", sa.String(length=100), nullable=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=100), nullable=True),
        sa.Column("version_num", sa.Integer(), nullable=False),
        sa.Column("result_state", sa.SmallInteger(), nullable=False),
        sa.Column("model_group_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("map", sa.Float(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("create_datetime", sa.DateTime(), nullable=False),
        sa.Column("update_datetime", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("project_id", "hash", name="uniq_project_hash"),
    )
    op.create_index(op.f("ix_model_hash"), "model", ["hash"], unique=False)
    op.create_index(op.f("ix_model_id"), "model", ["id"], unique=False)
    op.create_index(op.f("ix_model_model_group_id"), "model", ["model_group_id"], unique=False)
    op.create_index(op.f("ix_model_name"), "model", ["name"], unique=False)
    op.create_index(op.f("ix_model_project_id"), "model", ["project_id"], unique=False)
    op.create_index(op.f("ix_model_result_state"), "model", ["result_state"], unique=False)
    op.create_index(op.f("ix_model_task_id"), "model", ["task_id"], unique=False)
    op.create_index(op.f("ix_model_user_id"), "model", ["user_id"], unique=False)
    op.create_index(op.f("ix_model_version_num"), "model", ["version_num"], unique=False)
    op.create_table(
        "model_group",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=100), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("training_dataset_id", sa.Integer(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("create_datetime", sa.DateTime(), nullable=False),
        sa.Column("update_datetime", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_model_group_id"), "model_group", ["id"], unique=False)
    op.create_index(op.f("ix_model_group_name"), "model_group", ["name"], unique=False)
    op.create_index(op.f("ix_model_group_project_id"), "model_group", ["project_id"], unique=False)
    op.create_index(op.f("ix_model_group_training_dataset_id"), "model_group", ["training_dataset_id"], unique=False)
    op.create_index(op.f("ix_model_group_user_id"), "model_group", ["user_id"], unique=False)
    op.create_table(
        "project",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=100), nullable=True),
        sa.Column("iteration_target", sa.Integer(), nullable=True),
        sa.Column("map_target", sa.Float(), nullable=True),
        sa.Column("training_dataset_count_target", sa.Integer(), nullable=True),
        sa.Column("mining_strategy", sa.SmallInteger(), nullable=True),
        sa.Column("chunk_size", sa.Integer(), nullable=True),
        sa.Column("training_type", sa.SmallInteger(), nullable=False),
        sa.Column("training_keywords", sa.Text(length=20000), nullable=False),
        sa.Column("training_dataset_group_id", sa.Integer(), nullable=True),
        sa.Column("mining_dataset_id", sa.Integer(), nullable=True),
        sa.Column("testing_dataset_id", sa.Integer(), nullable=True),
        sa.Column("initial_model_id", sa.Integer(), nullable=True),
        sa.Column("current_iteration_id", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("create_datetime", sa.DateTime(), nullable=False),
        sa.Column("update_datetime", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_project_id"), "project", ["id"], unique=False)
    op.create_index(op.f("ix_project_initial_model_id"), "project", ["initial_model_id"], unique=False)
    op.create_index(op.f("ix_project_mining_dataset_id"), "project", ["mining_dataset_id"], unique=False)
    op.create_index(op.f("ix_project_mining_strategy"), "project", ["mining_strategy"], unique=False)
    op.create_index(op.f("ix_project_name"), "project", ["name"], unique=False)
    op.create_index(op.f("ix_project_testing_dataset_id"), "project", ["testing_dataset_id"], unique=False)
    op.create_index(
        op.f("ix_project_training_dataset_group_id"), "project", ["training_dataset_group_id"], unique=False
    )
    op.create_index(op.f("ix_project_training_type"), "project", ["training_type"], unique=False)
    op.create_index(op.f("ix_project_user_id"), "project", ["user_id"], unique=False)
    op.create_table(
        "role",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=True),
        sa.Column("description", sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_role_id"), "role", ["id"], unique=False)
    op.create_index(op.f("ix_role_name"), "role", ["name"], unique=False)
    op.create_table(
        "task",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("hash", sa.String(length=100), nullable=False),
        sa.Column("type", sa.Integer(), nullable=False),
        sa.Column("state", sa.Integer(), nullable=False),
        sa.Column("parameters", sa.Text(length=20000), nullable=True),
        sa.Column("config", sa.Text(length=20000), nullable=True),
        sa.Column("percent", sa.Float(), nullable=True),
        sa.Column("duration", sa.Integer(), nullable=True),
        sa.Column("error_code", sa.String(length=20), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("is_terminated", sa.Boolean(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("last_message_datetime", mysql.DATETIME(fsp=6), nullable=False),
        sa.Column("create_datetime", sa.DateTime(), nullable=False),
        sa.Column("update_datetime", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_task_hash"), "task", ["hash"], unique=False)
    op.create_index(op.f("ix_task_id"), "task", ["id"], unique=False)
    op.create_index(op.f("ix_task_name"), "task", ["name"], unique=False)
    op.create_index(op.f("ix_task_project_id"), "task", ["project_id"], unique=False)
    op.create_index(op.f("ix_task_state"), "task", ["state"], unique=False)
    op.create_index(op.f("ix_task_type"), "task", ["type"], unique=False)
    op.create_index(op.f("ix_task_user_id"), "task", ["user_id"], unique=False)
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("username", sa.String(length=100), nullable=True),
        sa.Column("phone", sa.String(length=20), nullable=True),
        sa.Column("avatar", sa.String(length=100), nullable=True),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.Column("state", sa.Integer(), nullable=True),
        sa.Column("role", sa.Integer(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=True),
        sa.Column("last_login_datetime", sa.DateTime(), nullable=True),
        sa.Column("create_datetime", sa.DateTime(), nullable=False),
        sa.Column("update_datetime", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=False)
    op.create_index(op.f("ix_user_phone"), "user", ["phone"], unique=True)
    op.create_index(op.f("ix_user_role"), "user", ["role"], unique=False)
    op.create_index(op.f("ix_user_state"), "user", ["state"], unique=False)
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_user_username"), table_name="user")
    op.drop_index(op.f("ix_user_state"), table_name="user")
    op.drop_index(op.f("ix_user_role"), table_name="user")
    op.drop_index(op.f("ix_user_phone"), table_name="user")
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
    op.drop_index(op.f("ix_task_user_id"), table_name="task")
    op.drop_index(op.f("ix_task_type"), table_name="task")
    op.drop_index(op.f("ix_task_state"), table_name="task")
    op.drop_index(op.f("ix_task_project_id"), table_name="task")
    op.drop_index(op.f("ix_task_name"), table_name="task")
    op.drop_index(op.f("ix_task_id"), table_name="task")
    op.drop_index(op.f("ix_task_hash"), table_name="task")
    op.drop_table("task")
    op.drop_index(op.f("ix_role_name"), table_name="role")
    op.drop_index(op.f("ix_role_id"), table_name="role")
    op.drop_table("role")
    op.drop_index(op.f("ix_project_user_id"), table_name="project")
    op.drop_index(op.f("ix_project_training_type"), table_name="project")
    op.drop_index(op.f("ix_project_training_dataset_group_id"), table_name="project")
    op.drop_index(op.f("ix_project_testing_dataset_id"), table_name="project")
    op.drop_index(op.f("ix_project_name"), table_name="project")
    op.drop_index(op.f("ix_project_mining_strategy"), table_name="project")
    op.drop_index(op.f("ix_project_mining_dataset_id"), table_name="project")
    op.drop_index(op.f("ix_project_initial_model_id"), table_name="project")
    op.drop_index(op.f("ix_project_id"), table_name="project")
    op.drop_table("project")
    op.drop_index(op.f("ix_model_group_user_id"), table_name="model_group")
    op.drop_index(op.f("ix_model_group_training_dataset_id"), table_name="model_group")
    op.drop_index(op.f("ix_model_group_project_id"), table_name="model_group")
    op.drop_index(op.f("ix_model_group_name"), table_name="model_group")
    op.drop_index(op.f("ix_model_group_id"), table_name="model_group")
    op.drop_table("model_group")
    op.drop_index(op.f("ix_model_version_num"), table_name="model")
    op.drop_index(op.f("ix_model_user_id"), table_name="model")
    op.drop_index(op.f("ix_model_task_id"), table_name="model")
    op.drop_index(op.f("ix_model_result_state"), table_name="model")
    op.drop_index(op.f("ix_model_project_id"), table_name="model")
    op.drop_index(op.f("ix_model_name"), table_name="model")
    op.drop_index(op.f("ix_model_model_group_id"), table_name="model")
    op.drop_index(op.f("ix_model_id"), table_name="model")
    op.drop_index(op.f("ix_model_hash"), table_name="model")
    op.drop_table("model")
    op.drop_index(op.f("ix_iteration_user_id"), table_name="iteration")
    op.drop_index(op.f("ix_iteration_project_id"), table_name="iteration")
    op.drop_index(op.f("ix_iteration_iteration_round"), table_name="iteration")
    op.drop_index(op.f("ix_iteration_id"), table_name="iteration")
    op.drop_index(op.f("ix_iteration_current_stage"), table_name="iteration")
    op.drop_table("iteration")
    op.drop_index(op.f("ix_docker_image_relationship_src_image_id"), table_name="docker_image_relationship")
    op.drop_index(op.f("ix_docker_image_relationship_dest_image_id"), table_name="docker_image_relationship")
    op.drop_table("docker_image_relationship")
    op.drop_index(op.f("ix_docker_image_config_type"), table_name="docker_image_config")
    op.drop_index(op.f("ix_docker_image_config_image_id"), table_name="docker_image_config")
    op.drop_table("docker_image_config")
    op.drop_index(op.f("ix_docker_image_url"), table_name="docker_image")
    op.drop_index(op.f("ix_docker_image_state"), table_name="docker_image")
    op.drop_index(op.f("ix_docker_image_name"), table_name="docker_image")
    op.drop_index(op.f("ix_docker_image_id"), table_name="docker_image")
    op.drop_index(op.f("ix_docker_image_hash"), table_name="docker_image")
    op.drop_table("docker_image")
    op.drop_index(op.f("ix_dataset_group_user_id"), table_name="dataset_group")
    op.drop_index(op.f("ix_dataset_group_project_id"), table_name="dataset_group")
    op.drop_index(op.f("ix_dataset_group_name"), table_name="dataset_group")
    op.drop_index(op.f("ix_dataset_group_id"), table_name="dataset_group")
    op.drop_table("dataset_group")
    op.drop_index(op.f("ix_dataset_version_num"), table_name="dataset")
    op.drop_index(op.f("ix_dataset_user_id"), table_name="dataset")
    op.drop_index(op.f("ix_dataset_task_id"), table_name="dataset")
    op.drop_index(op.f("ix_dataset_result_state"), table_name="dataset")
    op.drop_index(op.f("ix_dataset_project_id"), table_name="dataset")
    op.drop_index(op.f("ix_dataset_name"), table_name="dataset")
    op.drop_index(op.f("ix_dataset_id"), table_name="dataset")
    op.drop_index(op.f("ix_dataset_hash"), table_name="dataset")
    op.drop_index(op.f("ix_dataset_dataset_group_id"), table_name="dataset")
    op.drop_table("dataset")
    # ### end Alembic commands ###
