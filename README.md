<div align="center">
    <img src="docs/images/logo.png" height="200px">
    <h3>Medchem - Molecular filtering for drug discovery</h3>
</div>

---

[![test](https://github.com/datamol-io/medchem/actions/workflows/test.yml/badge.svg)](https://github.com/datamol-io/medchem/actions/workflows/test.yml)
[![release](https://github.com/datamol-io/medchem/actions/workflows/release.yml/badge.svg)](https://github.com/datamol-io/medchem/actions/workflows/release.yml)
[![code-check](https://github.com/datamol-io/medchem/actions/workflows/code-check.yml/badge.svg)](https://github.com/datamol-io/medchem/actions/workflows/code-check.yml)
[![doc](https://github.com/datamol-io/medchem/actions/workflows/doc.yml/badge.svg)](https://github.com/datamol-io/medchem/actions/workflows/doc.yml)

Medchem is a Python library that proposes multiple molecular medchem filters to a wide range of use cases relevant in a drug discovery context.

- ✅ xxxx
- 🐍 xxxx
- ⚗️ xxxx
- 🧠 xxxx
- ⮔ xxxx
- 🔌 xxxx

## Installation

```bash
micromamba install -c conda-forge medchem
```

## Documentation

Visit <https://medchem-docs.datamol.io/>.

## Development lifecycle

### Setup dev environment

```bash
micromamba create -n medchem -f env.yml
micromamba activate medchem

pip install --no-deps -e .
```

### Tests

You can run tests locally with:

```bash
pytest
```

## Changelogs

See the latest changelogs at [CHANGELOGS.md](./CHANGELOGS.md).

## License

Under the Apache-2.0 license. See [LICENSE.md](LICENSE.md).
