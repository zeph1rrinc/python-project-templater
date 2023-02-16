import argparse
import os
import pathlib
import shutil

from typing import Optional

from loguru import logger


def create_project(template: str, project_path: str) -> Optional[bool]:
    templates = os.listdir(os.path.join(pathlib.Path(__file__).parent.resolve(), "templates"))
    if template not in templates:
        raise ValueError(f"Template not found! ({template})")
    template_path = os.path.join(pathlib.Path(__file__).parent.resolve(), "templates", template)
    try:
        shutil.copytree(template_path, project_path)
        os.chdir(project_path)
        os.system("git init")
    except Exception as _ex:
        logger.error(_ex)
        return False
    return True


def main():
    parser = argparse.ArgumentParser(description="create new python project from template")
    parser.add_argument("-t", '--template', required=True, help='template for project')
    parser.add_argument("-p", '--project', required=True, help="project path")
    args = parser.parse_args()

    try:
        project_path = os.path.abspath(args.project)
        if not create_project(args.template, project_path):
            return
        logger.debug(f"Project {project_path} from template {args.template} successfully created!")
    except ValueError as _ex:
        logger.error(_ex)


if __name__ == '__main__':
    main()
