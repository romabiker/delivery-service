CREATE TABLE IF NOT EXISTS deliveries
(
    `type_id` UInt32,
    `transport_company_id` UInt32,
    `created_at` DateTime64(6),
    `weight_kg` Float32,
    `cost_of_content_usd` Float32,
    `cost_of_delivery_rub` Float32,
    `metadata_version` Int32 DEFAULT 1,
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(created_at)
ORDER BY (created_at, type_id)
SETTINGS index_granularity = 8192
