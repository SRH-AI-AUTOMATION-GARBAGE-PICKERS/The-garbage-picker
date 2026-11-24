from glob import glob
from setuptools import setup

package_name = 'picker_sim'

setup(
    name=package_name,
    version='0.3.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/worlds', glob('worlds/*.sdf')),
        ('share/' + package_name + '/rviz', glob('rviz/*.rviz')),
        ('share/' + package_name + '/urdf', glob('urdf/*.xacro')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Danni',
    maintainer_email='todo@example.com',
    description='Gazebo Fortress simulation of the Picker robot',
    license='Apache-2.0',
    entry_points={'console_scripts': ['teleop = picker_sim.teleop:main']},
)
