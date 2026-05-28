# GitHub Cleanup Notes

The refactored project avoids:

- local absolute runtime paths in config
- secrets committed to source control
- machine-specific service files
- China-market hardcoded ticker parsing
- local cache files
- generated reports outside sample artifacts

Before publishing:

1. Keep `.env` local and commit only `.env.example`.
2. Review `config/watchlist.yaml` for the intended public defaults.
3. Run tests.
4. Generate a fresh sample report only if it does not contain private notes or API keys.
5. Confirm `data/`, `logs/`, and `reports/output/` are ignored.

