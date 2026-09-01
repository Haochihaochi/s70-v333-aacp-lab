# Safety policy

This project concerns an embedded system integrated with a motor vehicle. Treat an infotainment failure as potentially distracting even when it does not directly control steering or braking.

## Required operating rules

- Develop and profile on a bench unit where possible.
- In-car work must be performed while safely parked, with no driving activity.
- Maintain stable power during any authorized installation or update operation.
- Confirm that reverse camera, 360 camera, parking warnings and factory controls work before moving the vehicle.
- Stop immediately if the IHU repeatedly reboots, overheats, loses camera functions or produces abnormal warning behaviour.

## Prohibited repository content

- Proprietary firmware images or partition dumps.
- Vendor signing keys, debug certificates or credentials.
- VINs, serial numbers, IMEIs, MAC addresses or personal logs.
- Paid installer packages copied without permission.
- Remote-service bypasses or credential attacks.
- CAN injection intended to alter safety-critical vehicle behaviour.

## Flashing policy

The foundation does not provide bootloader unlock, partition flashing or verified-boot bypass instructions. A contributor proposing any write to `boot`, `vendor`, `system`, `super`, `recovery`, `vbmeta` or bootloader storage must first provide a documented and tested recovery design for the exact IHU hardware revision.
