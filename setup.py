from setuptools import setup

tests_require = [
    'pytest',
]

setup(
    name='cornerstore',
    version='0.0.1',
    packages=['myapp'],
    install_requires=['pytest', 'pytest-cov', 'Flask', 'flask-wtf', 'flask-sqlalchemy', 'flask-login', 'WTForms==2.3.3',
                      'SQLAlchemy', 'email_validator', 'flask', 'flask-login', 'stripe', 'dnspython==2.0.0', 'click==7.1.2', 'itsdangerous==1.1.0', 'MarkupSafe==1.1.1', 'Werkzeug==1.0.1'],
    extras_require={
        'test': tests_require
    },
)


