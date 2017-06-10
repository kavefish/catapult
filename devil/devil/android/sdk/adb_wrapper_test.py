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


class AdbWrapperTest(unittest.TestCase):
  def setUp(self):
    self.adb_wrappers = [
      adb_wrapper.AdbWrapper('ABC12345678'),
      adb_wrapper.AdbWrapper('usb:1-2.3'),
    ]

  def _MockRunDeviceAdbCmd(self, adb, return_value):
    return mock.patch.object(
        adb,
        '_RunDeviceAdbCmd',
        mock.Mock(side_effect=None, return_value=return_value))

  def _MockRawDevices(self, adb, return_value):
    return mock.patch.object(
        adb,
        '_RawDevices',
        mock.Mock(side_effect=None, return_value=return_value))

  def testDisableVerityWhenDisabled(self):
    return_value = 'Verity already disabled on /system'
    for adb in self.adb_wrappers:
        with self._MockRunDeviceAdbCmd(adb, return_value):
          adb.DisableVerity()

  def testDisableVerityWhenEnabled(self):
    return_value ='Verity disabled on /system\nNow reboot your device for settings to take effect'
    for adb in self.adb_wrappers:
      with self._MockRunDeviceAdbCmd(adb, return_value):
        adb.DisableVerity()

  def testEnableVerityWhenEnabled(self):
    return_value = 'Verity already enabled on /system'
    for adb in self.adb_wrappers:
      with self._MockRunDeviceAdbCmd(adb, return_value):
        adb.EnableVerity()

  def testEnableVerityWhenDisabled(self):
    return_value = 'Verity enabled on /system\nNow reboot your device for ' \
                   'settings to take effect'
    for adb in self.adb_wrappers:
      with self._MockRunDeviceAdbCmd(adb, return_value):
        adb.EnableVerity()

  def testFailEnableVerity(self):
    return_value = 'error: closed'
    for adb in self.adb_wrappers:
      with self._MockRunDeviceAdbCmd(adb, return_value):
        self.assertRaises(
          device_errors.AdbCommandFailedError, adb.EnableVerity)

  def testFailDisableVerity(self):
    return_value = 'error: closed'
    for adb in self.adb_wrappers:
      with self._MockRunDeviceAdbCmd(adb, return_value):
        self.assertRaises(
          device_errors.AdbCommandFailedError, adb.DisableVerity)

  def testGetStateEmpty(self):
    return_value = [[]]
    for adb in self.adb_wrappers:
      with self._MockRawDevices(adb, return_value):
        self.assertEqual(adb.GetState(), 'offline')

  def testGetStateNoPermissions(self):
    return_value = [['PLACEHOLDER', 'no', 'permissions',
                     '(udev', 'requires', 'plugdev', 'group', 'membership);',
                     'see',
                     '[http://developer.android.com/tools/device.html]',
                     'usb:1-2.3'], []]
    for adb in self.adb_wrappers:
      # overwrite placeholder
      return_value[0][0] = adb.GetDeviceSerial()
      with self._MockRawDevices(adb, return_value):
        self.assertEqual(adb.GetState(), 'no')

  def testGetStateUnauthorized(self):
    return_value = [['PLACEHOLDER', 'unauthorized', 'usb:1-2.3'], []]
    for adb in self.adb_wrappers:
      # overwrite placeholder
      return_value[0][0] = adb.GetDeviceSerial()
      with self._MockRawDevices(adb, return_value):
        self.assertEqual(adb.GetState(), 'unauthorized')

  def testGetStateOffline(self):
    return_value = [['PLACEHOLDER', 'offline', 'usb:1-2.3'], []]
    for adb in self.adb_wrappers:
      # overwrite placeholder
      return_value[0][0] = adb.GetDeviceSerial()
      with self._MockRawDevices(adb, return_value):
        self.assertEqual(adb.GetState(), 'offline')

  def testGetStateOnline(self):
    return_value = [['PLACEHOLDER', 'device', 'usb:1-2.3',
                       'product:bullhead', 'model:Nexus_5X',
                       'device:bullhead'], []]
    for adb in self.adb_wrappers:
      # overwrite placeholder
      return_value[0][0] = adb.GetDeviceSerial()
      with self._MockRawDevices(adb, return_value):
        self.assertEqual(adb.GetState(), 'device')


if __name__ == '__main__':
  unittest.main()
