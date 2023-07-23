from setuptools import setup, find_namespace_packages

setup(name='clean_folder_asm',
      version='1.1.0',
      description='Clean Folder',
      author='Artem Shabltun',
      author_email='testvvm@example.com',
      packages=find_namespace_packages(),
      entry_points={'console_scripts': ['clean_folder=clean_folder_asm.main:start']}
)