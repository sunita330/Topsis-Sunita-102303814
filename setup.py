from setuptools import setup, find_packages

setup(
    name="Topsis-Sunita-102303814",
    version="1.0.0",
    author="Sunita",
    author_email="sunita@example.com",
    description="TOPSIS implementation for multi-criteria decision making",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["pandas", "numpy", "openpyxl"],
    entry_points={
        "console_scripts": [
            "topsis=topsis_sunita_102303814.topsis:main"
        ]
    },
)
