from setuptools import setup


setup(
    name='heed',
    version='0.0.3-dev',
    author='Johannes',
    author_email='johtso@gmail.com',
    description="A dead man's switch monitoring tool.",
    packages=['heed'],
    install_requires=[
        'arrow==0.4.2',
        'Flask==0.10.1',
        'pymongo==2.6.3',
        'schema==0.2.0',
    ],
)
