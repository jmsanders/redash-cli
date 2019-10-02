from setuptools import setup

setup(
    name="redash-cli",
    version="0.1",
    py_modules=["redash"],
    install_requires=["click", "requests"],
    entry_points="""
        [console_scripts]
        redash-cli=redash.cli:cli
    """,
)
