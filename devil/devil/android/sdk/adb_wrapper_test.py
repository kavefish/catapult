#!/usr/bin/env python
# Copyright 2017 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""
Unit tests for some APIs with conditional logic in adb_wrapper.py
"""

import unittest

from devil import devil_env
from devil.android import device_errors
from devil.android.sdk import adb_wrapper

with devil_env.SysPath(devil_env.PYMOCK_PATH):
  import mock  # pylint: disable=import-error


def MockRunDeviceAdbCmd(adb, return_value):
  return mock.patch.object(
    adb,
    '_RunDeviceAdbCmd',
    mock.Mock(side_effect=None, return_value=return_value))


class AdbWrapperTest(unittest.TestCase):
  def setUp(self):
    self.adb_wrappers = [
      adb_wrapper.AdbWrapper('ABC12345678'),
      adb_wrapper.AdbWrapper('usb:1-2.3'),
    ]

  def testDisableVerityWhenDisabled(self):
    return_value = 'Verity already disabled on /system'
    for adb in self.adb_wrappers:
      with MockRunDeviceAdbCmd(adb, return_value):
        adb.DisableVerity()

  def testDisableVerityWhenEnabled(self):
    return_value = 'Verity disabled on /system\nNow reboot your device for ' \
                   'settings to take effect'
    for adb in self.adb_wrappers:
      with MockRunDeviceAdbCmd(adb, return_value):
        adb.DisableVerity()

  def testEnableVerityWhenEnabled(self):
    return_value = 'Verity already enabled on /system'
    for adb in self.adb_wrappers:
      with MockRunDeviceAdbCmd(adb, return_value):
        adb.EnableVerity()

  def testEnableVerityWhenDisabled(self):
    return_value = 'Verity enabled on /system\nNow reboot your device for ' \
               'settings to take effect'
    for adb in self.adb_wrappers:
      with MockRunDeviceAdbCmd(adb, return_value):
        adb.EnableVerity()

  def testFailEnableVerity(self):
    return_value = 'error: closed'
    for adb in self.adb_wrappers:
      with MockRunDeviceAdbCmd(adb, return_value):
        self.assertRaises(device_errors.AdbCommandFailedError, adb.EnableVerity)

  def testFailDisableVerity(self):
    return_value = 'error: closed'
    for adb in self.adb_wrappers:
      with MockRunDeviceAdbCmd(adb, return_value):
        self.assertRaises(device_errors.AdbCommandFailedError,
                          adb.DisableVerity)

  def testGetStateOnline(self):
    return_value = 'device'
    for adb in self.adb_wrappers:
      with MockRunDeviceAdbCmd(adb, return_value):
        adb.GetState()

  def testGetStateOffline(self):
    return_value = 'offline'
    for adb in self.adb_wrappers:
      with MockRunDeviceAdbCmd(adb, return_value):
        adb.GetState()

  def testGetStateUnauthorized(self):
    return_value = 'unauthorized'
    for adb in self.adb_wrappers:
      with MockRunDeviceAdbCmd(adb, return_value):
        adb.GetState()

  def testGetStateBootloader(self):
    return_value = 'bootloader'
    for adb in self.adb_wrappers:
      with MockRunDeviceAdbCmd(adb, return_value):
        adb.GetState()

  def testGetStateNoPermissions(self):
    return_value = 'no' # as in 'no permissions'
    for adb in self.adb_wrappers:
      with MockRunDeviceAdbCmd(adb, return_value):
        adb.GetState()


if __name__ == '__main__':
  unittest.main()
