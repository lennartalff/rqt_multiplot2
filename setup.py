from setuptools import setup

PACKAGE_NAME = 'rqt_multiplot2'

setup(
    name=PACKAGE_NAME,
    version='0.0.0',
    packages=[PACKAGE_NAME],
    data_files=[
        ('share/' + PACKAGE_NAME + '/resource', ['resource/axis_scaling.ui']),
        ('share/ament_index/resource_index/packages',
         ['resource/' + PACKAGE_NAME]),
        ('share/' + PACKAGE_NAME, ['package.xml']),
        ('share/' + PACKAGE_NAME, ['plugin.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Thies Lennart Alff',
    maintainer_email='lennart.alff@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts':
        [PACKAGE_NAME + ' = ' + PACKAGE_NAME + '.__main__:main'],
    },
)
