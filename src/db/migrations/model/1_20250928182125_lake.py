from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `lake` (
    `id` CHAR(36) NOT NULL PRIMARY KEY,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `deleted_at` DATETIME(6),
    `app` VARCHAR(255) NOT NULL,
    `dataset` VARCHAR(255) NOT NULL,
    `ref_id` CHAR(36) NOT NULL UNIQUE,
    `meta` JSON,
    UNIQUE KEY `uid_lake_app_7a0112` (`app`, `dataset`, `ref_id`),
    KEY `idx_lake_app_6a9c76` (`app`),
    KEY `idx_lake_dataset_ef9e7a` (`dataset`),
    KEY `idx_lake_ref_id_de6975` (`ref_id`)
) CHARACTER SET utf8mb4 COMMENT='Lake';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `lake`;"""
