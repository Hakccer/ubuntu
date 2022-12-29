import time
import os
from zapv2 import ZAPv2
import requests
import json
import threading


class ZAPCrawler:
    def __init__(self, target, api_key, scan_id=None) -> None:
        self.is_destroyed = False
        self.running = 0
        self._api_key = api_key
        self.__current_zap = ZAPv2(apikey=api_key)
        self.__target = target
        self.max_childs = 0
        self.results = []
        self.max_depth = 0
        self.scan_id = scan_id

    def start_scan(self, new_target=None) -> str:
        if not self.scan_id:
            if not new_target:
                self.scan_id = self.__current_zap.spider.scan(self.__target)
            else:
                self.scan_id = self.__current_zap.spider.scan(new_target)
            self.running = 1
            print("Scan Started Successfully")
        else:
            print("Scan is Already Tracked")

    def get_scan_percentage(self, scan_id=None) -> int | str:
        if not scan_id:
            try:
                return int(self.__current_zap.spider.status(self.scan_id))
            except Exception as e:
                return "Please Start a scan first"
        try:
            return int(self.__current_zap.spider.status(scan_id))
        except Exception as e:
            return "No Scans Found wit this ID"

    def get_reuslts(self, scan_id=None):
        if not scan_id:
            try:
                col_scan = self.scan_id
                defo = 0
            except Exception as e:
                return "Error: <NO Scans Found with that ID>"
        else:
            col_scan = scan_id
            defo = 1
        try:
            latest_data = list(set(list(self.results + self.__current_zap.spider.results(col_scan))))
            new_url_founded = len(latest_data) - len(self.results)
            self.results = latest_data
            totals = len(self.results)
            for index in range(1, len(self.results) + 1):
                print(index, self.results[index - 1])
            print("Total Domains founded are:", totals)
            print("New Urls Founded are:", new_url_founded)
        except Exception as e:
            print("Error: <The First step is to intialize a scan than you can track it with (SCAN-ID)>")

    def pause_scan(self, scan_id=None):
        if not scan_id:
            try:
                col_scan = self.scan_id
            except Exception as e:
                return "Error: <No Scans Found with that id>"
        else:
            col_scan = scan_id
        try:
            print(self.__current_zap.spider.status(col_scan))
            self.__current_zap.spider.pause(col_scan)
        except Exception as e:
            error = "Error: <No Scans initiated>"
            print(error)
            return error

    def resume_scan(self, scan_id=None):
        try:
            print(self.__current_zap.spider.status(self.scan_id))
            self.__current_zap.spider.resume(self.scan_id)
            self.running = 1
        except Exception as e:
            error = "Error: <No Scans initiated>"
            print(error)
            return error

    def stop_scan(self):
        try:
            self.__current_zap.spider.stop(self.scan_id)
            self.running = 0
            self.is_destroyed = True
        except Exception as e:
            error = "Error: <No Scans Found with that ID>"
            print(error)
            return error

    # Optional and advance Parameters for the user to set
    def set_max_depth(self, new_depth):
        try:
            if int(new_depth) != self.max_depth:
                self.__current_zap.spider.set_option_max_depth(int(new_depth))
                self.max_depth = new_depth
        except Exception as e:
            return e

    def get_max_depth(self):
        return self.max_depth

    # Optional and advance Paramerters for the user to set
    def set_max_child_nodes(self, child_nodes):
        try:
            if int(child_nodes) != self.max_childs:
                self.__current_zap.spider.set_option_max_children(int(child_nodes))
                self.max_childs = int(child_nodes)
        except Exception as e:
            return e


def locs():
    while True:
        if z1.running == 1:
            print("Waiting for some results to come...")
            time.sleep(7)
            z1.get_reuslts()
        else:
            print("Scan is now not running exiting thread...")
            break


# locs()

if __name__ == '__main__':
    z1 = ZAPCrawler('https://iitk.ac.in', api_key='c3u2te4df0uomkt570je4pqeqk')
    new = threading.Thread(target=locs)
    while True:
        task = str(input(
            "Enter the process key you want -> \ns - (start scan)\np - (get status of scan)\nru - (resume scan)\nst - (stop scan)\npa - (pause scan)\nenter the key here -> "))
        if task.lower() == 's':
            if z1.running == 0:
                print("Starting Scan...")
                z1.start_scan()
                new.start()
            else:
                print("Scan is Aready Running...")
        elif task.lower() == 'pa':
            if z1.running == 1:
                z1.pause_scan()
                new.join()
            else:
                print("Scan is Already Paused")
        elif task.lower() == 'ru':
            if z1.results == 0:
                z1.resume_scan()
            else:
                print("Scan is already in resume state...")
        elif task.lower() == 'st':
            if not z1.is_destroyed():
                z1.stop_scan()
            else:
                print("Scan is Already stopped...")
        elif task.lower() == 'p':
            if z1.running == 1:
                print("Scan Percentage: ", z1.get_scan_percentage())
            else:
                print("No Scan in running state")
