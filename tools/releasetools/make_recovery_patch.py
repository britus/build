#!/usr/bin/env python
#
# Copyright (C) 2014 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

if sys.hexversion < 0x02070000:
  print >> sys.stderr, "Python 2.7 or newer is required."
  sys.exit(1)

import os
import common
import shutil

OPTIONS = common.OPTIONS

def main(argv):
  # def option_handler(o, a):
  #   return False

  args = common.ParseOptions(argv, __doc__)
  input_dir, output_dir = args

  OPTIONS.info_dict = common.LoadInfoDict(input_dir)

  recovery_img = common.GetBootableImage("recovery.img", "recovery.img",
                                         input_dir, "RECOVERY")
  boot_img = common.GetBootableImage("boot.img", "boot.img",
                                     input_dir, "BOOT")

  if not recovery_img or not boot_img:
    sys.exit(0)

  def output_sink(fn, data):
    with open(os.path.join(output_dir, "SYSTEM", *fn.split("/")), "wb") as f:
      f.write(data)

  common.MakeRecoveryPatch(input_dir, output_sink, recovery_img, boot_img)

def copy_patch_sh(argv):
  # description: copy recovery-from-boot.p and install-recovery.sh
  out_dir_path = argv[1]
  pre_path_list = out_dir_path.split("obj")
  pre_path = pre_path_list[0]

  patch_src = os.path.join(out_dir_path,"SYSTEM/recovery-from-boot.p")
  patch_dst = os.path.join(pre_path,"system/recovery-from-boot.p")

  sh_src = os.path.join(out_dir_path,"SYSTEM/bin/install-recovery.sh")
  sh_dst = os.path.join(pre_path,"system/bin/install-recovery.sh")

  shutil.copyfile(patch_src,patch_dst)
  shutil.copyfile(sh_src,sh_dst)
if __name__ == '__main__':
  main(sys.argv[1:])
  copy_patch_sh(sys.argv[1:])