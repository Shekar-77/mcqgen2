from setuptools import find_packages, setup

setup(
    name="mcqgenerato",
    author="shekar",
    install_requires=["openai","langchain","streamlit","PyPdf","python-dotenv"],
    packages=find_packages()
)
