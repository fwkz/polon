from setuptools import setup, find_packages

setup(
    name='polon',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/fwkz/polon',
    license='MIT',
    author='fwkz',
    author_email='f4wkes@gmail.com',
    description='Polon - test reactor.',
    scripts=["polon/core/management/polon-admin.py"],
    entry_points={
        'console_scripts': ['polon-admin = polon.core.management:execute_admin_command']
    },
    zip_safe=False,
)