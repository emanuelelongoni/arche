# Jobs

A job is one small unit of agent work that ends in one reviewable PR. Files: `jobs/open/J####.yaml` (schema: `schema/job.schema.json`); move to `jobs/done/` when the PR merges.

Lifecycle: `open` → `claimed` (first commit on branch `job/<id>`) → `in-review` (PR open, `pr:` set) → `done`.

A good job:
- fits in one session, with a PR a human can review in 20–30 minutes;
- has acceptance criteria a script can check (validator exit code, coverage numbers, lake build);
- says what not to touch.

Scheduled agent runs pick the lowest-numbered open job whose `depends_on` jobs are done (see `CLAUDE.md`).
