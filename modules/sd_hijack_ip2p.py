import os.path
def should_hijack_ip2p(checkpoint_info):A='pix2pix';B=checkpoint_info;from modules import sd_models_config as C;D=os.path.basename(B.filename).lower();E=os.path.basename(C.find_checkpoint_config_near_filename(B)).lower();return A in D and A not in E