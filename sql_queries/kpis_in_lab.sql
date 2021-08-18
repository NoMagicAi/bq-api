CREATE OR REPLACE VIEW `staging-nomagic-ai.api.kpis_in_lab` AS
WITH records AS (
SELECT
evaluation_id,
MIN(voyage) AS voyage,
run_id,
COUNT(*) AS attempts,
COUNTIF(is_success) AS successes,
COUNTIF(is_excluded) AS excluded,
COUNTIF(hard_failure) AS hard_failures,
COUNTIF(soft_failure) AS soft_failures,
COUNTIF(is_two_items) AS two_items,
ROUND(AVG(cycle_length_in_seconds), 2) AS avg_cycle_in_sec,
ROUND(SAFE_DIVIDE(COUNTIF(is_success), COUNT(*)), 2) AS ISR
FROM  `staging-nomagic-ai.kpi_v2.counters_base`
GROUP BY ROLLUP(evaluation_id, run_id)
)
SELECT
voyage,
IFNULL(run_id, "TOTAL") AS run_id,
* EXCEPT(voyage, run_id)
FROM records
ORDER BY evaluation_id, run_id ASC;