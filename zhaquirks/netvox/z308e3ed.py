"""Netvox device."""
import zigpy.types as t
from zigpy.profiles import zha
from zigpy.quirks import CustomDevice, CustomCluster
from zigpy.zcl.clusters.general import (
    Basic, Commissioning, Identify, PollControl)
from zigpy.zcl.clusters.security import IasZone

from zhaquirks.centralite import PowerConfigurationCluster

DIAGNOSTICS_CLUSTER_ID = 0x0B05  # decimal = 2821


class IASZoneCluster(CustomCluster, IasZone):
    """Centralite acceleration cluster."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        self.client_commands.update({
            0x0000: (
                'status_change_notification',
                (t.bitmap16, t.bitmap8),
                False
            ),
        })


class Z308E3ED(CustomDevice):
    """Netvox Z308E3ED."""

    signature = {
        #  <SimpleDescriptor endpoint=1 profile=260 device_type=1026
        #  device_version=0
        #  input_clusters=[0, 1, 3, 21, 1280, 32, 2821]
        #  output_clusters=[]>
        'endpoints': {
            1: {
                'profile_id': zha.PROFILE_ID,
                'device_type': zha.DeviceType.IAS_ZONE,
                'input_clusters': [
                    Basic.cluster_id,
                    PowerConfigurationCluster.cluster_id,
                    Identify.cluster_id,
                    PollControl.cluster_id,
                    IasZone.cluster_id,
                    Commissioning.cluster_id,
                    DIAGNOSTICS_CLUSTER_ID
                ],
                'output_clusters': [
                ],
            }
        }
    }

    replacement = {
        'endpoints': {
            1: {
                'input_clusters': [
                    Basic.cluster_id,
                    PowerConfigurationCluster,
                    Identify.cluster_id,
                    PollControl.cluster_id,
                    IASZoneCluster,
                    Commissioning.cluster_id,
                    DIAGNOSTICS_CLUSTER_ID
                ]
            }
        },
    }
