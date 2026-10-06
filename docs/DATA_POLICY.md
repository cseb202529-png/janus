# Data Policy
- Every source: URL/origin, license, date accessed, Director approval recorded in `datasets/`.
- Pipeline order: collect → clean → normalize → language filter → quality score → dedup (exact + near) → contamination check against eval sets → safety filter → tokenize → shard → pack → statistics.
- Dataset versions `dataset_v001, v002, ...` are immutable. Store: sources, licenses, size, token count, filter config, creation date, content hash.
- No restricted-license or personal data. No eval data in training (contamination check is mandatory).
- Teacher-generated data records teacher identity, prompts, filters, and license/terms of the teacher.
