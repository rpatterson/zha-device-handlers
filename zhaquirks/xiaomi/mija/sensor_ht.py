"""Xiaomi mija weather sensor device."""
import logging

from zigpy import quirks
from zigpy.profiles import zha
from zigpy.quirks.xiaomi import TemperatureHumiditySensor
from zigpy.zcl.clusters.general import (
    AnalogInput,
    Groups,
    Identify,
    MultistateInput,
    Ota,
    Scenes,
)
from zigpy.zcl.clusters.measurement import RelativeHumidity

from .. import (
    LUMI,
    BasicCluster,
    PowerConfigurationCluster,
    TemperatureMeasurementCluster,
    XiaomiCustomDevice,
)
from ...const import (
    DEVICE_TYPE,
    ENDPOINTS,
    INPUT_CLUSTERS,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PROFILE_ID,
)

TEMPERATURE_HUMIDITY_DEVICE_TYPE = 0x5F01
TEMPERATURE_HUMIDITY_DEVICE_TYPE2 = 0x5F02
TEMPERATURE_HUMIDITY_DEVICE_TYPE3 = 0x5F03
XIAOMI_CLUSTER_ID = 0xFFFF

_LOGGER = logging.getLogger(__name__)

#  remove the zigpy version of this device handler
if TemperatureHumiditySensor in quirks._DEVICE_REGISTRY:
    quirks._DEVICE_REGISTRY.remove(TemperatureHumiditySensor)


class Weather(XiaomiCustomDevice):
    """Xiaomi mija weather sensor device."""

    signature = {
        #  <SimpleDescriptor endpoint=1 profile=260 device_type=24321
        #  device_version=1
        #  input_clusters=[0, 3, 25, 65535, 18]
        #  output_clusters=[0, 4, 3, 5, 25, 65535, 18]>
        MODELS_INFO: [(LUMI, "lumi.sensor_ht"), (LUMI, "lumi.sens")],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: TEMPERATURE_HUMIDITY_DEVICE_TYPE,
                INPUT_CLUSTERS: [
                    BasicCluster.cluster_id,
                    Identify.cluster_id,
                    XIAOMI_CLUSTER_ID,
                    Ota.cluster_id,
                    MultistateInput.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    BasicCluster.cluster_id,
                    Groups.cluster_id,
                    Identify.cluster_id,
                    Scenes.cluster_id,
                    Ota.cluster_id,
                    XIAOMI_CLUSTER_ID,
                    MultistateInput.cluster_id,
                ],
            },
            # <SimpleDescriptor endpoint=2 profile=260 device_type=24322
            #  device_version=1
            #  input_clusters=[3, 18]
            #  output_clusters=[4, 3, 5, 18]>
            2: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: TEMPERATURE_HUMIDITY_DEVICE_TYPE2,
                INPUT_CLUSTERS: [Identify.cluster_id, MultistateInput.cluster_id],
                OUTPUT_CLUSTERS: [
                    Groups.cluster_id,
                    Identify.cluster_id,
                    Scenes.cluster_id,
                    MultistateInput.cluster_id,
                ],
            },
            # <SimpleDescriptor endpoint=3 profile=260 device_type=24323
            # device_version=1
            # input_clusters=[3, 12]
            # output_clusters=[4, 3, 5, 12]>
            3: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: TEMPERATURE_HUMIDITY_DEVICE_TYPE3,
                INPUT_CLUSTERS: [Identify.cluster_id, AnalogInput.cluster_id],
                OUTPUT_CLUSTERS: [
                    Groups.cluster_id,
                    Identify.cluster_id,
                    Scenes.cluster_id,
                    AnalogInput.cluster_id,
                ],
            },
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                DEVICE_TYPE: TEMPERATURE_HUMIDITY_DEVICE_TYPE2,
                INPUT_CLUSTERS: [
                    BasicCluster,
                    PowerConfigurationCluster,
                    Identify.cluster_id,
                    TemperatureMeasurementCluster,
                    RelativeHumidity.cluster_id,
                    XIAOMI_CLUSTER_ID,
                    Ota.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    BasicCluster.cluster_id,
                    Groups.cluster_id,
                    Identify.cluster_id,
                    Scenes.cluster_id,
                    Ota.cluster_id,
                    XIAOMI_CLUSTER_ID,
                    MultistateInput.cluster_id,
                ],
            },
            2: {
                DEVICE_TYPE: TEMPERATURE_HUMIDITY_DEVICE_TYPE2,
                INPUT_CLUSTERS: [Identify.cluster_id],
                OUTPUT_CLUSTERS: [
                    Groups.cluster_id,
                    Identify.cluster_id,
                    Scenes.cluster_id,
                    MultistateInput.cluster_id,
                ],
            },
            # <SimpleDescriptor endpoint=3 profile=260 device_type=24323
            # device_version=1
            # input_clusters=[3, 12]
            # output_clusters=[4, 3, 5, 12]>
            3: {
                DEVICE_TYPE: TEMPERATURE_HUMIDITY_DEVICE_TYPE3,
                INPUT_CLUSTERS: [Identify.cluster_id],
                OUTPUT_CLUSTERS: [
                    Groups.cluster_id,
                    Identify.cluster_id,
                    Scenes.cluster_id,
                    AnalogInput.cluster_id,
                ],
            },
        }
    }
