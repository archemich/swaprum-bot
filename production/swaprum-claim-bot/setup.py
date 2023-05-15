from setuptools import setup

NAME = 'swaprum-claim-bot'

setup(
    name=NAME,
    author='archemich',
    author_email='archemich@gmail.com',

    description=__doc__,
    # setup_requires=['setuptools_scm'],
    use_scm_version={'root': '../..',
                     'relative_to': __file__},
    install_requires=[
        'requests~=2.30'
    ],
    python_requires='==3.10.*',
    entry_points={
        'console_scripts': [
            f'{NAME} = swaprum_claim_bot.main:main'
        ]
    }
)