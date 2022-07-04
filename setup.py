from setuptools import setup

setup(
    name="pyxivcompanion",
    version="0.0.4",
    author='marimelon',
    packages=["pyxivcompanion"],
    package_data={'pyxivcompanion': ['public-key.pem']},
    install_requires=["aiohttp", "pycryptodome", "pydantic"]
)
