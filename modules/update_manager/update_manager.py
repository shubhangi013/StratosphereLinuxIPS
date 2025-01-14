from slips_files.common.abstracts import Module
import multiprocessing
from slips_files.core.database.database import __database__
from slips_files.common.slips_utils import utils
from slips_files.common.config_parser import ConfigParser
import sys
import traceback
import asyncio
from exclusiveprocess import Lock, CannotAcquireLock
from modules.update_manager.timer_manager import InfiniteTimer
from modules.update_manager.update_file_manager import UpdateFileManager


class UpdateManager(Module, multiprocessing.Process):
    # Name: short name of the module. Do not use spaces
    name = 'Update Manager'
    description = 'Update Threat Intelligence files'
    authors = ['Kamila Babayeva', 'Alya Gomaa']

    def __init__(self, outputqueue, redis_port):
        multiprocessing.Process.__init__(self)
        super().__init__(outputqueue)
        # All the printing output should be sent to the outputqueue.
        # The outputqueue is connected to another process called OutputProcess
        self.outputqueue = outputqueue
        self.read_configuration()
        # Start the DB
        self.redis_port = redis_port
        __database__.start(self.redis_port)
        # Update file manager
        self.update_manager = UpdateFileManager(
            self.outputqueue, redis_port
        )
        # Timer to update the ThreatIntelligence files
        self.timer_manager = InfiniteTimer(
            self.update_period, self.update_ti_files
        )
        # Timer to update the MAC db
        # when update_ti_files is called, it decides what exactly to update, the mac db,
        # online whitelist OT online ti files.
        self.mac_db_update_manager = InfiniteTimer(
            self.mac_db_update_period, self.update_ti_files
        )
        self.online_whitelist_update_timer = InfiniteTimer(
            self.online_whitelist_update_period, self.update_ti_files
        )

    def read_configuration(self):
        conf = ConfigParser()
        self.update_period = conf.update_period()
        self.mac_db_update_period = conf.mac_db_update_period()
        self.online_whitelist_update_period = conf.online_whitelist_update_period()

    def shutdown_gracefully(self):
        # terminating the timer for the process to be killed
        self.timer_manager.cancel()
        self.mac_db_update_manager.cancel()
        self.online_whitelist_update_timer.cancel()
        # Confirm that the module is done processing
        __database__.publish('finished_modules', self.name)
        return True

    async def update_ti_files(self):
        """
        Update TI files and store them in database before slips starts
        """
        # create_task is used to run update() function concurrently instead of serially
        update_finished = asyncio.create_task(self.update_manager.update())
        # wait for UpdateFileManager to finish before starting all the modules
        await update_finished
        self.print(f'{__database__.get_loaded_ti_files()} TI files successfully loaded.')

    def pre_main(self):
        utils.drop_root_privs()
        try:
            # only one instance of slips should be able to update TI files at a time
            # so this function will only be allowed to run from 1 slips instance.
            with Lock(name="slips_macdb_and_whitelist_and_TI_files_update"):
                asyncio.run(self.update_ti_files())
                # Starting timer to update files
                self.timer_manager.start()
                self.mac_db_update_manager.start()
                self.online_whitelist_update_timer.start()
        except CannotAcquireLock:
            # another instance of slips is updating TI files, tranco whitelists and mac db
            return 1

    def main(self):
        pass

