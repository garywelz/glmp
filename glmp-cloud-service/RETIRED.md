# glmp-service is retired

The Cloud Run service `glmp-service` is retired.

- It has no callers in this repo, on Jetson cron, or in the live GLMP
  viewer / decoder / ingest path. Charts and decoder output live in GCS
  and Firestore; the Knowledge Engine is `copernicus-web` Cloud Run.
- Do not redeploy it. Public access was closed on 2026-10-04 after an
  unauthenticated caller listed Secret Manager names via
  `GET /api/secrets/list`.
- Core will delete the service in the Phase 2 hosting cleanup
  (`copernicus-web` PR [#36](https://github.com/garywelz/copernicus-web/pull/36)).

The Python in this directory is unchanged and is not to be shipped.
`cloudbuild.yaml` and the deploy docs now use `--no-allow-unauthenticated`
so a mistaken Cloud Build cannot reopen public access.
