from setuptools import find_packages,setup

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='Shreya Singh',
    author_email='shreyasingh130617@gmail.com',
    install_requires=["huggingface_hub","langchain","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages()
)