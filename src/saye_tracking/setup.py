from glob import glob
import os

from setuptools import find_packages, setup

package_name = 'saye_tracking'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='lauraluna',
    maintainer_email='leticiafreitas.ti@gmail.com',
    description='Rastreamento de multiplos objetos 3D para o rover Ackermann "saye".',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'deteccao_node = saye_tracking.deteccao_node:main',
        ],
    },
)
