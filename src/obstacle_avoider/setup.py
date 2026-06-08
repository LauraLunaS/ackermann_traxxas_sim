
from setuptools import find_packages, setup

package_name = 'obstacle_avoider'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='lauraluna',
    maintainer_email='lauraluna@todo.todo',
    description='Obstacle avoider for Ackermann vehicle',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'obstacle_avoider = obstacle_avoider.ackermann_obstacle_avoider:main',
            'camera_info_publisher = obstacle_avoider.camera_info_publisher:main',
        ],
    },
)
