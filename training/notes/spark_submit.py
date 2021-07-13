import os
import subprocess
import re

class run_spark:

    __init__(self, conf, jar, args)
            self.conf = conf
            self.jar = jar
            self.args = args

    def spark_sub(self, conf=None, jar, args=None):
        os.system(f"spark-submit --conf {conf} --jar {jar} --args {args}")
        output=subprocess.check.output()
        for app_id in output.split():
            if app_id.startswith("application_"):
            return app_id








