from setuptools import setup, find_packages
setup(
    name="general-reposti",
    version="0.2112",
    py_modules=['general-reposti'],
    packages=find_packages(),
    python_requires='>=3',
    install_requires=['discord.py', 'praw']
)