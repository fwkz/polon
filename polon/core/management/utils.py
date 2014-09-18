import os
import errno
from string import Template


def create_resource(name, content=(), python_package=False):
    """
    Creates resource directory in current working directory.
    :param name: Name of the root directory of the resource
    :param content: Content of the resource in form of dictionary ex. {"resource_name.py": template_path, "/test": None}
    :return:
    """
    root_path = os.path.join(os.getcwd(), name)
    mkdir_p(root_path)
    print("\nDirectory {path} sucessfully created.".format(path=root_path))

    if python_package:
        open(os.path.join(root_path, "__init__.py"), "a").close()
        print("    __init__.py successfully created.")

    for name, template_path, context in content:
        if os.path.splitext(name)[-1] == "":  # Checking if resource has extension if not it's directory
            os.mkdir(os.path.join(root_path, name))
            print("    Sub-directory /{name} successfully created.".format(name=name))
        else:
            try:
                with open(template_path, "rb") as template_file:
                    template = Template(template_file.read())
            except (IOError, TypeError):
                template = Template("")
            finally:
                with open(os.path.join(root_path, name), "wb") as target_file:
                    target_file.write(template.substitute(**context))
                    print("    {file} successfully created.".format(file=name))


def mkdir_p(path):
    """
    Simulate mkdir -p shell command. Creates directory with all needed parents.
    :param path: Directory path that may include non existing parent directories
    :return:
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise