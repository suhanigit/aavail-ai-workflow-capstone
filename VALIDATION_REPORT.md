# Validation report

The project was validated before packaging.

- Model training: PASS
- EDA figure generation: PASS
- Single-script unit test run: PASS
- Unit test result: **7 passed**
- API tests cover `/health`, country-specific `/predict`, all-market `/predict`, and `/monitor`.
- Model/log/monitor writes in tests use temporary directories and do not overwrite production artifacts.
- Dockerfile and docker-compose configuration are included. Docker itself was not available in the packaging environment, so the image definition was not executed here.

Run the full test suite with:

```bash
python run_tests.py
```
