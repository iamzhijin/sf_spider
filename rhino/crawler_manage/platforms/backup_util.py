#coding=utf-8

# Author: Ron Lin
# Date: 2017/9/26
# Email: hdsmtiger@gmail.com

from rhino import settings


class BackupUtil:
    backup_server_host = settings.BACKUP_SERVER_SSH_HOST
    backup_server_port = settings.BACKUP_SERVER_SSH_PORT
    backup_server_username = settings.BACKUP_SERVER_SSH_USERNAME
    backup_server_password = settings.BACKUP_SERVER_SSH_PASSWORD

    def start_backup(self, task):

        pass

    def stop_backup(self, task):
        pass
