#!/usr/bin/env python
import glob
import pprint
import sys
import datetime
from ruamel.yaml import YAML

yaml = YAML(typ="rt")
yaml_str = YAML(typ=["rt", "string"])


class QuartoPost:
    def __init__(self, header, content):
        self.header = header  # dict
        self.content = content  # str

    @classmethod
    def from_filename(cls, filename):
        with open(filename, "r") as infile:
            line = next(infile)
            assert line == "---\n"
            line = next(infile)
            yaml_lst = list()
            while line != "---\n":
                yaml_lst.append(line)
                line = next(infile)
            content = infile.read()
            yaml_str = "".join(yaml_lst)
            header = yaml.load(yaml_str)
        return cls(header=header, content=content)

    def to_str(self):
        return "\n".join(
            [
                "---",
                yaml_str.dump_to_string(self.header),
                "---",
                self.content,
            ]
        )

    def write(self, filename):
        with open(filename, "w") as outfile:
            outfile.write(self.to_str())

    @property
    def date(self):
        return datetime.datetime.strptime(self.header["date"], "%Y-%m-%d")

    @property
    def is_due(self):
        return self.date <= datetime.datetime.today()

    @property
    def is_draft(self):
        return "draft" in self.header and self.header["draft"]

    def publish(self):
        newly_published = False
        if self.is_due and self.is_draft:
            self.header["draft"] = False
            newly_published = True
        return newly_published


def main(glob_path):
    for fp in glob.glob(glob_path, recursive=True):
        qp = QuartoPost.from_filename(fp)
        if qp.publish():
            print("PUBLISHING: ", qp.header["title"])
            qp.write(fp)


def examples():
    qp = QuartoPost.from_filename(
        "/Users/sovacool/projects/neighborhood-scientist/neighborhoodscientist.org/posts/2025/introducing-your-neighborhood-scientist/index.qmd"
    )
    print(qp.date)
    print(datetime.datetime.today())
    print(qp.is_due)


if __name__ == "__main__":
    main("./posts/**/*.qmd")
