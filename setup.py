from setuptools import setup, find_packages

setup(name='Celmon',
    version='0.0.1',
    description='Python Distribution Utilities',
    author='Arham Ansari',
    packages=find_packages(),
    install_requires=[
        'celery>=4.4.7',
        'rich>=12.0.1',
    ],
    license='MIT',
    entry_points = {
        'console_scripts': ['celmon=celmon.cli:run_cli'],
    }
)