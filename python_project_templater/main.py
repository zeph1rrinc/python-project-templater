"""
Module for creating projects based on poetry from predefined templates
"""
import argparse
import os
import pathlib
import shutil

from loguru import logger


def change_name_in_file(
        filename: str,
        template: str,
        project_name: str,
        count: int = -1,
        encoding: str = 'utf-8'
):
    """
    Change template name to project name in file
    """
    with open(filename, encoding=encoding) as file:
        data = file.read()
    with open(filename, 'w', encoding=encoding) as file:
        file.write(data.replace(template, project_name, count))


def create_project(template: str, project_path: str) -> bool:
    """
    Creating project from template

    :param template: Name of chosen template
    :type template: str

    :param project_path: Path to new project
    :type project_path: str

    :returns: status of creating
    :rtype: bool
    """
    templates = os.listdir(os.path.join(pathlib.Path(__file__).parent.resolve(), "templates"))
    if template not in templates:
        raise ValueError(f"Template not found! ({template})")
    template_path = os.path.join(pathlib.Path(__file__).parent.resolve(), "templates", template)
    project_name = project_path.split(os.sep)[-1]
    if project_name[0].isdigit():
        raise ValueError("Project name have to start with a letter")
    try:
        shutil.copytree(template_path, project_path)
        os.chdir(project_path)
        os.rename(template, project_name)
        change_name_in_file("pyproject.toml", template, project_name, 1)
        if "migrations" in os.listdir():
            change_name_in_file(os.path.join("migrations", "env.py"), template, project_name)
        os.system("git init")
    except FileExistsError as _ex:
        logger.error(_ex)
        return False
    return True


def main():
    """Main function of module"""
    parser = argparse.ArgumentParser(description="create new python project from template")
    parser.add_argument("-t", '--template', required=False, help='template for project')
    parser.add_argument("-p", '--project', required=False, help="project path")
    parser.add_argument("-ls",
                        '--templates-list',
                        required=False,
                        action="store_true",
                        help="list of templates"
                        )
    args = parser.parse_args()

    if args.templates_list:
        templates = os.listdir(os.path.join(pathlib.Path(__file__).parent.resolve(), "templates"))
        print(", ".join(templates))
        return

    try:
        project_path = os.path.abspath(args.project)
        if not create_project(args.template, project_path):
            return
        logger.debug(f"Project {project_path} from template {args.template} successfully created!")
    except ValueError as _ex:
        logger.error(_ex)


if __name__ == '__main__':
    main()
