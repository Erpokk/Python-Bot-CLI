from setuptools import setup, find_namespace_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="simple-cli-bot",
    version="0.0.4",
    description="A personal console bot assistant that helps you manage your contacts and notes.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/Erpokk/project-PyMaster.git",
    author="Group-8",
    author_email="dontwriteme@gmail.com",
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['bot = src.main:main']},
    install_requires=["prompt_toolkit"],
    keywords='cli bot console assistant contacts notes',
    python_requires='>=3.7',
    project_urls={
        'Source': 'https://github.com/Erpokk/project-PyMaster',
        'Bug Reports': 'https://github.com/Erpokk/project-PyMaster/issues',
    },
)