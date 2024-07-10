import json
import os
import socket

import requests
import streamlit as st
from shared.constants import (
    HOSTED_BACKGROUND_RUNNER_MODE,
    SERVER,
    InternalFileType,
    InternalResponse,
    ServerType,
)
from utils.common_decorators import log_time

from utils.constants import AUTH_TOKEN
from utils.local_storage.url_storage import delete_url_param, get_url_param


class APIRepo:
    def __init__(self):
        self._load_base_url()
        self._setup_urls()

    def _load_base_url(self):
        import dotenv

        dotenv.load_dotenv()

        SERVER_URL = os.getenv("SERVER_URL", "")
        if not SERVER_URL.startswith("http"):
            # connecting through service discovery
            self.base_url = "http://" + socket.gethostbyname(SERVER_URL) + ":8080"
        else:
            self.base_url = SERVER_URL

    def _setup_urls(self):
        # user
        self.USER_OP_URL = "/v1/user/op"
        self.USER_LIST_URL = "/v1/user/list"

        # payment
        self.ORDER_OP_URL = "/v1/payment/order"
        self.ORDER_LIST_URL = "/v1/payment/order/list"

        # auth
        self.AUTH_OP_URL = "/v1/authentication/op"
        self.AUTH_REFRESH_URL = "/v1/authentication/refresh"
        self.GOOGLE_LOGIN_URL = "/v1/authentication/google"

        # timing
        self.TIMING_URL = "/v1/data/timing"
        self.PROJECT_TIMING_URL = "/v1/data/timing/project"
        self.TIMING_NUMBER_URL = "/v1/data/timing/number"
        self.SHIFT_TIMING_URL = "/v1/data/timing/shift"
        self.TIMING_LIST_URL = "/v1/data/timing/list"

        # project
        self.PROJECT_URL = "/v1/data/project"
        self.PROJECT_LIST_URL = "/v1/data/project/list"
        self.EXPLORER_STATS_URL = "/v1/data/project/stats"

        # project setting
        self.PROJECT_SETTING_URL = "/v1/data/project-setting"

        # inference log
        self.LOG_URL = "/v1/data/log"
        self.LOG_LIST_URL = "/v1/data/log/list"

        # file
        self.FILE_URL = "/v1/data/file"
        self.FILE_LIST_URL = "/v1/data/file/list"
        self.FILE_UUID_LIST_URL = "/v1/data/file/uuid-list"
        self.FILE_UPLOAD_URL = "/v1/data/file/upload"
        self.FILE_EXTRA_URL = "/v1/data/file/extra"  # TODO: fix url patterns

        # app setting
        self.APP_SETTING_URL = "/v1/data/app-setting"
        self.APP_SECRET_URL = "/v1/data/app-secret"

        # ai model
        self.MODEL_URL = "/v1/data/model"
        self.MODEL_LIST_URL = "/v1/data/model/list"

        # payment
        self.STRIPE_PAYMENT_URL = "/v1/payment/stripe-link"

        # lock
        self.LOCK_URL = "/v1/data/lock"

        # shot
        self.SHOT_URL = "/v1/data/shot"
        self.SHOT_LIST_URL = "/v1/data/shot/list"
        self.SHOT_INTERPOLATED_CLIP = "/v1/data/shot/interpolated-clip"
        self.SHOT_DUPLICATE_URL = "/v1/data/shot/duplicate"

    def logout(self):
        delete_url_param(AUTH_TOKEN)
        st.rerun()

    ################### base http methods
    def _get_headers(self, content_type="application/json"):
        auth_token = get_url_param(AUTH_TOKEN)
        if not auth_token and SERVER != ServerType.DEVELOPMENT.value:
            if HOSTED_BACKGROUND_RUNNER_MODE in [False, "False"]:
                self.logout()
            else:
                from ui_components.methods.file_methods import load_from_env

                auth_token = load_from_env(AUTH_TOKEN)  # hackish sol, will fix later

        headers = {}
        headers["Authorization"] = f"Bearer {auth_token}"
        if content_type:
            headers["Content-Type"] = content_type

        return headers

    @log_time
    def http_get(self, url, params=None):
        self._load_base_url()
        res = requests.get(self.base_url + url, params=params, headers=self._get_headers())
        return res.json()

    @log_time
    def http_post(self, url, data={}, file_content=None):
        self._load_base_url()
        if file_content:
            files = {"file": file_content}
            res = requests.post(self.base_url + url, data=data, files=files, headers=self._get_headers(None))
        else:
            res = requests.post(self.base_url + url, json=data, headers=self._get_headers())

        return res.json()

    @log_time
    def http_put(self, url, data=None):
        self._load_base_url()
        res = requests.put(self.base_url + url, json=data, headers=self._get_headers())
        return res.json()

    @log_time
    def http_delete(self, url, params=None):
        self._load_base_url()
        res = requests.delete(self.base_url + url, params=params, headers=self._get_headers())
        return res.json()

    #########################################
    def refresh_auth_token(self, refresh_token):
        headers = {}
        headers["Authorization"] = f"Bearer {refresh_token}"
        headers["Content-Type"] = "application/json"
        res = requests.get(self.base_url + self.AUTH_REFRESH_URL, headers=headers)
        payload = {"data": None}
        res_json = json.loads(res._content)
        if res.status_code == 200 and res_json["status"]:
            payload = {"data": res_json["payload"]}
        return InternalResponse(payload, "user login successfully", res_json["status"])

    def user_password_login(self, **kwargs):
        headers = {}
        headers["Content-Type"] = "application/json"
        res = requests.post(self.base_url + self.AUTH_OP_URL, json=kwargs, headers=headers)
        payload = {"data": None}
        res_json = json.loads(res._content)
        if res.status_code == 200 and res_json["status"]:
            payload = {"data": res_json["payload"]}
        return InternalResponse(payload, "user login successfully", res_json["status"])

    def google_user_login(self, **kwargs):
        headers = {}
        headers["Content-Type"] = "application/json"
        res = requests.post(self.base_url + self.GOOGLE_LOGIN_URL, json=kwargs, headers=headers)
        payload = {"data": None}
        res_json = json.loads(res._content)
        if res.status_code == 200 and res_json["status"]:
            payload = {"data": res_json["payload"]}
        return InternalResponse(payload, "user login successfully", res_json["status"])

    def create_user(self, **kwargs):
        res = self.http_post(url=self.USER_OP_URL, data=kwargs)
        return InternalResponse(res["payload"], "success", res["status"])

    def update_user(self, user_id=None, **kwargs):
        if user_id:
            kwargs["uuid"] = user_id
        res = self.http_put(url=self.USER_OP_URL, data=kwargs)
        return InternalResponse(res["payload"], "success", res["status"])

    # making it fetch the current logged in user
    def get_first_active_user(self):
        res = self.http_get(self.USER_OP_URL)
        return InternalResponse(res["payload"], "success", res["status"])

    def get_user_by_email(self, email):
        res = self.http_get(self.USER_OP_URL, params={"email": email})
        return InternalResponse(res["payload"], "user fetched successfully", True)

    def get_total_user_count(self):
        res = self.http_get(self.USER_LIST_URL)
        payload = res["payload"]["count"] if "count" in res["payload"] else 0
        return InternalResponse(payload, "user count fetched successfully", True)

    def get_all_user_list(self):
        res = self.http_get(self.USER_LIST_URL)
        return InternalResponse(res["payload"], "success", res["status"])

    # TODO: remove this method from everywhere
    def delete_user_by_email(self, email):
        res = self.db_repo.delete_user_by_email(email)
        return InternalResponse(res["payload"], "success", res["status"]).status

    # internal file object
    # TODO: remove this method from everywhere
    def get_file_from_name(self, name):
        pass

    def get_file_from_uuid(self, uuid):
        res = self.http_get(self.FILE_URL, params={"uuid": uuid})
        return InternalResponse(res["payload"], "success", res["status"])

    def get_file_list_from_log_uuid_list(self, log_uuid_list):
        res = self.http_post(self.FILE_UUID_LIST_URL, data={"log_uuid_list": log_uuid_list})
        return InternalResponse(res["payload"], "success", res["status"])

    def get_all_file_list(self, **kwargs):
        res = self.http_get(self.FILE_LIST_URL, params=kwargs)
        return InternalResponse(res["payload"], "success", res["status"])

    def create_or_update_file(self, uuid, type=InternalFileType.IMAGE.value, **kwargs):
        update_data = kwargs
        update_data["uuid"] = uuid
        update_data["type"] = type
        res = self.http_put(url=self.FILE_URL, data=update_data)
        return InternalResponse(res["payload"], "success", res["status"])

    def upload_file(self, file_content, ext):
        res = self.http_post(url=self.FILE_UPLOAD_URL, data={"extension": ext}, file_content=file_content)
        return InternalResponse(res["payload"], "success", res["status"])

    def create_file(self, **kwargs):
        res = self.http_post(url=self.FILE_URL, data=kwargs)
        return InternalResponse(res["payload"], "success", res["status"])

    def delete_file_from_uuid(self, uuid):
        res = self.http_delete(url=self.FILE_URL, params={"uuid": uuid})
        return InternalResponse(res["payload"], "success", res["status"])

    # TODO: remove file_type from this method
    def get_image_list_from_uuid_list(self, image_uuid_list, file_type=InternalFileType.IMAGE.value):
        res = self.http_get(self.FILE_UUID_LIST_URL, params={"uuid_list": image_uuid_list, "type": file_type})
        return InternalResponse(res["payload"], "success", res["status"])

    def update_file(self, **kwargs):
        res = self.http_put(url=self.FILE_URL, data=kwargs)
        return InternalResponse(res["payload"], "success", res["status"])

    def get_file_count_from_type(self, file_tag, project_uuid):
        res = self.http_get(self.FILE_EXTRA_URL, params={"file_tag": file_tag, "project_uuid": project_uuid})
        return InternalResponse(res["payload"], "success", res["status"])

    def update_temp_gallery_images(self, project_uuid):
        res = self.http_put(self.FILE_EXTRA_URL, data={"uuid": project_uuid})
        return InternalResponse(res["payload"], "success", res["status"])

    # project
    def get_project_from_uuid(self, uuid):
        res = self.http_get(self.PROJECT_URL, params={"uuid": uuid})
        return InternalResponse(res["payload"], "success", res["status"])

    def get_all_project_list(self, user_id):
        res = self.http_get(self.PROJECT_LIST_URL, params={"user_id": user_id})
        return InternalResponse(res["payload"], "success", res["status"])

    def create_project(self, **kwargs):
        res = self.http_post(url=self.PROJECT_URL, data=kwargs)
        return InternalResponse(res["payload"], "success", res["status"])

    def delete_project_from_uuid(self, uuid):
        res = self.http_delete(self.PROJECT_URL, params={"uuid": uuid})
        return InternalResponse(res["payload"], "success", res["status"])

    def update_project(self, **kwargs):
        res = self.http_put(self.PROJECT_URL, data=kwargs)
        return InternalResponse(res["payload"], "success", res["status"])

    # ai model (custom ai model)
    def get_ai_model_from_uuid(self, uuid):
        res = self.http_get(self.MODEL_URL, params={"uuid": uuid})
        return InternalResponse(res["payload"], "success", res["status"])

    # TODO: remove this method from everywhere
    def get_ai_model_from_name(self, name, user_id):
        res = self.http_get(self.MODEL_URL, params={"replicate_url": name, "user_id": user_id})
        return InternalResponse(res["payload"], "success", res["status"])

    def get_all_ai_model_list(
        self, model_category_list=None, user_id=None, custom_trained=None, model_type_list=None
    ):
        params = {
            "user_id": user_id,
            "custom_trained": (
                "all" if custom_trained == None else ("user" if custom_trained else "predefined")
            ),
        }
        if model_category_list:
            params.update({"model_category_list": model_category_list})
        if model_type_list:
            params.update({"model_type_list": model_type_list})
        res = self.http_get(self.MODEL_LIST_URL, params=params)
        return InternalResponse(res["payload"], "success", res["status"])

    def create_ai_model(self, **kwargs):
        res = self.http_post(url=self.MODEL_URL, data=kwargs)
        return InternalResponse(res["payload"], "success", res["status"])

    def update_ai_model(self, **kwargs):
        res = self.http_put(url=self.MODEL_URL, data=kwargs)
        return InternalResponse(res["payload"], "success", res["status"])

    def delete_ai_model_from_uuid(self, uuid):
        res = self.http_delete(self.MODEL_URL, params={"uuid": uuid})
        return InternalResponse(res["payload"], "success", res["status"]).status

    # inference log
    def get_inference_log_from_uuid(self, uuid):
        res = self.http_get(self.LOG_URL, params={"uuid": uuid})
        return InternalResponse(res["payload"], "success", res["status"])

    def get_all_inference_log_list(self, **kwargs):
        res = self.http_get(self.LOG_LIST_URL, params=kwargs)
        return InternalResponse(res["payload"], "success", res["status"])

    def create_inference_log(self, **kwargs):
        res = self.http_post(url=self.LOG_URL, data=kwargs)
        return InternalResponse(res["payload"], "success", res["status"])

    def delete_inference_log_from_uuid(self, uuid):
        res = self.db_repo.delete_inference_log_from_uuid(uuid)
        return InternalResponse(res["payload"], "success", res["status"]).status

    def update_inference_log(self, uuid, **kwargs):
        kwargs["uuid"] = uuid
        res = self.http_put(url=self.LOG_URL, data=kwargs)
        return InternalResponse(res["payload"], "success", res["status"])

    def update_inference_log_list(self, uuid_list, **kwargs):
        kwargs["uuid_list"] = uuid_list
        res = self.http_put(url=self.LOG_LIST_URL, data=kwargs)
        return InternalResponse(res["payload"], "success", res["status"])

    # TODO: complete this: backend
    def get_ai_model_param_map_from_uuid(self, uuid):
        pass

    # def get_all_ai_model_param_map_list(self, model_id=None):
    #     pass

    # def create_ai_model_param_map(self, **kwargs):
    #     pass

    # def delete_ai_model(self, uuid):
    #     pass

    # timing
    def get_timing_from_uuid(self, uuid):
        res = self.http_get(self.TIMING_URL, params={"uuid": uuid})
        return InternalResponse(res["payload"], "success", res["status"])

    def get_timing_from_frame_number(self, shot_uuid, frame_number):
        res = self.http_get(
            self.PROJECT_TIMING_URL, params={"shot_id": shot_uuid, "frame_number": frame_number}
        )
        return InternalResponse(res["payload"], "success", res["status"])

    # this is based on the aux_frame_index and not the order in the db
    def get_next_timing(self, uuid):
        res = self.http_get(self.TIMING_NUMBER_URL, params={"uuid": uuid, "distance": 1})
        return InternalResponse(res["payload"], "success", res["status"])

    def get_prev_timing(self, uuid):
        res = self.http_get(self.TIMING_NUMBER_URL, params={"uuid": uuid, "distance": -1})
        return InternalResponse(res["payload"], "success", res["status"])

    def get_timing_list_from_project(self, project_uuid=None):
        res = self.http_get(self.TIMING_LIST_URL, params={"project_id": project_uuid, "page": 1})
        return InternalResponse(res["payload"], "success", res["status"])

    def get_timing_list_from_shot(self, shot_uuid=None):
        res = self.http_get(self.TIMING_LIST_URL, params={"shot_id": shot_uuid, "page": 1})
        return InternalResponse(res["payload"], "success", res["status"])

    def create_timing(self, **kwargs):
        res = self.http_post(url=self.TIMING_URL, data=kwargs)
        return InternalResponse(res["payload"], "success", res["status"])

    def update_specific_timing(self, uuid, **kwargs):
        kwargs["uuid"] = uuid
        res = self.http_put(url=self.TIMING_URL, data=kwargs)
        return InternalResponse(res["payload"], "success", res["status"])

    # TODO: complete this
    def update_bulk_timing(self, timing_uuid_list, data_list):
        res = self.http_put(url=self.TIMING_LIST_URL, data=data_list)
        return InternalResponse(res["payload"], "success", res["status"])

    def delete_timing_from_uuid(self, uuid):
        res = self.http_delete(self.TIMING_URL, params={"uuid": uuid})
        return InternalResponse(res["payload"], "success", res["status"])

    # removes all timing frames from the project
    def remove_existing_timing(self, project_uuid):
        res = self.http_delete(self.PROJECT_TIMING_URL, params={"uuid": project_uuid})
        return InternalResponse(res["payload"], "success", res["status"]).status

    def remove_primary_frame(self, timing_uuid):
        update_data = {"uuid": timing_uuid, "primary_image_id": None}
        res = self.http_put(self.TIMING_URL, data=update_data)
        return InternalResponse(res["payload"], "success", res["status"])

    def remove_source_image(self, timing_uuid):
        update_data = {"uuid": timing_uuid, "source_image_id": None}
        res = self.http_put(self.TIMING_URL, data=update_data)
        return InternalResponse(res["payload"], "success", res["status"])

    # app setting
    def get_app_setting_from_uuid(self, uuid=None):
        res = self.http_get(self.APP_SETTING_URL, params={"uuid": uuid})
        return InternalResponse(res["payload"], "success", res["status"])

    def get_app_secrets_from_user_uuid(self, uuid=None, secret_access=None):
        res = self.http_post(self.APP_SECRET_URL, data={"secret_access": secret_access})
        return InternalResponse(res["payload"], "success", res["status"])

    # TODO: complete this code
    def get_all_app_setting_list(self):
        pass

    def update_app_setting(self, **kwargs):
        res = self.http_put(url=self.APP_SETTING_URL, data=kwargs)
        return InternalResponse(res["payload"], "success", res["status"])

    def create_app_setting(self, **kwargs):
        res = self.http_post(url=self.APP_SETTING_URL, data=kwargs)
        return InternalResponse(res["payload"], "success", res["status"])

    def delete_app_setting(self, user_id):
        res = self.db_repo.delete_app_setting(user_id)
        return InternalResponse(res["payload"], "success", res["status"]).status

    # setting
    def get_project_setting(self, project_id):
        res = self.http_get(self.PROJECT_SETTING_URL, params={"uuid": project_id})
        return InternalResponse(res["payload"], "success", res["status"])

    # TODO: add valid model_id check throughout dp_repo
    def create_project_setting(self, **kwargs):
        res = self.http_post(url=self.PROJECT_SETTING_URL, data=kwargs)
        return InternalResponse(res["payload"], "success", res["status"])

    def update_project_setting(self, **kwargs):
        res = self.http_put(url=self.PROJECT_SETTING_URL, data=kwargs)
        return InternalResponse(res["payload"], "success", res["status"])

    # TODO: update or remove this
    def bulk_update_project_setting(self, **kwargs):
        pass

    # backup
    # TODO: complete this
    def get_backup_from_uuid(self, uuid):
        pass

    def create_backup(self, project_uuid, version_name):
        # backup = self.db_repo.create_backup(project_uuid, version_name).data['data']
        # return InternalBackupObject(**backup) if backup else None
        return None

    def get_backup_list(self, project_id=None):
        # backup_list = self.db_repo.get_backup_list(project_id).data['data']
        # return [InternalBackupObject(**backup) for backup in backup_list] if backup_list else []
        return InternalResponse({"data": []}, "success", True)

    def delete_backup(self, uuid):
        # res = self.db_repo.delete_backup(uuid)
        # return InternalResponse(res['payload'], 'success', res['status']).status
        return True

    def restore_backup(self, uuid):
        # res = self.db_repo.restore_backup(uuid)
        # return InternalResponse(res['payload'], 'success', res['status']).status
        return True

    # payment link
    def generate_payment_link(self, amount):
        res = self.http_get(self.STRIPE_PAYMENT_URL, params={"total_amount": amount})
        return InternalResponse(res["payload"], "success", res["status"])


    # shot
    def get_shot_from_uuid(self, shot_uuid):
        res = self.http_get(self.SHOT_URL, params={"uuid": shot_uuid})
        return InternalResponse(res["payload"], "success", res["status"])

    def get_shot_from_number(self, project_uuid, shot_number=0):
        res = self.http_get(self.SHOT_URL, params={"project_id": project_uuid, "shot_idx": shot_number})
        return InternalResponse(res["payload"], "success", res["status"])

    def get_shot_list(self, project_uuid):
        res = self.http_get(self.SHOT_LIST_URL, params={"project_id": project_uuid})
        return InternalResponse(res["payload"], "success", res["status"])

    def create_shot(self, project_uuid, duration, name, meta_data="", desc=""):
        data = {
            "project_id": project_uuid,
            "name": name,
            "duration": duration,
            "meta_data": meta_data,
            "desc": desc,
        }
        res = self.http_post(self.SHOT_URL, data=data)
        return InternalResponse(res["payload"], "success", res["status"])

    def update_shot(self, **kwargs):
        res = self.http_put(self.SHOT_URL, data=kwargs)
        return InternalResponse(res["payload"], "success", res["status"])

    def duplicate_shot(self, shot_uuid):
        res = self.http_post(self.SHOT_DUPLICATE_URL, data={"uuid": shot_uuid})
        return InternalResponse(res["payload"], "success", res["status"])

    def delete_shot(self, shot_uuid):
        res = self.http_delete(self.SHOT_URL, params={"uuid": shot_uuid})
        return InternalResponse(res["payload"], "success", res["status"])

    def add_interpolated_clip(self, shot_uuid, **kwargs):
        kwargs["uuid"] = shot_uuid
        res = self.http_post(self.SHOT_INTERPOLATED_CLIP, data=kwargs)
        return InternalResponse(res["payload"], "success", res["status"])

    # combined
    def get_explorer_pending_stats(self, project_uuid, log_status_list):
        res = self.http_get(
            self.EXPLORER_STATS_URL, params={"project_uuid": project_uuid, "log_status_list": log_status_list}
        )
        return InternalResponse(res["payload"], "success", res["status"])

    # lock
    def acquire_lock(self, key):
        res = self.http_get(self.LOCK_URL, params={"key": key, "action": "acquire"})
        return InternalResponse(res["payload"], "success", res["status"])

    def release_lock(self, key):
        res = self.http_get(self.LOCK_URL, params={"key": key, "action": "release"})
        return InternalResponse(res["payload"], "success", res["status"])