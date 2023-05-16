from setuptools import setup

NAME = 'swaprum-register-bot'
DESCRIBE = f'git describe --dirty --tags --long --match {NAME}/*[0-9]*'
TAG_REGEX = (
    '^(' + NAME +
    r'\/)?(?P<version>(v?\d+\.\d+\.\d+($|-(alpha|rc)\d+$))|(0\.0))'
)


setup(
    name=NAME,
    author='archemich',
    author_email='archemich@gmail.com',
    description=__doc__,
    setup_requires=['setuptools_scm'],
    use_scm_version={'root': '../..',
                     'relative_to': __file__,
                     'git_describe_command': DESCRIBE,
                     'tag_regex': TAG_REGEX},
    install_requires=[
        'selenium~=4.9',
        'pywinauto~=0.6'
    ],
    python_requires='==3.10.*',
    entry_points={
        'console_scripts': [
            f'{NAME} = swaprum_register_bot.main:main'
        ]
    },
    include_package_data=True
)