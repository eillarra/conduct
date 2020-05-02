Conduct
=======

[![github-tests-badge]][github-tests]
[![github-mypy-badge]][github-mypy]
[![codecov-badge]][codecov]
[![pypi-badge]][pypi]
[![pypi-versions]][pypi]
[![license-badge]](LICENSE)


Supported backends/wallets
--------------------------


Dependencies
------------

Only `httpx` is a hard dependency; the following are optional:

  - lnd-grpc - Required if you want to use the LndWallet.
  - pylightning - Required if you want to use the CLightningWallet.

You can install all of these with `pip install conduct[full]`.


[github-tests]: https://github.com/lnbits/conduct/actions?query=workflow%3A%22tests%22
[github-tests-badge]: https://github.com/lnbits/conduct/workflows/tests/badge.svg
[github-mypy]: https://github.com/lnbits/conduct/actions?query=workflow%3A%22mypy%22
[github-mypy-badge]: https://github.com/lnbits/conduct/workflows/mypy/badge.svg
[codecov]: https://codecov.io/gh/lnbits/conduct
[codecov-badge]: https://codecov.io/gh/lnbits/conduct/branch/master/graph/badge.svg
[pypi]: https://pypi.org/project/conduct/
[pypi-badge]: https://badge.fury.io/py/conduct.svg
[pypi-versions]: https://img.shields.io/pypi/pyversions/conduct.svg
[license-badge]: https://img.shields.io/badge/license-MIT-blue.svg
