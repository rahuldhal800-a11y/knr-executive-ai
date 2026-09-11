"""Consent-based device capability broker.

AEGIS works with explicitly registered device adapters and narrowly scoped
capabilities provisioned by the device owner. Arbitrary remote access is not
part of this module.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Set

@dataclass
class Device:
    device_id: str
    owner: str
    capabilities: Set[str] = field(default_factory=set)
    online: bool = False

class DeviceRegistry:
    def __init__(self) -> None:
        self._devices: Dict[str, Device] = {}

    def register(self, device_id: str, owner: str, capabilities: List[str]) -> Device:
        device = Device(device_id, owner, set(capabilities))
        self._devices[device_id] = device
        return device

    def list_devices(self) -> List[Dict]:
        return [{"device_id": d.device_id, "owner": d.owner, "capabilities": sorted(d.capabilities), "online": d.online} for d in self._devices.values()]

    def require_authorized(self, device_id: str, capability: str) -> None:
        device = self._devices.get(device_id)
        if not device or not device.online or capability not in device.capabilities:
            raise PermissionError(f"Capability '{capability}' is not authorized for '{device_id}'.")
