import argparse
import paramiko
import os
# from shashank.constants import *
import json_test


hosts = {
      "host3": {
         "IP": "1.1.1.0",
         "user": "admin",
         "password": "admin@123"
      },
      "host2": {
         "IP": "1.1.1.1",
         "user": "admin",
         "password": "admin@123"
      },
      "host1": {
         "IP": "1.1.1.2",
         "user": "admin",
         "password": "admin@123"
      },
      "host4": {
         "IP": "1.1.1.3",
         "user": "admin",
         "password": "admin@123"
      }
}






# def read_json(resource_file_path):
#     with open(resource_file_path) as f:
#         data = json.load(f)
#         return data
#
# def write_jason(resource_file_path, data):
#     with open(resource_file_path) as outfile:
#         json.dump(data, outfile)

resource_pool=['host1', 'host2', 'host2']
usage_data = {"host1":None, "Host2":None, "Host3":None}

deleted_server = None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", help="hostname/IP")
    parser.add_argument("--checkin", help="return server")
    parser.add_argument("--checkout", help="request server")
    parser.add_argument("--list", help='lists available servers')
    parser.add_argument("--user", required=True, help="user who request server")
    args=parser.parse_args()

    if not args.checkin and not args.checkout:
        return

    if args.checkin:
        print("zzzzzzz")
        check_in(args.server, args.user)
    elif args.checkout:
        check_out(args.user)


def check_out(user):
    if len(resource_pool) == 0:
        print('there are no resource available')
        return
    print(resource_pool[0])
    global deleted_server
    deleted_server = resource_pool.pop(0)
    usage_data.update(deleted_server=user)
    print(deleted_server)


def check_in(server, user):
    print("server is {}".format(server))
    print("user is {}".format(user))
    for key, value in usage_data.items():
        print(f"xxx1 : {key}", f"val1 : {value}")
        if key == server and value == user:
            resource_pool.append(server)
            usage_data.update(server = None)
            clean_up(server)
        else:
            print("you are not the owner of the server")
            return


def clean_up(server):
    client = paramiko.SSHClient()
    for key, value in hosts.items():
        print(f"xxx1 : {key}", f"val1 : {value}")
        if key == server:
            try:
                client.connect(hostname=value["ip"], username=value["user"], password=value['password'])
            except:
                print("[!] Cannot connect to the SSH Server")
                exit()

    ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command("rm -rf /tmp")
    print(ssh_stderr, ssh_stdin, ssh_stdout)


if __name__ == '__main__':
    main()










