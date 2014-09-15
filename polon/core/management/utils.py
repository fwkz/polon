import os
import errno


def create_resource(name, content, python_package=False):
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

    for name, template_path in content.iteritems():
        if os.path.splitext(name)[-1] == "":
            os.mkdir(os.path.join(root_path, name))
            print("    Sub-directory /{name} successfully created.".format(name=name))
        else:
            try:
                with open(template_path, "rb") as template_file:
                    feed = template_file.read()
            except (IOError, TypeError):
                feed = ""
            finally:
                with open(os.path.join(root_path, name), "wb") as target_file:
                    target_file.write(feed)
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