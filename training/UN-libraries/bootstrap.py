#!/usr/bin/python
#
# unravel_emr_bootstrap script
script_ver = 'v 1.2.9'
# -- Install Unravel EMR sensor (unravel_es)  on master node
# -- Install hive hook jar file in /usr/lib/hive/lib/
# -- Install spark sensor in /usr/local/unravel-agent
# -- Update /etc/spark/conf/spark-defaults.confPreparing unravel_es properties
# -- Update /etc/hive/conf/hive-site.xml
# -- Update /etc/hadoop/conf/mapred-site.xml
# -- Update /etc/hadoop/conf/yarn-site.xml
# Log can be found here: /tmp/unravel/unravel_emr_bootstrap.log

import os
import re
import sys
import pwd
import json
import urllib2, ssl
import zipfile
import logging
import argparse
import traceback
from time import sleep
from shutil import copyfile, rmtree, move
from datetime import datetime
import xml.etree.ElementTree as ET
from subprocess import call, Popen, PIPE

# configs for bootstrap mode
sleep_time = 60     # sleep time between each config file check
max_retry = 8       # max retry before skipping config file check
init_wait = 300     # initial wait time before bootstrap action starting checking for config file
URL_TIMEOUT = 60      # Overwrite default timeout for urlopen
tmp_dir = '/tmp/unravel'

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--unravel-server", help="Unravel Server hostname/IP", dest='unravel')
    parser.add_argument("--bootstrap", help="bootstrap script run in background", action='store_true')
    parser.add_argument("--is_bootstrap", help="bootstrap script run in background", action='store_true')
    parser.add_argument("--all", "-all", help="install and config all components", action='store_true')
    parser.add_argument("--hive-only", help="install and config hive sensor only", action='store_true')
    parser.add_argument("--spark-only", help="install and config spark sensor only", action='store_true')
    parser.add_argument("--mr-only", help="install and config mr sensor only", action='store_true')
    parser.add_argument("--tez-only", help="install and config tez sensor only", action='store_true')
    parser.add_argument("--lr-port", help="unravel log receiver port", default=4043)
    parser.add_argument("--cluster-id", help="EMR cluster id")
    parser.add_argument("--metrics-factor", help="Unravel Agent metrics factor", type=int, default=6)
    parser.add_argument("--sensor-autoscaling", help="Unravel Sensor autoscaling mode", action='store_true')
    parser.add_argument("--enable-am-polling", help="Enable Auto Action AM Metrics Polling", action='store_true', dest='enable_polling')
    parser.add_argument("--disable-aa", help="Disable Auto Action", action='store_true')
    parser.add_argument("--hive-id-cache", help="Max # of MR job id cache for long running Hive job", default=1000, dest='id_cache', type=int)
    parser.add_argument("--edge-node", help="Install unravel sensor and update configurations", action='store_true')
    parser.add_argument("--master-node-ip", help="EMR master node internal IP address")
    parser.add_argument("--user-id", help="User id to run Unravel Daemon", default="hadoop")
    parser.add_argument("--group-id", help="Group id to run Unravel Daemon", default="hadoop")
    parser.add_argument("--keytab-file", help="Path to the kerberos keytab file that will be used to kinit", default="/etc/hadoop.keytab")
    parser.add_argument("--principal", help="Kerberos principal name that will be used to kinit")
    parser.add_argument("--rm-userid", help="Yarn resource manager webui username", default="a")
    parser.add_argument("--rm-password", help="Yarn resource manager webui password", default="a")
    parser.add_argument("--sensor-root", help="btrace sensor root path")
    parser.add_argument("--uninstall", help="remove unravel_es, sensors, configuration", action='store_true')
    parser.add_argument("--sensor-url", help="provide a separate base url to download unravel sensors and daemons")
    parser.add_argument("--sensor-dfs-path", help="path in distributed file system where sensors are backed up to", default="/tmp/unravel-sensors/")
    parser.add_argument("--init-wait", help="initial wait time to wait for Hadoop components installation complete", type=int)
    argv = parser.parse_args()
    if argv.init_wait:
        global init_wait
        init_wait = argv.init_wait
    return argv

def args_checker(argv):
    global INSTALL_ALL, INSTALL_PARTIAL
    if not (argv.unravel or argv.uninstall):
        raise ValueError("error: argument --unravel-server is required")

    # Handle invalid cluster id only alphanumeric and hyphen are allowed
    if argv.cluster_id:
        old_id = argv.cluster_id
        argv.cluster_id = re.sub(r"[^a-zA-Z0-9\-]", "", argv.cluster_id)
        if len(argv.cluster_id) == 0:
            print_log("{} is invalid cluster id format only alphanumeric and hyphen is allowed using j-default instead".format(old_id), log_level='warn')
            argv.cluster_id = "j-default"
        for i, v in enumerate(sys.argv):
            if v == old_id:
                sys.argv[i] = argv.cluster_id

    if argv.user_id != "hadoop" and argv.group_id == "hadoop":
        argv.group_id = argv.user_id

    if argv.id_cache < 0:
        argv.id_cache = 1000

    if argv.metrics_factor < 1:
        argv.metrics_factor = 1

    if argv.unravel and len(argv.unravel.split(':')) == 2:
        argv.unravel_port = argv.unravel.split(':')[1]
        argv.unravel = argv.unravel.split(':')[0]
    else:
        argv.unravel_port = 3000

    INSTALL_ALL = False
    INSTALL_PARTIAL = True

    if argv.hive_only or argv.tez_only or argv.spark_only or argv.mr_only:
        INSTALL_PARTIAL = False
    if argv.all:
        INSTALL_ALL = True
    return argv


class Components:
    UNRAVEL_ES = 'UNRAVEL_ES'
    BTRACE_SENSOR = 'BTRACE_SENSOR'
    HIVE_HOOK = 'HIVE-HOOK'
    HIVE_SITE = 'HIVE-SITE'
    SPARK_DEFAULTS = 'SPARK-DEFAULTS'
    SPARK_SENSOR = 'SPARK-SENSOR'
    TEZ_SITE = 'TEZ-SITE'
    YARN_SITE = 'YARN-SITE'
    MAPRED_SITE = 'MAPRED-SITE'
    HIVESERVER2_RESTART = 'HiveServer2 Restart'

    class Status:
        RESTORE = 'RESTORED'
        REMOVE = 'REMOVED'
        FAIL = 'FAILED'
        SUCCESS = 'SUCCESS'
        SKIP = 'SKIPPED'
        DONE = 'DONE'


class XmlHandler:
    RESULT_CORRECT = 'correct'
    RESULT_INCORRECT = 'incorrect'
    RESULT_MISSING = 'missing'
    RESULT_NOT_FOUND = 'not found'
    RESULT_REMOVED = 'removed'

    def __init__(self, xml_path):
        self.xml_path = xml_path
        self.xml_dict = {}
        self.__xml_tree = None
        self.__root = None

    @staticmethod
    def generate_xml_property(prop_name, prop_val, description=''):
        """
        xml parser for Unravel hive-site.xml/mapred-site.xml
        :type prop_name:  string
        :type prop_val: string
        :type description: string
        :return: xml property string
        """
        return """
<property>
    <name>%s</name>
    <value>%s</value>
    <description>%s</description>
</property>
\n
    """ % (prop_name, prop_val, description)

    def xml_to_dict(self):
        self.__xml_tree = ET.parse(self.xml_path)
        self.__root = self.__xml_tree.getroot()
        ret_val = {}
        for prop in self.__root.findall('property'):
            name = prop.find('name').text or None
            val = prop.find('value').text or None
            if name and val:
                ret_val[name] = val
        self.xml_dict = ret_val

    def replace(self, prop_name, prop_val):
        """
        :param prop_name: property name that need to search
        :type prop_name: string
        :param prop_val: property value that need to set
        :type prop_val: string | int
        :return: dict of result, old value, new value
        :rtype: dict
        """
        result = self.RESULT_MISSING
        val = self.xml_dict.get(prop_name, '')
        org_val = val
        if val:
            if val == str(prop_val):
                result = self.RESULT_CORRECT
            else:
                result = self.RESULT_INCORRECT
        if result != self.RESULT_CORRECT:
            self.xml_dict[prop_name] = prop_val
        return {"result": result, "origin_val": org_val, "new_val": self.xml_dict[prop_name]}

    def append(self, prop_name, prop_val, val_regex, delimiter=','):
        result = self.RESULT_MISSING
        val = self.xml_dict.get(prop_name, '')
        org_val = val
        if val:
            if prop_val in val:
                result = self.RESULT_CORRECT
            elif re.search(val_regex, val):
                result = self.RESULT_INCORRECT
                val = re.sub(val_regex, prop_val, val)
                self.xml_dict[prop_name] = val
            else:
                result = self.RESULT_INCORRECT
                self.xml_dict[prop_name] = val + delimiter + prop_val
        if result == self.RESULT_MISSING:
            self.xml_dict[prop_name] = prop_val
        return {"result": result, "origin_val": org_val, "new_val": self.xml_dict[prop_name]}

    def remove(self, prop_name, val_regex, delimiter=','):
        result = self.RESULT_NOT_FOUND
        val = self.xml_dict.get(prop_name, '')
        org_val = val
        if delimiter:
            items = val.split(delimiter)
            for index, item in enumerate(items):
                if re.search(val_regex):
                    items[index] = re.sub(val_regex, '', item)
            val = delimiter.join(items)
        else:
            self.xml_dict[prop_name] = ''
        return {"result": result, "origin_val": org_val, "new_val": self.xml_dict[prop_name]}

    def write(self, xml_path):
        updated_list = []
        for prop in self.__root.findall('property'):
            name = prop.find('name').text or None
            if name in self.xml_dict.keys():
                prop.find('value').text = self.xml_dict[name]
            updated_list.append(name)
        for item in list(self.xml_dict.keys()):
            if item not in updated_list:
                self.__root.append(ET.fromstringlist(self.generate_xml_property(item, self.xml_dict[item])))
                updated_list.append(item)
        self.__xml_tree.write(xml_path)


class EmrSetup:
    class ConfAction:
        REPLACE = 'replace'
        APPEND = 'append'

    def __init__(self, args):
        """
        :param cluster_id: string custom cluster id
        :param metrics_factor: Unravel Sensor Metrics Factor
        :param master_ip: EMR master node IP address
        """
        self.restart_commands = [
            {
                "version": "5.0.0",
                "commands": {
                    "list": "initctl list",
                    "stop": "sudo stop",
                    "start": "sudo start"
                }
            },
            {
                "version": "5.30.0",
                "commands": {
                    "list": "systemctl --type=service",
                    "stop": "systemctl stop",
                    "start": "systemctl start"
                }
            }
        ]
        self.instance_data = self.get_instance_data()
        self.args = args
        self.args.hive_ver = self.get_cmd_ver('hive')
        self.args.spark_ver = self.get_cmd_ver('spark-submit')
        self.kerberos = None
        self.nn_ha = None
        print_log("Hive Version: {0}".format(self.args.hive_ver))
        print_log("Spark Version: {0}".format(self.args.spark_ver))
        self.hive_version_xyz = self.args.hive_ver.split('.')
        self.spark_version_xyz = self.args.spark_ver.split('.')
        self.unravel_base_url = "http://%s:%s/" % (args.unravel, args.unravel_port)
        self.metrics_factor = args.metrics_factor
        if args.sensor_url:
            self.unravel_url = args.sensor_url
        else:
            self.unravel_url = self.unravel_base_url + 'hh/'
        self.unravel_es_path = '/usr/local/unravel_es/'
        self.unravel_prop = os.path.join(self.unravel_es_path, 'etc/unravel.properties')
        self.unravel_ctl = os.path.join(self.unravel_es_path, "etc/unravel_ctl")
        self.spark_defaults_path = '/etc/spark/conf/spark-defaults.conf'
        self.tez_site_path = '/etc/tez/conf/tez-site.xml'
        self.hive_site_path = '/etc/hive/conf/hive-site.xml'
        self.yarn_site_xml = '/etc/hadoop/conf/yarn-site.xml'
        self.hdfs_site_xml = '/etc/hadoop/conf/hdfs-site.xml'
        self.mapred_site_xml = '/etc/hadoop/conf/mapred-site.xml'
        self.should_install_hive = os.path.exists(self.hive_site_path)
        self.is_master = check_master()
        self.components = None
        if args.cluster_id:
            self.cluster_id = args.cluster_id
        else:
            self.cluster_id = self.get_cluster_id()
        if args.master_node_ip:
            self.master_ip = args.master_node_ip
        else:
            self.master_ip = Popen(['hostname', '-s'], stdout=PIPE).communicate()[0].strip()
        self.unravel_ver = self.get_unravel_version()
        print_log("Unravel Version: {0}".format(self.unravel_ver))
        if self.args.sensor_root:
            self.spark_sensor_path = self.args.sensor_root
        elif compare_versions(self.unravel_ver, "4.5.2.0") >= 0 and args.sensor_autoscaling:
            if self.check_kerberos():
                self.args.sensor_root = '/tmp/unravel-agent/'
                self.spark_sensor_path = self.args.sensor_root
            else:
                self.spark_sensor_path = '/mnt/yarn/unravel-agent/'
        else:
            self.spark_sensor_path = '/usr/local/unravel-agent/jars/'
        self.hive_hook_path = '/usr/lib/hive/lib/'
        # new version means 4.5.0.0 and beyond with new hive hook class name and unravel_es daemon
        self.new_version = True if compare_versions(self.unravel_ver, "4.5.0.0") >= 0 else False
        self.configs = self.generate_configs(args.unravel)
        self.final_status = {}
        print_log("Metrics Facotr: {0}".format(args.metrics_factor))

    @staticmethod
    def check_user(username):
        """ Check user existence create if not exist """
        try:
            pwd.getpwnam(username)
        except Exception as e:
            print_log(e.message, log_only=True)
            print_log("User {0} does not exist".format(username))
            print_log("Creating User {0}".format(username))
            create_user_popen = Popen("useradd {0}".format(username), shell=True, stdout=PIPE, stderr=PIPE)
            result = create_user_popen.communicate()
            if create_user_popen.returncode != 0:
                print_log("Create User failed: {0}".format(result[1]), log_level='error')

    def check_kerberos(self):
        if self.kerberos is not None:
            return self.kerberos
        yarn_site = XmlHandler(self.yarn_site_xml)
        yarn_site.xml_to_dict()
        if yarn_site.xml_dict.get("yarn.resourcemanager.keytab", None):
            self.kerberos = True
        self.kerberos = False
        return self.kerberos

    def check_nn_ha(self):
        if self.nn_ha is not None:
            return self.nn_ha
        self.nn_ha = False
        try:
            hdfs_site = XmlHandler(self.hdfs_site_xml)
            hdfs_site.xml_to_dict()
            ns = hdfs_site.xml_dict.get("dfs.nameservices", None)
            if ns:
                if len(hdfs_site.xml_dict.get("dfs.ha.namenodes.{}".format(ns), "").split(",")) > 1:
                    self.nn_ha = True
        except:
            print_log(traceback.format_exc(), log_level="warn", log_only=True)
        return self.nn_ha

    def download_file(self, file_url, save_path):
        try:
            with open(save_path, 'wb') as f:
                print_log('Downloading file: %s to %s' % (file_url, save_path))
                f.write(urllib2.urlopen(file_url, timeout=URL_TIMEOUT, context=ssl._create_unverified_context()).read())
                f.close()
                if not self.check_kerberos():
                    if not self.hdfs_path_exists(self.args.sensor_dfs_path):
                        self.hdfs_dfs_cmd("-mkdir", self.args.sensor_dfs_path)
                    if not self.hdfs_path_exists(os.path.join(self.args.sensor_dfs_path, os.path.basename(save_path))):
                        self.hdfs_dfs_cmd("-put", save_path, self.args.sensor_dfs_path)
                return True
        except urllib2.URLError:
            print_log("Failed to download from {0}: {1}".format(file_url, traceback.format_exc()), log_level='error')
        return False

    @staticmethod
    def hdfs_dfs_cmd(*argv):
        cmd = ["hdfs", "dfs"] + list(argv)
        hdfs_popen = Popen(cmd, stderr=PIPE, stdout=PIPE)
        output = hdfs_popen.communicate()
        if hdfs_popen.returncode == 0:
            return True
        elif 'No such file or directory' not in output[1]:
            print_log("Failed to run {0}: {1}".format(cmd, output[1]), log_level='warn')
        return False

    def hdfs_path_exists(self, path):
        return self.hdfs_dfs_cmd("-ls", path)

    @staticmethod
    def get_instance_data():
        instance_data_path = "/mnt/var/lib/info/extraInstanceData.json"
        try:
            with open(instance_data_path, "r") as f:
                return json.loads(f.read())
        except Exception as e:
            print_log("Failed to read {}: {}".format(instance_data_path, e), log_level="error")
        return {}

    @staticmethod
    def get_cluster_id():
        """
        :return: string cluster id
        """
        job_flow_path = "/mnt/var/lib/info/job-flow.json"
        cluster_id = "j-default"
        try:
            with open(job_flow_path, "r") as f:
                cluster_id = json.loads(f.read()).get("jobFlowId", "j-default")
        except Exception as e:
            print_log("Failed to get cluster id from {0} return j-default".format(job_flow_path), log_level='error')
        finally:
            return cluster_id

    @staticmethod
    def print_column(msg_left, msg_right, width):
        """
        print column like message line
        :param msg_left: message that on the left side
        :param msg_right: message that on the right side
        :param width: max width of the line
        """
        print("{0} {1:>{width}}".format(msg_left, msg_right, width=width - len(msg_left)))

    def get_unravel_version(self):
        """
        :return: string of the version number e.g. 4.5.0.1
        """
        version_str = "4.6.1.0"
        try:
            version_txt = urllib2.urlopen(self.unravel_base_url + 'version.txt', timeout=URL_TIMEOUT, context=ssl._create_unverified_context()).read()
            if re.search("[45].[0-9]+.[0-9]+.[0-9]+", version_txt):
                version_str = re.search("[45].[0-9]+.[0-9]+.[0-9]+", version_txt).group(0)
        except Exception as e:
            print_log(e, log_level='error')
            print_log("Couldn't get unravel version txt file", log_level='error')
        finally:
            return version_str

    def get_components(self):
        """
        :return: string of all the components will be installed
        """
        components_file_path = '/mnt/var/lib/info/job-flow-state.txt'
        try:
            self.components = open(components_file_path, 'r').read()
        except Exception as e:
            print_log('Failed to get components', log_level='error')
            self.components = 'None'

    def generate_configs(self, unravel_host):
        """
        Generate all the instrumentation needed for Unravel EMR Setup
        :param unravel_host: Unravel host ip or hostname
        :return: dict of all the configurations
        """
        configs = {}
        cluster_id_format = "clusterId={}".format(self.cluster_id)
        hive_regex = "com.unraveldata.dataflow.hive.hook.Hive.*?Hook|com.unraveldata.dataflow.hive.hook.UnravelHiveHook"
        configs['hive-site'] = {
            "com.unraveldata.host": {
                "value": unravel_host,
                "action": self.ConfAction.REPLACE
            },
            "com.unraveldata.hive.hook.tcp": {
                "value": 'true',
                "action": self.ConfAction.REPLACE
            },
            "com.unraveldata.hive.hdfs.dir": {
                "value": "/user/unravel/HOOK_RESULT_DIR",
                "action": self.ConfAction.REPLACE
            },
            "hive.exec.driver.run.hooks": {
                "value": "com.unraveldata.dataflow.hive.hook.UnravelHiveHook",
                "action": self.ConfAction.APPEND,
                "regex": hive_regex,
                "delimiter": ","
            },
            "hive.exec.pre.hooks": {
                "value": "com.unraveldata.dataflow.hive.hook.UnravelHiveHook",
                "action": self.ConfAction.APPEND,
                "regex": hive_regex,
                "delimiter": ","
            },
            "hive.exec.post.hooks": {
                "value": "com.unraveldata.dataflow.hive.hook.UnravelHiveHook",
                "action": self.ConfAction.APPEND,
                "regex": hive_regex,
                "delimiter": ","
            },
            "hive.exec.failure.hooks": {
                "value": "com.unraveldata.dataflow.hive.hook.UnravelHiveHook",
                "action": self.ConfAction.APPEND,
                "regex": hive_regex,
                "delimiter": ","
            },
            "com.unraveldata.cluster.id": {
                "value": self.cluster_id,
                "action": self.ConfAction.REPLACE
            }
        }

        if self.args.lr_port != 4043:
            if self.new_version:
                configs['hive-site']['com.unraveldata.port'] = {
                    "value": self.args.lr_port,
                    "action": self.ConfAction.REPLACE
                }
            else:
                configs['hive-site']['com.unraveldata.live.logreceiver.port'] = {
                    "value": self.args.lr_port,
                    "action": self.ConfAction.REPLACE
                }

        if self.args.spark_ver:
            spark_lib = 'spark-{0}'.format(self.spark_version_xyz[0] + '.' + self.spark_version_xyz[1])
        else:
            spark_lib = ''

        configs['spark-defaults'] = {
            'spark.eventLog.enabled': 'true',
            'spark.unravel.server.hostport': unravel_host + ':' + str(self.args.lr_port),
            'spark.driver.extraJavaOptions': '-javaagent:{0}=config=driver,libs={1}{3} -Dunravel.metrics.factor={2}'.format(
                os.path.join(self.spark_sensor_path, "btrace-agent.jar"),
                spark_lib,
                self.metrics_factor,
                "," + cluster_id_format
            ),
            'spark.executor.extraJavaOptions': '-javaagent:{0}=config=executor,libs={1}{3} -Dunravel.metrics.factor={2}'.format(
                os.path.join(self.spark_sensor_path, "btrace-agent.jar"),
                spark_lib,
                self.metrics_factor,
                "," + cluster_id_format
            )
        }

        # 0: btrace jar path
        # 1: clusterId field for sensor
        # 2: unravel lr server hostname/IP
        # 3: unravel lr server port
        # 4: Sensor Metrics Factor
        tez_config_format = '-javaagent:{0}=libs=mr,config=tez{1} -Dunravel.server.hostport={2}:{3} -Dunravel.metrics.factor={4}'
        tez_regex = tez_config_format.format('.*?', r'[,a-zA-Z\d=-]*', '.*', '[0-9]{0,5}', '[0-9]+')
        configs['tez-site'] = {
            'tez.am.launch.cmd-opts': {
                "value": tez_config_format.format(
                    os.path.join(self.spark_sensor_path, "btrace-agent.jar"),
                    "," + cluster_id_format,
                    unravel_host,
                    self.args.lr_port,
                    self.metrics_factor
                ),
                "action": self.ConfAction.APPEND,
                "regex": tez_regex,
                "delimiter": " "
            },
            'tez.task.launch.cmd-opts': {
                "value": tez_config_format.format(
                    os.path.join(self.spark_sensor_path, "btrace-agent.jar"),
                    "," + cluster_id_format,
                    unravel_host,
                    self.args.lr_port,
                    self.metrics_factor
                ),
                "action": self.ConfAction.APPEND,
                "regex": tez_regex,
                "delimiter": " "
            }
        }

        # 0: btrace jar path
        # 1: clusterId field for sensor
        # 2: unravel lr server hostname/IP
        # 3: unravel lr server port
        # 4: Sensor Metrics Factor
        mapred_config_format = '-javaagent:{0}=libs=mr{1} -Dunravel.server.hostport={2}:{3} -Dunravel.metrics.factor={4}'
        mapred_regex = mapred_config_format.format('.*btrace-agent.jar', r'[,a-zA-Z\d=-]*', '.*', '[0-9]{1,5}', '[0-9]+')
        configs['mapred-site'] = {
            'yarn.app.mapreduce.am.command-opts': {
                "value": mapred_config_format.format(
                    os.path.join(self.spark_sensor_path, "btrace-agent.jar"),
                    "," + cluster_id_format,
                    unravel_host,
                    self.args.lr_port,
                    self.metrics_factor
                ),
                "action": self.ConfAction.APPEND,
                "delimiter": " ",
                "regex": mapred_regex
            },
            'mapreduce.task.profile': {
                "value": 'true',
                "action": self.ConfAction.REPLACE
            },
            'mapreduce.task.profile.maps': {
                "value": '0-5',
                "action": self.ConfAction.REPLACE
            },
            'mapreduce.task.profile.reduces': {
                "value": '0-5',
                "action": self.ConfAction.REPLACE
            },
            'mapreduce.task.profile.params': {
                "value": mapred_config_format.format(
                    os.path.join(self.spark_sensor_path, "btrace-agent.jar"),
                    "," + cluster_id_format,
                    unravel_host,
                    self.args.lr_port,
                    self.metrics_factor
                ),
                "action": self.ConfAction.APPEND,
                "delimiter": " ",
                "regex": mapred_regex
            }
        }

        if not self.check_nn_ha():
            configs['spark-defaults']['spark.eventLog.dir'] = 'hdfs://%s:8020/' % self.master_ip

        configs['yarn-site'] = {
            'yarn.timeline-service.webapp.address': {
                "value": '${yarn.timeline-service.hostname}:8188',
                "action": self.ConfAction.REPLACE
            }
        }

        # Old hive hook classname for Unravel 4.4 and prior
        if not self.new_version:
            configs['hive-site']['hive.exec.driver.run.hooks']['value'] = "com.unraveldata.dataflow.hive.hook.HiveDriverHook"
            configs['hive-site']['hive.exec.pre.hooks']['value'] = "com.unraveldata.dataflow.hive.hook.HivePreHook"
            configs['hive-site']['hive.exec.post.hooks']['value'] = "com.unraveldata.dataflow.hive.hook.HivePostHook"
            configs['hive-site']['hive.exec.failure.hooks']['value'] = "com.unraveldata.dataflow.hive.hook.HiveFailHook"
        return configs

    def gen_secure_config(self):
        """ Generating secure configurations in unravel.properties """
        if self.args.user_id == 'hadoop':
            self.args.user_id, self.args.group_id = 'unravel', 'unravel'
        if self.args.user_id != 'unravel' and self.args.group_id == 'unravel':
            self.args.group_id = self.args.user_id

        self.check_user(self.args.user_id)
        Popen("setfacl -m u:{0}:r-- {1}".format(self.args.user_id, self.args.keytab_file), shell=True)

        if self.args.keytab_file and not self.args.principal:
            self.args.principal = self.get_principal_from_key(self.args.keytab_file)

        ctl_content = """UNRAVEL_ES_USER={0}
UNRAVEL_ES_GROUP={1}"""

        prop_content = """com.unraveldata.kerberos.principal={principal}
com.unraveldata.kerberos.keytab.path={keytab}
yarn.resourcemanager.webapp.username={rm_user}
yarn.resourcemanager.webapp.password={rm_pass}
com.unraveldata.kerberos.kinit_scheduler.enabled=false""".format(
            principal=self.args.principal,
            keytab=self.args.keytab_file,
            rm_user=self.args.rm_userid,
            rm_pass=self.args.rm_password)

        if self.args.user_id != 'unravel':
            with open(self.unravel_ctl, 'w') as f:
                f.write(ctl_content.format(self.args.user_id, self.args.group_id))
                f.close()

        with open(self.unravel_prop, 'w+') as f:
            if len(f.readlines()) == 0 or prop_content not in f.read():
                f.write(prop_content)
            else:
                f.seek(0, os.SEEK_END)
                f.write("\n{}".format(prop_content))
            f.close()

    # Create unravel_es daemon in /etc/init.d/unravel_es
    def gen_sensor_daemon(self):
        if not self.new_version:
            pid_grep = '"unravel_emr_sensor.sh|unravel_es/unravel-emr-sensor.jar" '
            sensor_sh = './unravel_emr_sensor.sh'
        else:
            pid_grep = '"unravel_es|unravel_emr_sensor"'
            sensor_sh = './dbin/unravel_emr_sensor.sh'

        sensor_daemon_content = '''#!/bin/bash
# chkconfig: 2345 90 10
### BEGIN INIT INFO
# Provides:          Unravel EMR Sensor daemon
# Required-Start:
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Instrumentation for Unravel
# Description:       Instrumentation for Unravel, sends job logs to Unravel server
### END INIT INFO

. /lib/lsb/init-functions

#set -x
TMP_DIR="/tmp/unravel/tmp"
DAEMON_NAME="unravel_es"
PID_FILE="${{TMP_DIR}}/${{DAEMON_NAME}}.pid"
OUT_LOG="${{TMP_DIR}}/${{DAEMON_NAME}}.out"
UNRAVEL_ES_USER={run_as_user}
if [ -e /usr/local/unravel_es/etc/unravel_ctl ]; then
    source /usr/local/unravel_es/etc/unravel_ctl
fi

function get_pid {{
  cat $PID_FILE
}}

function is_running {{
  $([ -f $PID_FILE ] && ps $(get_pid) > /dev/null 2>&1) || $(ps -U $UNRAVEL_ES_USER -f | egrep "unravel_es|unravel_emr_sensor" | grep -v grep > /dev/null 2>&1)
}}

function start {{
  if is_running; then
    echo "$DAEMON_NAME already started"
  else
    echo "Starting $DAEMON_NAME..."
    su - ${{UNRAVEL_ES_USER}} -c bash -c "cd /usr/local/${{DAEMON_NAME}}; {emr_sh_path}" >$OUT_LOG 2>&1 &
    echo $! > $PID_FILE
    disown %1
    if ! is_running ; then
      echo "Unable to start $DAEMON_NAME, see $OUT_LOG"
      exit 1
    fi
  fi
}}

function stop {{
  if is_running; then
    pid=$(get_pid)
    echo "Stopping $DAEMON_NAME... PID: $pid"
    kill $pid
    sleep 1
    PIDS=$(ps -U ${{UNRAVEL_ES_USER}} -f | egrep {pid_grep} | grep -v grep | awk '{{ print $2 }}' )
    [ "$PIDS" ] && kill $PIDS
    for i in {{1..90}}
    do
        if ! is_running; then
            break
        fi
        echo -n "."
        sleep 1
        if [ $i -ge 90 ]; then
          echo "stop timed out force kill"
          [ "$PIDS" ] && kill -9 $PIDS
        fi
    done
    if is_running; then
        echo "$DAEMON_NAME not stopped; may still be shutting down or shutdown may have failed"
        exit 1
    else
        echo "$DAEMON_NAME stopped"
        if [ -f $PID_FILE ]; then
            rm $PID_FILE
        fi
    fi
  else
    echo "$DAEMON_NAME not running"
  fi
}}

case $1 in
  'start' )
     start
     ;;
  'stop' )
     stop
     ;;
  'restart' )
     stop
     if is_running; then
       echo "Unable to stop $DAEMON_NAME, will not attempt to start"
       exit 1
     fi
     start
     ;;
  'status' )
    if is_running; then
      echo "$DAEMON_NAME is running"
    else
      echo "$DAEMON_NAME is not running"
    fi
    ;;
  *)
    echo "usage: `basename $0` {{start|stop|status|restart}}"
esac

exit 0
'''.format(run_as_user=self.args.user_id, pid_grep=pid_grep, emr_sh_path=sensor_sh)
        daemon_temp = tmp_dir + '/tmp/unravel_es'
        if not os.path.exists(daemon_temp):
            call('mkdir -p {0}'.format(os.path.dirname(daemon_temp)), shell=True)

        print_log('Creating unravel daemon script in /etc/init.d/')
        sensor_script = open(daemon_temp, 'w')
        sensor_script.write(sensor_daemon_content)
        sensor_script.close()
        call('sudo mv %s /etc/init.d/unravel_es' % daemon_temp, shell=True)
        call('sudo chmod 744 /etc/init.d/unravel_es', shell=True)
        call('sudo chown -R {run_user}:{run_group} /etc/init.d/unravel_es'.format(run_user=self.args.user_id,
                                                                                  run_group=self.args.group_id),
             shell=True)
        print_log('unravel daemon created')

    # Create unravel_es sensor script for 4.4 and prior
    def gen_sensor_script(self):
        lr_arg = ''
        if self.args.lr_port != 4043:
            lr_arg = '--lr-port $UNRAVEL_PORT '
        sensor_script_content = '''#!/bin/bash
UNRAVEL_HOST={unravel_host}
UNRAVEL_PORT={unravel_port}
IDENT=unravel_es
cd /usr/local/unravel_es
# this script (process) will stick around as a nanny
FLAP_COUNT=0
MINIMUM_RUN_SEC=5
while true ; do
  # nanny loop
  START_AT=$(date +%s)
  java -server -Xmx2g -Xms2g -jar /usr/local/${{IDENT}}/unravel-emr-sensor.jar --cluster-id {cluster_id} --unravel-server $UNRAVEL_HOST {lr}> ${{IDENT}}.out  2>&1

  CHILD_PID=$!
  # if this script gets INT or TERM, then clean up child process and exit
  trap 'kill $CHILD_PID; exit 5' SIGINT SIGTERM
  # wait for child
  wait $CHILD_PID
  CHILD_RC=$?
  FINISH_AT=$(date +%s)
  RUN_SECS=$(($FINISH_AT-$START_AT))
  echo "$(date '+%Y%m%dT%H%M%S') ${{IDENT}} died after ${{RUN_SECS}} seconds" >> ${{IDENT}}.out
  if [ $CHILD_RC -eq 71 ]; then
      echo "$(date '+%Y%m%dT%H%M%S') ${{IDENT}} retcode is 71, indicating no restart required" >>$UNRAVEL_LOG_DIR/${{IDENT}}.out
      exit 71
    fi
    if [ $RUN_SECS -lt $MINIMUM_RUN_SEC ]; then
      FLAP_COUNT=$(($FLAP_COUNT+1))
      if [ $FLAP_COUNT -gt 10 ]; then
        echo "$(date '+%Y%m%dT%H%M%S') ${{IDENT}} died too fast, NOT restarting to avoid flapping" >>${{IDENT}}.out
        exit 6
      fi
  else
      FLAP_COUNT=0
  fi
  sleep 10
done
'''.format(unravel_host=self.args.unravel, unravel_port=self.args.lr_port, lr=lr_arg, cluster_id=self.cluster_id)

        print_log('Creating unravel_emr_sensor.sh')
        sensor_script = open(self.unravel_es_path + 'unravel_emr_sensor.sh', 'w')
        sensor_script.write(sensor_script_content)
        sensor_script.close()
        call('sudo chmod +x {0}*.sh'.format(self.unravel_es_path), shell=True)
        call('sudo chown -R hadoop:hadoop {0}'.format(self.unravel_es_path), shell=True)
        print_log('unravel_emr_sensor.sh created')

    # Create unravel_es sensor script for 4.5 and later
    def gen_sensor_properties(self):
        sensor_prop_name = 'unravel_es.properties'
        es_prop_path = "{0}/etc/{1}".format(self.unravel_es_path, sensor_prop_name)
        unravel_server = "{0}:{1}".format(self.args.unravel, self.args.lr_port)
        # Generate new properties file if not exists
        sensor_properties_content = '''# Unravel EMR Sensor properties
unravel-server={unravel_server}
cluster-id={cluster_id}'''.format(unravel_server=unravel_server, unravel_port=self.args.lr_port, cluster_id=self.cluster_id)
        print_log("Creating %s" % sensor_prop_name)
        if os.path.exists(es_prop_path):
            sensor_properties_content = open(es_prop_path, 'r').read()
            # Backup old unravel_es.properties
            os.rename(es_prop_path, "{0}.{1}".format(es_prop_path, datetime.now().strftime("%Y%m%d%H%S")))
            sensor_properties_content = re.sub("unravel-server\s?=\s?.*", "unravel-server=" + unravel_server, sensor_properties_content)

        # TODO: Write properties handler function
        found_exec_eng = re.search('exec-engine.*', sensor_properties_content)
        # Enable sensor autoscaling
        if self.args.sensor_autoscaling and not found_exec_eng:
            sensor_properties_content += '\nexec-engine=mr,tez,sensor'
        elif self.args.sensor_autoscaling and "sensor" not in found_exec_eng.group(0):
            sensor_properties_content = re.sub("exec-engine\s?=\s?.*", "{0},sensor".format(found_exec_eng.group(0)), sensor_properties_content)
        # Enable AM Polling for Auto Action
        am_prop = re.search('am-polling.*', sensor_properties_content)
        if self.args.enable_polling and not am_prop:
            sensor_properties_content += '\nam-polling=true'
        else:
            value = "false"
            if self.args.enable_polling:
                value = "true"
            sensor_properties_content = re.sub("am-polling\s?=\s?.*", "am-polling=" + value, sensor_properties_content)
        # Disable Auto Action
        aa_prop = re.search('enable-aa.*', sensor_properties_content)
        if self.args.disable_aa and not aa_prop:
            sensor_properties_content += '\nenable-aa=false'
        else:
            value = "true"
            if self.args.disable_aa:
                value = "false"
            sensor_properties_content = re.sub("enable-aa\s?=\s?.*", "enable-aa=" + value, sensor_properties_content)
        # Config hive-id-cache
        id_cache = re.search("hive-id-cache\s?=\s?(.*)", sensor_properties_content)
        if self.args.id_cache != 1000 and not id_cache:
            sensor_properties_content += '\nhive-id-cache={0}'.format(self.args.id_cache)
        elif id_cache and int(id_cache.group(1)) != self.args.id_cache:
            sensor_properties_content = re.sub("hive-id-cache\s?=\s?.*", "hive-id-cache={0}".format(self.args.id_cache),
                                               sensor_properties_content)

        sensor_script = open(es_prop_path, 'w')
        sensor_script.write(sensor_properties_content)
        sensor_script.close()
        call('sudo chown -R {user}:{group} /usr/local/unravel_es'.format(user=self.args.user_id,
                                                                         group=self.args.group_id), shell=True)
        print_log('unravel_emr_sensor.sh created')

    #   Download and install unravel_es
    def install_es(self):
        download_path = self.unravel_es_path + "download"
        if not self.new_version:
            emr_sensor_jar = 'unravel-emr-sensor.jar'
            emr_sensor_url = os.path.join(self.unravel_url, emr_sensor_jar)
            emr_sensor_path = self.unravel_es_path + emr_sensor_jar
        else:
            emr_sensor_archive = 'unravel-emrsensor-pack.zip'
            emr_sensor_url = os.path.join(self.unravel_url, emr_sensor_archive)
            emr_sensor_path = os.path.join(download_path, emr_sensor_archive)
        try:
            if not self.is_master:
                print_log('Not master node skip unravel_es installation')
                return None

            if not os.path.exists(self.unravel_es_path):
                os.makedirs(self.unravel_es_path)

            # Download EMR Sensor
            if not os.path.exists(download_path):
                os.makedirs(download_path)

            print_log('Downloading unravel_es')
            if not self.download_file(emr_sensor_url, emr_sensor_path) and not self.check_kerberos():
                dfs_path = os.path.join(self.args.sensor_dfs_path, os.path.basename(emr_sensor_path))
                print_log("Downloading file from dfs {0}".format(dfs_path))
                self.hdfs_dfs_cmd("-get", "-f", dfs_path, emr_sensor_path)
            if self.new_version:
                dlib_path = os.path.join(self.unravel_es_path, "dlib")
                self.remove_paths({dlib_path})
                zip_target = zipfile.ZipFile(emr_sensor_path, 'r')
                zip_target.extractall(self.unravel_es_path)
                zip_target.close()
                call('sudo chmod 0755 ' + self.unravel_es_path + '/dbin/*', shell=True)
            else:
                call('sudo chmod 0755 ' + emr_sensor_path, shell=True)
            call('sudo chown -R {user}:{group} '.format(user=self.args.user_id,
                                                        group=self.args.group_id) + self.unravel_es_path, shell=True)

            if self.check_kerberos():
                print_log("Setting up Secure configurations for secure cluster")
                self.gen_secure_config()

            print_log('Creating unravel_es daemon')
            self.gen_sensor_daemon()
            if self.new_version:
                print_log('Preparing unravel_es properties')
                self.gen_sensor_properties()
                if self.args.sensor_root:
                    self.update_sensor_deploy()
            else:
                print_log('Preparing unravel_emr_sensor.sh script')
                self.gen_sensor_script()
            call('sudo /sbin/chkconfig unravel_es on', shell=True)
            print_log('Starting unravel_es')
            call('sudo service unravel_es restart', shell=True)
            print_log("unravel_es run as user: {0}".format(self.args.user_id))
            sleep(5)
            try:
                print_log(Popen('sudo /etc/init.d/unravel_es status', shell=True, stdout=PIPE).communicate()[0])
            except:
                print_log('Unravel_es not started')

        except Exception as e:
            print_log(e, log_level='error')
            print_log('Install unravel_es failed', log_level='error')

    #   Download and install hive hook sensor
    def install_hive_hook(self):
        try:
            if 'hive-site' not in self.components:
                print_log('hive hook jar installation skip')
                return None
            hive_hook_jar = 'unravel-hive-%s.%s.0-hook.jar' % (self.hive_version_xyz[0], self.hive_version_xyz[1])
            if os.path.exists(os.path.join(self.hive_hook_path, hive_hook_jar)):
                print_log('hive hook jar already installed')
                print_log('updating hive hook jar')
            if self.should_install_hive:
                if not self.download_file(os.path.join(self.unravel_url, hive_hook_jar), self.hive_hook_path + hive_hook_jar) and not self.check_kerberos():
                    dfs_path = os.path.join(self.args.sensor_dfs_path, hive_hook_jar)
                    print_log("Downloading file from dfs {0}".format(dfs_path))
                    self.hdfs_dfs_cmd("-get", "-f", dfs_path, self.hive_hook_path + hive_hook_jar)
                if os.path.exists(self.hive_hook_path + hive_hook_jar):
                    print_log('hive hook jar installed')
                    self.final_status[Components.HIVE_HOOK] = Components.Status.DONE
                else:
                    print_log('hive hook jar installation failed')
                    self.final_status[Components.HIVE_HOOK] = Components.Status.FAIL
        except Exception as e:
            print_log(traceback.format_exc(), log_level='error')
            self.should_install_hive = False
            print_log('hive hook jar installation failed', 'error')
            print_log('Please make sure {0} is accessible'.format(self.unravel_url))
            self.final_status[Components.HIVE_HOOK] = Components.Status.FAIL

    #   Download and install spark/mr sensor
    def install_spark_sensor(self):
        spark_sensor_jar = 'unravel-agent-pack-bin.zip'
        spark_jar_save_path = os.path.join(self.spark_sensor_path, spark_sensor_jar)
        try:
            if not os.path.exists(self.spark_sensor_path):
                os.makedirs(self.spark_sensor_path)
            if not self.download_file(os.path.join(self.unravel_url, spark_sensor_jar),
                               os.path.join(self.spark_sensor_path, spark_sensor_jar)) and not self.check_kerberos():
                dfs_path = os.path.join(self.args.sensor_dfs_path, spark_sensor_jar)
                print_log("Downloading file from dfs {0}".format(dfs_path))
                self.hdfs_dfs_cmd("-get", "-f", dfs_path, spark_jar_save_path)
            zip_target = zipfile.ZipFile(spark_jar_save_path, 'r')
            zip_target.extractall(self.spark_sensor_path)
            zip_target.close()
            print_log('Spark Sensor Installed')
            self.final_status[Components.SPARK_SENSOR] = Components.Status.DONE
        except Exception as e:
            print_log(e, log_level='error')
            print_log(traceback.format_exc(), log_level='error', log_only=True)
            print_log('Spark sensor installation failed', 'error')
            print_log('Please make sure {0} is accessible'.format(self.unravel_url))
            self.final_status[Components.SPARK_SENSOR] = Components.Status.FAIL

    def install_sensors_configs(self):
        self.get_components()
        self.install_spark_sensor()
        if INSTALL_ALL or INSTALL_PARTIAL or self.args.hive_only:
            self.install_hive_hook()
            self.update_hive_site()
            if 'tez' in self.components:
                self.args.tez_only = True
            self.restart_hiveserver2()
        if INSTALL_ALL or INSTALL_PARTIAL or self.args.tez_only:
            self.update_tez_site()
        if INSTALL_ALL or INSTALL_PARTIAL or self.args.spark_only:
            self.update_spark_defaults()
        if INSTALL_ALL or self.args.mr_only:
            self.update_mapred_site()
        self.update_yarn_site()

    @staticmethod
    def remove_paths(paths):
        """
        Remove folders and its content if exists
        :type paths: dict
        :return:
        """
        for path in paths:
            if os.path.exists(path):
                if os.path.isdir(path):
                    rmtree(path)
                elif os.path.isfile(path):
                    os.remove(path)
                print_log("{0} found removing".format(path))

    #   Compare and Update hive-site.xml file
    def update_hive_site(self, retry=0):
        try:
            print_log('\nChecking hive-site.xml')
            hive_site_preunravel = self.hive_site_path + '.preunravel'

            # Wait for Hive installation complete
            if 'hive-site' in self.components and should_wait_for_file(self.hive_site_path, retry, self.args.is_bootstrap):
                self.update_hive_site(retry=retry + 1)
                return None
            elif not os.path.exists(self.hive_site_path):
                print_log('Skip hive-site.xml')
                self.final_status[Components.HIVE_SITE] = Components.Status.SKIP
                return None

            # Check hive version
            self.hive_ver = self.get_cmd_ver('hive')
            self.hive_version_xyz = self.hive_ver.split('.')
            self.configs = self.generate_configs(self.args.unravel)

            if self.final_status.get(Components.HIVE_HOOK, 'None') == Components.Status.FAIL:
                self.install_hive_hook()

            # Backup hive-site.xml
            if not os.path.exists(hive_site_preunravel):
                print_log("Backup original hive-site.xml")
                copyfile(self.hive_site_path, hive_site_preunravel)

            # Compare hive-site.xml properties
            handler = XmlHandler(self.hive_site_path)
            handler.xml_to_dict()
            for config, val_dict in self.configs['hive-site'].iteritems():
                if val_dict['action'] == self.ConfAction.REPLACE:
                    result = handler.replace(config, val_dict['value'])
                else:
                    result = handler.append(config, val_dict['value'], val_dict['regex'])
                self.print_column(config, result['result'], 80)
                print_log("Suggest config: {0}\nCurrent config: {1}".format(result['origin_val'], result['new_val']), log_only=True)
                sleep(1)
            handler.write(self.hive_site_path)

            self.final_status[Components.HIVE_SITE] = Components.Status.DONE
        except Exception as e:
            print_log(e, log_level='error')
            self.final_status[Components.HIVE_SITE] = Components.Status.FAIL

    #   Compare and Update mapred-site.xml file
    def update_mapred_site(self, retry=0):
        try:
            print("\nChecking mapred-site.xml")
            mapred_site_xml = self.mapred_site_xml
            preunravel_mapred_site = mapred_site_xml + '.preunravel'

            # Wait for mapreduce 2 installation complete
            if should_wait_for_file(mapred_site_xml, retry, self.args.is_bootstrap):
                self.update_mapred_site(retry=retry + 1)
                return None
            elif not os.path.exists(mapred_site_xml):
                print_log('Skip mapred-site.xml')
                self.final_status[Components.MAPRED_SITE] = Components.Status.SKIP
                return None

            # Backup mapred-site.xml
            if not os.path.exists(preunravel_mapred_site):
                print("Backup original mapred-site.xml")
                copyfile(mapred_site_xml, preunravel_mapred_site)

            # Compare mapred-site.xml properties
            handler = XmlHandler(mapred_site_xml)
            handler.xml_to_dict()
            for config, val_dict in self.configs['mapred-site'].iteritems():
                if val_dict['action'] == self.ConfAction.REPLACE:
                    result = handler.replace(config, val_dict['value'])
                else:
                    result = handler.append(config, val_dict['value'], val_dict['regex'], delimiter=val_dict['delimiter'])
                self.print_column(config, result['result'], 80)
                print_log("Suggest config: {0}\nCurrent config: {1}".format(result['origin_val'], result['new_val']),
                          log_only=True)
                sleep(1)
            handler.write(mapred_site_xml)

            self.final_status[Components.MAPRED_SITE] = Components.Status.DONE
        except Exception as e:
            print_log(e, log_level='error')
            print_log('Skip mapred-site.xml')
            self.final_status[Components.MAPRED_SITE] = Components.Status.FAIL

    #   Description: Compare and Update spark-defaults.conf file
    def update_spark_defaults(self, retry=0):
        try:
            print('\nChecking spark-defaults.conf')
            spark_defaults_preunravel = self.spark_defaults_path + '.preunravel'
            # Wait for Spark installation complete
            if 'spark-on-yarn' in self.components and should_wait_for_file(self.spark_defaults_path, retry, self.args.is_bootstrap):
                self.update_spark_defaults(retry=retry + 1)
                return None
            elif not os.path.exists(self.spark_defaults_path):
                print_log('Skip spark-defaults.conf')
                self.final_status[Components.SPARK_DEFAULTS] = Components.Status.SKIP
                return None

            # Get spark-submit version
            self.spark_ver = self.get_cmd_ver('spark-submit')
            self.spark_version_xyz = self.spark_ver.split('.')
            self.configs = self.generate_configs(self.args.unravel)

            # Backup original spark-defaults.conf
            if not os.path.exists(spark_defaults_preunravel):
                print_log('Backing up original spark-defaults.conf')
                copyfile(self.spark_defaults_path, spark_defaults_preunravel)

            content = open(self.spark_defaults_path, 'r').read()
            new_config = None

            def config_updater(content, append=False, config_regex=None, print_msg=True):
                global _config
                if append:
                    _config = ori_config + ' ' + config_val
                elif config_regex:
                    if re.search(config_regex, ori_config):
                        _config = re.sub(config_regex, config_val, ori_config)
                    else:
                        config_updater(content, append=True, print_msg=False)
                else:
                    _config = config_name + ' ' + config_val
                content = re.sub(ori_regex, _config, content)
                if print_msg:
                    self.print_column(config_name, "incorrect", 80)
                    print_log(config_name + ' incorrect: \nOld config:' + ori_config + '\nNew config:' + _config)
                return content

            # Compare spark-defaults.conf properties
            for config_name, config_val in self.configs['spark-defaults'].iteritems():
                if config_name in content:
                    ori_regex = config_name + '.*'
                    ori_config = re.search(ori_regex, content).group(0)
                    if config_val in content:
                        self.print_column(config_name, "correct", 80)
                        print_log(config_name + ' correct: \n' + config_val)
                    elif config_name == 'spark.eventLog.dir':
                        # add namenode url if missing
                        if "hdfs://" in ori_config:
                            content = config_updater(content, config_regex='hdfs://.*?/')
                            new_config = True
                        # skip if s3 protocol is used in spark event log dir
                        elif "s3" in ori_config:
                            print_log("s3 destination found in spark event log skip")
                    elif config_name == 'spark.unravel.server.hostport':
                        content = config_updater(content)
                        new_config = True
                    elif re.match("spark.*?.extraJavaOptions", config_name):
                        # modify spark.driver|executor.extraJavaOptions
                        joption_regex = '-javaagent:.*?btrace-agent.jar=config=.*?,libs=.*?[,a-zA-Z\d=-]* -Dunravel.metrics.factor=.*'
                        content = config_updater(content, config_regex=joption_regex)
                        new_config = True
                    else:
                        content = config_updater(content, append=True)
                        new_config = True
                else:
                    # handle in case spark.eventLog.dir is missing
                    if config_name == 'spark.eventLog.dir':
                        config_val = "hdfs:///var/log/spark/apps"
                    self.print_column(config_name, "missing", 80)
                    print_log(config_name + ' missing: \n' + config_val)
                    content += '\n' + config_name + ' ' + config_val
                    new_config = content
                sleep(1)

            if new_config:
                print_log('Updating spark-defaults.conf')
                with open(self.spark_defaults_path, 'w') as f:
                    f.write(content)
                    f.close()
            self.final_status[Components.SPARK_DEFAULTS] = Components.Status.DONE
        except Exception as e:
            print_log(e, log_level='error')
            self.final_status[Components.SPARK_DEFAULTS] = Components.Status.FAIL

    #   Description: Compare and Update tez-site.xml file
    def update_tez_site(self, retry=0):
        try:
            print_log('\nChecking tez-site.xml')
            tez_site_preunravel = self.tez_site_path + '.preunravel'
            # Wait for Tez installation complete
            if 'tez' in self.components and should_wait_for_file(self.tez_site_path, retry, self.args.is_bootstrap):
                self.update_tez_site(retry=retry + 1)
                return None
            elif not os.path.exists(self.tez_site_path):
                print_log('Skip tez-site.xml')
                self.final_status[Components.TEZ_SITE] = Components.Status.SKIP
                return None

            # Backup tez-site.xml
            if not os.path.exists(tez_site_preunravel):
                print_log("Backup original tez-site.xml")
                copyfile(self.tez_site_path, tez_site_preunravel)

            # Compare tez-site.xml properties
            handler = XmlHandler(self.tez_site_path)
            handler.xml_to_dict()
            for config, val_dict in self.configs['tez-site'].iteritems():
                if val_dict['action'] == self.ConfAction.REPLACE:
                    result = handler.replace(config, val_dict['value'])
                else:
                    result = handler.append(config, val_dict['value'], val_dict['regex'], delimiter=val_dict['delimiter'])
                self.print_column(config, result['result'], 80)
                print_log("Suggest config: {0}\nCurrent config: {1}".format(result['origin_val'], result['new_val']),
                          log_only=True)
                sleep(1)
            handler.write(self.tez_site_path)

            self.final_status[Components.TEZ_SITE] = Components.Status.DONE
        except Exception as e:
            print_log(e, log_level='error')
            self.final_status[Components.TEZ_SITE] = Components.Status.FAIL

    #   Description: Compare and Update yarn-site.xml file
    def update_yarn_site(self, retry=0):
        try:
            print("\nChecking yarn-site.xml")
            yarn_site_xml = self.yarn_site_xml
            preunravel_yarn_site = yarn_site_xml + '.preunravel'
            # Wait for Yarn installation complete
            if should_wait_for_file(yarn_site_xml, retry, self.args.is_bootstrap):
                self.update_mapred_site(retry=retry + 1)
                return None
            elif not os.path.exists(yarn_site_xml):
                print_log('Skip yarn-site.xml')
                self.final_status[Components.YARN_SITE] = Components.Status.SKIP
                return None

            # Backup yarn-site.xml
            if not os.path.exists(preunravel_yarn_site):
                print("Backup original yarn-site.xml")
                copyfile(yarn_site_xml, preunravel_yarn_site)

            # Compare yarn-site.xml properties
            handler = XmlHandler(yarn_site_xml)
            handler.xml_to_dict()
            for config, val_dict in self.configs['yarn-site'].iteritems():
                result = handler.replace(config, val_dict['value'])
                self.print_column(config, result['result'], 80)
                print_log("Suggest config: {0}\nCurrent config: {1}".format(result['origin_val'], result['new_val']),
                          log_only=True)
                sleep(1)
            handler.write(yarn_site_xml)

            self.final_status[Components.YARN_SITE] = Components.Status.DONE
        except Exception as e:
            print_log(e, log_level='error')
            print_log('Skip yarn-site.xml')
            self.final_status[Components.YARN_SITE] = Components.Status.FAIL

    def update_sensor_deploy(self):
        sensor_script_path = os.path.join(self.unravel_es_path, 'dbin/sensor_deploy.sh')
        if os.path.exists(sensor_script_path):
            with open(sensor_script_path, 'w') as f:
                content = """cd {0}
wget --no-check-certificate http://$1:3000/hh/unravel-agent-pack-bin.zip -O ./unravel-agent-pack-bin.zip;
unzip -o unravel-agent-pack-bin.zip
cat version.txt""".format(self.spark_sensor_path)
                f.write(content)
                f.close()

    def uninstall(self):
        if self.is_master:
            self.remove_es()
        self.remove_sensor()
        config_files = [self.spark_defaults_path, self.mapred_site_xml, self.hive_site_path,
                        self.tez_site_path, self.yarn_site_xml]
        self.remove_configs(config_files)

    def remove_sensor(self):
        try:
            self.remove_paths({self.spark_sensor_path})
            self.final_status[Components.BTRACE_SENSOR] = Components.Status.REMOVE
        except:
            self.final_status[Components.BTRACE_SENSOR] = Components.Status.SKIP
        try:
            hive_hook_jar = 'unravel-hive-%s.%s.0-hook.jar' % (self.hive_version_xyz[0], self.hive_version_xyz[1])
            self.remove_paths({os.path.join(self.hive_hook_path, hive_hook_jar)})
            self.final_status[Components.HIVE_HOOK] = Components.Status.REMOVE
        except:
            self.final_status[Components.HIVE_HOOK] = Components.Status.SKIP

    def remove_es(self):
        try:
            if os.path.exists(self.unravel_es_path):
                call('sudo service unravel_es stop', shell=True)
                self.remove_paths({self.unravel_es_path})
                self.final_status[Components.UNRAVEL_ES] = Components.Status.REMOVE
        except:
            self.final_status[Components.UNRAVEL_ES] = Components.Status.FAIL
            print_log(traceback.format_exc(), log_level='error')

    def remove_configs(self, config_paths):
        for config_path in config_paths:
            try:
                preunravel_path = config_path + '.preunravel'
                if os.path.exists(preunravel_path):
                    move(preunravel_path, config_path)
                    print_log("Recovering {0} from {1}".format(config_path, preunravel_path))
                    self.final_status[os.path.basename(config_path).upper()] = Components.Status.RESTORE
            except:
                self.final_status[os.path.basename(config_path).upper()] = Components.Status.FAIL
                print_log(traceback.format_exc(), log_level='error')

    @staticmethod
    def get_principal_from_key(keytab_file):
        try:
            return Popen("klist -kt {0}| tail -n 1 | awk '{{print $4}}'".format(keytab_file), shell=True, stdout=PIPE).communicate()[0].strip()
        except:
            return ' '

    def kinit_cmd(self, keytab_file):
        Popen("kinit -kt {0} {1}".format(keytab_file, self.get_principal_from_key(keytab_file)), shell=True).communicate()

    @staticmethod
    def get_cmd_ver(cmd):
        """ Getting version number from hive and spark-submit cli """
        ver = '2.2.0'
        if cmd == 'spark-submit':
            grep_str = r'.*?version\s+\K([0-9.]+)'
        elif cmd == 'hive':
            grep_str = r'Hive \K([0-9]+\.[0-9]+\.[0-9]+)'
        try:
            result = Popen("$(which {0}) --version 2>&1 | grep -Po '{1}'".format(cmd, grep_str), shell=True,
                         stdout=PIPE).communicate()[0].strip().split('\n')[0]
            if len(result) > 1:
                ver = result
        except:
            print_log(traceback.format_exc(), 'error')
            print_log("Failed to get {0} version".format(cmd), 'warn')
        return ver

    def get_emr_ver(self):
        default_ver = "emr-5.30.0"
        if self.instance_data:
            return self.instance_data.get("releaseLabel", default_ver)
        return default_ver

    def get_commands(self):
        emr_ver = self.get_emr_ver()
        for com in self.restart_commands:
            if compare_versions(emr_ver.split("-")[1], com["version"]) >= 0:
                commands = com["commands"]
        return commands

    def get_service_list(self):
        cmd = self.get_commands()
        s_popen = Popen("{} | awk '{{print $1}}'".format(cmd["list"]), shell=True, stdout=PIPE)
        s_list = s_popen.communicate()[0]
        if s_popen.returncode == 0:
            return s_list
        else:
            print_log("Failed to get list of services")
            return ""

    def restart_hiveserver2(self):
        try:
            service_name = "hive-server2"
            cmd = self.get_commands()
            if service_name not in self.get_service_list():
                print_log("{} not in service list skip service restart".format(service_name))
                self.final_status[Components.HIVESERVER2_RESTART] = Components.Status.SKIP
                return
            print_log("Restarting {}".format(service_name))
            stop_res = call("{} {}".format(cmd["stop"], service_name), shell=True)
            start_res = call("{} {}".format(cmd["start"], service_name), shell=True)
            print_log("{} stop start: {} {}".format(service_name, stop_res, start_res))
            self.final_status[Components.HIVESERVER2_RESTART] = Components.Status.SUCCESS
        except Exception as e:
            pass
        return


def compare_versions(version1, version2):
    """
    :param version1: string of version number
    :type version1: str
    :param version2: string of version number
    :type version2: str
    :return: int 1: v1 > v2 0: v1 == v2 -1 v1 < v2
    """
    result = 0
    version1_list = version1.split('.')
    version2_list = version2.split('.')
    max_version = max(len(version1_list), len(version2_list))
    for index in range(max_version):
        v1_digit = int(version1_list[index]) if len(version1_list) > index else 0
        v2_digit = int(version2_list[index]) if len(version2_list) > index else 0
        if v1_digit > v2_digit:
            return 1
        elif v1_digit < v2_digit:
            return -1
        elif version1_list == version2_list:
            pass
    return result


def should_wait_for_file(file_path, retry, is_bootstrap,retry_max=max_retry):
    """
    :param file_path: string file we need to wait to show up
    :param retry: int retry count
    :param retry_max: int maximum retries
    :param is_bootstrap: whether the it's bootstrap mode
    :return: boolean True: file not exists should wait, False: file exists no need to wait
    """
    if retry < retry_max and is_bootstrap and not os.path.exists(file_path):
        print_log('Waiting for %s %i s, retry %i' % (os.path.basename(file_path), sleep_time, retry))
        sleep(sleep_time)
        return True
    else:
        return False


#   Current node is master or slave node
def check_master():
    try:
        instance_json = json.loads(open('/mnt/var/lib/info/instance.json').read())
        return instance_json['isMaster']
    except IOError:
        print_log("/mnt/var/lib/info/instance.json file not found", "warn")
    except Exception as e:
        print_log(e.message, "error")
    return False


def check_root():
    if os.geteuid() == 0:
        return True
    return False


def print_log(log_content, log_level='info', log_only=False):
    global LOGGER
    if not log_only:
        print(log_content)
    try:
        if log_level == 'error':
            LOGGER.error(log_content)
        elif log_level == 'debug':
            LOGGER.debug(log_content)
        elif log_level == 'warn':
            LOGGER.warn(log_content)
        else:
            LOGGER.info(log_content)
    except NameError:
        pass


# Initial Idle time for EMR Components Installation
def wait_for_installation():
    spark_sensor_path = '/usr/local/unravel-agent/'
    hive_site_path = '/etc/hive/conf/hive-site.xml'
    hadoop_path = '/etc/hadoop/conf/core-site.xml'
    if not (os.path.exists(spark_sensor_path) or os.path.exists(hive_site_path) or os.path.exists(hadoop_path)):
        print_log('Waiting for Installation complete, wait %i s' % init_wait)
        sleep(init_wait)
    else:
        print_log('Ready to setup Unravel, wait %i' % sleep_time)
        sleep(sleep_time)


def filter_arg(arg_name):
    if arg_name == '--bootstrap':
        return False
    return True


def check_hdfs_cmd():
    hdfs_ver_cmd = "hdfs version"
    hdfs_popen = Popen(hdfs_ver_cmd, stdout=PIPE, stderr=PIPE, shell=True)
    hdfs_popen.communicate()
    if hdfs_popen.returncode == 0 and os.path.exists('/etc/hadoop/conf/hdfs-site.xml'):
        return True
    print_log("{} command return {}".format(hdfs_ver_cmd, hdfs_popen.returncode), log_level='warn')
    return False


def main():
    print_log(script_ver)
    if check_root():
        if ARGV.edge_node:
            print_log("Master: False")
            print_log("Edge Node: True")
            emr_setup = EmrSetup(ARGV)
            if ARGV.uninstall:
                emr_setup.uninstall()
            else:
                emr_setup.install_sensors_configs()
        elif check_master():
            print_log("Master: True")
            if ARGV.is_bootstrap:
                wait_for_installation()
            emr_setup = EmrSetup(ARGV)
            print_log("cluster-id: {0}".format(emr_setup.cluster_id))
            print_log("namenode HA: {0}".format(emr_setup.check_nn_ha()))
            if ARGV.uninstall:
                emr_setup.uninstall()
            else:
                if emr_setup.check_kerberos():
                    print_log("Kerberos: True")
                    emr_setup.kinit_cmd(emr_setup.args.keytab_file)
                else:
                    print_log("Kerberos: False")
                emr_setup.install_sensors_configs()
                emr_setup.install_es()
        else:
            print_log("Master: False")
            emr_setup = EmrSetup(ARGV)
            if ARGV.uninstall:
                emr_setup.remove_sensor()
            else:
                retry = 0
                # Wait for hdfs command installed in worker nodes
                while max_retry >= retry:
                    if check_hdfs_cmd():
                        if emr_setup.check_kerberos():
                            emr_setup.kinit_cmd(emr_setup.args.keytab_file)
                        emr_setup.install_spark_sensor()
                        if Components.Status.DONE in emr_setup.final_status.values():
                            break
                    print_log("Download Spark Sensor failed retry {0}".format(retry), log_level="warn")
                    retry += 1
                    sleep(30)
        print_log('*************************Final Results*************************')
        for item, result in emr_setup.final_status.iteritems():
            print_log(item + ': ' + result)
    else:
        print_log("{0} is not running as root, running the script with sudo".format(sys.argv[0]))
        print(' '.join(sys.argv))
        call('sudo python {0}'.format(' '.join(sys.argv)), shell=True)


if __name__ == '__main__':
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir + '/tmp')
    LOGGER = logging.getLogger('unravel_emr_bootstrap')
    LOGGER.setLevel(logging.DEBUG)
    LOGFILE = tmp_dir + '/unravel_emr_bootstrap.log'
    FILEHANDLER = logging.FileHandler(LOGFILE)
    LOGFORMAT = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
    FILEHANDLER.setFormatter(LOGFORMAT)
    LOGGER.addHandler(FILEHANDLER)
    ARGV = get_args()
    ARGV = args_checker(ARGV)

    if ARGV.bootstrap:
        print_log('Going in the background')
        call('sudo nohup python ' + ' '.join(filter(filter_arg, sys.argv)) + ' --is_bootstrap &', shell=True)
        sleep(5)
    else:
        main()