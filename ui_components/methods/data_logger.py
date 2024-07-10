import json
import streamlit as st
import time
from shared.constants import InferenceParamType, InferenceStatus
from shared.logging.constants import LoggingPayload, LoggingType
from utils.common_utils import get_current_user_uuid
from utils.data_repo.data_repo import DataRepo

from utils.ml_processor.constants import ML_MODEL, MLModel


def log_model_inference(model: MLModel, time_taken, **kwargs):
    kwargs_dict = dict(kwargs)

    # removing object like bufferedreader, image_obj ..
    for key, value in dict(kwargs_dict).items():
        if not isinstance(value, (int, str, list, dict)):
            del kwargs_dict[key]

    data_str = json.dumps(kwargs_dict)
    origin_data = kwargs_dict.get(InferenceParamType.ORIGIN_DATA.value, {})
    time_taken = round(time_taken, 2) if time_taken else 0

    # system_logger = AppLogger()
    # logging_payload = LoggingPayload(message="logging inference data", data=data)

    # # logging in console
    # system_logger.log(LoggingType.INFERENCE_CALL, logging_payload)

    # storing the log in db
    data_repo = DataRepo()
    user_id = get_current_user_uuid()
    ai_model = data_repo.get_ai_model_from_name(model.name, user_id)

    # TODO: fix this - we were initially storing all the models and their versions in the database but later moved on from it
    # so earlier models are found when fetching ai_model but for the new models we are adding this hack for adding dummy model_id
    # hackish sol for insuring that inpainting logs don't have an empty model field
    if ai_model is None and model.name in [
        ML_MODEL.sdxl_inpainting.name,
        ML_MODEL.ad_interpolation.name,
        ML_MODEL.sd3.name,
    ]:
        ai_model = data_repo.get_ai_model_from_name(ML_MODEL.sdxl.name, user_id)

    log_data = {
        "project_id": st.session_state["project_uuid"],
        "model_id": ai_model.uuid if ai_model else None,
        "input_params": data_str,
        "output_details": json.dumps({"model_name": model.display_name(), "version": model.version}),
        "total_inference_time": time_taken,
        "status": (
            InferenceStatus.COMPLETED.value
            if time_taken
            else (
                InferenceStatus.BACKLOG.value
                if "backlog" in kwargs and kwargs["backlog"]
                else InferenceStatus.QUEUED.value
            )
        ),
        "model_name": model.display_name(),
        "generation_source": origin_data.get("inference_type", ""),
        "generation_tag": origin_data.get("inference_tag", "")
    }

    log = data_repo.create_inference_log(**log_data)
    return log
