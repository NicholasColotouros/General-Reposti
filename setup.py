from setuptools import setup, find_packages
setup(
    name="reposti",
    version="2.1.12",
    py_modules=['reposti'],
    packages=find_packages(),
    python_requires='>=3',
    install_requires=['discord.py>=1.2.3<1.3', 'praw>=6.3.0<6.4', 'regex'],
    entry_points={
        'console_scripts': [
            'reposti = reposti.__main__:main',
        ],
    }
)