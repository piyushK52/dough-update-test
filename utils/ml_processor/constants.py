from dataclasses import dataclass
from shared.constants import InferenceStatus
from utils.enum import ExtendedEnum


class ComfyWorkflow(ExtendedEnum):
    IP_ADAPTER_PLUS = "ip_adapter_plus"
    IP_ADAPTER_FACE = "ip_adapter_face"
    IP_ADAPTER_FACE_PLUS = "ip_adapter_face_plus"
    SDXL = "sdxl"
    SDXL_CONTROLNET = "sdxl_controlnet"
    SDXL_CONTROLNET_OPENPOSE = "sdxl_controlnet_openpose"
    LLAMA_2_7B = "llama_2_7b"
    SDXL_INPAINTING = "sdxl-inpainting"
    STEERABLE_MOTION = "steerable_motion"
    SDXL_IMG2IMG = "sdxl_img2img"
    UPSCALER = "upscale"
    MOTION_LORA = "motion_lora"
    IPADAPTER_COMPOSITION = "ipadapter_composition"
    DYNAMICRAFTER = "dynamicrafter"
    CREATIVE_IMAGE_GEN = "creative_image_gen"
    SD3 = "sd3"


@dataclass
class MLModel:
    # properties for replicate (result of ad-hoc coding new features :<)
    name: str
    version: str

    # workflow name (multiple workflows can be run through a common replicate endpoint)
    workflow_name: str = None

    # NOTE: changing the display name will lead to issues with filtering
    def display_name(self):
        for model in ML_MODEL.__dict__.values():
            if isinstance(model, MLModel):
                if self.workflow_name and model.workflow_name != self.workflow_name:
                    continue

                if self.name == model.name:
                    return model.workflow_name.value if model.workflow_name else model.name.split("/")[-1]
        return None


# comfy runner replicate endpoint
class ComfyRunnerModel:
    name = "voku682/comfy_runner"
    version = "36d691e7ae92a8f29194bb6ee5aa61a6ab23c77ad7fb5b2cb6f31641512ca21c"


class ML_MODEL:
    sdxl_inpainting = MLModel(
        "lucataco/sdxl-inpainting",
        "f03c01943bacdee38d6a5d216586bf9bfbfd799350aed263aa32980efc173f0b",
    )
    clones_lora_training = MLModel(
        "cloneofsimo/lora-training",
        "b2a308762e36ac48d16bfadc03a65493fe6e799f429f7941639a6acec5b276cc",
    )
    clones_lora_training_2 = MLModel(
        "cloneofsimo/lora",
        "fce477182f407ffd66b94b08e761424cabd13b82b518754b83080bc75ad32466",
    )
    google_frame_interpolation = MLModel(
        "google-research/frame-interpolation",
        "4f88a16a13673a8b589c18866e540556170a5bcb2ccdc12de556e800e9456d3d",
    )
    pollination_modnet = MLModel(
        "pollinations/modnet",
        "da7d45f3b836795f945f221fc0b01a6d3ab7f5e163f13208948ad436001e2255",
    )
    clip_interrogator = MLModel(
        "pharmapsychotic/clip-interrogator",
        "a4a8bafd6089e1716b06057c42b19378250d008b80fe87caa5cd36d40c1eda90",
    )
    gfp_gan = MLModel(
        "xinntao/gfpgan",
        "6129309904ce4debfde78de5c209bce0022af40e197e132f08be8ccce3050393",
    )
    ghost_face_swap = MLModel(
        "arielreplicate/ghost_face_swap",
        "106df0aaf9690354379d8cd291ad337f6b3ea02fe07d90feb1dafd64820066fa",
    )
    stylegan_nada = MLModel(
        "rinongal/stylegan-nada",
        "6b2af4ac56fa2384f8f86fc7620943d5fc7689dcbb6183733743a215296d0e30",
    )
    img2img_sd_2_1 = MLModel(
        "cjwbw/stable-diffusion-img2img-v2.1",
        "650c347f19a96c8a0379db998c4cd092e0734534591b16a60df9942d11dec15b",
    )
    cjwbw_style_hair = MLModel(
        "cjwbw/style-your-hair",
        "c4c7e5a657e2e1abccd57625093522a9928edeccee77e3f55d57c664bcd96fa2",
    )
    depth2img_sd = MLModel(
        "jagilley/stable-diffusion-depth2img",
        "68f699d395bc7c17008283a7cef6d92edc832d8dc59eb41a6cafec7fc70b85bc",
    )
    salesforce_blip_2 = MLModel(
        "salesforce/blip-2",
        "4b32258c42e9efd4288bb9910bc532a69727f9acd26aa08e175713a0a857a608",
    )
    phamquiluan_face_recognition = MLModel(
        "phamquiluan/facial-expression-recognition",
        "b16694d5bfed43612f1bfad7015cf2b7883b732651c383fe174d4b7783775ff5",
    )
    arielreplicate = MLModel(
        "arielreplicate/instruct-pix2pix",
        "10e63b0e6361eb23a0374f4d9ee145824d9d09f7a31dcd70803193ebc7121430",
    )
    cjwbw_midas = MLModel(
        "cjwbw/midas",
        "a6ba5798f04f80d3b314de0f0a62277f21ab3503c60c84d4817de83c5edfdae0",
    )
    jagilley_controlnet_normal = MLModel(
        "jagilley/controlnet-normal",
        "cc8066f617b6c99fdb134bc1195c5291cf2610875da4985a39de50ee1f46d81c",
    )
    jagilley_controlnet_canny = MLModel(
        "jagilley/controlnet-canny",
        "aff48af9c68d162388d230a2ab003f68d2638d88307bdaf1c2f1ac95079c9613",
    )
    jagilley_controlnet_hed = MLModel(
        "jagilley/controlnet-hed",
        "cde353130c86f37d0af4060cd757ab3009cac68eb58df216768f907f0d0a0653",
    )
    jagilley_controlnet_scribble = MLModel(
        "jagilley/controlnet-scribble",
        "435061a1b5a4c1e26740464bf786efdfa9cb3a3ac488595a2de23e143fdb0117",
    )
    jagilley_controlnet_seg = MLModel(
        "jagilley/controlnet-seg",
        "f967b165f4cd2e151d11e7450a8214e5d22ad2007f042f2f891ca3981dbfba0d",
    )
    jagilley_controlnet_hough = MLModel(
        "jagilley/controlnet-hough",
        "854e8727697a057c525cdb45ab037f64ecca770a1769cc52287c2e56472a247b",
    )
    jagilley_controlnet_depth2img = MLModel(
        "jagilley/controlnet-depth2img",
        "922c7bb67b87ec32cbc2fd11b1d5f94f0ba4f5519c4dbd02856376444127cc60",
    )
    jagilley_controlnet_pose = MLModel(
        "jagilley/controlnet-pose",
        "0304f7f774ba7341ef754231f794b1ba3d129e3c46af3022241325ae0c50fb99",
    )
    real_esrgan_upscale = MLModel(
        "cjwbw/real-esrgan",
        "d0ee3d708c9b911f122a4ad90046c5d26a0293b99476d697f6bb7f2e251ce2d4",
    )
    controlnet_1_1_x_realistic_vision_v2_0 = MLModel(
        "usamaehsan/controlnet-1.1-x-realistic-vision-v2.0",
        "7fbf4c86671738f97896c9cb4922705adfcdcf54a6edab193bb8c176c6b34a69",
    )
    urpm = MLModel(
        "mcai/urpm-v1.3-img2img",
        "4df956e8dbfebf1afaf0c3ee98ad426ec58c4262d24360d054582e5eab2cb5f6",
    )
    sdxl = MLModel(
        "stability-ai/sdxl",
        "af1a68a271597604546c09c64aabcd7782c114a63539a4a8d14d1eeda5630c33",
        ComfyWorkflow.SDXL,
    )
    sdxl_img2img = MLModel(
        "stability-ai/sdxl",
        "af1a68a271597604546c09c64aabcd7782c114a63539a4a8d14d1eeda5630c33",
        ComfyWorkflow.SDXL_IMG2IMG,
    )

    # addition 30/9/2023
    realistic_vision_v5 = MLModel(
        "heedster/realistic-vision-v5",
        "c0259010b93e7a4102a4ba946d70e06d7d0c7dc007201af443cfc8f943ab1d3c",
    )
    deliberate_v3 = MLModel(
        "pagebrain/deliberate-v3",
        "1851b62340ae657f05f8b8c8a020e3f9a46efde9fe80f273eef026c0003252ac",
    )
    dreamshaper_v7 = MLModel(
        "pagebrain/dreamshaper-v7",
        "0deba88df4e49b302585e1a7b6bd155e18962c1048966a40fe60ba05805743ff",
    )
    epicrealism_v5 = MLModel(
        "pagebrain/epicrealism-v5",
        "222465e57e4d9812207f14133c9499d47d706ecc41a8bf400120285b2f030b42",
    )
    sdxl_controlnet = MLModel(
        "lucataco/sdxl-controlnet",
        "db2ffdbdc7f6cb4d6dab512434679ee3366ae7ab84f89750f8947d5594b79a47",
        ComfyWorkflow.SDXL_CONTROLNET,
    )
    realistic_vision_v5_img2img = MLModel(
        "lucataco/realistic-vision-v5-img2img",
        "82bbb4595458d6be142450fc6d8c4d79c936b92bd184dd2d6dd71d0796159819",
    )
    ad_interpolation = MLModel(
        ComfyRunnerModel.name, ComfyRunnerModel.version, ComfyWorkflow.STEERABLE_MOTION
    )
    dynamicrafter = MLModel(ComfyRunnerModel.name, ComfyRunnerModel.version, ComfyWorkflow.DYNAMICRAFTER)

    # addition 17/10/2023
    llama_2_7b = MLModel(
        "meta/llama-2-7b",
        "527827021d8756c7ab79fde0abbfaac885c37a3ed5fe23c7465093f0878d55ef",
        ComfyWorkflow.LLAMA_2_7B,
    )

    # addition 11/11/2023
    sdxl_controlnet_openpose = MLModel(
        "lucataco/sdxl-controlnet-openpose",
        "d63e0b238b2d963d90348e2dad19830fbe372a7a43d90d234b2b63cae76d4397",
        ComfyWorkflow.SDXL_CONTROLNET_OPENPOSE,
    )

    # addition 05/02/2024 (workflows)
    ipadapter_plus = MLModel(ComfyRunnerModel.name, ComfyRunnerModel.version, ComfyWorkflow.IP_ADAPTER_PLUS)
    ipadapter_face = MLModel(ComfyRunnerModel.name, ComfyRunnerModel.version, ComfyWorkflow.IP_ADAPTER_FACE)
    ipadapter_face_plus = MLModel(
        ComfyRunnerModel.name, ComfyRunnerModel.version, ComfyWorkflow.IP_ADAPTER_FACE_PLUS
    )
    video_upscaler = MLModel(ComfyRunnerModel.name, ComfyRunnerModel.version, ComfyWorkflow.UPSCALER)
    motion_lora_trainer = MLModel(ComfyRunnerModel.name, ComfyRunnerModel.version, ComfyWorkflow.MOTION_LORA)
    ipadapter_composition = MLModel(
        ComfyRunnerModel.name, ComfyRunnerModel.version, ComfyWorkflow.IPADAPTER_COMPOSITION
    )

    # addition 21/04/2024
    sd3 = MLModel("stability-ai/sd3", "")

    # addition 12/06/2024
    creative_image_gen = MLModel(
        ComfyRunnerModel.name, ComfyRunnerModel.version, ComfyWorkflow.CREATIVE_IMAGE_GEN
    )
    sd3_local = MLModel(
        ComfyRunnerModel.name, ComfyRunnerModel.version, ComfyWorkflow.SD3
    )

    @staticmethod
    def get_model_by_db_obj(model_db_obj):
        for model in ML_MODEL.__dict__.values():
            if (
                isinstance(model, MLModel)
                and model.name == model_db_obj.replicate_url
                and model.version == model_db_obj.version
            ):
                return model
        return None


MODEL_FILTERS = [
    ML_MODEL.sdxl,
    ML_MODEL.sdxl_controlnet,
    ML_MODEL.sdxl_controlnet_openpose,
    ML_MODEL.sdxl_img2img,
    ML_MODEL.sdxl_inpainting,
    ML_MODEL.ad_interpolation,
    ML_MODEL.dynamicrafter,
    ML_MODEL.ipadapter_face,
    ML_MODEL.ipadapter_face_plus,
    ML_MODEL.ipadapter_plus,
    ML_MODEL.ipadapter_composition,
]

DEFAULT_LORA_MODEL_URL = "https://replicate.delivery/pbxt/nWm6eP9ojwVvBCaWoWZVawOKRfgxPJmkVk13ES7PX36Y66kQA/tmpxuz6k_k2datazip.safetensors"

CONTROLNET_MODELS = [
    ML_MODEL.jagilley_controlnet_normal,
    ML_MODEL.jagilley_controlnet_canny,
    ML_MODEL.jagilley_controlnet_hed,
    ML_MODEL.jagilley_controlnet_scribble,
    ML_MODEL.jagilley_controlnet_seg,
    ML_MODEL.jagilley_controlnet_hough,
    ML_MODEL.jagilley_controlnet_depth2img,
    ML_MODEL.jagilley_controlnet_pose,
]

replicate_status_map = {
    "starting": InferenceStatus.QUEUED.value,
    "processing": InferenceStatus.IN_PROGRESS.value,
    "succeeded": InferenceStatus.COMPLETED.value,
    "failed": InferenceStatus.FAILED.value,
    "canceled": InferenceStatus.CANCELED.value,
}
