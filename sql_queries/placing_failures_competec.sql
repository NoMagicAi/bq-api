CREATE OR REPLACE VIEW `staging-nomagic-ai.api.placing_failures_competec` AS
WITH attempts AS (
SELECT
athena_url,
RANK() OVER (PARTITION BY videos_v2.uid ORDER BY videos_v2.metadata.gcs_path ASC) AS rank,
raw.time_interval_item.begin,
-- FORMAT('%s/%s', metrics.raw.metadata.run_id, raw.place_attempts[SAFE_OFFSET(0)].place_prediction.all_drop_actions[SAFE_OFFSET(0)].heightmap_planner.debug_image_file),
FORMAT('https://athena-statics.prod.nomagic.io/%s', REPLACE(videos_v2.metadata.gcs_path, 'gs://', '')) as video_1,
helper.img_before_first_pick(metrics.raw.metadata.run_id, metrics.raw.metadata.user, metrics.raw.pick_attempts).img AS before_pick,
CONCAT(
    metrics.raw.metadata.run_id, CONCAT('_control-server/',
    raw.place_attempts[SAFE_OFFSET(0)].place_prediction.all_drop_actions[SAFE_OFFSET(0)].heightmap_planner.debug_image_file.filename))
AS planner_debug,
CONCAT(metrics.raw.metadata.run_id, CONCAT('_control-server/', raw.place_validation.snapshot_of_last_container.rgb.file.filename)) as place_validation,
category_1,
category_2,
category_3,
FROM `prod-nomagic-ai.stats.competec_items_v2_with_categories` as metrics
LEFT JOIN `prod-nomagic-ai.magicloader.videos_v2` AS videos_v2
     ON metrics.raw.uid = videos_v2.uid
     AND videos_v2.metadata.camera_name='CMP-Sophie-02 5'
WHERE metrics.policy.is_isr_success = False
ORDER BY metrics.raw.time_interval_item.begin DESC
)
SELECT * FROM attempts
WHERE rank=1
AND category_2="PLACE_FATAL";