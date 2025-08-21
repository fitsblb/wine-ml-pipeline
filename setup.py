from setuptools import setup, find_packages

setup(
    name="datascience",          # import name you'll use in code
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},     # <-- critical for src/ layout
    include_package_data=True,
    install_requires=[],         # keep empty; you already use requirements.txt
    python_requires=">=3.9",
)
