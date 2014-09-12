import os


def create_resource(name, content):
    root_path = os.path.join(os.getcwd(), name)
    os.mkdir(root_path)
    print("\nDirectory {path} sucessfully created.".format(path=root_path))

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
